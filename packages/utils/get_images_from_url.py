from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup  # Import BeautifulSoup

# import requests
import os

base_url = "https://pcclegacy.smugmug.com/"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}


def url_is_image(url: str):
    extension = os.path.splitext(url)[1]
    return extension in IMAGE_EXTENSIONS


# Set up Selenium to use Chrome
def get_image_urls(url: str):
    chrome_service = ChromeService(executable_path=ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument(
        "--headless"
    )  # Run Chrome in headless mode (without UI)
    chrome_options.add_argument("--disable-gpu")  # Disable GPU for headless mode

    # Use WebDriver Manager to get the correct ChromeDriver

    def get_image_urls_rec(url: str):
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        # Fetch the website
        driver.get(url)

        # Wait for the page to load completely
        try:
            # WebDriverWait(driver, 0).until(
            #     EC.presence_of_element_located(
            #         (By.CSS_SELECTOR, "body")
            #     )  # Modify this selector as needed
            # )

            # Once the page is fully loaded, get the full HTML content
            html_content = driver.page_source

            # Use BeautifulSoup to parse and extract all image URLs
            soup = BeautifulSoup(html_content, "html.parser")

            # Find all <img> tags and extract the 'src' attributes

            img_tags = soup.find_all("img")
            img_urls = [img.get("src") for img in img_tags if img.get("src")]

            # Find any background images (CSS style)
            # Search for style attributes in elements that may have background images
            background_images = []
            for tag in soup.find_all(style=True):
                style = tag["style"]
                # Look for background-image CSS rule
                if "background-image" in style:
                    url = style.split('background-image: url("')[1].split('")')[0]
                    background_images.append(url)

            # Pretty-print the remaining HTML content without script tags

            # Combine image URLs from <img> tags and CSS background images
            all_image_urls = img_urls + background_images
            all_image_urls = list(set(all_image_urls))

            for url in all_image_urls:
                print(url)

            a_tags = soup.find_all("a")
            for a_tag in a_tags:
                a_link = a_tag.get("href")
                if not (a_link.strip() in url.strip()) and not (
                    url.strip() in a_link.strip() and not url_is_image(a_link)
                ):
                    print("\n\n\n\n\n\n", a_link, ", ", url, "\n\n\n\n\n\n")
                    all_image_urls + get_image_urls_rec(a_link)
            # Remove duplicates (optional)

            # Print out all image URLs found
            return all_image_urls
        finally:
            # Close the WebDriver
            driver.quit()

    return get_image_urls_rec(url)


url_is_image(
    "https://photos.smugmug.com/Website-Images/HeadShots/HeadShots/i-SVmsNsG/0/NgKHGLVTTPmJzCLHM7gqZGR6TCf3W9q89WpCzrKs3/L/Alfred_Grace-L.jpg"
)

medias = get_image_urls(base_url)
print(len(medias))
