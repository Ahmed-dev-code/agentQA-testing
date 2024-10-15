import agentql
from playwright.sync_api import sync_playwright 
import json

URL ="https://www.chocolate.co.uk/collections/all"

PRODUCTS_QUERY = """
{   
    currency
    product_items[] {
        title
        price
    }
}
"""
PAGE_TITLE_QUERY = """
{
    title
}
"""
PAGE_TITLE_PROMPT = "GET the current PAGE TITLE"

def main():
    with sync_playwright() as playwright, playwright.chromium.launch(headless=False) as browser:
        # Create a new page in the browser and wrap it to get access to the AgentQL's querying API
        page = agentql.wrap(browser.new_page())

        page.goto(URL)
        
        page_title = page.get_by_prompt(PAGE_TITLE_PROMPT)
        print(page_title.text_content())

        # Use query_data() method to fetch the products from the page
        response = page.query_data(PRODUCTS_QUERY)

        print(response)
        
        # Write the JSON data to a file
        with open('chocolate_products.json', 'w', encoding='utf-8') as file:
            json.dump(response, file, ensure_ascii=False, indent=4)
        
if __name__ == "__main__":
    main()
    
    