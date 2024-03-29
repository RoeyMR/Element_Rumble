from PIL import Image
import os


def mirror_image(image_name, old_dir, new_dir):
    # Open the image
    image = Image.open(os.path.join(old_dir, image_name))

    # Mirror the image horizontally (left to right)
    mirrored_image = image.transpose(Image.FLIP_LEFT_RIGHT)

    # Save the mirrored image
    mirrored_image.save(os.path.join(new_dir, "left_" + image_name))

dir = r"C:\Users\roeym\PycharmProjects\Element_Rumble\enemy assets\Fire Worm\Sprites\Worm\take_hit"
new_dir = r"C:\Users\roeym\PycharmProjects\Element_Rumble\enemy assets\Fire Worm\Sprites\Worm\left_take_hit"
os.mkdir(new_dir)
for image_name in os.listdir(dir):
    mirror_image(image_name, dir, new_dir)
    os.rename(os.path.join(dir, image_name), os.path.join(dir, "right_" + image_name))

