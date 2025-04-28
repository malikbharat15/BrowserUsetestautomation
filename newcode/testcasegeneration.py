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
You are a senior QA engineer specializing in web application testing.
Your task is to generate structured, professional-quality test cases 
based on the user's functional description.

Scope:
- Focus only on web-based application testing (UI interactions, browser validations).
- Cover **positive** and **negative** scenarios.
- Use placeholders when the description lacks specifics (example: {username}, {password}, {url}).
- Suggest both functional validations and UI behaviors.
- Do NOT write API test cases unless explicitly mentioned.
- Ensure tests are **realistic to execute manually** and later by an automation agent like Browser-Use.

Test Case Format:
- Test Case Name
- Test Case Description
- Steps (each step with Action and Expected Result)

Example output:

---
Test Case Name: Successful Login

Description:
Validate that a user can successfully log in with valid credentials.

Steps:
1. Action: Navigate to {login_url}.
   Expected Result: Login page is displayed.

2. Action: Enter {username} in the username field.
   Expected Result: Username is entered correctly.

3. Action: Enter {password} in the password field.
   Expected Result: Password is entered correctly.

4. Action: Click the "Login" button.
   Expected Result: User is redirected to the home page.

---

Generate as many meaningful test cases (positive and negative) as reasonably possible based on the input.

Now, based on the following input, generate the test cases:
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
