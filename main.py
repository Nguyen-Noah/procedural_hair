import pygame, sys, os
from pygame.locals import *
from player import Player

# Constants
WIDTH = 320
HEIGHT = 180
FPS = 60
dt = 1/FPS
BASE_RESOLUTION = (320, 180)
SCALED_RESOLUTION = (320 * 3, 180 * 3)


class Platform:
    def __init__(self, left, top, width, height):
        self.left = left
        self.top = top
        self.right = left + width
        self.bottom = self.top + height

    def render(self, surf):
        pygame.draw.rect(surf, (255, 0, 0), (self.left, self.top, self.right - self.left, self.bottom - self.top))


platforms = [
    Platform(0, 0, 20, HEIGHT),
    Platform(0, 0, WIDTH, 20),
    Platform(20, HEIGHT - 20, WIDTH, 20),
    Platform(WIDTH - 20, 20, 20, HEIGHT)
]


# Load assets
def load_img(path, ck):
    img = pygame.image.load(path).convert_alpha()
    img.set_colorkey(ck)
    return img

def load_dir(path):
    image_dir = {}
    for file in os.listdir(path):
        image_dir[file.split('.')[0]] = load_img(path + '/' + file, (255, 255, 255))
    return image_dir


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCALED_RESOLUTION)
        self.display = pygame.Surface(BASE_RESOLUTION)
        pygame.display.set_caption('Celeste Hair')
        self.clock = pygame.time.Clock()

        self.inputs = {
            "left": False,
            "right": False,
            "up": False,
            "down": False
        }
        self.load_assets()

        self.player = Player(self, 100, 100)

    def update(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == 27):
                pygame.quit()
                sys.exit()
            
            if event.type == KEYDOWN:
                if event.key == 97:
                    self.inputs['left'] = True
                if event.key == 100:
                    self.inputs['right'] = True
                if event.key == 119:
                    self.inputs['up'] = True
                if event.key == 115:
                    self.inputs['down'] = True

            if event.type == KEYUP:
                if event.key == 97:
                    self.inputs['left'] = False
                if event.key == 100:
                    self.inputs['right'] = False
                if event.key == 119:
                    self.inputs['up'] = False
                if event.key == 115:
                    self.inputs['down'] = False

        self.player.update(platforms, self.inputs, dt)

        for platform in platforms:
            platform.render(self.display)

        self.player.render(self.display)

        self.screen.blit(pygame.transform.scale(self.display, (WIDTH * 3, HEIGHT * 3)), (0, 0))
        self.clock.tick(FPS)
        self.display.fill((0, 0, 0))
        pygame.display.update()

    def run(self):
        while True:
            self.update()

    def load_assets(self):
        self.assets = load_dir('assets')

game = Game()
game.run()
