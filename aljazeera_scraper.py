import requests
from bs4 import BeautifulSoup
import re
import time

# Set the base URL (Al Jazeera homepage)
BASE_URL = "https://www.aljazeera.com/"

# Headers to avoid blocking
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0"
}

# Store visited URLs to avoid duplicate scraping
visited_urls = set()

# Store vocabulary words
unique_words = set()

# Limit to 30 pages
MAX_PAGES = 10
page_count = 0


def clean_text(text):
    """Clean and extract words from text"""
    text = text.lower()
    # text = re.sub(r"[^\w\s]", ",", text)  # Remove punctuation and replace with spaces
    words = text.split()
    return set(words)


def scrape_page(url):
    """Fetch page content, extract text, and find links"""
    global page_count
    if url in visited_urls or page_count >= MAX_PAGES:
        return  # Skip if already visited or limit reached

    print(f"📄 Scraping ({page_count + 1}/{MAX_PAGES}): {url}")
    visited_urls.add(url)
    page_count += 1

    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract all visible text
        texts = soup.find_all(text=True)
        visible_texts = [
            t.strip()
            for t in texts
            if t.parent.name not in ["script", "style", "meta", "head", "title"]
        ]

        # Clean and collect words
        page_words = clean_text(" ".join(visible_texts))
        unique_words.update(page_words)

        # Find and scrape internal links (only if under the page limit)
        for link in soup.find_all("a", href=True):
            if page_count >= MAX_PAGES:
                break  # Stop if limit is reached
            href = link["href"]
            if href.startswith("/"):  # Convert relative URL to absolute
                full_link = BASE_URL.rstrip("/") + href
            elif href.startswith(BASE_URL):  # Ensure it's an internal link
                full_link = href
            else:
                continue  # Skip external links

            scrape_page(full_link)  # Recursively scrape

    except requests.exceptions.RequestException as e:
        print(f"❌ Error scraping {url}: {e}")


# Start scraping
scrape_page(BASE_URL)

# Save unique words in a single-row text file
with open("english_aljazeera_news_part11.txt", "w", encoding="utf-8") as file:
    file.write(" ".join(sorted(unique_words)))  # Save as single row

print("\n✅ Scraping complete! Vocabulary saved in 'aljazeera_eng_vocabulary.txt'.")
