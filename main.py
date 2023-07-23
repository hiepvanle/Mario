import os
import sys

import pygame as pygame

FPS = 50

WIDTH, HEIGHT = None, None

pygame.init()
pygame.display.set_caption("game")


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"images file '{fullname}' not found")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mario.png')

tile_width = tile_height = 50

# main character
player = None

# sprite groups
all_sprites = pygame.sprite.Group()

tiles_group = pygame.sprite.Group()
borders_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, border=False):
        super().__init__(tiles_group, all_sprites)
        if border:
            borders_group.add(self)

        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)

    def move(self, dx, dy):
        dx = tile_width * dx
        dy = -tile_width * dy

        if 0 <= self.rect.x + dx <= WIDTH and 0 <= self.rect.y + dy <= HEIGHT:
            source_rect = self.rect
            self.rect = self.rect.move(dx, dy)

            if pygame.sprite.spritecollideany(self, borders_group):
                self.rect = source_rect


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y, True)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # return the player, as well as the size of the field in cells
    return new_player, x, y


class Camera:
    # set the initial camera shift
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # shift obj object by camera offset
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # position the camera on the target object
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


def terminate():
    pygame.quit()
    sys.exit()


def load_level(filename):
    filename = "data/maps/" + filename
    # read the level, removing line breaks
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # calculate the maximum length
    max_width = max(map(len, level_map))

    # pad each line with empty cells ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


map_file = input()
try:
    level = load_level(map_file)
    player, level_x, level_y = generate_level(level)

    WIDTH = (level_x + 1) * 50
    HEIGHT = (level_y + 1) * 50
except FileNotFoundError as e:
    print(e)
    terminate()

screen = pygame.display.set_mode((WIDTH, HEIGHT))


def start_screen():
    intro_text = ["SCREENSAVER", "",
                  "v",
                  "1) You are free to do whatever you want. There are no rules"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return


hero_at_center = True
if __name__ == "__main__":
    start_screen()

    camera = Camera()
    clock = pygame.time.Clock()

    screen.fill((0, 0, 0))

    if hero_at_center:
        camera.update(player)
        for sprite in all_sprites:
            camera.apply(sprite)

    tiles_group.draw(screen)
    player_group.draw(screen)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_w, pygame.K_s):
                    player.move(0, 1 if event.key == pygame.K_w else -1)
                if event.key in (pygame.K_d, pygame.K_a):
                    player.move(1 if event.key == pygame.K_d else -1, 0)

                if hero_at_center:
                    camera.update(player)
                    for sprite in all_sprites:
                        camera.apply(sprite)

                screen.fill((0, 0, 0))
                tiles_group.draw(screen)
                player_group.draw(screen)
                pygame.display.flip()

        clock.tick(FPS)
