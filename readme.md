# AgentQL technical testing report 

## Installation

- Used CLI For the installation.
- The installation was easy and straight forward, starting from installing agentQL using pip, then installing the dependencies using agentQL init command.
- Set up the API key: The process for acquiring and setting the API key is simple and can be followed from AgentQL’s documentation.

## testing

### Example script (provided by agentQL)

The example script provided by AgentQL was well-written and executed as expected. Below are the modifications and additional functionalities tested.

- Adding a Product to the Basket
I extended the functionality to add a product to the basket and print the total price:
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

- Removing a Product from the Basket
Next, I modified the script to remove the product from the basket and print the updated total price:

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

I encountered an issue with removing the product from the basket. The error indicated that the element was outside the viewport and required hovering over the basket for the button to become visible.



### testing with other websites
#### Jumia (Arabic Version)


Task: Navigate to the Jumia website, close the popup window, search for a product in Arabic, and print the product name and price.

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

The script initially worked as expected, returning product names and prices. However, when re-executed, it got stuck while searching for products. Switching from query_data() to to_data() resolved the issue.
```python
# Extract the product data using the AgentQL query
        response = page.query_elements(PRODUCT_DATA_QUERY)

        # Print the extracted data
        print(response.to_data())
```
the script worked as expected.

output :
``` json
{'currency': '7,600 دج', 
'articles': [{'name': 'حذاء جلد سهل الارتداء مريح للغاية للرجال - أسود', 'price': '7,600 دج'},
 {'name': 'Bokai Shoes حذاء رجالي -', 'price': '5,500 دج'},
  {'name': 'Bokai Shoes حذاء رجالي -', 'price': '5,500 دج'}, 
  ],}
```
note : the currency is in arabic, the script didn't return the currency in the correct format.

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
again the problem is with the query_data method, it takes too long to process.
replace the query_data method with to_data() method, the script worked as expected.

code:
```python
# Extract the categories using the AgentQL query
        response = page.query_elements(LANGUAGES_QUERY)

        # Print the extracted categories
        print(response.to_data())
```

output:
```
{'languaes': [{'name': 'العربية'}, {'name': 'Français'}, {'name': 'Français'}, {'name': 'العربية'}]}
```

#### YouTube

Task: Navigate to a YouTube video URL and print the video title, channel name, and comments.
code:
```python
QUERY = """
{
    video_title
    video_channel
    comments[] {
        comment_text
        author
    }
}
"""


def get_comments():
    with sync_playwright() as playwright, playwright.chromium.launch(headless=False) as browser:
        # Create a new page in the browser and wrap it to get access to the AgentQL's querying API
        page = agentql.wrap(browser.new_page())

        page.goto(URL,timeout=100000)

        for _ in range(5):
            # Wait for the page to load (helps to load the comments on the video)
            page.wait_for_page_ready_state()

            # Scroll down the page to load more comments
            page.keyboard.press("PageDown")

        # Use query_data() method to fetch the comments from the page
        response = page.query_elements(QUERY)


        return response.to_data()
```
the script worked as expected (although this script is from the example, the query_data() method got stuck. had to use to_data() method), the video title, channel name, and comments were printed.

output :
```
{'video_title': '؟ Docker ليه بنستخدم 💙',
 'video_channel': 'Yehia Tech يحيى تك', 
 'comments': [{'comment_text': 'فيديوهاتك من كثر ما هي قيمة جدا جدا ،، انا بخاف بيوم من الايام تنمسح .. فبحفظها مباشرة كل ما تنزل عشان ما ضيع مني بيوم من الايام.\nشكرا من كل قلبي. جزاك الله كل خير.', 'author': '@hammam92'}, 
 'comment_text': 'شرح واضح ومبسط جداً, اشكرك يامهندس يحيى على هذا المحتوى التعليمي العربي القيم ذو الجوده العاليه, أنت من بعد الله سبب ففي تطور الكثير, استمر و أتمنى لك كل التوفيق.', 'author': '@khalidal-nasser7953']
}
```


### the chocolate society website
Task: Navigate to the Chocolate Society website, retrieve the page title, and list all products along with their prices.

code:
```python
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
        
        page_title = page.query_data(PAGE_TITLE_QUERY)
        # page_title = page.get_by_prompt(PAGE_TITLE_PROMPT)
        print(page_title)

        # Use query_data() method to fetch the products from the page
        response = page.query_data(PRODUCTS_QUERY)

        print(response)

```
the script doesn't return the page title, it returns 'chocolate society' instead of the page title 'Products'
i think the problem is with the query, it can be confusing for the agentQL to get the page title.

for the products, the script finds the products elements (using query_elements).
example of the product element:
```json
{
      "title": {
        "role": "link",
        "tf623_id": "748",
        "html_tag": "a",
        "name": "Dark Chocolate Ginger",
        "attributes": {
          "href": "/products/dark-chocolate-ginger",
          "class": "product-item-meta__title"
        }
      },
      "price": {
        "role": "text",
        "tf623_id": "753",
        "html_tag": "span",
        "name": "\u00a35.00",
        "attributes": {}
      }
}
```
when trying to get the product name and price using the query_data method, it stucks and doesn't stop (maybe it takes too long to process).
instead of query_data method, i used to_data() method to get the product name and price from the product element.
it worked as expected.

code:
```python
# Use query_data() method to fetch the products from the page
        response = page.query_elements(PRODUCTS_QUERY)

        print(response.to_data())
```
ouput :
```
{'currency': 'United Kingdom (GBP £)', 
'product_items': [{'title': '2.5kg Bulk 41% Milk Hot Chocolate Drops', 'price': '£45.00'}, 
{'title': '2.5kg Bulk 61% Dark Hot Chocolate Drops', 'price': '£45.00'}, 
{'title': '41% Milk Hot Chocolate Drops', 'price': '£8.75'}, 
{'title': '61% Dark Hot Chocolate Drops', 'price': '£8.75'}] 
}
```

### Conclusion

AgentQL proves to be a robust and intuitive tool for web scraping and automation. The querying API is user-friendly, enabling smooth interaction with web elements and efficient data extraction. The example script provided by AgentQL worked flawlessly, and I successfully extended its functionality to simulate adding products to a basket. 

While I encountered a challenge with removing items from the basket due to the element being outside the viewport and only visible upon hover, this highlights an edge case that could benefit from refinement.

Beyond the initial script, I tested AgentQL on various websites, including those in different languages, such as Jumia (Arabic), YouTube, and the Chocolate Society website. In most cases, the tool performed well, extracting data and interacting with elements as expected. However, the `query_data()` method occasionally stalled on certain websites. Switching to the `to_data()` method proved to be a reliable alternative and resolved the issue consistently.

In summary, AgentQL offers a powerful solution for web automation and scraping across various platforms and languages. While there are some edge cases that could benefit from optimization, its overall performance, ease of use, and versatility make it an excellent tool for developers. I'm eager to continue exploring its capabilities and potential in more complex scenarios.

### Author

**[Ahmed B]**

*software developer, web scraping and automation enthusiast*

*Date: 12/10/2024*


