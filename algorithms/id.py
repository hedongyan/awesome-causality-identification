import os
# import networkx as nx

def list_is(v,y):
    result=[]
    for i in v:
        if i in y:
            result.append(i)
    if len(result) == len(v):
        return True
    else:
        return False

def list_difference(v,y):
    result=[]
    for i in v:
        if i not in y:
            result.append(i)
    return result

# list in: b belong b_arr
def list_in(b, a_arr):
    b_in_a = False
    for a in a_arr:
        a_b = list_difference(a,b)
        b_a = list_difference(b,a)
        if len(a_b) == 0 and len(b_a) == 0:
            b_in_a = True
            break
    return b_in_a

# list union
def list_union(v,y):
    result=[]
    for i in v:
        if i not in result:
            result.append(i)
    for i in y:
        if i not in result:
            result.append(i)
    return result

# list minus
def list_minus(v,y):
    result=[]
    for i in v:
        if i not in y:
            result.append(i)
    return result
# list intersection
def list_intersection(v,y):
    result=[]
    for i in v:
        if i in y:
            result.append(i)
    return result


# directed edge, undirected edge, and node

# acyclic directed mixed graph

class ADMG:
    def __init__(self):
        self.node_names = []
        self.out_edges = {}
        self.in_edges = {}
        self.birected_edges = {}

    def add_node(self, name):
        if name in self.node_names:
            raise Exception("node name already exists: " + name)
        self.node_names.append(name)
    
    def add_nodes(self, names):
        for name in names:
            self.add_node(name)
    
    def exist_node_names(self, names):
        for name in names:
            if name not in self.node_names:
                return False
        return True

    def add_directed_edge(self, from_name, to_name):

        if self.exist_node_names([from_name, to_name]) == False:
            raise Exception("node name not in names")
        if from_name == to_name:
            raise Exception("from_name == to_name")
        
        if from_name not in self.out_edges:
            self.out_edges[from_name] = []
        if to_name not in self.out_edges[from_name]:
            self.out_edges[from_name].append(to_name)
        # else:
        #     raise Exception("edge already exists")
        
        if to_name not in self.in_edges:
            self.in_edges[to_name] = []
        if from_name not in self.in_edges[to_name]:
            self.in_edges[to_name].append(from_name)
        # else:
        #     raise Exception("edge already exists")
    
    def add_birected_edge(self, from_name, to_name):
        
        if self.exist_node_names([from_name, to_name]) == False:
            raise Exception("node name not in names")
        if from_name == to_name:
            raise Exception("from_name == to_name, self loop!")
        
        if from_name not in self.birected_edges:
            self.birected_edges[from_name] = []
        if to_name not in self.birected_edges:
            self.birected_edges[to_name] = []

        if to_name not in self.birected_edges[from_name] and from_name not in self.birected_edges[to_name]:
            self.birected_edges[from_name].append(to_name)
            self.birected_edges[to_name].append(from_name)
        # else:
        #     raise Exception("birected edge already exists")
    
    def print(self):
        print("node_names: ", self.node_names)
        print("out_edges: ", self.out_edges)
        print("in_edges: ", self.in_edges)
        print("birected_edges: ", self.birected_edges)
   
    def ancestors(self, names):
        if self.exist_node_names(names)==False:
            raise Exception("node name not in names")
        
        ancestors = []
        for name in names:
            ancestors.append(name)
            if name not in self.in_edges:
                continue
            for from_name in self.in_edges[name]:
                ancestors.append(from_name)
                ancestors += self.ancestors([from_name])
        
        no_repeat_ancestors = list(dict.fromkeys(ancestors))
        return no_repeat_ancestors
    
    def copy(self):
        newgraph = ADMG()
        for name in self.node_names:
            newgraph.add_node(name)
        for from_name in self.out_edges:
            for to_name in self.out_edges[from_name]:
                newgraph.add_directed_edge(from_name, to_name)
        for from_name in self.birected_edges:
            for to_name in self.birected_edges[from_name]:
                newgraph.add_birected_edge(from_name, to_name)
        return newgraph

    def induced_diagram(self, keep_nodes):
        ind_admg = ADMG()
        ind_admg.add_nodes(keep_nodes)
        
        for from_name in self.out_edges:
            if from_name in ind_admg.node_names:
                for to_name in self.out_edges[from_name]:
                    if to_name in ind_admg.node_names:
                        ind_admg.add_directed_edge(from_name, to_name)
        
        for from_name in self.birected_edges:
            if from_name in ind_admg.node_names:
                for to_name in self.birected_edges[from_name]:
                    if to_name in ind_admg.node_names:
                        ind_admg.add_birected_edge(from_name,to_name)
        return ind_admg

    def delete_directed_edge(self, from_name, to_name):
        if from_name not in self.out_edges:
            return
        if to_name not in self.out_edges[from_name]:
            return
        
        self.out_edges[from_name].remove(to_name)
        self.in_edges[to_name].remove(from_name)
        if len(self.out_edges[from_name]) == 0:
            del self.out_edges[from_name]
        if len(self.in_edges[to_name]) == 0:
            del self.in_edges[to_name]

    def delete_in_edge(self, to_names):
        for to_name in to_names:
            if to_name not in self.in_edges:
                return
            for from_name in self.in_edges[to_name]:
                self.delete_directed_edge(from_name, to_name)

    def get_confounded_components(self):
        components = []
        visited = {}
        for name in self.node_names:
            visited[name] = False
        for name in self.node_names:
            if not visited[name]:
                component = []
                self.get_confounded_components_visit(name, visited, component)
                components.append(component)
        return components
    
    def get_confounded_components_visit(self, name, visited, component):
        if visited[name]:
            return
        visited[name] = True
        component.append(name)
        if name not in self.birected_edges:
            return
        for to_name in self.birected_edges[name]:
            self.get_confounded_components_visit(to_name, visited, component) 
    


    def topological_sort(self):
        visited = {}
        for name in self.node_names:
            visited[name] = False
        sorted_names = []
        for name in self.node_names:
            if not visited[name]:
                self.topological_sort_visit(name, visited, sorted_names)
        
        return sorted_names
    
    def topological_sort_visit(self, name, visited, sorted_names):
        if visited[name]:
            return
        visited[name] = True
        if name not in self.in_edges:
            sorted_names.append(name)
            return
        for to_name in self.in_edges[name]:
            self.topological_sort_visit(to_name, visited, sorted_names)
        sorted_names.append(name)

    def sub_graph(self, indel, outdel):
        sub_admg = ADMG()
        for id in self.nodes:
            if id not in indel and id not in outdel:
                sub_admg.addnode(self.nodes[id].name, self.nodes[id].observable)
        for id in self.out_edges:
            if id not in indel:
                for to_id in self.out_edges[id]:
                    if to_id not in outdel:
                        sub_admg.adddirectededge(self.nodes[id].name, self.nodes[to_id].name)
        for id in self.birected_edges:
            if id not in indel:
                for to_id in self.birected_edges[id]:
                    if to_id not in outdel:
                        sub_admg.addbirectededge(self.nodes[id].name, self.nodes[to_id].name)
        return sub_admg

class InterventionQuery:
    def __init__(self):
        #  -----------------------data generating diagram -----------------------
        self.diagram = None
        self.variables = []

        # -----------------------original intervention probability expression-----------------------
        self.outcomes = []
        self.treatments = []
        self.covariates = []
        self.probability = None
        # -----------------------original intervention probability expression-----------------------
        
        # -----------------------identified observaion probability expression-----------------------
        self.identified = True
    
    def set_all(self, diagram, outcomes, treatments, covariates, probability, identified):
        self.set_intervention_query(diagram, outcomes, treatments, covariates)
        self.set_identified(identified)
        self.probability = probability

    def set_identified(self, identified):
        self.identified = identified

    def set_intervention_query(self, diagram, outcome_list, treatment_list, covariate_list):
        # data generating diagram
        self.set_diagram(diagram)
        self.set_variables(diagram.node_names)

        # intervention query
        self.set_outcomes(outcome_list)
        self.set_treatments(treatment_list)
        self.set_covariates(covariate_list)
    
    # -----------------------set intervention query-----------------------
    def set_diagram(self, diagram:ADMG):
        self.diagram = diagram.copy()
    
    def set_variables(self,variable_name_list):
        self.variables = variable_name_list[:]
    
    def set_covariates(self, variable_name_list):
        for covariate in variable_name_list:
            if covariate not in self.variables:
                raise Exception("covariate not in variables")
        self.covariates = variable_name_list[:]
    
    def set_outcomes(self, variable_name_list):
        for outcome in variable_name_list:
            if outcome not in self.variables:
                raise Exception("outcome not in variables")
        self.outcomes = variable_name_list[:]
        
    def set_treatments(self, variable_name_list):
        for treatment in variable_name_list:
            if treatment not in self.variables:
                raise Exception("treatment not in variables")
        self.treatments = variable_name_list[:]

class ObservationProbability:
    def __init__(self):
        # paraent probability
        self.parent_probability = None
        
        # all variables
        self.variables = []

        # marginalize out variables
        self.control_variable_list = []
    
        # product list
        self.numerator_product_list = []
        self.denominator_product_list = []

    def set_all(self, parent, control_list, numerator_product_list, denominator_product_list, variables):
        self.variables = variables[:]
        self.set_parent(parent)
        self.set_identified_probability(control_list, numerator_product_list, denominator_product_list)

    def set_parent(self, probability):
        self.parent_probability = probability
    
    def set_identified_probability(self, control_list, numerator_product_list, denominator_product_list):
        if len(control_list) > 0:
            self.set_controls(control_list)
        
        if len(numerator_product_list) > 0:
            self.numerator_product_list = numerator_product_list[:]
            self.denominator_product_list = denominator_product_list[:]
    
    # -----------------------set identified expression-----------------------
    def set_controls(self, variable_name_list):
        for control in variable_name_list:
            if control not in self.variables:
                raise Exception("control not in variables")
        self.control_variable_list = variable_name_list[:]

    def copy(self):
        new_prob = ObservationProbability()
        new_prob.set_all(self.parent_probability, self.control_variable_list, self.numerator_product_list, self.denominator_product_list, self.variables)
        return new_prob

    def get_latex_expression(self):
        # print("get_latex_expression")
        # print("numerator_product_list:", self.numerator_product_list)
        # print("denominator_product_list:", self.denominator_product_list)
        # Simplfy expression
        for numerator in self.numerator_product_list:
            for denominator in self.denominator_product_list:
                if numerator == denominator:
                    self.numerator_product_list.remove(numerator)
                    self.denominator_product_list.remove(denominator)
        # print(self.parent_probability)
        latex_expression = ""
        # if this probability is leaf node
        if self.parent_probability is None:
            latex_expression += "p(V)"
            # latex_expression += "p("
            # for name in self.variables:
            #     latex_expression += name + ","
            # # remove last comma
            # if len(self.variables) > 0:
            #     latex_expression = latex_expression[:-1]
            # latex_expression += ")"
            return latex_expression

        if len(self.control_variable_list) > 0: # control list start
            latex_expression += "\\sum_{"
            for name in self.control_variable_list:
                latex_expression += name + ","
            # remove last comma
            if len(self.control_variable_list) > 0:
                latex_expression = latex_expression[:-1]
            latex_expression += "}{"

        if len(self.denominator_product_list) > 0: # \frac{a}{b} start
            latex_expression += "\\frac{"
        
        if len(self.numerator_product_list) == 0: # a start
            latex_expression += self.parent_probability.get_latex_expression()

        for product_varibles in self.numerator_product_list: # numerator start
            # if numerators are not final product, numerators are some probabilities: line 4
            if type(product_varibles) == ObservationProbability:
                latex_expression += product_varibles.get_latex_expression() + "*"
                continue
            tmp_factor = ""
            if len(product_varibles) == len(self.parent_probability.variables):
                tmp_factor = ""
            elif len(product_varibles) > 0: # control start; use control to represent the factor
                tmp_factor += "\\sum_{"
                for name in product_varibles:
                    tmp_factor += name + ","
                # remove last comma
                if len(product_varibles) > 0:
                    tmp_factor = tmp_factor[:-1]
                tmp_factor += "}{"
            
            if self.parent_probability is not None:
                tmp_factor += self.parent_probability.get_latex_expression()
            if len(product_varibles) > 0 and len(product_varibles) != len(self.parent_probability.variables):# control end; use control to represent the factor
                tmp_factor += "}"
            if len(tmp_factor) > 0:
                latex_expression += tmp_factor + "*"
        # remove last *
        if len(self.numerator_product_list) > 0:
            latex_expression = latex_expression[:-1]
        
        if len(self.denominator_product_list) > 0: # numerator end
            latex_expression += "}"
        
        if len(self.denominator_product_list) > 0: # denominator start
            latex_expression += "{"
        
        for product_varibles in self.denominator_product_list: 
            tmp_factor = ""
            if len(product_varibles) == len(self.parent_probability.variables):
                tmp_factor = ""
            elif len(product_varibles) > 0:
                tmp_factor += "\\sum_{"
                for name in product_varibles:
                    tmp_factor += name + ","
                # remove last comma
                if len(product_varibles) > 0:
                    tmp_factor = tmp_factor[:-1]
                tmp_factor += "}{"
            if self.parent_probability is not None and len(product_varibles) != len(self.parent_probability.variables):
                tmp_factor += self.parent_probability.get_latex_expression()
            if len(product_varibles) > 0 and len(product_varibles) != len(self.parent_probability.variables):# control end; use control to represent the factor
                tmp_factor += "}"
            if len(tmp_factor) > 0:
                latex_expression += tmp_factor + "*"
        # remove last *
        if len(self.denominator_product_list) > 0:
            latex_expression = latex_expression[:-1]

        if len(self.denominator_product_list) > 0: # denominator end
            latex_expression += "}"

        if len(self.control_variable_list) > 0:        # control list end
            latex_expression += "}"
        return latex_expression
    
class ID:
    def __init__(self):
        self.hedge = []

    # Shpitser's algorithm shared 2006 best student paper with Huang's algprithm on UAI 2006
    # nodes list: y,t,v
    # probability: p(y|do(t))
    # graph: g
    def id(self, q:InterventionQuery):
        t = q.treatments
        y = q.outcomes
        v = q.variables
        g = q.diagram
        p = q.probability

        # print("begin ID")
        # print("t:",t)
        # print("y:",y)
        # print("v:",v)
        # q.diagram.print()

        # line 1
        if len(t)==0:
            print("line 1")
            return_p = ObservationProbability()
            posterior = [v]
            prior = []
            numerators = [list_minus(v, list_union(posterior, prior))]
            # print("numerators:", numerators)
            # print("variables:", v)
            return_p.set_all(p, list_minus(v, y), [], [], v)
            # print("line 1 returnp:",return_p.get_latex_expression())
            return return_p

        # line 2
        an_y = g.ancestors(y)
        if len(list_minus(v,an_y))>0:
            print("line 2")
            new_p = ObservationProbability()
            new_p.set_all(p, list_minus(v, an_y), [v], [], v)
            # print("line 2 return p",new_p.get_latex_expression())
            new_q = InterventionQuery()
            new_q.set_all(g.induced_diagram(an_y), y, list_intersection(t, an_y), [], new_p, False)#list_intersection(t, an_y), [], new_p, False)
            return self.id(new_q)
        
        # line 3
        p_do_t_diagram = g.copy()
        p_do_t_diagram.delete_in_edge(t)
        w = list_minus(list_minus(v,t),p_do_t_diagram.ancestors(y))
        if len(w) > 0:
            print("line 3")
            new_q = InterventionQuery()
            new_q.set_all(g, y, list_union(t, w), [], p, False)
            return self.id(new_q)

        # line 4
        # list: components
        ccomponents_of_g_minus_x = g.induced_diagram(list_minus(v,t)).get_confounded_components()
        # print("ccomponents_of_g_minus_x", ccomponents_of_g_minus_x)
        if len(ccomponents_of_g_minus_x) > 1:
            print("line 4")
            return_p = ObservationProbability()
            id_p_list = []
            for ccomponent in ccomponents_of_g_minus_x:
                # print("ccomponent:",ccomponent)
                # print("v:",list_minus(v,ccomponent))
                new_q = InterventionQuery()
                new_q.set_all(g, ccomponent, list_minus(v,ccomponent), [], p, False)
                id_p_list.append(self.id(new_q))
            # print(list_minus(v, list_union(y, t)))
            return_p.set_all(p, list_minus(v, list_union(y, t)), id_p_list, [], v)
            return return_p

        ccomponent_g_minus_x = ccomponents_of_g_minus_x[0]
        ccomponents_g = g.get_confounded_components()

        # line 5
        if len(ccomponents_g)==1:
            # print(ccomponents_g[0])
            # print(v)
            if list_is(ccomponents_g[0], v):
                print("line 5")
                raise Exception("failed")

        g_topological_sorts = g.topological_sort()
        print("g_topological_sorts:",g_topological_sorts)

        # line 6
        if list_in(ccomponent_g_minus_x, ccomponents_g):
            print("line 6")
            return_p = ObservationProbability()
            numerators = []
            denominators = []
            for vi in g_topological_sorts:
                if vi in ccomponent_g_minus_x:
                    posterior = [vi]
                    prior = g_topological_sorts[:g_topological_sorts.index(vi)]
                    numerators.append(list_minus(v, list_union(posterior, prior)))
                    denominators.append(list_minus(v, prior))
            # print("numerators:", numerators)
            # print("denominators:", denominators)
            return_p.set_all(p, list_minus(ccomponent_g_minus_x, y), numerators, denominators, v)
            # print("line 6 returnp:",return_p.get_latex_expression())
            return return_p
        
        # line 7
        # find s_tmp that ccomponent_g_minus_x real belong to s_tmp which is in ccomponents_g
        for s_tmp in ccomponents_g:
            if len(list_difference(s_tmp, ccomponent_g_minus_x)) > 0 and len(list_difference(ccomponent_g_minus_x, s_tmp)) == 0:
                print("line 7")
                new_q = InterventionQuery()
                numerators = []
                denominators = []
                g_s_tmp = g.induced_diagram(s_tmp)
                new_p = ObservationProbability()
                for vi in g_topological_sorts:
                    if vi in s_tmp:
                        posterior = [vi]
                        prior = g_topological_sorts[:g_topological_sorts.index(vi)]
                        numerators.append(list_minus(v, list_union(posterior, prior)))
                        denominators.append(list_minus(v, prior))
                new_p.set_all(p, [], numerators, denominators, s_tmp)
                new_q.set_all(g_s_tmp, y, list_intersection(t, s_tmp), [], new_p, False)
                return self.id(new_q)
        # raise Exception("failed")
        print("impossible!")
        os.system("pause")
        return p

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
    g.add_node("X1")
    g.add_node("X2")
    g.add_node("X3")
    g.add_node("X4")
    g.add_directed_edge("X1","X2")
    g.add_directed_edge("X2","X4")
    g.add_directed_edge("X3","X4")

    g.add_birected_edge("X1","X4")
    g.add_birected_edge("X3","X4")
    # g.add_birected_edge("X1","X4")
    return g

def create_4_v_loss20():
    g = ADMG()
    g.add_node("X1")
    g.add_node("X2")
    g.add_node("X3")
    g.add_node("X4")
    g.add_directed_edge("X1","X3")
    g.add_directed_edge("X3","X4")
    g.add_directed_edge("X2","X4")

    g.add_birected_edge("X1","X2")
    g.add_birected_edge("X2","X4")
    # g.add_birected_edge("X1","X4")
    return g
# ----------------------2 VARIABLES----------------------
# g = create_1_bow() # line 5
# p = ObservationProbability()
# p.set_all(None, [], ["T","Y"], [], ["T","Y"])
# ----------------------2 VARIABLES----------------------

# ----------------------3 VARIABLES----------------------
# g = create_backdoor1() # line 4->2->1 ; line 4->6
# g = create_backdoor2() # line 6
# g = create_frontdoor() # line 4->2->6 ; line 7->2->1
# g = create_1_bow_3_v() # line 4->2->5
# g = create_2_bow_3_v_nonid1() # line 5
# g = create_2_bow_3_v_nonid2() # line 5
# g = create_2_bow_3_v_nonid3() # line 3->5
# p = ObservationProbability()
# p.set_all(None, [], ["X","T","Y"], [], ["X","T","Y"])
# ----------------------3 VARIABLES----------------------

# ----------------------4 VARIABLES----------------------
# g = create_napkin() # line 3->7->2->6
# g = create_2_bow_4_v_nonid1() # line 4->2->5
# g = create_2_bow_4_v_id2() # line 4->6; line 4->2->7->2->1
# g = create_4_bow_4_v_nonid2() # line 3->4->5
# g = create_4_v_bug1() #
# g = create_4_v_loss1() #
g = create_4_v_loss2() # 4->2->6; ->7->2->1
p = ObservationProbability()
# p.set_all(None, [], ["X1","X2","T","Y"], [], ["X1","X2","T","Y"])
p.set_all(None, [], ["X1","X2","X3","X4"], [], ["X1","X2","X3","X4"])
# ----------------------4 VARIABLES----------------------

# ----------------------5 VARIABLES----------------------
# g = create_4_bow_5_v() # line 4->2->6; line 7->2->6; line 2->6
# p = ObservationProbability()
# p.set_all(None, [], ["X1","X2","X3","T","Y"], [], ["X1","X2","X3","T","Y"])
# # ----------------------5 VARIABLES----------------------


q = InterventionQuery()
# q.set_all(g, ["Y"], ["T"], [], p, False)
q.set_all(g, ["X4"], ["X1"], [], p, False)
newid = ID()
identified_p = newid.id(q)
print("identification result:\n",identified_p.get_latex_expression())


# checking all 4 variables#

# direct_edge = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
birected_edge = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
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

# import numpy as np
# total_admg = 0
# not_identifiable = 0
# identifiable = 0
# identified_results = []
# # for all direct edges
# for i in range(2**16):
#     tmp_direct_edge = bin(i)[2:].zfill(16)
#     tmp_direct_edge = np.array(list(map(int, tmp_direct_edge))).reshape(4,4)
#     if noselfLoop(tmp_direct_edge) is False:
#         continue
#     if isDirectedAcyclicGraph(tmp_direct_edge) is False:
#         continue
#     # g = create_graph(tmp_direct_edge, birected_edge, ["X1","X2","X3","X4"])
#     # x = g.topological_sort()
#     # print("topological sort:",x)
#     # print("direct edge:",noselfLoop(tmp_direct_edge))
#     # for all birected edges
#     for j in range(2**16):
#         # print(tmp_direct_edge)
#         tmp_birected_edge = bin(j)[2:].zfill(16)
#         tmp_birected_edge = np.array(list(map(int, tmp_birected_edge))).reshape(4,4)
#         # print(tmp_direct_edge)
#         if isBirected(tmp_birected_edge) is False \
#             or noselfLoop(tmp_birected_edge) is False:
#             continue
#         total_admg += 1
#         g = create_graph(tmp_direct_edge, tmp_birected_edge, ["X1","X2","X3","X4"])
#         p = ObservationProbability()
#         p.set_all(None, [], ["X1","X2","X3","X4"], [], ["X1","X2","X3","X4"])
#         q = InterventionQuery()
#         q.set_all(g, ["X4"], ["X1"], [], p, False)
#         newid = ID()
#         identifable = True
#         try:
#             identified_p = newid.id(q)
#             identifiable += 1
#             latexstr = identified_p.get_latex_expression()
#             # print(latexstr)
#             aa = r"\sum_{X2,X3}{\sum_{X1}{\frac{\sum_{X3,X4}{p(V)}*p(V)}{\sum_{X4}{p(V)}}}*\frac{\sum_{X2,X4}{p(V)}}{\sum_{X3}{\sum_{X2,X4}{p(V)}}}}"
#             if latexstr == aa:
#                 g.print()
#                 import os
#                 os.system("pause")
#             if latexstr not in identified_results:
#                 # print(latexstr)
#                 identified_results.append(latexstr)
#                 # print("\n")
#                 # print(identified_results)
#                 # print("not in")
#                 # print(latexstr)
#             # else:
#                 # print("already in")
#                 # print(latexstr)
#             # print("identification result:\n",identified_p.get_latex_expression())
#         except:     
#             # print("not identifiable")
#             not_identifiable += 1
#         print("total:",total_admg)
#         print("identifiable:",identifiable)
#         print("not identifiable:",not_identifiable)
    # print("total:",total_admg)
    # for ss in identified_results:
    #     print(ss)
    #     if identified_p.get_latex_expression() == "\\text{True}":
    #         print("direct edge:",direct_edge)
    #         print("birected edge:",birected_edge)
    #         print("identification result:\n",identified_p.get_latex_expression())
    #         print("\n")

# print("len(identified_results):",len(identified_results))
# identified_results = list(set(identified_results))
# print("len(identified_results):",len(identified_results))
# for ss in identified_results:
#     print(ss)
# print("total:",total_admg)
# print("identifiable:",identifiable)
# print("not identifiable:",not_identifiable)
# print("identifiable/total:",identifiable/total_admg)

# np.savetxt("identified_results.txt",identified_results,fmt="%s")



# import numpy as np
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
# import numpy as np
# # np.readtxt("identified_results.txt",dtype=str)
# expressions = np.loadtxt("identified_results.txt",dtype=str)
# for i in range(len(expressions)):
#     print(expressions[i])

#     parse_latex(repr(expressions[i]))
#     print(expressions[i])
# print("len(expressions):",len(expressions))
