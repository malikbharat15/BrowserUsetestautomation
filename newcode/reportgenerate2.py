import json

def generate_html_report(json_file, output_file="report.html"):
    """
    Generates a fancy HTML report from the structured JSON file (test suite) with expand/collapse functionality.
    """
    # Load the structured JSON file
    with open(json_file, "r") as file:
        test_suite_data = json.load(file)

    # Calculate summary statistics
    total_test_cases = len(test_suite_data)
    passed_test_cases = sum(1 for test_case in test_suite_data if test_case.get("overall_status") == "PASS")
    failed_test_cases = sum(1 for test_case in test_suite_data if test_case.get("overall_status") == "FAIL")
    unknown_test_cases = sum(1 for test_case in test_suite_data if test_case.get("overall_status") == "UNKNOWN")

    # Generate the HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Test Suite Execution Report</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f4f4;
                margin: 0;
                padding: 20px;
            }}
            .report-container {{
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                padding: 20px;
                max-width: 800px;
                margin: 0 auto;
            }}
            h1 {{
                color: #333;
                text-align: center;
            }}
            h2 {{
                color: #555;
                border-bottom: 2px solid #ddd;
                padding-bottom: 10px;
            }}
            .summary {{
                margin-bottom: 20px;
                padding: 15px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #f9f9f9;
            }}
            .summary p {{
                margin: 5px 0;
            }}
            .test-case {{
                margin-bottom: 10px;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #f9f9f9;
            }}
            .test-case-header {{
                cursor: pointer;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            .test-case-header h3 {{
                margin: 0;
                color: #333;
            }}
            .test-case-header.failed {{
                color: #721c24;
                background-color: #f8d7da;
                padding: 10px;
                border-radius: 5px;
            }}
            .test-case-details {{
                display: none;
                margin-top: 10px;
            }}
            .status {{
                font-size: 1.2em;
                font-weight: bold;
                text-align: center;
                padding: 10px;
                border-radius: 5px;
            }}
            .status.pass {{
                background-color: #d4edda;
                color: #155724;
            }}
            .status.fail {{
                background-color: #f8d7da;
                color: #721c24;
            }}
            .status.unknown {{
                background-color: #fff3cd;
                color: #856404;
            }}
            .step {{
                margin-bottom: 10px;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #f9f9f9;
            }}
            .step h4 {{
                margin: 0;
                color: #333;
            }}
            .step p {{
                margin: 5px 0;
            }}
            .errors {{
                color: #721c24;
                background-color: #f8d7da;
                padding: 10px;
                border-radius: 5px;
                margin-top: 10px;
            }}
            .recording-link {{
                margin-top: 10px;
            }}
            .recording-link a {{
                color: #007bff;
                text-decoration: none;
                font-weight: bold;
            }}
            .recording-link a:hover {{
                text-decoration: underline;
            }}
        </style>
        <script>
            function toggleDetails(testCaseId) {{
                var details = document.getElementById(testCaseId);
                if (details.style.display === "none") {{
                    details.style.display = "block";
                }} else {{
                    details.style.display = "none";
                }}
            }}
        </script>
    </head>
    <body>
        <div class="report-container">
            <h1>Test Suite Execution Report</h1>

            <!-- Summary Section -->
            <div class="summary">
                <h2>Summary</h2>
                <p><strong>Total Test Cases:</strong> {total_test_cases}</p>
                <p><strong>Passed:</strong> {passed_test_cases}</p>
                <p><strong>Failed:</strong> {failed_test_cases}</p>
                <p><strong>Unknown:</strong> {unknown_test_cases}</p>
            </div>
    """

    # Iterate through each test case and generate its report
    for idx, test_case in enumerate(test_suite_data):
        task_name = test_case.get("task_name", "N/A")
        task_description = test_case.get("task_description", "N/A")
        steps = test_case.get("steps", [])
        final_result = test_case.get("final_result", "N/A")
        errors = test_case.get("errors", [])
        overall_status = test_case.get("overall_status", "UNKNOWN")
        recording_link = test_case.get("recording_link", "")

        # Add test case header with expand/collapse functionality
        html_content += f"""
            <div class="test-case">
                <div class="test-case-header {'failed' if overall_status == 'FAIL' else ''}" onclick="toggleDetails('test-case-{idx}')">
                    <h3>Test Case {idx + 1}: {task_name}</h3>
                    <div class="status {overall_status.lower()}">
                        {overall_status}
                    </div>
                </div>
                <div id="test-case-{idx}" class="test-case-details">
                    <p><strong>Task Description:</strong> {task_description}</p>

                    <h4>Steps</h4>
        """

        # Add steps for the test case
        for i, step in enumerate(steps):
            html_content += f"""
                <div class="step">
                    <h5>Step {i + 1}: {step.get('step_description', 'N/A')}</h5>
                    <p><strong>Thought Process:</strong> {step.get('step_thought_process', 'N/A')}</p>
                    <p><strong>Action:</strong> {step.get('step_action', 'N/A')}</p>
                    <p><strong>Result:</strong> {step.get('step_result', 'N/A')}</p>
                </div>
            """

        # Add final result and errors for the test case
        html_content += f"""
                    <h4>Final Result</h4>
                    <p>{final_result}</p>
        """

        if errors:
            html_content += """
                    <div class="errors">
                        <h4>Errors</h4>
                        <ul>
            """
            for error in errors:
                html_content += f"<li>{error}</li>"
            html_content += """
                        </ul>
                    </div>
            """

        # Add recording link for the test case
        if recording_link:
            html_content += f"""
                    <div class="recording-link">
                        <h4>Recording</h4>
                        <p><a href="{recording_link}" target="_blank">View Recording</a></p>
                    </div>
            """

        html_content += """
                </div>
            </div>
        """

    # Close the HTML content
    html_content += """
        </div>
    </body>
    </html>
    """

    # Save the HTML report to a file
    with open(output_file, "w") as file:
        file.write(html_content)

    print(f"Test Suite Report generated successfully: {output_file}")


# Example usage
if __name__ == "__main__":
    # Path to the structured JSON file (test suite)
    json_file = "/Users/bharatmalik/Documents/web-ui-main/tmp/agent_history/My test suite_structured.json"

    # Generate the HTML report
    generate_html_report(json_file, output_file="test_suite_report.html")