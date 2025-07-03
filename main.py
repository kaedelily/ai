import os
from dotenv import load_dotenv
from google import genai
import argparse
import sys
import os

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

parser = argparse.ArgumentParser(description="Generate content using the Gemini API with a custom prompt.")

parser.add_argument("prompt", help="The text prompt to send to the Gemini model.")

args = parser.parse_args()
if args.prompt == None:
    print("No question asked!")

else:
    user_prompt = args.prompt
    response = client.models.generate_content(model="gemini-2.0-flash-001", contents=user_prompt)
    print(response.text)
    usage_info = response.usage_metadata
    if usage_info:
        print(f"Prompt tokens: {usage_info.prompt_token_count}")
        print(f"Response tokens: {usage_info.candidates_token_count}")

