import dropbox
import os

# Replace with your Dropbox API access token
ACCESS_TOKEN = "your_dropbox_access_token"

# File extensions to consider as images
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"}


def count_images_in_dropbox(dbx, path=""):
    image_count = 0

    try:
        # List all files and folders in the current path
        result = dbx.files_list_folder(path)

        for entry in result.entries:
            if isinstance(entry, dropbox.files.FileMetadata):
                # If the file is an image (check by file extension)
                if os.path.splitext(entry.name)[1].lower() in IMAGE_EXTENSIONS:
                    image_count += 1
            elif isinstance(entry, dropbox.files.FolderMetadata):
                # If it's a folder, recurse into it
                image_count += count_images_in_dropbox(dbx, entry.path_display)

        # If there are more files/folders (pagination), keep listing
        while result.has_more:
            result = dbx.files_list_folder_continue(result.cursor)
            for entry in result.entries:
                if isinstance(entry, dropbox.files.FileMetadata):
                    if os.path.splitext(entry.name)[1].lower() in IMAGE_EXTENSIONS:
                        image_count += 1
                elif isinstance(entry, dropbox.files.FolderMetadata):
                    image_count += count_images_in_dropbox(dbx, entry.path_display)
    except Exception as e:
        print(f"Error: {e}")

    return image_count


def main():
    # Initialize Dropbox client
    dbx = dropbox.Dropbox(ACCESS_TOKEN)

    # Count images in Dropbox
    total_images = count_images_in_dropbox(dbx)
    print(f"Total images in Dropbox: {total_images}")


if __name__ == "__main__":
    main()
