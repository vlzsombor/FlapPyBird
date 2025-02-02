# import pygame
 
# # pygame.init()
# # screen = pygame.display.set_mode((400, 300))
# # done = False
# # red = (255,0,0)
# # green = (0,255,0)
# # blue = (0,0,255)
# # white = (255,255,255)
# # while not done:
# #    for event in pygame.event.get():
# #       if event.type == pygame.QUIT:
# #          done = True
# #    pygame.draw.circle(screen, red, (90,180), 60+20)
# #    pygame.draw.circle(screen, white, (90,180), 60)
# #    pygame.display.update()


# def greeting(name: int) -> int:
#     return 3 + name

# greeting(3)         # Argument 1 to "greeting" has incompatible type "int"; expected "str"
# greeting(b'Alice')  # Argument 1 to "greeting" has incompatible type "bytes"; expected "str"
# greeting("World!")  # No error

# def bad_greeting(name: str) -> int:
#     return 'Hello ' + name  # Unsupported operand types for * ("str" and "str")

from typing import TypeVar, Generic
import pygame

T = TypeVar("T", bound=pygame.sprite.Sprite)  # Restrict to Sprite subclasses

class SpriteGroup(pygame.sprite.Group, Generic[T]):
    """A type-safe pygame sprite group."""
    pass

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

# Usage
enemies: SpriteGroup[Enemy] = SpriteGroup()
enemies.add(Enemy())  # ✅ Works
