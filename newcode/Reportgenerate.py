import json

def generate_html_report(json_file, recording_path, output_file="report.html"):
    """
    Generates a fancy HTML report from the structured JSON file and includes a link to the recording.
    """
    # Load the structured JSON file
    with open(json_file, "r") as file:
        test_data = json.load(file)

    # Extract data from the JSON file
    task_name = test_data.get("task_name", "N/A")
    task_description = test_data.get("task_description", "N/A")
    steps = test_data.get("steps", [])
    final_result = test_data.get("final_result", "N/A")
    errors = test_data.get("errors", [])
    overall_status = test_data.get("overall_status", "UNKNOWN")

    # Generate the HTML content
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Test Execution Report</title>
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
            .status {{
                font-size: 1.2em;
                font-weight: bold;
                text-align: center;
                padding: 10px;
                border-radius: 5px;
                margin-bottom: 20px;
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
                margin-bottom: 20px;
                padding: 15px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #f9f9f9;
            }}
            .step h3 {{
                margin-top: 0;
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
                margin-top: 20px;
            }}
            .recording-link {{
                text-align: center;
                margin-top: 20px;
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
    </head>
    <body>
        <div class="report-container">
            <h1>Test Execution Report</h1>
            <div class="status {overall_status.lower()}">
                Overall Status: {overall_status}
            </div>
            <h2>Task Details</h2>
            <p><strong>Task Name:</strong> {task_name}</p>
            <p><strong>Task Description:</strong> {task_description}</p>

            <h2>Steps</h2>
    """

    # Add steps to the HTML content
    for i, step in enumerate(steps):
        html_content += f"""
            <div class="step">
                <h3>Step {i + 1}: {step.get('step_description', 'N/A')}</h3>
                <p><strong>Thought Process:</strong> {step.get('step_thought_process', 'N/A')}</p>
                <p><strong>Action:</strong> {step.get('step_action', 'N/A')}</p>
                <p><strong>Result:</strong> {step.get('step_result', 'N/A')}</p>
            </div>
        """

    # Add final result, errors, and recording link
    html_content += f"""
            <h2>Final Result</h2>
            <p>{final_result}</p>
    """

    if errors:
        html_content += """
            <div class="errors">
                <h2>Errors</h2>
                <ul>
        """
        for error in errors:
            html_content += f"<li>{error}</li>"
        html_content += """
                </ul>
            </div>
        """

    html_content += f"""
            <div class="recording-link">
                <h2>Recording</h2>
                <p><a href="{recording_path}" target="_blank">View Recording</a></p>
            </div>
        </div>
    </body>
    </html>
    """

    # Save the HTML report to a file
    with open(output_file, "w") as file:
        file.write(html_content)

    print(f"Report generated successfully: {output_file}")


# Example usage
if __name__ == "__main__":
    # Path to the structured JSON file
    json_file = "/Users/bharatmalik/Documents/web-ui-main/tmp/agent_history/structured_history.json"

    # Path to the recording (replace with the actual path)
    recording_path = "/Users/bharatmalik/Documents/web-ui-main/tmp/record_videos/008ded92aa06a6ff0649fe940140789b.webm"

    # Generate the HTML report
    generate_html_report(json_file, recording_path, output_file="report.html")