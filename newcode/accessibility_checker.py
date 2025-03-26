import argparse
import os
import openai
from axe_selenium_python import Axe
from selenium import webdriver
from bs4 import BeautifulSoup




def analyze_with_gpt4o(source_code):
    """
    Analyzes the given source code using GPT-4O and returns accessibility issues.
    """
    prompt = f"""
    You are an AI accessibility expert specializing in the WCAG 2.1 standard (Levels A, AA, and AAA). You will analyze the given HTML, React, or JavaScript source code to find all possible accessibility issues based on WCAG guidelines. You must examine the code from the perspective of semantic structure, ARIA usage, keyboard navigation, focus management, and screen reader compatibility.

    1. **Identify all WCAG violations** in the source code, including:
       - **Perceivable Issues**:
         - Missing alternative text for images (WCAG 1.1.1).
         - Insufficient color contrast (WCAG 1.4.3).
         - Missing captions for multimedia (WCAG 1.2.2).
         - Improper use of semantic HTML elements (WCAG 1.3.1).
    
       - **Operable Issues**:
         - Keyboard accessibility issues (WCAG 2.1.1).
         - Missing focus indicators (WCAG 2.4.7).
         - Incorrect ARIA roles, properties, and attributes (WCAG 4.1.2).
         - Lack of focus trapping in modals (WCAG 2.4.3).
    
       - **Understandable Issues**:
         - Missing form labels (WCAG 3.3.2).
         - Links without descriptive text (WCAG 2.4.4).
         - Non-descriptive button text (e.g., "Click here").
    
       - **Robust Issues**:
         - Deprecated HTML tags or attributes.
         - Incorrect ARIA usage, such as unnecessary roles or redundant attributes.

    2. **Explain each issue found**, following this format:
       - **Issue Description**: Describe the issue and how it violates WCAG.
       - **Suggested Fix**: Provide a detailed solution with sample code.
       - **Impact**: Explain how this issue affects users with disabilities (e.g., screen reader users, keyboard-only users, users with low vision).
    
    3. **Go beyond static analysis by reasoning at the source code level**, considering dynamic behaviors like JavaScript-driven modals, dropdowns, and accordions. Suggest accessibility improvements for interactive components (e.g., role assignments, keyboard bindings, focus management).
    
    4. **Check JavaScript, React components, and DOM manipulation logic for potential accessibility issues**, like improper ARIA usage, focus mismanagement, and missing keyboard handlers. If the code dynamically updates content, suggest using ARIA live regions or other techniques to announce changes.
    
    5. **Suggest best practices** to improve the overall accessibility of the page, even if specific issues aren't detected, to ensure compliance with WCAG Level AA or AAA.
    

    Code:
    ```
    {source_code}
    ```
    """
    try:
        response = openai.Completion.create(
            model="gpt-4o",
            prompt=prompt,
            temperature=0.2,
            max_tokens=500,
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"Error analyzing with GPT-4O: {e}"


def analyze_with_axe(file_path):
    """
    Performs static accessibility analysis using Axe on the given HTML file.
    """
    try:
        driver = webdriver.Firefox()  # Requires geckodriver installed
        driver.get(f"file://{os.path.abspath(file_path)}")
        axe = Axe(driver)
        axe.inject()
        results = axe.run()
        driver.quit()

        violations = []
        for violation in results["violations"]:
            violations.append({
                "description": violation["description"],
                "help": violation["help"],
                "nodes": [node["html"] for node in violation["nodes"]]
            })
        return violations

    except Exception as e:
        return f"Error running Axe analysis: {e}"


def get_combined_results(source_code, static_violations):
    """
    Combines AI-based and static accessibility violations.
    """
    ai_analysis = analyze_with_gpt4o(source_code)
    combined_results = {
        "GPT-4O Analysis": ai_analysis,
        "Static Violations": static_violations,
    }
    return combined_results


def main():
    parser = argparse.ArgumentParser(description="Accessibility Checker with GPT-4O and Axe.")
    parser.add_argument("file", help="HTML or React source code file to analyze.")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print("Error: File does not exist.")
        return

    # Read source code and run analyses
    with open(args.file, "r") as file:
        source_code = file.read()

    print("\nRunning Axe Static Analysis...")
    static_violations = analyze_with_axe(args.file)

    print("\nRunning GPT-4O Accessibility Analysis...")
    combined_results = get_combined_results(source_code, static_violations)

    print("\nAccessibility Analysis Results:\n")
    print("GPT-4O Analysis:")
    print(combined_results["GPT-4O Analysis"])

    print("\nStatic Violations Detected by Axe:")
    for violation in combined_results["Static Violations"]:
        print(f"\nDescription: {violation['description']}")
        print(f"Suggestion: {violation['help']}")
        print(f"Affected Nodes: {', '.join(violation['nodes'])}")

    print("\n--- Accessibility Analysis Complete ---\n")


if __name__ == "__main__":
    main()
