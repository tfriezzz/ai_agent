import sys

# import os
# from dotenv import load_dotenv
# from google import genai
from agent import call_agent


if len(sys.argv) > 1:
    call_agent(sys.argv[1])

elif not len(sys.argv) > 1:
    raise ValueError("No prompt provided")
    raise SystemExit(1)
