import cv2
import numpy as np

# Load YOLO model
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")  # Adjust the paths as necessary
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]

# Define class names (replace these with your actual brand names)
class_names = ["Colgate Toothpaste", "Other Brand"]  # Add your brands


# Function to detect objects in an image
def detect_objects(image):
    height, width = image.shape[:2]
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outputs = net.forward(output_layers)

    boxes, confidences, class_ids = [], [], []
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5:  # Threshold for detection
                center_x, center_y, w, h = (detection[0:4] * np.array([width, height, width, height])).astype('int')
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Non-maximum suppression to remove duplicate boxes
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    detected_objects = []
    for i in indices:
        box = boxes[i[0]]
        detected_objects.append({
            'class_id': class_ids[i[0]],
            'box': box,
            'confidence': confidences[i[0]]
        })
    return detected_objects


# Function to process the image and count items
def process_image(image_path):
    image = cv2.imread(image_path)
    detected_objects = detect_objects(image)

    item_counts = {}

    for obj in detected_objects:
        class_id = obj['class_id']
        brand = class_names[class_id]

        # Count the number of items
        if brand in item_counts:
            item_counts[brand] += 1
        else:
            item_counts[brand] = 1

        # Draw bounding box and label
        box = obj['box']
        x, y, w, h = box
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, f"{brand} ({item_counts[brand]})", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (255, 255, 255), 2)

    # Show the image with detections
    cv2.imshow("Detections", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return item_counts


# Example usage
image_path = r"C:\Users\SHIVANSH SHEKHAR\Desktop\eyedrop2.jpg"  # Update with your image path
item_counts = process_image(image_path)
print("Item Counts:", item_counts)
