import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt 
from call_function import available_functions, call_function

def main():
    parser = argparse.ArgumentParser(description="AI Code Assistant")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY environment variable not set")

    client = genai.Client(api_key=api_key)
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\n")


    for _ in range(20):
        final_response = generate_content(client, messages, args.verbose)
        if final_response:
            print("Final response:")
            print(final_response)
            return
    print("Maximum iterations reached")
    sys.exit(1)

def generate_content(client, messages, verbose):
    if verbose:
        print("System prompt being used:")
        print(repr(system_prompt))
        
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )

    if response.candidates:
        for candidate in response.candidates:
            messages.append(candidate.content)

    if not response.usage_metadata:
        raise RuntimeError("Gemini API response appears to be malformed")

    if verbose:
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    function_results = []

    if response.function_calls:
        for function_call in response.function_calls:
            function_call_result = call_function(function_call, verbose=verbose)

            # 1. Ensure parts exists and is non-empty
            if not function_call_result.parts:
                raise Exception("...")

            first_part = function_call_result.parts[0]

            # 2. Ensure function_response is not None
            if not first_part.function_response:
                raise Exception("...")

            func_response = first_part.function_response

            # 3. Ensure response field is not None
            if func_response.response is None:
                raise Exception("Function call result has no parts")

            # 4. Store the part
            function_results.append(first_part)

            # 5. If verbose, print the result
            if verbose:
                print(f"-> {func_response.response}")
        
        messages.append(types.Content(role="user", parts=function_results))
        return None
    
    else:
        return response.text


if __name__ == "__main__":
    main()
