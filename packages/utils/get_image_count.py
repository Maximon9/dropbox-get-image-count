from dropbox import Dropbox, files
import os
import time

from concurrent.futures import ThreadPoolExecutor, as_completed

# from threading import Thread
# from queue import Queue

# Replace with your Dropbox API access token
ACCESS_TOKEN = "TOKEN"

# File extensions to consider as images
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}


def is_image(entry):
    """Checks if a Dropbox entry is an image file."""
    return (
        isinstance(entry, files.FileMetadata)
        and os.path.splitext(entry.name)[1].lower() in IMAGE_EXTENSIONS
    )


def list_files_recursive(dbx: Dropbox, folder_path: str):
    """Lists all files in a given Dropbox folder recursively."""
    entries = []
    try:
        result = dbx.files_list_folder(folder_path, recursive=True)

        while True:
            entries.extend(result.entries)
            if not result.has_more:
                break
            result = dbx.files_list_folder_continue(result.cursor)

    except Exception as e:
        print(f"Error fetching {folder_path}: {e}")

    return entries


def get_shared_folders(dbx: Dropbox):
    """Retrieves paths of all shared folders."""
    shared_folders = []
    try:
        result = dbx.sharing_list_folders()
        shared_folders.extend(
            [entry.path_lower for entry in result.entries if entry.path_lower]
        )

        while result.cursor:
            result = dbx.sharing_list_folders_continue(result.cursor)
            shared_folders.extend(
                [entry.path_lower for entry in result.entries if entry.path_lower]
            )

    except Exception as e:
        print(f"Error fetching shared folders: {e}")

    return shared_folders


def get_all_files(dbx: Dropbox):
    """
    Fetches all Dropbox files (personal & shared).
    Uses multithreading to fetch shared folders faster.
    """
    all_entries = []

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(list_files_recursive, dbx, "")]  # Personal files

        # Fetch shared folders and process them in parallel
        shared_folders = get_shared_folders(dbx)
        for folder in shared_folders:
            futures.append(executor.submit(list_files_recursive, dbx, folder))

        # Collect all entries
        for future in as_completed(futures):
            all_entries.extend(future.result())

    return all_entries


def get_image_count(dbx: Dropbox):
    """
    Efficiently counts images in all Dropbox files using multithreading.
    """
    total_image_count = 0

    # Step 1: Collect all file entries (personal + shared)
    all_entries = get_all_files(dbx)

    # Step 2: Spread workload across multiple threads
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(is_image, entry) for entry in all_entries]

        for future in as_completed(futures):
            total_image_count += future.result()

    return total_image_count


dbx = Dropbox(ACCESS_TOKEN)

start_time = time.time()
total_images = get_image_count(dbx)
print(f"Total images: {total_images}")
print(f"Time taken: {time.time() - start_time:.2f} seconds")

# dbx = Dropbox(ACCESS_TOKEN)

# start_time = time.time()  # Start timing
# print(get_image_count(dbx, ""))
# print(time.time() - start_time)
