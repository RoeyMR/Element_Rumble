import os

# a code for renaming assets

dir = r".\Elementals_fire_knight_FREE_v1.1\png\fire_knight\air_attack"
previous_name = "air_atk_"
new_name = "air_attack_"

for filename in os.listdir(dir):
	if filename.startswith(previous_name):
		os.rename(os.path.join(dir, filename), os.path.join(dir, new_name + filename[len(previous_name):]))