from PIL import Image
import os

# a code for cropping images so that the will contain the smallest rectangle that has all the pixels in it

def crop_image(image_path):
    # Open the image
    image = Image.open(image_path)

    # Find the bounding box of non-transparent pixels
    bbox = image.getbbox()

    # Crop the image to the bounding box
    cropped_image = image.crop(bbox)

    # Save the cropped image (optional)
    cropped_image.save(image_path)

dir = r"C:\Users\roeym\PycharmProjects\Element_Rumble\Elementals_fire_knight_FREE_v1.1\png\fire_knight\air_attack"
for image_name in os.listdir(dir):
    crop_image(os.path.join(dir, image_name))