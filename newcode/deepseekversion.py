import argparse
import os
import google.generativeai as genai
from google.api_core import exceptions



def analyze_with_gemini(source_code):
    """
    Analyzes source code for accessibility issues using Google's Gemini.
    Uses the same WCAG-focused prompt structure.
    """
    prompt = f"""
    You are an AI accessibility expert specializing in WCAG 2.1 standards. Analyze this source code:

    Code:
    ```
    {source_code}
    ```

    Identify all accessibility issues including:
    1. Semantic HTML violations (e.g., missing headings, improper nesting)
    2. ARIA misuse (redundant roles, missing properties)
    3. Keyboard navigation blockers
    4. Form labeling issues
    5. Image/text alternative problems
    6. Color contrast concerns (for hardcoded values)
    7. Dynamic content accessibility (focus management, live regions)

    For each issue found:
    - Describe the WCAG violation
    - Provide line number/location if detectable
    - Suggest a code fix
    - Explain user impact

    Format your response with clear issue headings.
    """

    try:
        genai.configure(api_key=GEMINI_API_KEY)

        # Use the correct model name for your API version
        model = genai.GenerativeModel('gemini-1.5-pro-latest')  # Updated model name

        # Adjust generation parameters
        response = model.generate_content(
            prompt,
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 2000,
            },
            safety_settings={
                "HARM_CATEGORY_HARASSMENT": "BLOCK_NONE",
                "HARM_CATEGORY_HATE_SPEECH": "BLOCK_NONE",
                "HARM_CATEGORY_SEXUALLY_EXPLICIT": "BLOCK_NONE",
                "HARM_CATEGORY_DANGEROUS_CONTENT": "BLOCK_NONE",
            }
        )

        # Handle the response properly
        if response.text:
            return response.text
        return "No response generated (possibly blocked by safety filters)"

    except exceptions.NotFound as e:
        return f"Model not found. Available models: {genai.list_models()}"
    except Exception as e:
        return f"Gemini analysis failed: {str(e)}"


def main():
    parser = argparse.ArgumentParser(
        description="GenAI Accessibility Analyzer (Gemini)"
    )
    parser.add_argument("file", help="HTML/JS/JSX file to analyze")
    args = parser.parse_args()

    if not os.path.exists(args.file):
        print("Error: File does not exist.")
        return

    with open(args.file, "r") as f:
        source_code = f.read()

    print("\n=== Gemini Accessibility Analysis ===")
    results = analyze_with_gemini(source_code)
    print(results)


if __name__ == "__main__":
    main()