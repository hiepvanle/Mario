import os
import sys

import pygame


def load_image(name, prefix="..\data"):
    fullname = os.path.join(prefix, name)
    if not os.path.isfile(fullname):
        print(f"Images file '{fullname}' not found")
        sys.exit()
    image = pygame.image.load(fullname)
    return image