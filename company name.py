import easyocr
import cv2
import mysql.connector

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])

# Load and process the image
image_path = r"C:\Users\SHIVANSH SHEKHAR\Desktop\eyedrop2.jpg"
image = cv2.imread(image_path)
grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply image enhancement techniques
processed_image = cv2.GaussianBlur(grayscale_image, (5, 5), 0)
processed_image = cv2.adaptiveThreshold(processed_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

# Extract text using EasyOCR
results = reader.readtext(processed_image)

# Show the extracted text
'''print("Extracted Text:")
for (bbox, text, prob) in results:
    print(f"{text}")'''

# Connect to MySQL database
cnx = mysql.connector.connect(
    host="DESKTOP-C3OJ4V1",
    user="root",
    password="Shekhar21,",
    database="company_brands"
)
cursor = cnx.cursor()

# Function to find company name in the database
def find_company_name(text, cursor):
    query = "SELECT brand_name FROM brands WHERE brand_name LIKE %s"
    cursor.execute(query, (f"%{text}%",))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return "Company name not found in database"

# Find company name in the extracted text
company_name = None
for (bbox, text, prob) in results:
    company_name = find_company_name(text, cursor)
    if company_name != "Company name not found in database":
        break

print(f"Company Name: {company_name}")

# Close the database connection
cursor.close()
cnx.close()

# Optional: Save processed image
cv2.imwrite(r'C:\Users\SHIVANSH SHEKHAR\Desktop\processed_image.png', processed_image)
