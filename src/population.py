import random
from typing import List

from src.flappy import AutoPlayer, GeneHistory
from src.utils import GameConfig

class Population:
    def __init__(self, config: GameConfig, gh: GeneHistory, pop_size: int = 2) -> None: 
        self.best_fitness = 0
        self.pop_size = pop_size  # Size of population
        self.population: List[AutoPlayer] = []  # Population is sprite group
        for _ in range(self.pop_size):
            self.population.append(AutoPlayer(config, gh))
        self.gh = gh
        self.best_fitness = 0
        pass


    def reset(self):
        parents = self.population.copy()

        parents.sort(key = lambda x: x.fitness, reverse=True)
        self.population.clear()

        for _ in range(self.pop_size):
            parent1 = parents[random.randint(0,len(parents) // 10)]
            parent2 = parents[random.randint(0, len(parents) // 10)]
            
            
            childPlayer = parent1.mate(parent2)
            childPlayer.brain.mutate()
            
            self.population.append(childPlayer)        
        self.best_fitness = 0
        pass


    # def update(self, pipes: Pipes, player: Player, window: Window):
    #     best_bird = AutoPlayer()

    #     for bird in self.population:
    #         bird.update(pipes, player, window)
    #         if bird.fitness > self.best_fitness:
    #             self.best_fitness = bird.fitness
    #             best_bird = bird
    #     return best_bird

