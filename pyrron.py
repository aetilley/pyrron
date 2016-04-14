"""A PageRank-style node-centrality algorithm consuming arbitrary weighted digraphs."""

import numpy as np
from scipy import linalg
from scipy.spatial.distance import euclidean as distance

class Pyrron():

    def __init__(self, digraph = None, input_type = "walist", damp = .85,
                 method = "algebraic", tolerance = .001):
        """
        digraph: the graph data, in the form of input_type
        input_type: "walist" or "wamatrix" (weighted adjacency list or matrix)
        damp: damping factor. probability of following a random, available outgoing edge 
        and not resetting to a random vertex.
        method: "iterative" vs. "algebraic"
        tolerance: to be used if method == "iterative"
        """
        if input_type == "walist":
            #run check
            M_given, vert_map = compute_w_a_matrix(digraph) #compute weighted adjacency matrix.

        elif input_type == "wamatrix":
            #run check
            M_given = digraph
            vert_map = list(np.arange(M_given.shape(0)))
        else:
            print("Stated input type must be wamatrix or walist")
            exit()
        
        size = M_given.shape[0] #Number of vertices in the graph
        M_sums = M_given.sum(axis=0) #Find columns of zeros
        inds = np.arange(size) 
        inds = inds[M_sums == 0]
        M_given[:,inds] = 1 #Set zero columns equal to ones columns
        new_sums = M_given.sum(axis=0)
        M_norm = M_given / new_sums
        M_final = damp * M_norm + ((1-damp) / size) * np.ones((size, size))

        if method == "algebraic":
            vector = compute_perron_vector(M_final)
        elif method == "iterative":
            vector = power_method(M_final, tolerance = tolerance)
        else:
            print("Method must be one of \"algebraic\" or \"iterative.\"")
            quit()
        self.distribution = distribution_from_vector(vector, vert_map)

def compute_perron_vector(matrix):
    #first we check that matrix is positive
    pos = matrix > 0
    assert pos.all(), "Input matrix must be everywhere positive."
    vals, vects = linalg.eig(matrix)
    perron = vects[:, vals == 1]
    perron = perron / perron.sum()
    return perron

def power_method(M_final, tolerance = .001, init = None):
    size = M_final.shape[0]
    init = init or (1 / size) * np.ones(size)
    dist_old = init
    dist_new = M_final.dot(dist_old)
    while distance(dist_old, dist_new) > tolerance:
        dist_old = dist_new
        dist_new = M_final.dot(dist_old)
    scaled_result = dist_new / dist_new.sum()
    return scaled_result

def compute_w_a_matrix(w_a_list):
    """
    Compute weighted adjacency matrix and mapping from vertices to indices.
    """
    verts = list(w_a_list.V) #FIX AN ORDERING
    num_verts = len(verts)
    M = np.zeros((num_verts, num_verts))
    for source_ind in np.arange(num_verts):
        source = verts[source_ind]
        for target in w_a_list.get_targets(source):
            target_ind = verts.index(target)
            weight = w_a_list.get_weight(source, target)
            M[target_ind, source_ind] = weight
    return M, verts #verts can be used to recover vertices from indices
            
        
def distribution_from_vector(vector, vertex_list):
    """
    Returns a dictionary giving the probability of a vertex in the vertex list 
    the probability of which is the corresponding element in vector
    """
    dist = dict()
    size = len(vertex_list)
    vector = vector.reshape((size,))
    for i in range(size):
        dist[vertex_list[i]] = vector[i]
    return dist
