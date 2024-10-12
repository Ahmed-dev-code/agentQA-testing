import agentql
from playwright.sync_api import sync_playwright

URL ="https://www.chocolate.co.uk/collections/all"

PRODUCTS_QUERY = """
{   
    currency
    products[] {
        title
        price
    }
}
"""

def main():
    with sync_playwright() as playwright, playwright.chromium.launch(headless=False) as browser:
        # Create a new page in the browser and wrap it to get access to the AgentQL's querying API
        page = agentql.wrap(browser.new_page())

        page.goto(URL)

        # Use query_data() method to fetch the products from the page
        response = page.query_data(PRODUCTS_QUERY)

        print(response)
        
if __name__ == "__main__":
    main()
    
    