import pygame, math, os
from primitives.vec2 import vec2

def lerp(v1, v2, t):
    return vec2(v1.x + t * (v2.x - v1.x), v1.y + t * (v2.y - v1.y))


"""
REFERENCE VIDEO: https://www.youtube.com/watch?v=imkT4kFP43k
"""

class HairPart:
    def __init__(self, target, img, main_hair_part=False):
        self.target = target                  # the target position that each hair part wants to be at
        self.img = img
        self.main_hair_part = main_hair_part         # 

        self.lerp_speed = 5                      # speed in which hair part moves to new distance
        self.max_distance = 3                    # the max distance in which the hair part can move
        self.gravity = 0.5                       # the gravity of the hair part

        self._player_movement = None
        self._ready = False

        self.position = vec2(0, 0)

    def init_hair(self, owner):
        self._player_movement = owner

        # binding the player's hair gravity delegate to the set_gravity() function
        self._player_movement.hair_gravity = self.set_gravity
        self._ready = True

    def on_destroy(self):
        self._player_movement -= self.set_gravity

    def set_gravity(self, new_gravity):
        self.gravity = new_gravity

    def update(self, dt):
        if not self._ready:
            return
        
        # applying gravity
        self.position = vec2(self.position.x, self.position.y + self.gravity)

        #print(type(self.target))
        difference = vec2(self.position - self.target.position)
        direction = vec2(difference.normalize())
        dist = min(self.max_distance, difference.magnitude())

        # FIX THIS IN VEC2 CLASS TO SUPPORT TUPLE-FLOAT OPERATIONS
        final_pos = vec2(self.target.position.x + direction.x * dist, self.target.position.y + direction.y * dist)

        new_position_lerped = vec2(lerp(final_pos, self.target.position, dt * self.lerp_speed))

        self.position = new_position_lerped

    def render(self, surf):
        surf.blit(self.img, self.position.tuple)

class Hair:
    def __init__(self, game, owner):
        self.game = game
        self.owner = owner
        self.hair_segments = []

        # temp
        self.segment_offset = 2

    def gen_hair(self):
        # Initializing the anchor of the hair, this piece will remain static on the player's head
        self.hair_segments.append(HairPart(self.owner, self.game.assets['0'], main_hair_part=True))

        for i in range(1, len(self.game.assets)):
            self.hair_segments.append(HairPart(self.hair_segments[i-1], self.game.assets[str(i)]))

        for segment in self.hair_segments:
            segment.init_hair(self.owner)

    def update(self, dt):
        print(self.hair_segments[0].target)
        for segment in self.hair_segments:
            segment.update(dt)

    def render(self, surf):
        for segment in self.hair_segments:
            segment.render(surf)

    def debug(self):
        print('--------------------')
        for i, segment in enumerate(self.hair_segments):
            print(f'Segment {i} at position: {segment.position}')

hair_offsets = {
    "path": "idle",
    "hair": [
        (0, -2),
        (0, -2),
        (0, -2),
        (0, -2),
        (0, -1),
        (0, -1),
        (0, -1),
        (0, -1),
        (0, -1)
    ]
}