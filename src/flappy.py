import asyncio
import math
import sys

import pygame
from pygame.locals import K_ESCAPE, K_SPACE, K_UP, KEYDOWN, QUIT

from .entities import (
    Background,
    Floor,
    GameOver,
    Pipes,
    Player,
    PlayerMode,
    Score,
    WelcomeMessage,
)
from .utils import GameConfig, Images, Sounds, Window


class Flappy:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Flappy Bird")
        window = Window(288, 512)
        screen = pygame.display.set_mode((window.width, window.height))
        images = Images()

        self.config = GameConfig(
            screen=screen,
            clock=pygame.time.Clock(),
            fps=30,
            window=window,
            images=images,
            sounds=Sounds(),
        )

    async def start(self):
        while True:
            self.background = Background(self.config)
            self.floor = Floor(self.config)
            self.player = Player(self.config)
            self.welcome_message = WelcomeMessage(self.config)
            self.game_over_message = GameOver(self.config)
            self.pipes = Pipes(self.config)
            self.score = Score(self.config)
            await self.splash()
            await self.play()
            await self.game_over()

    async def splash(self):
        """Shows welcome splash screen animation of flappy bird"""

        self.player.set_mode(PlayerMode.SHM)

        while True:
            for event in pygame.event.get():
                self.check_quit_event(event)
                if self.is_tap_event(event):
                    return

            self.background.tick()
            self.floor.tick()
            self.player.tick()
            self.welcome_message.tick()

            pygame.display.update()
            await asyncio.sleep(0)
            self.config.tick()

    def check_quit_event(self, event):
        if event.type == QUIT or (
            event.type == KEYDOWN and event.key == K_ESCAPE
        ):
            pygame.quit()
            sys.exit()

    def is_tap_event(self, event):
        m_left, _, _ = pygame.mouse.get_pressed()
        space_or_up = event.type == KEYDOWN and (
            event.key == K_SPACE or event.key == K_UP
        )
        screen_tap = event.type == pygame.FINGERDOWN

        cp = self.computer_prediction()

        return m_left or space_or_up or screen_tap or cp

    def computer_prediction(self) -> bool:

        return False
    

    def get_inputs(self, pipes: Pipes) -> list:
        inputs = []

        input2 = (pipes.upper[0].y - self.player.y) / self.config.window.height
        input3 = (self.player.y - pipes.upper[0].y) / self.config.window.height
           # (self.rect.y - closest.bottomPos) / win_height
        inputs.append(input2)  # Dist from bird to top Pipe
        inputs.append(input3)  # Dist from bird to bottom Pipe
        return inputs

    def think(self, pipes: Pipes) -> bool:
        inputs = self.get_inputs(pipes)

        should_flap = False
        sigmoid = lambda x: 1 / (1 + math.exp(-x))

        # Get outputs from brain
        # outs = self.brain.get_outputs(inputs)
        
        outs =[0.89, sigmoid(inputs[0]*-0.922838921439954 + inputs[1] * 1.8011388502959025)]
        # with open("C:\\Users\\ZsomborVeres-Lakos\\Documents\\flappy_outputs.csv", 'a') as f:
        #     f.write(str(outs[1]) + '\n')
        # use outputs to flap or not
        if outs[1] > outs[0]:
            should_flap = True
        
        if should_flap:
            pygame.event.post(pygame.event.Event(KEYDOWN, {"key": K_SPACE}))

        return should_flap

    async def play(self):
        self.score.reset()
        self.player.set_mode(PlayerMode.NORMAL)

        while True:
            if self.player.collided(self.pipes, self.floor):
                return
            
            computer_decision = self.think(self.pipes)
            for i, pipe in enumerate(self.pipes.upper):
                if self.player.crossed(pipe):
                    self.score.add()
            
            for event in pygame.event.get():
                self.check_quit_event(event)
                # $$$ is tap event, this controls the flap
                if self.is_tap_event(event):
                    self.player.flap()

            self.background.tick()
            self.floor.tick()
            self.pipes.tick()
            self.score.tick()
            self.player.tick()

            pygame.display.update()
            await asyncio.sleep(0)
            self.config.tick()

    async def game_over(self):
        """crashes the player down and shows gameover image"""

        self.player.set_mode(PlayerMode.CRASH)
        self.pipes.stop()
        self.floor.stop()

        while True:
            for event in pygame.event.get():
                self.check_quit_event(event)
                if self.is_tap_event(event):
                    if self.player.y + self.player.h >= self.floor.y - 1:
                        return

            self.background.tick()
            self.floor.tick()
            self.pipes.tick()
            self.score.tick()
            self.player.tick()
            self.game_over_message.tick()

            self.config.tick()
            pygame.display.update()
            await asyncio.sleep(0)
