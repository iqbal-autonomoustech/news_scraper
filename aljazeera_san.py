import requests
from bs4 import BeautifulSoup
import re
import time

# Set the base URL (Al Jazeera homepage)
BASE_URL = "https://arabic.cnn.com/"

# Headers to avoid blocking
HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/109.0"
}

# Store visited URLs to avoid duplicate scraping
visited_urls = set()

# Store sentences
sentences = set()

# Limit to 10 pages
MAX_PAGES = 1000
page_count = 0


def clean_text(text):
    """Clean text and extract sentences"""
    text = text.strip()
    text = re.sub(r"\s+", " ", text)  # Remove extra spaces
    extracted_sentences = re.split(r"(?<=[.!?])\s+", text)  # Split text into sentences
    return extracted_sentences


def scrape_page(url):
    """Fetch page content, extract sentences, and find links"""
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

        # Clean and collect sentences
        page_sentences = clean_text(" ".join(visible_texts))
        sentences.update(page_sentences)

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

# Save sentences in a text file, each sentence on a new line
with open("full_arabic-cnn-news.txt", "w", encoding="utf-8") as file:
    file.write("\n".join(sorted(sentences)))  # Save each sentence on a new line

print("\n✅ Scraping complete! Sentences saved in 'https://www.skynewsarabia.txt'.")
