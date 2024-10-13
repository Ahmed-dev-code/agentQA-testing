import agentql
from agentql.ext.playwright.sync_api import Page

# Import the synchronous playwright library
# This library is used to launch the browser and interact with the web page
from playwright.sync_api import sync_playwright

URL = "https://www.jumia.com.dz/ar"  # the url in arabic language accessed from algeria

POPUP = """
{
    popup_form {
        close_btn
    }
}
"""

SEARCH_BOX_QUERY = """
{
    search_products_input
}
"""

ARTICLE_DATA_QUERY = """
{
    currency
    articles[] {
        name
        price
    }
}
"""

LANGUAGES_QUERY = """
{
    languaes[] {
        name
    }
}
"""



def main():
    with sync_playwright() as playwright, playwright.chromium.launch(
        headless=False
    ) as browser:
        # Create a new page in the browser and wrap it get access to the AgentQL's querying API
        page = agentql.wrap(browser.new_page())

        page.goto(URL)

        page.wait_for_timeout(500)
        # Use query_elements() method to fetch the close popup button from the page
        response = page.query_elements(POPUP)

        # Click the close button to close the popup
        response.popup_form.close_btn.click()
        # Wait for 10 seconds to see the browser in action
        page.wait_for_timeout(500)
        # Use the AgentQL query to locate the search box element
        search_box = page.query_elements(SEARCH_BOX_QUERY)
        print(search_box)

        # # Type the search query into the search box
        # search_box.search_products_input.type("حذاء رجال")
        # page.keyboard.press("Enter")

        # # # Extract the product data using the AgentQL query
        # product_data = page.query_elements(ARTICLE_DATA_QUERY)

        # # # Print the extracted data
        # print(product_data.to_data())
        
        # Extract the categories using the AgentQL query
        languages = page.query_data(LANGUAGES_QUERY)
    
        # Print the extracted data
        print(languages)


if __name__ == "__main__":
    main()
    
    
