import random
import pygame

from src.flappy import AutoPlayer


class Population:
    def __init__(self, population: pygame.sprite.Group[AutoPlayer], pop_size = 1) -> None: # type: ignore
        self.population: pygame.sprite.Group[AutoPlayer] = pygame.sprite.Group[AutoPlayer]()  # type: ignore # this has Birds
        self.best_fitness = 0
        self.pop_size = pop_size  # Size of population


    def reset(self):
        parents = self.population.sprites()

        parents.sort(key = lambda x: x.fitness, reverse=True)
        self.population.empty()

        for i in range(self.pop_size):
            parent1 = parents[random.randint(0,len(parents) // 10)]
            parent2 = parents[random.randint(0, len(parents) // 10)]

            bird = parent1.mate(parent2)



    # def update(self, pipes: Pipes, player: Player, window: Window):
    #     best_bird = AutoPlayer()

    #     for bird in self.population:
    #         bird.update(pipes, player, window)
    #         if bird.fitness > self.best_fitness:
    #             self.best_fitness = bird.fitness
    #             best_bird = bird
    #     return best_bird

