import math
import random
from typing import Callable, List
from typing import Self

import pygame
from src.entities import Player
from src.entities.pipe import Pipes

from src.neat.geneHistory import GeneHistory
from src.neat.genome import Genome
from src.utils import GameConfig, Window


class AutoPlayer(Player):
    def __init__(self, config: GameConfig, gh: GeneHistory, clone: bool = False) -> None:
        super().__init__(config) # type: ignore
        self.gh = gh  # The genome history
        self.brain = Genome(gh)
        self.fitness = 0
        self.alive = True
        # Random mutations for brain at start
        if not clone:
            for _ in range(10):
                self.brain.mutate()
    def mate(self, partner: Self):
        child = AutoPlayer(self.config, self.gh)
        child.brain = self.brain.crossover(partner.brain)
        return child

    def update(self, pipes: Pipes, window: Window):
        # # if self.on_ground:
        # #     return
        # if self.alive:
        #     self.fitness += 1
        return self.think(pipes, window)
        
    def get_inputs(self, pipes: Pipes, window: Window) -> List[float]:
        inputs: List[float] = []
        y_pos_ground = 512 # I guess thats the ground y height
        input0 = (y_pos_ground - self.rect.y) / window.height  # bird height
        input1 = (pipes.upper[0].x - self.rect.x) / window.width  # Dist from pipe

        input2 = (pipes.upper[0].y - self.y) / window.height
        input3 = (self.y - pipes.lower[0].y) / window.height
           # (self.rect.y - closest.bottomPos) / win_height
        inputs.append(input0)  # Dist from bird to top Pipe
        inputs.append(input1)  # Dist from bird to top Pipe
        inputs.append(input2)  # Dist from bird to top Pipe
        inputs.append(input3)  # Dist from bird to bottom Pipe
        return inputs

    def think(self, pipes: Pipes, window: Window) -> bool:
        inputs = self.get_inputs(pipes, window)
        should_flap = False
        # Get outputs from brain
        #outs = self.brain.get_outputs(inputs)
        sigmoid: Callable[[float], float] = lambda x: 1 / (1 + math.exp(-x))
        #outs: List[float] =[0.89, sigmoid(inputs[2]*-0.922838921439954 + -inputs[2] * 1.8011388502959025)]
        outs: List[float] =[0.89, sigmoid(-2.72397777 * inputs[2])]
        # with open("C:\\Users\\ZsomborVeres-Lakos\\Documents\\flappy_outputs.csv", 'a') as f:
        #     f.write(str(outs[1]) + '\n')
        # use outputs to flap or not
        if outs[1] > outs[0]:
            should_flap = True
       
 
        return should_flap