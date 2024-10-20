import easyocr
import cv2
import numpy as np
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.models import load_model
import mysql.connector

# Initialize the EasyOCR reader
reader = easyocr.Reader(['en'])


# Load the YOLOv3 object detection model (you can replace this with a pre-trained one)
def load_yolo_model():
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
    return net


# Preprocess the image for YOLO
def preprocess_image_for_yolo(image):
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    return blob


# Detect objects using YOLO and count the number of products in the image
def detect_and_count_items(image, net):
    height, width = image.shape[:2]
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

    net.setInput(preprocess_image_for_yolo(image))
    detections = net.forward(output_layers)

    count = 0
    for detection in detections:
        for obj in detection:
            scores = obj[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:  # Adjust threshold as needed
                count += 1

    return count


# Load and preprocess image for brand recognition
def preprocess_image_for_brand(image):
    image = cv2.resize(image, (224, 224))  # Resize image for MobileNetV2
    image = image.astype('float32') / 255.0  # Normalize
    image = np.expand_dims(image, axis=0)
    return image


# Predict brand using pre-trained CNN (e.g., MobileNetV2)
def predict_brand(image, model):
    processed_image = preprocess_image_for_brand(image)
    prediction = model.predict(processed_image)
    return np.argmax(prediction)  # Assuming the model output is the brand index


# Extract text using OCR (EasyOCR in this case)
def extract_text(image):
    results = reader.readtext(image)
    extracted_text = " ".join([text for (bbox, text, prob) in results])
    return extracted_text


# Function to find company name in the MySQL database based on text
def find_company_name(text, cursor):
    query = "SELECT brand_name FROM brands WHERE brand_name LIKE %s"
    cursor.execute(query, (f"%{text}%",))
    result = cursor.fetchone()
    if result:
        return result[0]
    else:
        return "Company name not found in database"


# Main function to handle the entire process
def process_image(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Step 1: Brand Recognition
    model = load_model('brand_model.h5')  # Load the pre-trained CNN model for brand recognition
    brand = predict_brand(image, model)

    # Step 2: Count number of products using YOLO
    yolo_net = load_yolo_model()
    count = detect_and_count_items(image, yolo_net)

    # Step 3: Extract text using OCR
    extracted_text = extract_text(image)

    # Step 4: Connect to MySQL to find the brand name
    cnx = mysql.connector.connect(
        host="DESKTOP-C3OJ4V1",  # Adjust based on your MySQL setup
        user="root",
        password="Shekhar21,",  # Replace with your password
        database="company_brands"
    )
    cursor = cnx.cursor()
    company_name = find_company_name(extracted_text, cursor)

    # Close the database connection
    cursor.close()
    cnx.close()

    # Output the results
    print(f"Brand (CNN Prediction): {brand}")
    print(f"Number of products detected (YOLO): {count}")
    print(f"Extracted text (OCR): {extracted_text}")
    print(f"Company Name (from database): {company_name}")


# Run the process
if __name__ == "__main__":
    image_path = r"C:\Users\SHIVANSH SHEKHAR\Desktop\eyedrop2.jpg"  # Your image path
    process_image(image_path)
