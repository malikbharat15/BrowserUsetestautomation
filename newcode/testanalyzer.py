import json
from openai import OpenAI   # Ensure you have the OpenAI library installed

# Set your OpenAI API key
# openai.api_key = ""
client = OpenAI(api_key="")
class TestResultAnalyzer:

    @staticmethod
    def evaluate_test_case(test_execution_data):
        """
        Sends the test execution data to Google Gemini for evaluation and returns the overall_status.
        """
        # Create the prompt for the model
        prompt = f"""
            You are a Test Result Analyzer. Analyze the following test execution data and determine if the test case PASSED, FAILED, or is UNKNOWN. Provide a detailed JSON response with the following structure:

            {{
                "overall_status": "PASS/FAIL/UNKNOWN"
            }}

            Guidelines:
            1. FAIL if any critical step fails (e.g., login, search).
            2. FAIL if the final result does not match expectations.
            3. Use the model's thoughts and actions to explain the status.

            Test Execution Data:
            {json.dumps(test_execution_data, indent=4)}

            Response:
            """

        # Send the prompt to Google Gemini
        model = genai.GenerativeModel("gemini-2.0-flash")  # Use the Gemini Flash model
        response = model.generate_content(prompt)

        # Extract the model's response
        model_response = response.text

        # Parse the response as JSON
        try:
            analysis_result = json.loads(model_response)
            overall_status = analysis_result.get("overall_status", "UNKNOWN")
            print("overall status is", overall_status)
        except json.JSONDecodeError:
            # If the response is not valid JSON, try to extract the status directly
            if "PASS" in model_response.upper():
                overall_status = "PASS"
            elif "FAIL" in model_response.upper():
                overall_status = "FAIL"
            else:
                overall_status = "UNKNOWN"

        return overall_status


# Example usage
if __name__ == "__main__":
    # Load the structured JSON output (created earlier)
    input_file = "/Users/bharatmalik/Documents/web-ui-main/tmp/agent_history/structured_history.json"
    with open(input_file, "r") as file:
        test_execution_data = json.load(file)

    # Evaluate the test case using the model
    analyzer = TestResultAnalyzer()
    overall_status = analyzer.evaluate_test_case(test_execution_data)

    # Append the overall_status to the input file
    test_execution_data["overall_status"] = overall_status

    # Save the updated data back to the input file
    with open(input_file, "w") as file:
        json.dump(test_execution_data, file, indent=4)

    # Print the overall_status
    print(f"Overall Test Case Status: {overall_status}")
