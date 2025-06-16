import sys

# import os
# from dotenv import load_dotenv
# from google import genai
from agent import Agent

agent = Agent(sys.argv[1])


if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
    agent.call_agent(verbose=True)

elif len(sys.argv) > 1:
    agent.call_agent()

elif not len(sys.argv) > 1:
    raise ValueError("No prompt provided")
    raise SystemExit(1)
