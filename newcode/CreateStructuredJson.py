import json

class createStructureJson:

    @staticmethod
    def create_structured_json(history, task_description):
        """
        Converts agent history into a structured JSON with specific fields for each step.
        The final_result is extracted from the "text" key in the "done" action of the last step
        where "is_done": true is present in the results.
        """
        # Initialize structured data with the correct order
        structured_data = {
            "task_name": "test case",  # Fixed task name
            "task_description": task_description,  # Use external task description
            "steps": [],  # Steps will be populated later
            "final_result": "No final result available",  # Default final result
            "errors": []  # Errors will be populated later
        }

        # Process all steps
        history_steps = history.get("history", [])
        for idx, raw_step in enumerate(history_steps):
            if not isinstance(raw_step, dict):
                continue

            model_output = raw_step.get("model_output", {})
            current_state = model_output.get("current_state", {})
            actions = model_output.get("action", [{}])
            results = raw_step.get("result", [{}])

            # Check if this is the final step (has "is_done": true in any result)
            is_final_step = False
            for result in results:
                if result.get("is_done", False):
                    is_final_step = True
                    break

            # If this is the final step, extract the final_result from the "done" action
            if is_final_step:
                for action in actions:
                    if "done" in action:
                        structured_data["final_result"] = action["done"].get("text", "Task completed.")
                        break  # Stop after finding the "done" action

            # Extract step description and thought process
            step_description = current_state.get("summary", "No step description available")
            step_thought_process = current_state.get("thought", "No thought process available")

            # Extract step action
            step_action = "No action available"
            if actions:
                action_type = list(actions[0].keys())[0]  # Get the action type (e.g., "go_to_url")
                action_details = actions[0][action_type]  # Get the action details (e.g., {"url": "..."})
                if action_type == "go_to_url":
                    step_action = f"Go to URL, {action_details.get('url', 'No URL provided')}"
                elif action_type == "click_element":
                    step_action = f"Click on button: {action_details.get('index', 'No index provided')}"
                elif action_type == "input_text":
                    step_action = f"Input text: {action_details.get('text', 'No text provided')}"
                else:
                    step_action = f"Action: {action_type}"

            # Extract step result (prev_action_evaluation of the next step)
            step_result = "No result available"
            if idx + 1 < len(history_steps):
                next_step = history_steps[idx + 1]
                next_step_state = next_step.get("model_output", {}).get("current_state", {})
                step_result = next_step_state.get("prev_action_evaluation", "No result available")

            # Add step data to structured_data
            structured_data["steps"].append({
                "step_description": step_description,
                "step_thought_process": step_thought_process,
                "step_action": step_action,
                "step_result": step_result
            })

            # Collect errors (if any)
            if results[0].get("error"):
                structured_data["errors"].append(results[0]["error"])

        return structured_data