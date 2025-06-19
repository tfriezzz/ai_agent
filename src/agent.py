import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info, get_file_content, write_file
from functions.run_python import run_python_file


def feedback_loop(user_prompt, verbose=False):
    # result = []
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    for i in range(0, 20):
        response = generate_content(messages, verbose)
        found_tool = False

        for candidate in response.candidates:
            messages.append(candidate.content)

            for part in candidate.content.parts:
                if hasattr(part, "function_call") and part.function_call is not None:
                    # call the tool
                    found_tool = True

        if not found_tool:
            print(response.candidates[0].content.parts[0].text)
            break

        #    else:
        #        print(candidate.content.parts[0].text)
        #        break

        # else:
        #    continue
        # break

    # return result


def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_map = {
        "get_files_info": get_files_info,
        "get_file_content": get_file_content,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }

    if function_name in function_map:
        function = function_map[function_name]
        args = dict(function_call_part.args)
        args["working_directory"] = "./calculator"

        if verbose:
            print(
                f"Calling function: {function_call_part.name}({function_call_part.args})"
            )

        if not verbose:
            print(f" - Calling function: {function_call_part.name}")

        function_result = function(**args)

        function_call_result = types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        )

        # if verbose:
        #    print(f"-> {function_call_result.parts[0].function_response.response}")

        return function_call_result

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )


def generate_content(messages, verbose=False):
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    schema_get_files_info = types.FunctionDeclaration(
        name="get_files_info",
        description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "directory": types.Schema(
                    type=types.Type.STRING,
                    description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
                ),
            },
        ),
    )

    schema_get_file_content = types.FunctionDeclaration(
        name="get_file_content",
        description="Lists the content of a specified file, constrained to the working directory.",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file_path is the relative path to the file. This has to be provided",
                ),
            },
        ),
    )

    schema_write_file = types.FunctionDeclaration(
        name="write_file",
        description="Writes the specified content to the specified file_path",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file_path is the relative path to the file. This has to be provided",
                ),
                "content": types.Schema(
                    type=types.Type.STRING,
                    description="The content is what is to be written to the specified file_path",
                ),
            },
        ),
    )

    schema_run_python_file = types.FunctionDeclaration(
        name="run_python_file",
        description="Executes the specified python file",
        parameters=types.Schema(
            type=types.Type.OBJECT,
            properties={
                "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="The file_path is the relative path to the file. This has to be provided",
                ),
            },
        ),
    )

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file,
        ]
    )

    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:
    When you are able, always start by calling a function. Do not just describe your plan.

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    # messages = []

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if response.function_calls:
        for call in response.function_calls:
            if verbose:
                call_result = call_function(call, verbose=True)

            if not verbose:
                call_result = call_function(call)

            try:
                response_data = call_result.parts[0].function_response.response
            except (IndexError, AttributeError):
                raise RuntimeError("Critical object missing")

            # print(call_result.parts[0].function_response.response["result"])

            if call_result.parts[0].function_response.response and verbose:
                print(f"-> {call_result.parts[0].function_response.response}")

    if not verbose and not response.function_calls:
        return response

    if verbose and not response.function_calls:
        print(f"User prompt: {messages}\n")
        print(f"{response.text}\n")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    return response
