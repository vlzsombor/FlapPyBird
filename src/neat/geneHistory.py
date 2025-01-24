class GeneHistory:
    def __init__(self, n_inputs: int, n_outputs: int):
        self.n_inputs = n_inputs
        self.n_outputs = n_outputs
        self.all_genes = []
        # Global highest innovation
        self.global_inno = 0
        self.highest_hidden = 2
        pass

    def exists(self, input_node_id, output_node_id):
        for g in self.all_genes:
            if g.in_node.number == input_node_id.number and g.out_node.number == output_node_id.number:
                return g.clone()
        return None
