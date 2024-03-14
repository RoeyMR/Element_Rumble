WIDTH, HEIGHT = 1280, 720
FPS = 60
TILE_SIZE = 64
PLAYER_SPRITE_SCALE = 2


DASH_SPEED = 15
NORMAL_SPEED = 10

# cooldowns
ATTACK_COOLDOWN = 400
DASH_COOLDOWN = 600


_props_dir = r".\map\props\\"
PROPS_IMAGES = {"0": _props_dir + "open_door.png", "1": _props_dir + "pot.png", "2": _props_dir + "pot_2.png",
                "3": _props_dir + "right_sign.png", "4": _props_dir + "rock.png", "5": _props_dir + "rune.png",
                "6": _props_dir + "rune_2.png", "7": _props_dir + "rune_3.png", "8": _props_dir + "stone.png",
                "9": _props_dir + "stone_2.png", "10": _props_dir + "stone_3.png", "11": _props_dir + "stone_4.png",
                "12": _props_dir + "stone_5.png", "13": _props_dir + "stone_6.png", "14": _props_dir + "tomb.png",
                "15": _props_dir + "barrel.png", "16": _props_dir + "box.png", "17": _props_dir + "box_2.png",
                "18": _props_dir + "chest.png", "19": _props_dir + "closed_door.png", "20": _props_dir + "cross_tomb.png",
                "21": _props_dir + "left_sign.png", "22": _props_dir + "open_chest.png"}
_trees_dir = r".\map\trees\\"
TREES_IMAGES = {"0": _trees_dir + "bush_6.png", "1": _trees_dir + "grass_1.png", "2": _trees_dir + "grass_2.png",
                "3": _trees_dir + "grass_3.png", "4": _trees_dir + "grass_4.png", "5": _trees_dir + "tree_1.png",
                "6": _trees_dir + "tree_2.png", "7": _trees_dir + "tree_3.png", "8": _trees_dir + "bush_1.png",
                "9": _trees_dir + "bush_2.png", "10": _trees_dir + "bush_3.png", "11": _trees_dir + "bush_4.png",
                "12": _trees_dir + "bush_5.png"}

FIRE_WORM_DATA = {"health": 60, "speed": 5, "damage": 25, "attack radius": 200,
                  "notice radius": 400, "attack cooldown": 200, "assets path": r".\enemy assets\Fire Worm\Sprites\Worm"}

ENEMIES_DATA = {"fire worm": FIRE_WORM_DATA}