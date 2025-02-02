import pygame

from src.neat.AutoPlayer import AutoPlayer
from .entities import (
    Player,
    Pipes
)
from .utils import Window


class Population:
    def __init__(self) -> None:
        self.population: pygame.sprite.Group[Bird] = pygame.sprite.Group[Bird]()  # type: ignore # this has Birds
        self.best_fitness = 0


    # def update(self, pipes: Pipes, player: Player, window: Window):
    #     best_bird = AutoPlayer()

    #     for bird in self.population:
    #         bird.update(pipes, player, window)
    #         if bird.fitness > self.best_fitness:
    #             self.best_fitness = bird.fitness
    #             best_bird = bird
    #     return best_bird

