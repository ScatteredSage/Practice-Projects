from playwright.sync_api import sync_playwright

def run_scraper():
    with sync_playwright() as p:
        
        # 1. Launch the Chromium browser in the background
        browser = p.chromium.launch(headless=False)
        
        # 2. Open a new tab
        page = browser.new_page()
        
        # 3. Navigate to a target Walmart product URL (Paste a URL here)
        target_url = "https://www.walmart.com/ip/Simzlife-Nugget-Ice-Maker-Countertop-44lbs-24H-Self-Cleaning-Soft-Chewable-Pellet-Ice-Pebble-Ice-Maker-Machine-for-Home-Kitchen-Party/6130916832?athAsset=eyJhdGhjcGlkIjoiNjEzMDkxNjgzMiIsImF0aHN0aWQiOiJDUzAyMCIsImF0aGFuY2lkIjoiSXRlbUNhcm91c2VsIiwiYXRocmsiOjAuMH0=&athena=true&athbdg=L1800"  
        page.goto(target_url)
        
        # 4. Wait for the specific HTML element holding the product title to load
        title_selector = "h1[itemprop='name']"
        page.wait_for_selector(title_selector)
        
        # 5. Extract the text from that element
        product_title = page.locator(title_selector).inner_text()
        
        print(f"Extracted Title: {product_title}")
        
        # 6. Close the browser session
        browser.close()

if __name__ == "__main__":
    run_scraper()