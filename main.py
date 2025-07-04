import os
from dotenv import load_dotenv
from google import genai
import sys
from google.genai import types
from functions.get_files_info import schema_get_files_info

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in the environment variables.")
client = genai.Client(api_key=api_key)

if len(sys.argv) < 2:
    print("No input provided. Please provide a prompt as a command line argument.")
    exit(1)

user_prompt = sys.argv[1]
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
    ]
)
config=types.GenerateContentConfig(
    tools=[available_functions], system_instruction=system_prompt
)
system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=system_prompt
)
if response.candidates:
    for candidate in response.candidates:
        if hasattr(candidate, 'content') and candidate.content and hasattr(candidate.content, 'parts'):
            for part in candidate.content.parts:
                if hasattr(part, 'function_call') and part.function_call:
                    function_call_part = part.function_call
                    print(f"Calling function: {function_call_part.name}({function_call_part.args})")
                elif hasattr(part, 'text') and part.text:
                    print(response.text)
     
if "--verbose" in sys.argv:
    if response.usage_metadata:
            print(response.text)
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
else:
    print(response.text)