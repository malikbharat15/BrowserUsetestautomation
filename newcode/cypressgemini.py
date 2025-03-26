import google.generativeai as genai
import argparse
import os

# Configure Gemini

genai.configure(api_key=GEMINI_API_KEY)


def generate_cypress_tests(component_code):
    """
    Generates Cypress accessibility tests for a React component using Gemini.
    """
    prompt = f"""
    You are an expert in accessibility testing. Create Cypress end-to-end tests that validate 
    WCAG 2.1 AA compliance for this React component. Focus on:

    1. Keyboard navigation
    2. Screen reader compatibility (use cy.realPress() and aria attributes)
    3. Focus management
    4. Dynamic content announcements

    Include tests for:
    - Modal dialogs
    - Form controls
    - Interactive elements
    - Loading/error states

    Output ONLY the Cypress test code with no additional explanation.

    Component code:
    ```jsx
    {component_code}
    ```

    Example test structure:
    ```javascript
    describe('Component Accessibility', () => {{
      it('should trap focus in modal', () => {{
        cy.get('#open-modal').click();
        cy.focused().should('have.attr', 'role', 'dialog');
      }});
    }});
    ```
    """

    try:
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error generating tests: {str(e)}"


def main():
    parser = argparse.ArgumentParser(description="Generate Cypress tests from React components")
    parser.add_argument("file", help="React component file path")
    args = parser.parse_args()

    with open(args.file, "r") as f:
        component_code = f.read()

    print("Generating Cypress tests...")
    tests = generate_cypress_tests(component_code)

    # Save to test file
    test_file = os.path.join(".", os.path.basename(args.file).replace(".js", ".accessibility1.cy.js"))
    with open(test_file, "w") as f:
        f.write(tests)

    print(f"Tests saved to {test_file}")


if __name__ == "__main__":
    main()