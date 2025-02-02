from enum import Enum
from itertools import cycle

import pygame

from ..utils import GameConfig, clamp
from .entity import Entity
from .floor import Floor
from .pipe import Pipe, Pipes

import math
from typing import Callable, List

from ..utils import Window


class PlayerMode(Enum):
    SHM = "SHM"
    NORMAL = "NORMAL"
    CRASH = "CRASH"


class Player(Entity):
    def __init__(self, config: GameConfig) -> None:
        image = config.images.player[0]
        x = int(config.window.width * 0.2)
        y = int((config.window.height - image.get_height()) / 2)
        super().__init__(config, image, x, y) # type: ignore
        self.min_y = -2 * self.h
        self.max_y = config.window.viewport_height - self.h * 0.75
        self.img_idx = 0
        self.img_gen = cycle([0, 1, 2, 1])
        self.frame = 0
        self.crashed = False
        self.crash_entity = ""
        self.set_mode(PlayerMode.SHM)

    def set_mode(self, mode: PlayerMode) -> None:
        self.mode = mode
        if mode == PlayerMode.NORMAL:
            self.reset_vals_normal()
            self.config.sounds.wing.play()
        elif mode == PlayerMode.SHM:
            self.reset_vals_shm()
        elif mode == PlayerMode.CRASH:
            self.stop_wings()
            self.config.sounds.hit.play()
            if self.crash_entity == "pipe":
                self.config.sounds.die.play()
            self.reset_vals_crash()

    def reset_vals_normal(self) -> None:
        self.vel_y = -9.0  # player's velocity along Y axis
        self.max_vel_y = 10.0  # max vel along Y, max descend speed
        self.min_vel_y = -8.0  # min vel along Y, max ascend speed
        self.acc_y = 1.0  # players downward acceleration

        self.rot = 80.0  # player's current rotation
        self.vel_rot = -3  # player's rotation speed
        self.rot_min = -90  # player's min rotation angle
        self.rot_max = 20  # player's max rotation angle

        self.flap_acc = -9  # players speed on flapping
        self.flapped = False  # True when player flaps

    def reset_vals_shm(self) -> None:
        self.vel_y = 1.0  # player's velocity along Y axis
        self.max_vel_y = 4  # max vel along Y, max descend speed
        self.min_vel_y = -4  # min vel along Y, max ascend speed
        self.acc_y = 0.5  # players downward acceleration

        self.rot = 0.0  # player's current rotation
        self.vel_rot = 0  # player's rotation speed
        self.rot_min = 0  # player's min rotation angle
        self.rot_max = 0  # player's max rotation angle

        self.flap_acc = 0  # players speed on flapping
        self.flapped = False  # True when player flaps

    def reset_vals_crash(self) -> None:
        self.acc_y = 2.0
        self.vel_y = 7.0
        self.max_vel_y = 15
        self.vel_rot = -8

    def update_image(self): # type: ignore
        self.frame += 1.0
        if self.frame % 5 == 0:
            self.img_idx = next(self.img_gen)
            self.image = self.config.images.player[self.img_idx]
            self.w = self.image.get_width()
            self.h = self.image.get_height()

    def tick_shm(self) -> None:
        if self.vel_y >= self.max_vel_y or self.vel_y <= self.min_vel_y:
            self.acc_y *= -1
        self.vel_y += self.acc_y
        self.y += self.vel_y

    def tick_normal(self) -> None:
        if self.vel_y < self.max_vel_y and not self.flapped:
            self.vel_y += self.acc_y
        if self.flapped:
            self.flapped = False

        self.y = clamp(self.y + self.vel_y, self.min_y, self.max_y)
        self.rotate()

    def tick_crash(self) -> None:
        if self.min_y <= self.y <= self.max_y:
            self.y = clamp(self.y + self.vel_y, self.min_y, self.max_y)
            # rotate only when it's a pipe crash and bird is still falling
            if self.crash_entity != "floor":
                self.rotate()

        # player velocity change
        if self.vel_y < self.max_vel_y:
            self.vel_y += self.acc_y

    def rotate(self) -> None:
        self.rot = clamp(self.rot + self.vel_rot, self.rot_min, self.rot_max)

    def draw(self) -> None:
        self.update_image()
        if self.mode == PlayerMode.SHM:
            self.tick_shm()
        elif self.mode == PlayerMode.NORMAL:
            self.tick_normal()
        elif self.mode == PlayerMode.CRASH:
            self.tick_crash()

        self.draw_player()

    def draw_player(self) -> None:
        rotated_image = pygame.transform.rotate(self.image, self.rot)
        rotated_rect = rotated_image.get_rect(center=self.rect.center)
        self.config.screen.blit(rotated_image, rotated_rect)

    def stop_wings(self) -> None:
        self.img_gen = cycle([self.img_idx])

    def flap(self) -> None:
        if self.y > self.min_y:
            self.vel_y = self.flap_acc
            self.flapped = True
            self.rot = 80
            self.config.sounds.wing.play()

    def crossed(self, pipe: Pipe) -> bool:
        return pipe.cx <= self.cx < pipe.cx - pipe.vel_x

    def collided(self, pipes: Pipes, floor: Floor) -> bool:
        """returns True if player collides with floor or pipes."""

        # if player crashes into ground
        if self.collide(floor): # type: ignore
            self.crashed = True
            self.crash_entity = "floor" 
            return True

        for pipe in pipes.upper:
            if self.collide(pipe): # type: ignore
                self.crashed = True
                self.crash_entity = "pipe"
                return True
        for pipe in pipes.lower:
            if self.collide(pipe): # type: ignore
                self.crashed = True
                self.crash_entity = "pipe"
                return True

        return False
    
    def update(self, pipes: Pipes, window: Window):
        # # if self.on_ground:
        # #     return
        # if self.alive:
        #     self.fitness += 1
        self.think(pipes, window)
        
    def get_inputs(self, pipes: Pipes, window: Window) -> List[float]:
        inputs: List[float] = []
        input2 = (pipes.upper[0].y - self.y) / window.height
        input3 = (self.y - pipes.upper[0].y) / window.height
           # (self.rect.y - closest.bottomPos) / win_height
        inputs.append(input2)  # Dist from bird to top Pipe
        inputs.append(input3)  # Dist from bird to bottom Pipe
        return inputs

    def think(self, pipes: Pipes, window: Window) -> bool:
        inputs = self.get_inputs(pipes, window)
        should_flap = False
        sigmoid: Callable[[float], float] = lambda x: 1 / (1 + math.exp(-x))
        # Get outputs from brain
        # outs = self.brain.get_outputs(inputs)
        
        outs: List[float] =[0.89, sigmoid(inputs[0]*-0.922838921439954 + inputs[1] * 1.8011388502959025)]
        # with open("C:\\Users\\ZsomborVeres-Lakos\\Documents\\flappy_outputs.csv", 'a') as f:
        #     f.write(str(outs[1]) + '\n')
        # use outputs to flap or not
        if outs[1] > outs[0]:
            should_flap = True
        
        if should_flap:
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE}))

        return should_flap