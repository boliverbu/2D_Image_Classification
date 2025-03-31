import os
import random
from PIL import Image
import numpy as np

# Paths
bg_path = 'images/backgrounds/'
waldo_path = 'images/waldo/'
output_path = 'images/waldo_backgrounds/'

# Load waldo images
waldo_imgs = [
    Image.open(os.path.join(waldo_path, waldo_img)).convert('RGBA')
    for waldo_img in os.listdir(waldo_path)
    if waldo_img.lower().endswith(('.png', '.jpg', '.jpeg'))
]
print(type(waldo_imgs))

def overlay_waldo(bg_img, waldo_img):
    bg_w, bg_h = bg_img.size

    # Random scale for Waldo (10% - 30% of background width)
    scale_factor = random.uniform(0.1, 0.3)
    new_waldo_width = int(bg_w * scale_factor)
    aspect_ratio = waldo_img.height / waldo_img.width
    new_waldo_height = int(new_waldo_width * aspect_ratio)
    waldo_resized = waldo_img.resize((new_waldo_width, new_waldo_height), resample=Image.Resampling.LANCZOS)

    # Random position for Waldo
    max_x = bg_w - new_waldo_width
    max_y = bg_h - new_waldo_height
    pos_x = random.randint(0, max(0, max_x))
    pos_y = random.randint(0, max(0, max_y))

    # Overlay Waldo onto background
    bg_img.paste(waldo_resized, (pos_x, pos_y), waldo_resized)
    return bg_img

# Iterate through background images
bg_files = [f for f in os.listdir(bg_path)]

for i, bg_file in enumerate(bg_files):
    bg_img = Image.open(os.path.join(bg_path, bg_file)).convert('RGBA')

    # Create two versions (one with Waldo, one without)
    # Waldo Present
    for j in range(len(waldo_imgs)):
        waldo_bg_img = bg_img.copy()
        waldo_bg_img = overlay_waldo(waldo_bg_img, waldo_imgs[j])
        waldo_bg_img = waldo_bg_img.convert('RGB')  # save as JPG
        waldo_bg_img.save(os.path.join(output_path, f'waldo_present_{i}_{j}.jpg'))

print(f"Dataset created with {len(bg_files)} pairs of images.")
