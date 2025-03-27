import json

from playwright.sync_api import sync_playwright


def get_accessibility_dom(url, options={}):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=options.get('headless', True))
        page = browser.new_page()

        try:
            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_load_state(options.get('wait_for', 'networkidle'))

            # Get accessibility-focused DOM
            dom_data = page.evaluate("""({include_full_tree}) => {
                const clone = document.cloneNode(true);

                // Remove non-accessibility elements
                clone.querySelectorAll(`
                    script, noscript, 
                    style, link[rel="stylesheet"], 
                    meta, [aria-hidden="true"],
                    [style*="display:none"], [style*="display: none"],
                    [hidden]:not([hidden="false"])
                `).forEach(el => el.remove());

                // Process shadow DOM if needed
                if (include_full_tree) {
                    const walker = document.createTreeWalker(
                        clone, 
                        NodeFilter.SHOW_ELEMENT, 
                        { acceptNode: function(node) { 
                            return NodeFilter.FILTER_ACCEPT; 
                        }},
                        false
                    );

                    while(walker.nextNode()) {
                        const node = walker.currentNode;
                        if (node.shadowRoot) {
                            node.setAttribute('data-shadow-root', node.shadowRoot.innerHTML);
                        }
                    }
                }

                return {
                    html: clone.documentElement.outerHTML
                };
            }""", {"include_full_tree": options.get('include_full_tree', False)})

            if options.get('include_screenshot', False):
                dom_data['screenshot'] = page.screenshot(full_page=True)

            browser.close()
            return dom_data
        except Exception as e:
            browser.close()
            raise e

if __name__ == '__main__':
    data=get_accessibility_dom("https://broken-workshop.dequelabs.com/")
    with open("accessibility_data.json", "w") as f:
        json.dump(data, f, indent=2)