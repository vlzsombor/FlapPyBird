


import pygame
import math

class Node:
    def __init__(self, id: int, layer_id: int):
        self.id: int = id
        self.layer_id: int = layer_id
        self.output: int = 0
        self.in_genes: list = []
        self.activation_function = lambda x : 1 / (1 + math.exp(-x))

        # showing
        self.color = (255, 255, 255)
        self.bcolor = (0, 0, 0)

        self.radius = 5
        self.border_radius = 2
        self.pos = [0, 0]

        pass

    def clone(self):
        n = Node(self.id, self.layer_number)
        n.output = self.output
        n.pos = self.pos
        return n
    
    def calculate(self):
        if self.layer_id == 0:
            print("No calculations for first layer")
            return
        
        s = 0
        for g in self.in_genes:
            if g.enabled:
                s += g.in_node.output * g.weight
        
        self.output = self.activation_function(s)
        pass
    def show(self, ds):
        pygame.draw.circle(ds, self.bcolor, self.pos, self.radius + self.border_radius)
        pygame.draw.circle(ds, self.color, self.pos, self.radius)
        pass