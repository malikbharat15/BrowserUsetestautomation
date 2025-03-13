import json


class TaskResultParser:

    @staticmethod
    def parse_history(history_data, task_description, task_name="Test Case"):
        structured_data = {
            "task_name": task_name,
            "task_description": task_description,
            "steps": [],
            "final_result": "No completion status captured",
            "errors": []
        }

        history_steps = history_data.get("history", [])
        total_steps = len(history_steps)

        for step_idx, current_step in enumerate(history_steps):
            if not isinstance(current_step, dict):
                continue

            model_output = current_step.get("model_output", {})
            actions = model_output.get("action", [])
            current_state = model_output.get("current_state", {})
            results = current_step.get("result", [])

            # Skip steps that mark task completion
            if any("done" in action for action in actions):
                # Extract final result from "done" action
                for action in actions:
                    if "done" in action:
                        structured_data["final_result"] = action["done"].get("text", "Task completed")
                continue  # Skip processing this step entirely

            # Step description from current step
            step_description = current_state.get("next_goal", "No goal defined")

            # Step action from current step
            step_action = TaskResultParser._parse_actions(actions)

            # Step result from NEXT step's evaluation_previous_goal
            step_result = "No result captured"
            if step_idx < total_steps - 1:
                next_step = history_steps[step_idx + 1]
                next_state = next_step.get("model_output", {}).get("current_state", {})
                step_result = next_state.get("evaluation_previous_goal", step_result)

            # Add step to structured data
            structured_data["steps"].append({
                "step_description": step_description,
                "step_action": step_action,
                "step_result": step_result
            })

            # Collect errors
            for result in results:
                if result.get("error"):
                    structured_data["errors"].append({
                        "step": step_idx + 1,
                        "description": step_description,
                        "error": result["error"]
                    })

        return structured_data

    @staticmethod
    def _parse_actions(actions):
        """Convert raw actions to human-readable format"""
        action_strings = []
        for action in actions:
            for action_type, details in action.items():
                if action_type == "go_to_url":
                    action_strings.append(f"Navigated to: {details.get('url', 'Unknown URL')}")
                elif action_type == "click_element":
                    action_strings.append(f"Clicked element index {details.get('index', 'Unknown')}")
                elif action_type == "done":
                    action_strings.append("Marked task as complete")
                else:
                    action_strings.append(f"Performed {action_type} action")
        return action_strings or ["No action recorded"]

def process_and_save(input_path, output_path, task_description, task_name):
    # Load input data
    with open(input_path, 'r') as f:
        history_data = json.load(f)

    # Process through parser
    structured_data = TaskResultParser.parse_history(
        history_data,
        task_description=task_description,
        task_name=task_name
    )

    # Save structured output
    with open(output_path, 'w') as f:
        json.dump(structured_data, f, indent=2)

    return f"Successfully saved structured output to {output_path}"

    # _parse_actions() remains unchanged
if __name__ == '__main__':
    process_and_save("output.json","structured.json","test desc","tc1")