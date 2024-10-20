import easyocr
import cv2
import re

# Initialize the reader
reader = easyocr.Reader(['en'])

# Load and process the image
image_path = r"C:\Users\SHIVANSH SHEKHAR\Desktop\eyedrop2.jpg"
image = cv2.imread(image_path)
grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
processed_image = cv2.threshold(grayscale_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# Extract text using EasyOCR
results = reader.readtext(processed_image)

# Function to find all dates in the text
def extract_dates(results):
    date_pattern = re.compile(r'\b(0[1-9]|1[0-2])/(\d{2}|\d{4})\b')
    dates = []
    for (bbox, text, prob) in results:
        matches = date_pattern.findall(text)
        for match in matches:
            full_date = "/".join(match)
            dates.append(full_date)
    return dates

# Extract dates and sort them
dates = extract_dates(results)
sorted_dates = sorted(dates)

# Assume first is mfg date and second is expiry date
if len(sorted_dates) >= 2:
    mfg_date = sorted_dates[0]
    expiry_date = sorted_dates[1]
    print(f"Expiry Date: {mfg_date}")
    print(f"MFG Date: {expiry_date}")
else:
    print("Unable to find both MFG and expiry dates")

# Optional: Save processed image
cv2.imwrite(r'C:\Users\SHIVANSH SHEKHAR\Desktop\processed_image.png', processed_image)
