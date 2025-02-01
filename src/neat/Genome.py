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
        pass

    def add_gene(self):
        n1 = random.choice(self.nodes)
        n2 = random.choice(self.nodes)

        while n1.layer == n2.layer:
            n1 = random.choice(self.nodes)
            n2 = random.choice(self.nodes)
        self.connect_nodes(n1, n2)
        pass

    def mutate(self):
        if len(self.genes) == 0:
            self.add_gene()
        if random.random() < 0.8:
            for i in range(len(self.genes)):
                self.genes[i].mutate()
        if random.random() < 0.08:
            self.add_gene()
        if random.random() < 0.02:
            self.add_node()
        pass
    ####

    def add_node(self):
        if len(self.genes) == 0:
            self.add_gene()
        
        if random.random() < 0.9:
            self.gh.highest_hidden += 1

        n = Node(self.total_nodes, random.randint(2, self.gh.highest_hidden))
        self.total_nodes += 1

        g = random.choice(self.genes)
        l1 = g.in_node.layer
        l2 = g.out_node.layer

        if l2 == 1:
            l2 = 1000000 # $$$ wtf is this?
        
        while l1 > n.layer or l2 < n.layer:
            g = random.choice(self.genes)
            l1 = g.in_node.layer
            l2 = g.out_node.layer
            if l2 == 1:
                l2 = 1000000
        self.connect_nodes


    def get_node(self, n: int):
        for i in range(len(self.nodes)):
            if self.nodes[i].number == n:
                return self.nodes[i]
        raise ValueError("Node not found : Something's Wrong")

    def connect_genes(self) -> None:
        for i in range(len(self.genes)):
            self.genes[i].in_node = self.get_node(self.genes[i].in_node.number)
            self.genes[i].out_node = self.get_node(self.genes[i].out_node.number)
        
        for i in range(len(self.nodes)):
            self.nodes[i].in_genes.clear()
        
        for i in range(len(self.genes)):
            self.genes[i].out_node.in_genes.append(self.genes[i])
        pass

    def get_outputs(self, inputs: List[float]):
        if len(inputs) != self.n_inputs:
            print("Wrong number of inputs")
            return [-1]
        

        for i in range(self.n_inputs):
            self.nodes[i].output = inputs[i]
        
        self.connect_genes()

        for layer in range(2, self.gh.highest_hidden + 1):
            nodes_in_layer: List[Node] = []
            for n in range(len(self.nodes)):
                if self.nodes[n].layer == layer:
                    nodes_in_layer.append(self.nodes[n])
            
            for n in range(len(nodes_in_layer)):
                nodes_in_layer[n].calculate()

            final_outputs: List[float] = []

            for n in range(self.n_inputs, self.n_inputs + self.n_outputs):
                self.nodes[n].calculate()
                final_outputs.append(self.nodes[n].output)

            return final_outputs


