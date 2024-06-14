import pygame, math
from primitives.vec2 import vec2
from hair.hair import Hair

class Player:
    def __init__(self, game, x, y):
        self.game = game
        self.position = vec2(x, y)
        self.velocity = vec2(0, 0)
        self.speed = 5
        self.jump_force = 15
        self.gravity = 1
        self.is_grounded = False

        self.width = 8
        self.height = 8


        # Hair
        self.hair_anchor = self.position         # the main anchor for the hair

        self.hair_gravity = None        # delegate function retrieved from the hair segments

        self.hair = Hair(game, self)

    def handle_input(self, inputs):
        if inputs['left']:
            self.position.x -= 1
        if inputs['right']:
            self.position.x += 1
        if inputs['up']:
            self.position.y -= 5

    def apply_gravity(self):
        if not self.is_grounded:
            self.position.y += self.gravity

    def move(self, platforms):
        self.position += self.velocity
        self.hair_anchor = self.position

        self.is_grounded = False
        for platform in platforms:
            if self.position.y + self.height > platform.top and self.position.y < platform.bottom:
                if self.position.x + self.width > platform.left and self.position.x < platform.right:
                    self.position.y = platform.top - self.height
                    self.velocity.y = 0
                    self.is_grounded = True

        # setting hair gravity to each segment individually
        if self.is_grounded:
            self.hair_gravity(-.1)
        else:
            self.hair_gravity(-.025)

    def update(self, platforms, inputs, dt):
        self.handle_input(inputs)
        self.apply_gravity()
        self.move(platforms)
        self.hair.update(dt)

    def render(self, surf):
        self.hair.render(surf)
        #pygame.draw.rect(surf, (255, 255, 255), (self.position.x, self.position.y, self.width, self.height))