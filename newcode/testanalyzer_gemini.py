import json
import google.generativeai as genai  # Import the Google Generative AI library

# Set your Google API key

class TestResultAnalyzer:

    @staticmethod
    def evaluate_test_case(test_execution_data):
        print(test_execution_data)
        """
        Sends the test execution data to Google Gemini for evaluation and returns the overall_status.
        """
        # Create the prompt for the model
        prompt = f"""
        You are a Test Result Analyzer. Analyze the test execution data below and determine if the test case PASSED, FAILED, or is UNKNOWN. 

        Provide ONLY the status in this format:
        overall_status:PASS/FAIL/UNKNOWN

        **Evaluation Rules**:
        1. FAIL if:
           - Any critical step fails (navigation, search, checkout).
           - The final result does not match the expected outcome described in the test case description.
           - A step fails despite the model claiming success (contradiction).
        2. PASS if:
           - All critical steps succeed.
           - The final result matches the test case description, even if non-critical steps failed.
           - Partial failures are explicitly acknowledged but do not block success.

        **Test Case Description**:
        {test_execution_data["task_description"]}

        **Test Execution Data**:
        {json.dumps(test_execution_data, indent=4)}

        Response:
        """

        # Send the prompt to Google Gemini
        model = genai.GenerativeModel("gemini-2.0-flash")  # Use the Gemini Pro model
        response = model.generate_content(prompt)
        print("model response is", response)

        # Extract the model's response
        model_response = response.candidates[0].content.parts[0].text.strip()
        print("model response 2  is", model_response)


        # Parse the response as JSON
        if model_response.startswith("overall_status:"):
            overall_status = model_response.split(":")[1].strip().upper()
            if overall_status not in ["PASS", "FAIL", "UNKNOWN"]:
                overall_status = "UNKNOWN"
        else:
            overall_status = "UNKNOWN"

        return overall_status


# Example usage
if __name__ == "__main__":
    # Load the structured JSON output (created earlier)
    input_file = "/Users/bharatmalik/Documents/web-ui-main/src/utils/structured.json"
    with open(input_file, "r") as file:
        test_execution_data = json.load(file)

    # Evaluate the test case using Google Gemini
    analyzer = TestResultAnalyzer()
    overall_status = analyzer.evaluate_test_case(test_execution_data)
    print("overall status is ",overall_status)

    # Append the overall_status to the input file
    test_execution_data["overall_status"] = overall_status

    # Save the updated data back to the input file
    with open(input_file, "w") as file:
        json.dump(test_execution_data, file, indent=4)

    # Print the overall_status
    print(f"Overall Test Case Status: {overall_status}")
