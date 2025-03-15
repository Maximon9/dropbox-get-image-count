from playwright.sync_api import sync_playwright
from urllib.parse import urljoin


def get_media_urls_with_playwright(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)

        media_urls = []

        # Get all image URLs
        images = page.query_selector_all("img")
        for img in images:
            src = img.get_attribute("src")
            if src:
                media_urls.append(urljoin(url, src))

        # Get all video URLs
        videos = page.query_selector_all("video")
        for video in videos:
            src = video.get_attribute("src")
            if src:
                media_urls.append(urljoin(url, src))

            # Get source tags inside video tags
            sources = video.query_selector_all("source")
            for source in sources:
                srcset = source.get_attribute("src")
                if srcset:
                    media_urls.append(urljoin(url, srcset))

        browser.close()

    return media_urls


# Example usage:
base_url = "https://pcclegacy.smugmug.com/"
media_urls = get_media_urls_with_playwright(base_url)
for url in media_urls:
    print(url)
# base_url = "https://pcclegacy.smugmug.com/"
