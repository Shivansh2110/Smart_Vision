import os

# Base directory for your dataset
base_dir = 'dataset1'

# Subdirectories for images and labels
sub_dirs = [
    'images/train', 'images/val', 'images/test',
    'labels/train', 'labels/val', 'labels/test'
]

# Create directories
for sub_dir in sub_dirs:
    path = os.path.join(base_dir, sub_dir)
    os.makedirs(path, exist_ok=True)

print("Dataset directories created successfully.")
