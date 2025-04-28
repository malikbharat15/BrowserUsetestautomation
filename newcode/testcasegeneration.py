# File: generate_webapp_testcases.py

import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

def read_input_file(file_path):
    """Reads the content of a file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def generate_test_cases(file_content):
    """Generates plain text test cases for web applications using an LLM."""

    system_prompt = """
You are an expert QA Engineer creating professional web application test cases.

Your task:
- From the provided feature description, generate plain text test cases.
- Every Test Case must include:
    - Test Case Name
    - Objective
    - Steps (each step must have an Action and an Expected Result)

Steps Format (STRICT):
- For each step, define:
    - Action: (what the user does)
    - Expected Result: (what the application/system must do)

Structure:
Test Case Name: <Name>
Objective: <Objective of the test case>
Steps:
1.
   Action: <Action description>
   Expected Result: <Expected result after action>
2.
   Action: <Action description>
   Expected Result: <Expected result after action>
...

Rules:
- Only create test cases relevant for Web Applications.
- If the feature description is high-level or has missing info, create placeholders like {username}, {password}, {url}.
- Generate Positive and Negative test cases based on the description.
- Be exhaustive but practical (don't over-generate unnecessary cases).
- Maintain professionalism: spelling, grammar, and formatting should match real industry standards.
- No test data hardcoding unless provided.

Output strictly in plain text format. No JSON, YAML, or markdown.
"""

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": file_content}
        ],
        temperature=0.2,
        max_tokens=3000
    )

    output = response['choices'][0]['message']['content']
    return output

def save_output_file(output_text, output_path):
    """Saves the output text to a file."""
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(output_text)

def main():
    input_file = "webapp_input.txt"     # Update this
    output_file = "webapp_testcases.txt"  # Update this

    file_content = read_input_file(input_file)
    test_cases = generate_test_cases(file_content)
    save_output_file(test_cases, output_file)

    print(f"Web app test cases generated and saved to {output_file}")

if __name__ == "__main__":
    main()
