import agentql
from playwright.sync_api import sync_playwright

URL = "https://www.youtube.com/watch?v=8Zi_8-9f7xk"

# Define the queries to interact with the page
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




def main():
    comments = get_comments()
    print(comments)


if __name__ == "__main__":
    main()