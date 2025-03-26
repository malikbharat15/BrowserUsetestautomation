import argparse
import os
from langchain_community.llms import OpenAI  # Supports multiple providers
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

# Configuration - Set your API key



def analyze_with_llm(source_code):
    """
    Analyzes source code using LangChain with a structured prompt.
    """
    prompt_template = PromptTemplate.from_template("""
    You are an accessibility expert auditing code for WCAG 2.1 AA compliance.
    Analyze this code and identify violations:

    Code:
    ```html
    {source_code}
    ```

    For each issue:
    1. Describe the WCAG violation (include guideline number)
    2. Provide the exact location (line number if possible)
    3. Suggest a code fix
    4. Explain user impact

    Format response with clear headings.
    """)

    try:
        # Initialize LLM (works with OpenAI, Anthropic, etc.)
        llm = OpenAI(
            model_name=MODEL_NAME,
            temperature=0.2,
            max_tokens=2000,
            openai_api_key=LLM_API_KEY
        )

        # Create chain
        chain = LLMChain(llm=llm, prompt=prompt_template)
        response = chain.run(source_code=source_code)

        return response.strip()

    except Exception as e:
        return f"LLM analysis failed: {str(e)}"

# ... (keep the rest of your script's main() function unchanged)