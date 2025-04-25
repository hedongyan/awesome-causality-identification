from algorithms.id import *
import networkx as nx
import numpy as np

# -----------------------identify all with 4 measured variables----------------------- 
direct_edge = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
birected_edge = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

# create a graph with 4 nodes, 
# X1, X2, X3, X4, 
def create_graph(direct_edge, birected_edge, name):
    g = ADMG()
    g.add_node(name[0])
    g.add_node(name[1])
    g.add_node(name[2])
    g.add_node(name[3])
    for i in range(4):
        for j in range(4):
            if direct_edge[i][j] == 1:
                g.add_directed_edge(name[i],name[j])
            if birected_edge[i][j] == 1:
                g.add_birected_edge(name[i],name[j])
    return g

def noselfLoop(direct_edges):
    for i in range(4):
        if direct_edges[i][i] == 1:
            return False
    return True

def isBirected(birected_edges):
    for i in range(4):
        for j in range(4):
            if birected_edges[i][j] == 1 and birected_edges[j][i] == 0:
                return False
    return True

def isDirectedAcyclicGraph(direct_edges):

    g = nx.DiGraph()
    for i in range(4):
        for j in range(4):
            if direct_edges[i][j] == 1:
                g.add_edge(i,j)
    return nx.is_directed_acyclic_graph(g)

total_admg = 0
not_identifiable = 0
identifiable = 0
identified_results = []
# for all direct edges
for i in range(2**16):
    tmp_direct_edge = bin(i)[2:].zfill(16)
    tmp_direct_edge = np.array(list(map(int, tmp_direct_edge))).reshape(4,4)
    if noselfLoop(tmp_direct_edge) is False:
        continue
    if isDirectedAcyclicGraph(tmp_direct_edge) is False:
        continue
    # g = create_graph(tmp_direct_edge, birected_edge, ["X1","X2","X3","X4"])
    # x = g.topological_sort()
    # print("topological sort:",x)
    # print("direct edge:",noselfLoop(tmp_direct_edge))
    # for all birected edges
    for j in range(2**16):
        # print(tmp_direct_edge)
        tmp_birected_edge = bin(j)[2:].zfill(16)
        tmp_birected_edge = np.array(list(map(int, tmp_birected_edge))).reshape(4,4)
        # print(tmp_direct_edge)
        if isBirected(tmp_birected_edge) is False \
            or noselfLoop(tmp_birected_edge) is False:
            continue
        total_admg += 1
        g = create_graph(tmp_direct_edge, tmp_birected_edge, ["X1","X2","X3","X4"])
        p = ObservationProbability()
        p.set_all(None, [], ["X1","X2","X3","X4"], [], ["X1","X2","X3","X4"])
        q = InterventionQuery()
        q.set_all(g, ["X4"], ["X1"], [], p, False)
        newid = ID()
        identifable = True
        try:
            identified_p = newid.id(q)
            identifiable += 1
            latexstr = identified_p.get_latex_expression()
            # print(latexstr)
            aa = r"\sum_{X2,X3}{\sum_{X1}{\frac{\sum_{X3,X4}{p(V)}*p(V)}{\sum_{X4}{p(V)}}}*\frac{\sum_{X2,X4}{p(V)}}{\sum_{X3}{\sum_{X2,X4}{p(V)}}}}"
            if latexstr == aa:
                g.print()
                import os
                os.system("pause")
            if latexstr not in identified_results:
                # print(latexstr)
                identified_results.append(latexstr)
                # print("\n")
                # print(identified_results)
                # print("not in")
                # print(latexstr)
            # else:
                # print("already in")
                # print(latexstr)
            # print("identification result:\n",identified_p.get_latex_expression())
        except:     
            # print("not identifiable")
            not_identifiable += 1
        print("total:",total_admg)
        print("identifiable:",identifiable)
        print("not identifiable:",not_identifiable)
    print("total:",total_admg)
    for ss in identified_results:
        print(ss)
        if identified_p.get_latex_expression() == "\\text{True}":
            print("direct edge:",direct_edge)
            print("birected edge:",birected_edge)
            print("identification result:\n",identified_p.get_latex_expression())
            print("\n")

print("len(identified_results):",len(identified_results))
identified_results = list(set(identified_results))
print("len(identified_results):",len(identified_results))
for ss in identified_results:
    print(ss)
print("total:",total_admg)
print("identifiable:",identifiable)
print("not identifiable:",not_identifiable)
print("identifiable/total:",identifiable/total_admg)

np.savetxt("identified_results.txt",identified_results,fmt="%s")


# manually check the identified results, 
# 1. copy the "identified_results.txt" result to "MY_identified_results.txt",
#   where "MY_identified_results.txt" is the 

# expressions_before = np.loadtxt("identified_results.txt",dtype=str)
# expressions_after = np.loadtxt("MY_identified_results.txt",dtype=str)
# before_after = list_minus(expressions_before,expressions_after)
# np.savetxt("before_after.txt",before_after,fmt="%s")
# print("len(before_after):",len(before_after))
# after_before = list_minus(expressions_after,expressions_before)
# np.savetxt("after_before.txt",after_before,fmt="%s")
# print("len(after_before):",len(after_before))
# from sympy.parsing.latex import parse_latex
# import sympy.parsing.latex._antlr.latexparser as lp
# expr = parse_latex(r"\frac {1 + \sqrt {\a}} {\b}")
# print(expr)

# # np.readtxt("identified_results.txt",dtype=str)
# expressions = np.loadtxt("identified_results.txt",dtype=str)
# for i in range(len(expressions)):
#     print(expressions[i])
#     parse_latex(repr(expressions[i]))
#     print(expressions[i])
# print("len(expressions):",len(expressions))