import numpy as np
from PIL import Image

list_images = ["1.png", "2.png", "3.png", "4.png"]
images = [Image.open(f"./images/{image}") for image in list_images]

min_width, min_height = min((i.size for i in images))
# Resize and convert images to 'RGB' color mode
images_resized = [i.resize((min_width, min_height)).convert("RGB") for i in images]
# Create a vertical stack of images
imgs_comb = np.vstack([np.array(i) for i in images_resized])
# Create a PIL image from the numpy array
imgs_comb = Image.fromarray(imgs_comb)

# Save the concatenated image
imgs_comb.save("./images/vertical_image.png")