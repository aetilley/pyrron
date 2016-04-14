A PageRank-style node-centrality algorithm for ranking vertices (nodes) in an arbitrary
weighted digraph.

Recall the PageRank model postulates a surfer clicking random links with uniform probability of
clicking any given link on a page and with the assumption that if the surfer enters a dead end,
on the next iteration they re-materialize at another page with uniform probability.
Furthermore there is a damping coefficient d, such that at any iteration the user has
probability (1-d) of "stopping," meaning that they re-materialize at another page with
uniform probability at the next iteration.

Pyrron generalizes this by not assuming that the transition probabilities are uniform across
the outgoing edges, and by allowing loops.  Thus instead of taking a naked (unweighted),
simple (not loops or multiple edges between pairs of vertices) digraph for input,
the Pyrron constructor takes any non-negatively weighted digraph (which may have loops,
but no multiple edges). 

More specifically:
i) After formating the input into a weighted adjacency matrix called M_given, we construct
M_norm by dividing each non-zero column of M_given by its sum and replacing columns of
zeros in M_norm by (1/N)*ones(N).

ii) We then construct M_final by scaling each entry of M_norm by a damping coefficient
d in (0,1) (so that the columns now sum to d) and then adding (1-d)/N to each element.

We can think of the damping-coefficient d as the probability at any given iteration a given
process, travelling along some path in the graph, continues along one of the available outgoing
edges instead of choosing to reset randomly to an arbitrary vertex.

Note that M_final
a) Is column stochastic, so it has maximum eigenvalue 1.
b) Has all positive entries, so Perron's Theorem tells us that:
   b1) The algebraic muliplicity of the eigenvalue 1 is 1 (1 is a simple eigenvalue).
   b2) The eigenvalue 1 is the only eigenvalue on the unit circle.
   b3) There exist unique right and left eigenvectors v and w^T for the eigenvalue 1 such
   that |v|_1 = |w|_1 = 1.  These are the Perron right and left eigenvector respectively.

Now recall that the matrices M for which M^k converges are precisely those for which

(*) the spectral radius is no greater than 1 with no eigenvalues on the unit circle other than 1,
and any eigenvalue 1 semi-simple.

But we have just shown that these all hold (simple implies semi-simple).

It follows that we can compute the limiting output distribution either by

i) Approximating the limit of M^k(p_0) as k -> infinity (for some starting distribution p_0) OR
ii) By computing the Perron right-eigenvector of M_final.


Example:

In [1]: from pyrron import Pyrron

In [2]: from w_a_list import Weighted_Adj_List

In [3]: a_list = {"a":{"b", "c"}, "b":{"c"}}

In [4]: weights = {('a', 'b'):.25, ('a', 'c'):1, ('b','c'):13}

In [5]: wal = Weighted_Adj_List(a_list, weights)

In [6]: p = Pyrron(wal)

In [7]: p.distribution
Out[7]: {'a': 0.20641965115078956, 'b': 0.24151099184642372, 'c': 0.5520693570027867}

In [8]: q = Pyrron(wal, method='iterative')

In [9]: q.distribution
Out[9]: {'a': 0.20628784190538035, 'b': 0.24142762834334819, 'c': 0.55228452975127151}
