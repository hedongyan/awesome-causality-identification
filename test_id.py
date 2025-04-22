from algorithms.id import *

# ----------------------create ADMG----------------------
g = ADMG()

# add nodes names
g.add_node("u1")
g.add_node("u2")
g.add_node("u3")
g.add_node("u4")
g.add_node("X")
g.add_node("EC")
g.add_node("Y")
g.add_node("u5")

# add directed edges
g.add_directed_edge("u1","X")
g.add_directed_edge("u2","X")
g.add_directed_edge("X","EC")
g.add_directed_edge("u3","EC")
g.add_directed_edge("u4","EC")
g.add_directed_edge("EC","Y")
g.add_directed_edge("u5","Y")

# add bidirected edges with hidden confounders

# ----------------------create ADMG----------------------

# ----------------------create probability----------------------
# use ObservationProbability to represent a distribution
p = ObservationProbability()
# put all names and joint distribution into the list as start
p.set_all(None, [], ["u1","u2","u3","u4", "X", "EC", "Y", "u5"], [], ["u1","u2","u3","u4", "X", "EC", "Y", "u5"])
# ----------------------create probability----------------------

# ----------------------create causal query----------------------
# use InterventionQuery to represent a causal query
q = InterventionQuery()
# add the causal query: graph, [intervention], [outcome], [condition], probability, identified?)
q.set_all(g, ["X"], ["Y"], [], p, False)
# ----------------------create causal query----------------------

# ----------------------create identification algorithm and identify----------------------
# use ID to represent the identification algorithm
# add identification algorithm, 
newid = ID()
# start identify the causal query, 
identified_p = newid.id(q)
# ----------------------create identification algorithm and identify----------------------

# ----------------------print the identification result----------------------
print("identification result:\n",identified_p.get_latex_expression())
# ----------------------print the identification result----------------------