
class Weighted_Adj_List:
    """
    Initialized by 
    1) A dict adj_list of items of the form vertex : set[of Vertices] and
    2) A dict weights with items of the form (source_vertex, target_vertex) : float 
    """

    def __init__(self, adj_list, weights):
        self.V = set()
        self.E = adj_list or dict()
        self.weights = weights
        for tail in self.E.keys():
            self.V.add(tail)
            for tip in self.E[tail]:
                self.V.add(tip)
        for v in self.V:
            if v not in self.E.keys():
                self.E[v] = set()
    def get_targets(self, source):
        return self.E[source]
    def get_weight(self, source, target):
        return self.weights[(source, target)]
