import os
from dotenv import load_dotenv
from google import genai
from google.genai import types


class Agent:
    def __init__(self, user_prompt):
        self.user_prompt = user_prompt
        load_dotenv()
        self.__api_key = os.environ.get("GEMINI_API_KEY")
        self.__client = genai.Client(api_key=self.__api_key)

        self.messages = [
            types.Content(role="user", parts=[types.Part(text=user_prompt)]),
        ]

        self.response = self.__client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=self.messages,
        )

    def call_agent(self, verbose=False):
        response = self.__client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=self.messages,
        )

        if not verbose:
            print(response.text)
            # print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            # print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        if verbose:
            print(f"User prompt: {self.user_prompt}\n")
            print(f"{response.text}\n")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
