import openai
import json

# Define the prompt template for the test case generator
prompt_template = """
You are a test case generator. Your task is to convert user input into a structured, step-by-step test case. Follow these rules:
1. Break the user input into clear, actionable steps.
2. Each step should describe what needs to be done in natural language.
3. Include an "Objective" and "Expected Result" for the test case.
4. Ensure the steps are specific and unambiguous.

**Example 1:**
User Input: "Fill out the registration form with first name John, last name Doe, select gender as Male, country as United States, and upload a profile picture."
Test Case:
### Test Case: Complete User Registration Form

**Objective:**  
Fill out the user registration form with all required fields and submit it.

**Steps:**
1. Go to https://example.com/register.
2. Enter "John" in the "First Name" field.
3. Enter "Doe" in the "Last Name" field.
4. Select "Male" as the gender.
5. Choose "United States" from the "Country" dropdown.
6. Upload the file "profile.jpg" to the "Profile Picture" field.
7. Click the "Submit" button.

**Expected Result:**  
The form is submitted successfully, and the user is redirected to the dashboard.

**Example 2:**
User Input: "Search for 'laptops' on Amazon, filter by 4-star ratings, and click the first result."
Test Case:
### Test Case: Search for Laptops on Amazon

**Objective:**  
Search for laptops on Amazon, filter by 4-star ratings, and click the first result.

**Steps:**
1. Go to https://www.amazon.com.
2. Enter "laptops" in the search bar and press Enter.
3. On the search results page, click the "4 Stars & Up" filter.
4. Click the first laptop in the filtered results.

**Expected Result:**  
The product page for the selected laptop is displayed.

**Now, convert the following user input into a structured test case:**
User Input: "{user_input}"
"""


# Function to generate structured test case
def generate_test_case(user_input):
    # Format the prompt with the user input
    prompt = prompt_template.format(user_input=user_input)

    # Call the LLM (e.g., OpenAI GPT-4) to generate the test case
    response = openai.Completion.create(
        engine="gpt-4",  # Use the appropriate model
        prompt=prompt,
        max_tokens=500,  # Adjust based on the expected length of the test case
        temperature=0.3 # Lower temperature for more deterministic output
    )

    # Extract the generated test case
    structured_test_case = response.choices[0].text.strip()

    # Return the test case as a dictionary or JSON object
    return structured_test_case


# Example usage
if __name__ == "__main__":
    # Example user input
    user_input = "Fill out the registration form with first name John, last name Doe, select gender as Male, country as United States, and upload a profile picture."

    # Generate the structured test case
    test_case = generate_test_case(user_input)

    # Print the generated test case
    print("Generated Test Case:")
    print(test_case)