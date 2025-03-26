import os
from langchain_openai import OpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
import argparse

# Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or "your_api_key_here"
MODEL_NAME = "gpt-4-turbo"  # or "gpt-4o"


def generate_cypress_tests(component_code):
    """
    Generates Cypress accessibility tests using LangChain + GPT-4
    """
    prompt = PromptTemplate.from_template("""
    You are an accessibility testing expert. Generate comprehensive Cypress tests for this React component
    that validate WCAG 2.1 AA compliance. Focus on:

    1. Keyboard navigation (tab order, arrow keys)
    2. Screen reader compatibility (ARIA attributes)
    3. Focus management (modals, dialogs)
    4. Dynamic content (loading states, errors)
    5. Color contrast verification (where detectable)

    Include tests for all interactive elements. Output ONLY the Cypress test code.

    Component:
    ```jsx
    {component_code}
    ```

    Example Structure:
    ```javascript
    describe('Component Accessibility', () => {{
      it('should manage focus correctly', () => {{
        // Test implementation
      }});
    }});
    ```
    """)

    llm = OpenAI(
        model_name=MODEL_NAME,
        temperature=0.3,
        max_tokens=2000,
        openai_api_key=OPENAI_API_KEY
    )

    chain = LLMChain(llm=llm, prompt=prompt)
    return chain.run(component_code=component_code)


def main():
    parser = argparse.ArgumentParser(description="Generate Cypress tests with GPT-4")
    parser.add_argument("file", help="React component file path")
    args = parser.parse_args()

    with open(args.file, "r") as f:
        component_code = f.read()

    print("Generating Cypress tests...")
    tests = generate_cypress_tests(component_code)

    # Save to test directory
    test_dir = "cypress/e2e/accessibility"
    os.makedirs(test_dir, exist_ok=True)
    test_file = os.path.join(test_dir,
                             f"{os.path.splitext(os.path.basename(args.file))[0]}.accessibility.cy.js")

    with open(test_file, "w") as f:
        f.write(tests)

    print(f"Tests saved to {test_file}")


if __name__ == "__main__":
    main()