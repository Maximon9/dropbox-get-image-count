import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_images_from_page(url):
    """Fetch images from a single page."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all images on the page
    image_elements = soup.find_all("img")
    image_urls = [
        urljoin(url, img["src"]) for img in image_elements if "src" in img.attrs
    ]

    return image_urls


def get_next_page_url(soup, base_url):
    """Find the 'Next' page URL from the pagination."""
    next_button = soup.find("a", {"rel": "next"})  # Example selector
    if next_button:
        return urljoin(base_url, next_button["href"])
    return None


def scrape_images(url):
    """Scrape images across multiple pages."""
    image_urls = []
    while url:
        print(f"Scraping page: {url}")
        page_images = get_images_from_page(url)
        image_urls.extend(page_images)

        # Fetch next page URL
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        url = get_next_page_url(soup, url)

    return image_urls


# Example usage
base_url = "https://example.com"
all_images = scrape_images(base_url)
print(f"Found {len(all_images)} images.")
