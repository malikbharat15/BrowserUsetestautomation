from langchain.prompts import PromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import json

# Initialize the chat model
chat = ChatOpenAI(model_name="gpt-4-turbo", temperature=0.3)

# Define the prompt template
prompt_template = PromptTemplate(
    input_variables=["html", "url"],
    template="""
    Generate a Playwright test file that validates WCAG 2.1 Level A and AA compliance.
    Include both automated (@axe-core) and manual checks.

    Requirements:
    1. Structure tests using Playwright's describe/test format
    2. Cover these WCAG 2.1 criteria:
       - A: 1.1.1, 2.1.1, 4.1.2
       - AA: 1.4.3, 2.4.6, 3.2.3
    3. Use semantic selectors (roles, text) over CSS classes
    4. Include clear comments mapping to WCAG criteria

    Return ONLY the code block in this format:
    ```javascript
    const {{ test, expect }} = require('@playwright/test');
    const AxeBuilder = require('@axe-core/playwright').default;

    test.describe('WCAG 2.1 A/AA Compliance: {url}', () => {{
        // Automated axe-core scan
        test('Automated WCAG violations', async ({{ page }}) => {{
            /* WCAG 2.1 A/AA rules */
            await page.goto('{url}');
            const results = await new AxeBuilder({{ page }})
                .withTags(['wcag2a', 'wcag2aa'])
                .disableRules(['color-contrast'])
                .analyze();
            expect(results.violations).toEqual([]);
        }});

        // Manual checks
        test('Manual WCAG verification', async ({{ page }}) => {{
            await page.goto('{url}');
            /* 1.1.1 Non-text Content (A) */
            // Test implementation...
        }});
    }});
    ```

    HTML Content:
    {html}
    """
)


def generate_wcag_tests(html_content, page_url):
    # Format the prompt
    prompt = prompt_template.format(html=html_content[:10000], url=page_url)

    # Generate response
    response = chat([HumanMessage(content=prompt)])

    # Extract the code block
    try:
        code_block = response.content.split("```javascript")[1].split("```")[0].strip()
        return code_block
    except Exception as e:
        print(f"Error parsing response: {str(e)}")
        return None


# Example usage
with open("accessibility_data.json") as f:
    data = json.load(f)

tests = generate_wcag_tests(data["html"], data.get("url", "https://example.com"))
if tests:
    with open("wcag_tests.spec.js", "w") as f:
        f.write(tests)