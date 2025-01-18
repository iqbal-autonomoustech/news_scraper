from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

# Configure Selenium WebDriver
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode (no UI)
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent bot detection
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--user-agent=Mozilla/5.0 (X11; Ubuntu; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

# Start ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

# List of Sky News pages to scrape
pages_to_scrape = [
    "https://www.skynewsarabia.com/most-popular",
    "https://www.skynewsarabia.com/tv_reports",
    "https://www.skynewsarabia.com/recommended",
    "https://www.skynewsarabia.com/exclusive",
    "https://www.skynewsarabia.com/middle-east",
    "https://www.skynewsarabia.com/from_egypt",
    "https://www.skynewsarabia.com/middle-east/northafrica",
    "https://www.skynewsarabia.com/food",
    "https://www.skynewsarabia.com/epidemics"
]

# Output file
output_file = "skynewsarabia_news.txt"

def scrape_page(url):
    """ Load the page with Selenium and extract news content """
    try:
        print(f"📄 Scraping: {url}")
        driver.get(url)
        time.sleep(5)  # Allow time for JavaScript to load

        # Extract news paragraphs
        paragraphs = driver.find_elements(By.TAG_NAME, "p")

        # Save to file
        with open(output_file, "a", encoding="utf-8") as file:
            for paragraph in paragraphs:
                text = paragraph.text.strip()
                if text:
                    file.write(text + "\n")  # Each paragraph on a new line

    except Exception as e:
        print(f"❌ Error scraping {url}: {e}")

# Start scraping all pages
for page in pages_to_scrape:
    scrape_page(page)

# Close the browser
driver.quit()

print("\n✅ Scraping complete! News saved in 'skynewsarabia_news.txt'.")

