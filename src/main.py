import sys

# import os
# from dotenv import load_dotenv
# from google import genai
from agent import feedback_loop


if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
    feedback_loop(sys.argv[1], True)
elif len(sys.argv) > 1:
    feedback_loop(sys.argv[1])

elif not len(sys.argv) > 1:
    raise ValueError("No prompt provided")
    raise SystemExit(1)
