import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
import sys

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")

client = genai.Client(api_key=api_key)

if len(sys.argv) < 2:
    print("No input provided. Please provide a prompt as a command line argument.")
    exit(1)

# Check for --verbose flag
verbose = False
args = sys.argv[1:]
if '--verbose' in args:
    verbose = True
    args.remove('--verbose')

if not args:
    print("No prompt provided. Please provide a prompt as a command line argument.")
    exit(1)

user_prompt = args[0]
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages
)
if verbose:
    print(f"User prompt: {user_prompt}")
print(response.text)
if verbose and response.usage_metadata:
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
