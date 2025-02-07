import asyncio
import math
import sys

import pygame
from pygame.locals import K_ESCAPE, K_SPACE, K_UP, KEYDOWN, QUIT

from src.neat.autoPlayer import AutoPlayer, GeneHistory
from src.population import Population

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
            n_inputs=4,
            n_outputs=2
        )
        self.gh = GeneHistory(self.config.n_inputs, self.config.n_outputs)
        self.population = Population(self.config, self.gh)


    async def start(self):
        while True:
            self.background = Background(self.config)
            self.floor = Floor(self.config)


            # self.player = AutoPlayer(self.config, self.gh)
            #self.player = Player(self.config)
            self.welcome_message = WelcomeMessage(self.config)
            self.game_over_message = GameOver(self.config)
            self.pipes = Pipes(self.config)
            self.score = Score(self.config)
            # await self.splash()
            await self.play()
            # await self.game_over()
            # game over:
            self.population.reset()
            
    async def splash(self, player):
        """Shows welcome splash screen animation of flappy bird"""

        player.set_mode(PlayerMode.SHM)

        while True:
            for event in pygame.event.get():
                self.check_quit_event(event)
                if self.is_tap_event(event):
                    return

            self.background.tick()
            self.floor.tick()
            player.tick()
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


        return m_left or space_or_up or screen_tap

    async def play(self):
        self.score.reset()
        while True:
            # alive or dead
            for player in self.population.population:
                player.set_mode(PlayerMode.NORMAL)
                if player.collided(self.pipes, self.floor):
                    return
                autoFlap = player.update(self.pipes, self.config.window)


                # self.think(self.pipes)
                for i, pipe in enumerate(self.pipes.upper):
                    if player.crossed(pipe):
                        self.score.add()

                if autoFlap:
                    player.flap()
                else:
                    for event in pygame.event.get():
                        self.check_quit_event(event)
                        # $$$ is tap event, this controls the flap
                        if self.is_tap_event(event):
                            player.flap()

                self.background.tick()
                self.floor.tick()
                self.pipes.tick()
                self.score.tick()
                player.tick()

                pygame.display.update()
                await asyncio.sleep(0)
                self.config.tick()

    async def game_over(self, player):
        """crashes the player down and shows gameover image"""

        player.set_mode(PlayerMode.CRASH)
        self.pipes.stop()
        self.floor.stop()

        while True:
            for event in pygame.event.get():
                self.check_quit_event(event)
                if self.is_tap_event(event):
                    if player.y + player.h >= self.floor.y - 1:
                        return

            self.background.tick()
            self.floor.tick()
            self.pipes.tick()
            self.score.tick()
            player.tick()
            self.game_over_message.tick()

            self.config.tick()
            pygame.display.update()
            await asyncio.sleep(0)
