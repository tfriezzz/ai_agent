import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


def call_agent(user_prompt, verbose=False):
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
    )

    if not verbose:
        print(response.text)
        # print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        # print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if verbose:
        print(f"User prompt: {user_prompt}\n")
        print(f"{response.text}\n")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
