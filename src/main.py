import sys

# import os
# from dotenv import load_dotenv
# from google import genai
from agent import generate_content


if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
    generate_content(sys.argv[1], True)
elif len(sys.argv) > 1:
    generate_content(sys.argv[1])

elif not len(sys.argv) > 1:
    raise ValueError("No prompt provided")
    raise SystemExit(1)
