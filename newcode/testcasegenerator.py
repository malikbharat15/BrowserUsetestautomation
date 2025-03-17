from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
import json

# Initialize the ChatOpenAI model
llm = ChatOpenAI(model="gpt-4")  # Use the appropriate model (e.g., "gpt-4", "gpt-3.5-turbo")

# Define the system message (instructions for the LLM)
system_message = """
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
"""


# Function to generate structured test case
def generate_test_case(user_input):
    # Create the chat messages
    messages = [
        SystemMessage(content=system_message),  # System message with instructions
        HumanMessage(content=f"User Input: {user_input}")  # User input
    ]

    # Call the ChatOpenAI model
    response = llm(messages)

    # Extract the generated test case from the response
    structured_test_case = response.content.strip()

    # Return the test case as a string
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