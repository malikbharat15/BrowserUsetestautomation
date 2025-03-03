import json
import os
from pathlib import Path
import gradio as gr

class testcaseutils:
    # Function to save test suite to a JSON file
    def save_test_suite(test_suite_name, test_cases):
        """
        Saves a test suite to a JSON file.
        """
        test_suite_dir = Path("test_suites")
        test_suite_dir.mkdir(exist_ok=True)  # Create the directory if it doesn't exist

        test_suite_file = test_suite_dir / f"{test_suite_name}.json"
        with open(test_suite_file, "w") as file:
            json.dump(test_cases, file, indent=4)

        return f"Test suite '{test_suite_name}' saved to {test_suite_file}."

    # Function to load test suite from a JSON file
    def load_test_suite(test_suite_name):
        """
        Loads a test suite from a JSON file.
        """
        test_suite_file = Path("test_suites") / f"{test_suite_name}.json"
        if test_suite_file.exists():
            with open(test_suite_file, "r") as file:
                return json.load(file)
        return []

    # Function to add a new test case to a test suite
    def add_test_case(test_suite_name, test_case_name, test_case_description, test_cases):
        """
        Adds a new test case to the test suite.
        """
        test_cases.append({
            "test_case_name": test_case_name,
            "test_case_description": test_case_description
        })
        testcaseutils.save_test_suite(test_suite_name, test_cases)
        return test_cases, f"Test case '{test_case_name}' added to '{test_suite_name}'."

    # Function to create a new test suite
    def create_new_test_suite(test_suite_name):
        """
        Creates a new test suite.
        """
        test_cases = []
        testcaseutils.save_test_suite(test_suite_name, test_cases)
        return test_cases, f"New test suite '{test_suite_name}' created."

    # Gradio UI for Test Case Management
def create_test_case_management_tab():
        """
        Creates the Test Case Management tab in the Gradio UI.
        """
        with gr.TabItem("🧪 Test Case Management", id=7):
            with gr.Row():
                test_suite_name = gr.Textbox(
                    label="Test Suite Name",
                    placeholder="Enter test suite name...",
                    interactive=True
                )
                new_test_suite_button = gr.Button("🆕 New Test Suite", variant="primary")

            with gr.Row():
                test_case_name = gr.Textbox(
                    label="Test Case Name",
                    placeholder="Enter test case name...",
                    interactive=True
                )
                test_case_description = gr.Textbox(
                    label="Test Case Description",
                    placeholder="Enter test case description...",
                    lines=3,
                    interactive=True
                )
                add_test_case_button = gr.Button("➕ Add Test Case", variant="secondary")

            with gr.Row():
                test_cases_output = gr.JSON(
                    label="Test Cases"
                )
                status_output = gr.Textbox(
                    label="Status",
                    interactive=False
                )

            # Event handlers
            new_test_suite_button.click(
                fn=testcaseutils.create_new_test_suite,
                inputs=test_suite_name,
                outputs=[test_cases_output, status_output]
            )

            add_test_case_button.click(
                fn=testcaseutils.add_test_case,
                inputs=[test_suite_name, test_case_name, test_case_description, test_cases_output],
                outputs=[test_cases_output, status_output]
            )

            # Load test cases when test suite name changes
            test_suite_name.change(
                fn=testcaseutils.load_test_suite,
                inputs=test_suite_name,
                outputs=test_cases_output
            )

    # Add the Test Case Management tab to the existing UI

