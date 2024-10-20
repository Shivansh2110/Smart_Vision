from bing_image_downloader import downloader

# Create a folder for images
image_folder = 'closeup_images'
search_term = 'Closeup toothpaste'

# Download images
downloader.download(search_term, limit=40, output_dir=image_folder, adult_filter_off=True, force_replace=False, timeout=60)

print("Image download complete.")

