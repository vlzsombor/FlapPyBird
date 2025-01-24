import random
import pygame
 
 
class Gene:
    def __init__(self, in_node: int, out_node: int):
        self.in_node: int = in_node
        self.out_node: int = out_node
        self.weight = default_weight() 
        self.enabled = True
        self.innovation = 0
 
        self.color = (0, 255, 0)
 
 
    def clone(self):
        clone = Gene(self.in_node, self.out_node)
        clone.weight = self.weight
        clone.enabled = self.enabled
        clone.innovation = self.innovation
        return clone
    
    def mutation(self):
        if random.random() < 0.1:
            self.weight = default_weight()
        else:
            self.weight += random.uniform(-0.02, 0.02)
 
            self.weight = self.weight if self.weight < 2 else 2
            self.weight = self.weight if self.weight > -2 else -2
 
    def get_info(self):
        s = str(self.inno) + "] "
        s += str(self.in_node.number) + "(" + str(self.in_node.layer) + ") -> "
        s += str(self.out_node.number) + "(" + str(self.out_node.layer) + ") "
        s += str(self.weight) + " "
        s += str(self.enabled) + "\n"
        return s
 
    def __str__(self) -> str:
        return self.get_info()
 
    def show(self, ds):
        self.color = (255, 0, 0) if self.weight > 0 else (0, 0, 255)
        if not self.enabled:
            self.color = (0, 255, 0)
        pygame.draw.line(ds, self.color, self.in_node.pos, self.out_node.pos, 2)
        pass
    
    def show(self, ds):
        self.color = (255, 0, 0) if self.weight > 0 else (0,0, 255)
        if not self.enabled:
            self.color = (0, 255, 0)
        pygame.draw.line(ds, self.color, self.in_node.pos, self.out_node.pos, 2)
 
def default_weight():
    return random.random() * 4 - 2
