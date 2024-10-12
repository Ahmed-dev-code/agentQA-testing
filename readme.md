# AgentQL technical testing report 

## installation

using cli to install.
the installation was easy and straight forward, starting from installing agentQL using pip, then installing the dependencies using agentQL init command.
getting the api key was easy and straight forward.

## testing

### example_script (provided by agentQL)

the script was so clear and easy to understand, the output was as expected.
modified the script in order to make adds the product to the basket and print the basket total price.
the added code was:
```python
BASKET_TOTAL_PROMPT = "Basket total"

ADD_BASKET_BTN = """
    {
    add_to_basket
    }
"""

def _add_qwillfish_to_cart(page : Page):
    # the above code was not modified

    # Add to basket
    add_to_basket_btn = page.query_elements(ADD_BASKET_BTN)
    add_to_basket_btn.add_to_basket.click()
    page.wait_for_timeout(5000)
    
    basket_total = page.get_by_prompt(BASKET_TOTAL_PROMPT)
    print(f'basket total after adding qwilfish : {basket_total.text_content()}')
```

worked as expected.

modified the script to delete the product from the basket and print the basket total price.

the added code was:
```python
REMOVE_BASKET_BTN = """
    {
    remove_from_basket
    }
"""
def _add_qwillfish_to_cart(page : Page):
    # the above code was not modified

    # Add to basket
    add_to_basket_btn = page.query_elements(ADD_BASKET_BTN)
    print(add_to_basket_btn)
    add_to_basket_btn.add_to_basket.click()
    page.wait_for_timeout(5000)
    
    basket_total = page.get_by_prompt(BASKET_TOTAL_PROMPT)
    print(f'basket total after adding qwilfish : {basket_total.text_content()}')
 # Remove from basket
    remove_from_basket_btn = page.query_elements(REMOVE_BASKET_BTN)
    
    remove_from_basket_btn.remove_from_basket.click()
    page.wait_for_timeout(5000)
    
    basket_total = page.get_by_prompt(BASKET_TOTAL_PROMPT)
    print(f'basket total after removing qwilfish : {basket_total.text_content()}')
```
log :
  - retrying click action, attempt #60
  -   waiting 500ms
  -   waiting for element to be visible, enabled and stable
  -   element is visible, enabled and stable
  -   scrolling into view if needed
  -   done scrolling
  -   element is outside of the viewport

had problem with deleting the product from the basket, the element was outside of the viewport, tried to scroll into view but it didn't work. the deleteing button can be visible only when hovering over the basket.


please provide more about AQLResponseProxy class, and how to use it.

### testing with other websites
#### Jumiia website (arabic version)
navigate to the website, close the popup window, locate the search bar, serach for a product in arabic. and then print the product name and price.

code:
```python
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
    search_product_box
}
"""

PRODUCT_DATA_QUERY = """
{
    price_currency
    products[] {
        name
        price
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

        # Type the search query into the search box
        search_box.search_product_box.type("حذاء رجال")
        page.keyboard.press("Enter")

        # Extract the product data using the AgentQL query
        product_data = page.query_data(PRODUCT_DATA_QUERY)

        # Print the extracted data
        print(product_data)


if __name__ == "__main__":
    main()
```

the script worked as expected, the product name and price were printed.
I reexecuted the script but it didn't work, it was stuck searching for the products.

tried to get the different language version of the website, but the script didn't work, it was stuck.
code :
```python
LANGUAGES_QUERY = """
{
    languaes[] {
        name
    }
}
"""

# Extract the categories using the AgentQL query
        languages = page.query_data(LANGUAGES_QUERY)

        # Print the extracted categories
        print(languages)
```

#### youtube website
navigate to the website, search for a video, click on the video, and print the video title. 
