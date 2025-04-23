from algorithms.id import *

# --------------------many admg examples--------------------
def create_napkin():
    g = ADMG()
    g.add_node("X1")
    g.add_node("X2")
    g.add_node("T")
    g.add_node("Y")
    g.add_directed_edge("X1","X2")
    g.add_directed_edge("X2","T")
    g.add_directed_edge("T","Y")

    g.add_birected_edge("X1","T")
    g.add_birected_edge("X1","Y")
    return g

def create_backdoor1():
    g = ADMG()
    g.add_node("X")
    g.add_node("T")
    g.add_node("Y")
    g.add_directed_edge("X","T")
    g.add_directed_edge("X","Y")
    g.add_directed_edge("T","Y")

    g.add_birected_edge("X","T")
    return g

def create_backdoor2():
    g = ADMG()
    g.add_node("X")
    g.add_node("T")
    g.add_node("Y")
    g.add_directed_edge("X","T")
    g.add_directed_edge("X","Y")
    g.add_directed_edge("T","Y")

    g.add_birected_edge("X","Y")
    return g

def create_frontdoor():
    g = ADMG()
    g.add_node("X")
    g.add_node("T")
    g.add_node("Y")
    g.add_directed_edge("T","X")
    g.add_directed_edge("X","Y")

    g.add_birected_edge("T","Y")
    return g

def create_1_bow_3_v():
    g = ADMG()
    g.add_node("X")
    g.add_node("T")
    g.add_node("Y")
    g.add_directed_edge("T","X")
    g.add_directed_edge("X","Y")

    g.add_birected_edge("T","X")
    return g

def create_2_bow_3_v_nonid1():
    g = ADMG()
    g.add_node("X")
    g.add_node("T")
    g.add_node("Y")
    g.add_directed_edge("T","Y")
    g.add_directed_edge("X","Y")

    g.add_birected_edge("T","X")
    g.add_birected_edge("Y","X")
    return g

def create_2_bow_3_v_nonid2():
    g = ADMG()
    g.add_node("X")
    g.add_node("T")
    g.add_node("Y")
    g.add_directed_edge("T","X")
    g.add_directed_edge("X","Y")

    g.add_birected_edge("T","Y")
    g.add_birected_edge("Y","X")
    return g

def create_2_bow_3_v_nonid3():
    g = ADMG()
    g.add_node("X")
    g.add_node("T")
    g.add_node("Y")
    g.add_directed_edge("X","T")
    g.add_directed_edge("T","Y")

    g.add_birected_edge("T","X")
    g.add_birected_edge("Y","X")
    return g

def create_1_bow():
    g = ADMG()
    g.add_node("T")
    g.add_node("Y")
    g.add_directed_edge("T","Y")

    g.add_birected_edge("T","Y")
    return g

def create_2_bow_4_v_nonid1():
    g = ADMG()
    g.add_node("X1")
    g.add_node("T")
    g.add_node("Y")
    g.add_node("X2")
    g.add_directed_edge("T","X1")
    g.add_directed_edge("X1","Y")
    g.add_directed_edge("X2","Y")

    g.add_birected_edge("X2","X1")
    g.add_birected_edge("T","X2")
    return g

def create_2_bow_4_v_id2():
    g = ADMG()
    g.add_node("X1")
    g.add_node("T")
    g.add_node("Y")
    g.add_node("X2")
    g.add_directed_edge("T","X1")
    g.add_directed_edge("X1","X2")
    g.add_directed_edge("X2","Y")
    g.add_directed_edge("X1","Y")
    g.add_directed_edge("T","Y")

    g.add_birected_edge("Y","X1")
    g.add_birected_edge("T","X2")
    return g

def create_4_bow_4_v_nonid2():
    g = ADMG()
    g.add_node("X1")
    g.add_node("T")
    g.add_node("Y")
    g.add_node("X2")
    g.add_directed_edge("X1","T")
    g.add_directed_edge("T","X2")
    g.add_directed_edge("X2","Y")

    g.add_birected_edge("X1","T")
    g.add_birected_edge("X1","X2")
    g.add_birected_edge("X1","Y")
    g.add_birected_edge("T","Y")
    return g

def create_4_bow_5_v():
    g = ADMG()
    g.add_node("X1")
    g.add_node("T")
    g.add_node("Y")
    g.add_node("X2")
    g.add_node("X3")
    g.add_directed_edge("X2","T")
    g.add_directed_edge("T","X1")
    g.add_directed_edge("X2","X1")
    g.add_directed_edge("X2","X3")
    g.add_directed_edge("X3","Y")
    g.add_directed_edge("X1","Y")

    g.add_birected_edge("T","X2")
    g.add_birected_edge("T","X3")
    g.add_birected_edge("T","Y")
    g.add_birected_edge("X2","Y")
    return g

def create_4_v_bug1():
    g = ADMG()
    g.add_node("X1")
    g.add_node("T")
    g.add_node("Y")
    g.add_node("X2")
    g.add_directed_edge("T","X1")
    g.add_directed_edge("X2","X1")
    g.add_directed_edge("X1","Y")

    g.add_birected_edge("T","Y")
    return g

def create_4_v_loss1():
    g = ADMG()
    g.add_node("X1")
    g.add_node("T")
    g.add_node("Y")
    g.add_node("X2")
    g.add_directed_edge("T","X2")
    g.add_directed_edge("X2","X1")
    g.add_directed_edge("T","Y")
    g.add_directed_edge("X1","Y")
    g.add_directed_edge("X2","Y")

    g.add_birected_edge("T","X1")
    return g

def create_4_v_loss2():
    g = ADMG()
    g.add_node("T")
    g.add_node("X2")
    g.add_node("X1")
    g.add_node("Y")
    g.add_directed_edge("T","X2")
    g.add_directed_edge("X2","Y")
    g.add_directed_edge("X1","Y")

    g.add_birected_edge("T","Y")
    g.add_birected_edge("X1","Y")
    # g.add_birected_edge("X1","X4")
    return g

def create_4_v_loss20():
    g = ADMG()
    g.add_node("T")
    g.add_node("X2")
    g.add_node("X1")
    g.add_node("Y")
    g.add_directed_edge("T","X1")
    g.add_directed_edge("X1","Y")
    g.add_directed_edge("X2","Y")

    g.add_birected_edge("T","X2")
    g.add_birected_edge("X2","Y")
    # g.add_birected_edge("X1","X4")
    return g
# --------------------many admg examples--------------------

# ----------------------2 VARIABLES----------------------
print("-----------------------2 variable cases-----------------------")
print("1 bow:")
# create ADMG,
g = create_1_bow() # line 5
# create probability,
p = ObservationProbability()
p.set_all(None, [], ["T","Y"], [], ["T","Y"])
# create causal query,
q = InterventionQuery()
q.set_all(g, ["Y"], ["T"], [], p, False)
# create identification algorithm, 
newid = ID()
try:
    # start identify the causal query, 
    identified_p = newid.id(q)
    # print the identification result, 
    print("identification result:\n",identified_p.get_latex_expression())
except Exception as e:
    print("identification result:\n",e)
    identified_p = None
# ----------------------2 VARIABLES----------------------

# ----------------------3 VARIABLES----------------------
graphs = [create_backdoor1(), create_backdoor2(), create_frontdoor(), 
         create_1_bow_3_v(), create_2_bow_3_v_nonid1(), create_2_bow_3_v_nonid2(), 
         create_2_bow_3_v_nonid3()]
graph_names = ["backdoor1", "backdoor2", "frontdoor",
            "1_bow_3_v", "2_bow_3_v_nonid1", "2_bow_3_v_nonid2", 
            "2_bow_3_v_nonid3"]
# g = create_backdoor1() # line 4->2->1 ; line 4->6
# g = create_backdoor2() # line 6
# g = create_frontdoor() # line 4->2->6 ; line 7->2->1
# g = create_1_bow_3_v() # line 4->2->5
# g = create_2_bow_3_v_nonid1() # line 5
# g = create_2_bow_3_v_nonid2() # line 5
# g = create_2_bow_3_v_nonid3() # line 3->5
print("-----------------------3 variable cases-----------------------")
for i, g in enumerate(graphs):
    print("--------------------------------------")
    print(f"{graph_names[i]}:")
    g.print()
    # create probability,
    p = ObservationProbability()
    p.set_all(None, [], ["X","T","Y"], [], ["X","T","Y"])
    # create causal query,
    q = InterventionQuery()
    q.set_all(g, ["Y"], ["T"], [], p, False)
    # create identification algorithm,
    newid = ID()
    try:
        # start identify the causal query, 
        identified_p = newid.id(q)
        # print the identification result,
        print("identification result:\n",identified_p.get_latex_expression())
    except Exception as e:
        print("identification result:\n",e)
        identified_p = None
    print("--------------------------------------")
print("------------------------------------------------------------")
# ----------------------3 VARIABLES----------------------

# ----------------------4 VARIABLES----------------------
graphs = [create_napkin(), create_2_bow_4_v_nonid1(), 
          create_2_bow_4_v_id2(), create_4_bow_4_v_nonid2(),
            create_4_v_bug1(), create_4_v_loss1(), create_4_v_loss2()]
graph_names = ["napkin", "2_bow_4_v_nonid1",
            "2_bow_4_v_id2", "4_bow_4_v_nonid2",
            "4_v_bug1", "4_v_loss1", "4_v_loss2"]
# g = create_napkin() # line 3->7->2->6
# g = create_2_bow_4_v_nonid1() # line 4->2->5
# g = create_2_bow_4_v_id2() # line 4->6; line 4->2->7->2->1
# g = create_4_bow_4_v_nonid2() # line 3->4->5
# g = create_4_v_bug1() #
# g = create_4_v_loss1() #
# g = create_4_v_loss2() # 4->2->6; ->7->2->1
print("-----------------------4 variable cases-----------------------")
for i, g in enumerate(graphs):
    print("--------------------------------------")
    print(f"{graph_names[i]}:")
    g.print()
    # create probability,
    p = ObservationProbability()
    p.set_all(None, [], ["X1","X2","T","Y"], [], ["X1","X2","T","Y"])
    # create causal query,
    q = InterventionQuery()
    q.set_all(g, ["Y"], ["T"], [], p, False)
    # create identification algorithm,
    newid = ID()
    try:
        # start identify the causal query, 
        identified_p = newid.id(q)
        # print the identification result,
        print("identification result:\n",identified_p.get_latex_expression())
    except Exception as e:
        print("identification result:\n",e)
        identified_p = None
    print("--------------------------------------")
# ----------------------4 VARIABLES----------------------

# ----------------------5 VARIABLES----------------------
print("-----------------------5 variable cases-----------------------")
graphs = [create_4_bow_5_v()]
graph_names = ["4_bow_5_v"]
# g = create_4_bow_5_v() # line 4->2->6; line 7->2->6; line 2->6
for i, g in enumerate(graphs):
    print("--------------------------------------")
    print(f"{graph_names[i]}:")
    g.print()
    # create probability,
    p = ObservationProbability()
    p.set_all(None, [], ["X1","X2","X3","T","Y"], [], ["X1","X2","X3","T","Y"])
    # create causal query,
    q = InterventionQuery()
    q.set_all(g, ["Y"], ["T"], [], p, False)
    # create identification algorithm,
    newid = ID()
    try:
        # start identify the causal query, 
        identified_p = newid.id(q)
        # print the identification result,
        print("identification result:\n",identified_p.get_latex_expression())
    except Exception as e:
        print("identification result:\n",e)
        identified_p = None
    print("--------------------------------------")
print("------------------------------------------------------------")
# # ----------------------5 VARIABLES----------------------

