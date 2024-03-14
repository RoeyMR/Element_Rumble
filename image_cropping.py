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

dir = r"C:\Users\roeym\PycharmProjects\Element_Rumble\character\left_attack"
for image_name in os.listdir(dir):
    #crop_image(os.path.join(dir, image_name))
    img_split = image_name.split("_")
    os.rename(os.path.join(dir, image_name), os.path.join(dir, "left_attack_" + img_split[3]))