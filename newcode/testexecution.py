import json
from pathlib import Path
import gradio as gr

from src.utils.TestCaseutils import testcaseutils



def create_test_execution_tab():
    """
    Creates the Test Execution tab in the Gradio UI.
    """
    with gr.TabItem("🚀 Test Execution", id=10):
        with gr.Row():
            test_suite_name = gr.Textbox(
                label="Test Suite Name",
                placeholder="Enter test suite name...",
                interactive=True
            )
            load_test_suite_button = gr.Button("📂 Load Test Suite", variant="primary")

        with gr.Row():
            test_case_index = gr.Number(
                label="Test Case Index",
                value=0,
                precision=0,
                interactive=True,
                info="Enter the index of the test case to run (starting from 0)."
            )
            run_test_case_button = gr.Button("▶️ Run Test Case", variant="secondary")

        with gr.Row():
            run_entire_suite_checkbox = gr.Checkbox(
                label="Run Entire Test Suite",
                value=False,
                interactive=True
            )
            run_test_suite_button = gr.Button("▶️ Run Test Suite", variant="primary")

        with gr.Row():
            test_execution_output = gr.Textbox(
                label="Test Execution Output",
                interactive=False
            )
            test_results_output = gr.JSON(
                label="Test Results",
                interactive=False
            )

        # Event handlers
        load_test_suite_button.click(
            fn=testcaseutils.load_test_suite,
            inputs=test_suite_name,
            outputs=test_results_output
        )

        run_test_case_button.click(
            fn=run_test_case_or_suite,
            inputs=[test_suite_name, test_case_index, gr.State(False)],
            outputs=[test_execution_output, test_results_output, None, None, None]
        )

        run_test_suite_button.click(
            fn=run_test_case_or_suite,
            inputs=[test_suite_name, gr.State(0), gr.State(True)],
            outputs=[test_execution_output, test_results_output, None, None, None]
        )

async def run_test_case_or_suite(test_suite_name, test_case_index, run_entire_suite):
    """
    Runs a specific test case or the entire test suite.
    """
    # Load the test suite
    test_cases = testcaseutils.load_test_suite(test_suite_name)
    if not test_cases:
        return "No test cases found in the test suite.", None, None, None, None

    # Prepare the task(s) to run
    if run_entire_suite:
        tasks = [test_case["test_case_description"] for test_case in test_cases]
        return tasks
    else:
        if test_case_index >= len(test_cases):
            return "Invalid test case index.", None, None, None, None
        tasks = [test_cases[test_case_index]["test_case_description"]]
        return tasks


def get_test_case_description(test_results_output, test_case_index):
    """
    Fetch the test case description from test_results_output based on test_case_index.
    Handle cases where test_results_output is None or test_case_index is out of bounds.
    """
    print("test results output",test_results_output.value)
    print("test case index",test_case_index.value)
    if test_results_output is None or not isinstance(test_results_output, list):
        return "No test cases loaded."

    if not (0 <= test_case_index < len(test_results_output)):
        return "Invalid test case index."

    return test_results_output[test_case_index].get("description", "No description available.")


