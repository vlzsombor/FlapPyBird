import random
from typing import List
from src.neat.Gene import Gene
from src.neat.GeneHistory import GeneHistory
from src.neat.Node import Node


class Genome:
    def __init__(self, gh: GeneHistory, c1: float = 1.0, c2: float = 1.0, c3: float = 1.0):
        self.gh: GeneHistory = gh
        self.n_inputs: int = self.gh.n_inputs
        self.n_outputs: int = gh.n_outputs
        self.total_nodes = 0
        self.nodes: List[Node] = []
        self.genes: List[Gene] = []

        self.c1 = c1
        self.c2 = c2
        self.c3 = c3


        self.fitness = random.uniform(0,200)
        self.adjusted_fitness = 0

        for _ in range(self.n_inputs):
            self.nodes.append(Node(self.total_nodes, 0))
            self.total_nodes += 1

        for _ in range(self.n_outputs):
            self.nodes.append(Node(self.total_nodes, 1))
            self.total_nodes += 1
        pass

    def clone(self):
        clone = Genome(self.gh)
        clone.total_nodes = self.total_nodes
        clone.nodes.clear()
        clone.genes.clear()

        for i in range(len(self.nodes)):
            clone.nodes.append(self.nodes[i].clone())

        for i in range(len(self.genes)):
            clone.genes.append(self.genes[i].clone())

        clone.connect_genes()
        return clone
    
    def exists(self, inno: int):
        for g in self.genes:
            if g.innovation == inno:
                return True
        return False
    
    def connect_nodes(self, n1: Node, n2: Node):
        n1Layer= n1.layer if n1.layer != 1 else 1000000
        n2layer = n2.layer if n2.layer != 1 else 1000000

        if n1Layer > n2layer:
            n1, n2 = n2, n1

        c = self.gh.exists(n1, n2)
        x = Gene(n1, n2)


        if c:
            x.innovation = c.innovation
            if not self.exists(x.innovation):
                self.genes.append(x)
        else:
            x.innovation = self.gh.global_inno
            self.gh.global_inno += 1
            self.gh.all_genes.append(x.clone())
            self.genes.append(x)







    def connect_genes(self) -> None:
        pass
