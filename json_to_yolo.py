import json
import os

# Define the directories
json_dir = r"C:\Users\SHIVANSH SHEKHAR\Desktop\new\closeup_labeled"      # Directory where your JSON annotations are stored      # Directory where you want to save YOLO annotations
yolo_dir = r"C:\Users\SHIVANSH SHEKHAR\Desktop\new\yolo_closeup"
image_dir =   "closeup_images/Closeup toothpaste"

# Create YOLO directory if it doesn't exist
os.makedirs(yolo_dir, exist_ok=True)

# Convert annotations
for json_file in os.listdir(json_dir):
    if json_file.endswith('.json'):
        json_path = os.path.join(json_dir, json_file)
        with open(json_path, 'r') as f:
            annotation = json.load(f)

        image_width = annotation['imageWidth']
        image_height = annotation['imageHeight']

        yolo_annotations = []
        for shape in annotation['shapes']:
            label = shape['label']
            points = shape['points']
            x_min = min(points[0][0], points[1][0])
            y_min = min(points[0][1], points[1][1])
            x_max = max(points[0][0], points[1][0])
            y_max = max(points[0][1], points[1][1])

            x_center = (x_min + x_max) / 2 / image_width
            y_center = (y_min + y_max) / 2 / image_height
            width = (x_max - x_min) / image_width
            height = (y_max - y_min) / image_height

            yolo_label = f"{label} {x_center} {y_center} {width} {height}\n"
            yolo_annotations.append(yolo_label)

        # Save YOLO annotation file
        yolo_file = os.path.join(yolo_dir, json_file.replace('.json', '.txt'))
        with open(yolo_file, 'w') as f:
            f.writelines(yolo_annotations)
