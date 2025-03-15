from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup  # Import BeautifulSoup
import requests
import os
from concurrent.futures import ThreadPoolExecutor
from glob import glob

base_url = "https://pcclegacy.smugmug.com/"

EXCEPTIONS = {"https://pcclegacy.smugmug.com/Website-Images/Contact-us/Contact"}

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".tiff", ".webp"}


def download_image(url: str, folder: str):
    """Download a single image and save it."""
    try:
        response = requests.get(url, timeout=10, stream=True)
        response.raise_for_status()  # Raise error for bad responses

        # Extract file extension or default to .jpg
        file_name = os.path.basename(url)
        split = os.path.splitext(file_name)
        ext = split[1].lower()
        if ext not in IMAGE_EXTENSIONS:
            ext = ".jpg"
            file_name = split[0] + ext

        # Save image with a unique name
        filepath = os.path.join(folder, file_name)

        with open(filepath, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

    except requests.exceptions.RequestException as e:
        print(f"❌ Failed to download {url}: {e}")


# def bulk_download_images(
#     image_urls: list[str], folder="downloaded_images", num_threads=5
# ):
#     """Download images using multiple threads for speed."""
#     if not os.path.exists(folder):
#         os.makedirs(folder)


#     with ThreadPoolExecutor(max_workers=num_threads) as executor:
#         for index, url in enumerate(image_urls):
#             executor.submit(download_image, url, folder, index)
def already_downloaded(folder: str, url: str):
    files = glob.glob(f"{folder}/*")
    file_name = os.path.basename(url)

    for file in files:
        if file_name in file:
            return True

    return False


def is_exception(url: str) -> bool:
    return url.strip() in EXCEPTIONS


def is_reachable_url(url: str) -> bool:
    try:
        response = requests.get(url, timeout=10)  # 10 seconds timeout
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False


def url_is_same_domain(domain: str, url: str):
    return domain in url


def url_is_image(url: str):
    extension = os.path.splitext(url)[1]
    return extension in IMAGE_EXTENSIONS


# Set up Selenium to use Chrome
def get_image_urls(main_url: str, download_path: str) -> set[str]:
    visited_urls: set[str] = set()
    media_urls: set[str] = set()

    chrome_service = ChromeService(executable_path=ChromeDriverManager().install())
    chrome_options = Options()
    chrome_options.add_argument(
        "--headless"
    )  # Run Chrome in headless mode (without UI)
    chrome_options.add_argument("--disable-gpu")  # Disable GPU for headless mode

    # Use WebDriver Manager to get the correct ChromeDriver
    # driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    def get_image_urls_rec(rec_url: str):
        if rec_url in visited_urls:
            return

        visited_urls.add(rec_url.strip())

        # Fetch the website
        driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        driver.get(rec_url)

        # Wait for the page to load completely
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "body")
                )  # Modify this selector as needed
            )

            # Once the page is fully loaded, get the full HTML content
            html_content = driver.page_source

            # Use BeautifulSoup to parse and extract all image URLs
            soup = BeautifulSoup(html_content, "html.parser")

            # Find all <img> tags and extract the 'src' attributes

            vid_tags = soup.find_all("video")
            for vid_tag in vid_tags:
                vid_src = vid_tag.get("src").strip()
                if vid_src != None:
                    if not vid_src in media_urls and not already_downloaded(
                        download_path, vid_src
                    ):
                        print(vid_src)
                        media_urls.add(vid_src)
                        download_image(vid_src, download_path)

            img_tags = soup.find_all("img")
            for img_tag in img_tags:
                img_src = img_tag.get("src").strip()
                if img_src != None and url_is_image(img_src):
                    if not img_src in media_urls and not already_downloaded(
                        download_path, img_src
                    ):
                        print(img_src)
                        media_urls.add(img_src)
                        download_image(img_src, download_path)

            # Find any background images (CSS style)
            # Search for style attributes in elements that may have background images
            for tag in soup.find_all(style=True):
                style = tag["style"]
                # Look for background-image CSS rule
                if "background-image" in style:
                    background_url = (
                        style.split('background-image: url("')[1].split('")')[0].strip()
                    )
                    if url_is_image(background_url):
                        if not background_url in media_urls and not already_downloaded(
                            download_path, background_url
                        ):
                            print(background_url)
                            media_urls.add(background_url)
                            download_image(background_url, download_path)

            # Pretty-print the remaining HTML content without script tags

            # Combine image URLs from <img> tags and CSS background images

            a_tags = soup.find_all("a")
            for a_tag in a_tags:
                a_link = a_tag.get("href")
                if (
                    a_link != None
                    and not a_link.strip() in visited_urls
                    and not url_is_image(a_link.strip())
                    and is_reachable_url(a_link.strip())
                    and url_is_same_domain(main_url, a_link.strip())
                    and not is_exception(a_link)
                ):
                    print(
                        "\n\n\n",
                        rec_url,
                        ", ",
                        a_link,
                        ", ",
                        not a_link.strip() in visited_urls,
                        ", ",
                        not url_is_image(a_link.strip()),
                        ", ",
                        is_reachable_url(a_link.strip()),
                        "\n\n\n",
                    )
                    get_image_urls_rec(a_link)
            # Remove duplicates (optional)

            # Print out all image URLs found
        finally:
            # Close the WebDriver
            driver.quit()

    get_image_urls_rec(main_url)
    return list[media_urls]


# print(
#     url_is_image(
#         "https://photos.smugmug.com/PCC-60th-Anniversary/Alumni-Gallery/Gallery-Example-1/i-Xvd6qBD/0/MMfVLZLdwVsCGb95Kpjt3dD6S5JsxpGwjkpscWFPJ/X3/Fiji_sm-X3.jpg"
#     )
# )

medias = get_image_urls(base_url)

# bulk_download_images(image_urls=medias, folder="./web_images", num_threads=10)

print(len(medias))
