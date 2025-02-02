import math
from typing import Callable, List

import pygame
from src.entities import Player
from src.entities.pipe import Pipes

from src.neat.geneHistory import GeneHistory
from src.neat.genome import Genome
from src.utils import GameConfig, Window


class AutoPlayer(Player):
    def __init__(self, config: GameConfig, gh: GeneHistory) -> None:
        super().__init__(config) # type: ignore
        self.gh = gh  # The genome history
        self.brain = Genome(gh)

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
        outs = self.brain.get_outputs(inputs)
        
        # outs: List[float] =[0.89, sigmoid(inputs[0]*-0.922838921439954 + inputs[1] * 1.8011388502959025)]
        # with open("C:\\Users\\ZsomborVeres-Lakos\\Documents\\flappy_outputs.csv", 'a') as f:
        #     f.write(str(outs[1]) + '\n')
        # use outputs to flap or not
        if outs[1] > outs[0]:
            should_flap = True
        
        if should_flap:
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {"key": pygame.K_SPACE}))

        return should_flap