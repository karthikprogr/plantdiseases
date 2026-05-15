"""
Organize test images into class folders for training
"""

import os
import shutil
from pathlib import Path

print("📁 Organizing test images into class folders...")

source_dir = "test_images"
output_dir = "organized_dataset/train"

# Create output directory
os.makedirs(output_dir, exist_ok=True)

# Get all image files
image_files = [f for f in os.listdir(source_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]

print(f"Found {len(image_files)} images")

# Organize by filename (extract class name from filename)
for img_file in image_files:
    # Skip non-plant images
    if img_file.lower() in ['back.png', 'background_without_leaves.jpg', 'photo.jpg', 'readme.md']:
        continue
    
    # Extract class name from filename
    # Examples: "Apple_scab.JPG" -> "Apple_scab"
    #           "tomato_healthy.JPG" -> "tomato_healthy"
    class_name = os.path.splitext(img_file)[0]
    
    # Clean up class name
    class_name = class_name.replace('-', '_')
    class_name = class_name.replace(' ', '_')
    
    # Create class folder
    class_folder = os.path.join(output_dir, class_name)
    os.makedirs(class_folder, exist_ok=True)
    
    # Copy image to class folder
    src = os.path.join(source_dir, img_file)
    dst = os.path.join(class_folder, img_file)
    shutil.copy2(src, dst)
    
    print(f"  ✅ {img_file} -> {class_name}/")

print(f"\n✅ Images organized into {len(os.listdir(output_dir))} classes")
print(f"✅ Dataset ready at: {output_dir}")
