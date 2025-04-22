# import networkx as nx
import os

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
        
        # check if the edge already exists
        # from_name = 1; to_name = 2 1->2
        # check 1->2 or 2->1 exists
        if to_name in self.birected_edges[from_name] or from_name in self.birected_edges[to_name]:
            return

        # if 1->2 not exists
        if to_name not in self.birected_edges[from_name]:
            self.birected_edges[from_name].append(to_name)
        # if 2->1 not exists
        if from_name not in self.birected_edges[to_name]:
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
    def delete_out_edge(self, from_names):
        for from_name in from_names:
            if from_name not in self.out_edges:
                return
            for to_name in self.out_edges[from_name]:
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

    # def sub_graph(self, indel, outdel):
    #     sub_admg = ADMG()
    #     for id in self.nodes:
    #         if id not in indel and id not in outdel:
    #             sub_admg.addnode(self.nodes[id].name, self.nodes[id].observable)
    #     for id in self.out_edges:
    #         if id not in indel:
    #             for to_id in self.out_edges[id]:
    #                 if to_id not in outdel:
    #                     sub_admg.adddirectededge(self.nodes[id].name, self.nodes[to_id].name)
    #     for id in self.birected_edges:
    #         if id not in indel:
    #             for to_id in self.birected_edges[id]:
    #                 if to_id not in outdel:
    #                     sub_admg.addbirectededge(self.nodes[id].name, self.nodes[to_id].name)
    #     return sub_admg
    
    # given t, test if y is d-separated from c given t
    # y, t, c are all node names
    def is_d_separated(self, y, t, c):
        # print("ddd seperated")
        G = nx.DiGraph()
        # print("ddd seperated")
        for name in self.node_names:
            # print("xxx")
            G.add_node(name)
        # print("ddd seperated")
        for from_name in self.out_edges:
            for to_name in self.out_edges[from_name]:
                G.add_edge(from_name, to_name)
        # print("ddd seperated")
        for from_name in self.birected_edges:
            for to_name in self.birected_edges[from_name]:
                # check if from_id is already in G
                new_name_1 = from_name + "_" + to_name
                new_name_2 = to_name + "_" + from_name
                if G.has_node(new_name_1) or G.has_node(new_name_2):
                    continue
                # create a new node
                new_node_name = from_name + "_" + to_name
                G.add_node(new_node_name)
                # add edges from new node to from_id and to_id
                G.add_edge(new_node_name, from_name)
                G.add_edge(new_node_name, to_name)
        # check if y is d-separated from c given t
        # print("ddddd")
        # print("g edge",G.edges())
        # print("y,c,t", y, c, t)
        # print("g node", G.nodes())
        # list to set
        y_set = set()
        for name in y:
            y_set.add(name)
        c_set = set()
        for name in c:
            c_set.add(name)
        t_set = set()
        for name in t:
            t_set.add(name)
        flag = nx.d_separated(G, y_set,c_set, t_set)
        # print("flag", flag)
        G.clear()
        return flag


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

        # idc2
        self.idc_2 = False
        self.y_list = []
    
    def set_idc_2(self, idc_2, y):
        self.idc_2 = idc_2
        self.y_list = y[:]

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
            return latex_expression

        # print("control_variable_list:", self.control_variable_list)
        if len(self.control_variable_list) > 0: # control list start
            latex_expression += "\\sum_{"
            for name in self.control_variable_list:
                latex_expression += name + ","
            # remove last comma
            if len(self.control_variable_list) > 0:
                latex_expression = latex_expression[:-1]
            latex_expression += "}{"

        # print("numerator_product_list:", self.numerator_product_list)
        # print("denominator_product_list:", self.denominator_product_list)
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
            if len(product_varibles) == len(self.parent_probability.variables) or len(product_varibles) == 0:
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
            if len(product_varibles) == len(self.parent_probability.variables) or len(product_varibles) == 0:
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
        
        # 
        if self.idc_2:
            tmp_factor = ""
            for name in self.y_list:
                tmp_factor += name + ","
            # remove last comma
            if len(self.y_list) > 0:
                tmp_factor = tmp_factor[:-1]
            latex_expression = "\\frac{" + latex_expression + "}"+ \
                "{" + "\\sum_{" + tmp_factor + "}{" + latex_expression + "}" + "}"
            "" + "}" + latex_expression + "}"
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
        q.diagram.print()

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
        # print("ancestor y",an_y)
        # print("v",v)
        print(list_minus(v,an_y))
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
        # print("v:",v)
        # print("t:",t)
        # print("v-t:",list_minus(v,t))
        # print("v:",p_do_t_diagram.ancestors(y))
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
        # print("g_topological_sorts:",g_topological_sorts)

        # line 6
        # print("ccomponent_g_minus_x:",ccomponent_g_minus_x)
        # print("ccomponents_g:",ccomponents_g)
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

class IDC:
    def __init__(self):
        self.hedge = []
        self.flag=False

    # def get_latex_expression(self):
    #     if self.flag:
    #         self.

    # Shpitser's algorithm on UAI 2006
    # nodes list: y,t,v
    # probability: p(y|do(t),x)
    # graph: g
    def id(self, q:InterventionQuery):
        # print("IDC")
        t = q.treatments
        y = q.outcomes
        c = q.covariates
        v = q.variables
        g = q.diagram
        p = q.probability

        # line 1
        # print("line 1")
        p_do_t_mute_z_diagram = g.copy()
        # print("p_do_t_mute_z_diagram:")
        p_do_t_mute_z_diagram.delete_in_edge(t)
        # print("p_do_t_mute_z_diagram:")
        p_do_t_mute_z_diagram.delete_out_edge(c)
        # print("........................................")
        # print("p_do_t_mute_z_diagram:")
        is_d_separated = p_do_t_mute_z_diagram.is_d_separated(y, t, c)
        # print("is_d_separated:",is_d_separated)
        if is_d_separated and len(c)>0:
            print("idc line 1")
            new_t = list_union(t, c)
            new_p = ObservationProbability()
            new_p.set_all(p, [], [v], [], v)
            new_q = InterventionQuery()
            new_q.set_all(g, y, new_t, [], new_p, False)
            return self.id(new_q)
        
        # line 2
        flag = True
        print("idc line 2")
        id = ID()
        new_q = InterventionQuery()
        new_q.set_all(g, list_union(y,c), t, [], p, False)
        p_result = id.id(new_q)
        p_result.set_idc_2(True, y=y)
        print("p_result:",p_result.get_latex_expression())
        print("mention!")
        # de_p_result = p_result.copy()
        # de_p_result.set_all(p_result, y, v, [], v)
        # # p_result_denominator = p_result.copy()
        # # p_result_numerator = p_result.copy()
        # # p_result_denominator.set_all(p_result, [y], [v], [], v)
        # new_p = ObservationProbability()
        # print("v,y,c:",v,y,c)
        # new_p.set_all(p_result, y, [], [], v)
        # print("new_p",new_p.get_latex_expression())
        return p_result

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

def create_graph():
    g = ADMG()
    g.add_node("X")
    g.add_node("Y")
    g.add_node("T")

    g.add_directed_edge("T","Y")
    # g.add_directed_edge("T","X")
    g.add_directed_edge("X","T")
    # g.add_directed_edge("Y","X")
    # g.add_directed_edge("X","Y")

    # g.add_birected_edge("T","X")
    # g.add_birected_edge("T","Y")
    # g.add_birected_edge("X","Y")
    return g
# -------IDENTIFY IDC---------------
# Order: X->T, X->Y, T->X, T->Y, Y->X, Y->T
directed_edges_list = [  [],[('T','Y')],[('Y','T')],[('T','X')],[('X','T')],[('Y','X')],[('X','Y')],
                    [('T','X'),('X','Y')],[('T','Y'),('Y','X')],[('Y','T'),('X','Y')],
                    [('X','T'),('T','Y')],[('T','X'),('Y','T')],[('X','T'),('Y','X')],
                    [('T','X'),('T','Y')],[('X','T'),('X','Y')],
                    [('Y','T'),('Y','X')],[('X','T'),('Y','T')],[('T','X'),('Y','X')],[('T','Y'),('X','Y')],
                    [('X','T'),('X','Y'),('T','Y')],[('X','T'),('X','Y'),('Y','T')],
                    [('T','X'),('T','Y'),('X','Y')],[('T','X'),('T','Y'),('Y','X')],
                    [('X','T'),('Y','T'),('Y','X')],[('T','X'),('Y','T'),('Y','X')]]

directed_edges_name_list =['000000','000100','000001','001000','100000','000010','010000',
                            '011000','000110','010001',
                            '100100','001001','100010','001100','110000',
                            '000011','100001','001010','010100',
                            '110100','110001',
                            '011100','001110',
                            '100011','001011']

# Order: T<->X, X<->Y, Y<->T
bidirected_edges_list = [   [],
                            [('X','Y')],[('T','X')],[('Y','T')],
                            [('X','Y'),('T','X')],[('X','Y'),('Y','T')],[('T','X'),('Y','T')],
                            [('X','Y'),('T','X'),('Y','T')]]

bidirected_edges_name_list = ['000','010','100','001',
                            '110','011','101','111']

def create_graph_3(directed_edges,bidirected_edges):
    g = ADMG()
    g.add_node("X")
    g.add_node("Y")
    g.add_node("T")

    for i in range(len(directed_edges)):
        g.add_directed_edge(directed_edges[i][0],directed_edges[i][1])

    for i in range(len(bidirected_edges)):
        g.add_birected_edge(bidirected_edges[i][0],bidirected_edges[i][1])

    return g

not_identified = 0
identified = 0
identified_results = []
saved_results=[
r"\frac{\sum_{X,T}{p(V)}}{\sum_{Y}{\sum_{X,T}{p(V)}}}",
r"\frac{\sum_{T}{p(V)}}{\sum_{Y}{\sum_{T}{p(V)}}}",
r"\frac{\frac{\sum_{X}{p(V)}}{\sum_{Y}{\sum_{X}{p(V)}}}}{\sum_{Y}{\frac{\sum_{X}{p(V)}}{\sum_{Y}{\sum_{X}{p(V)}}}}}",
r"\frac{\frac{\sum_{Y,T}{p(V)}*p(V)}{\sum_{Y}{p(V)}}}{\sum_{Y}{\frac{\sum_{Y,T}{p(V)}*p(V)}{\sum_{Y}{p(V)}}}}",
r"\frac{\frac{p(V)}{\sum_{X,Y}{p(V)}}}{\sum_{Y}{\frac{p(V)}{\sum_{X,Y}{p(V)}}}}",
r"\frac{\frac{\sum_{T}{p(V)}}{\sum_{Y}{\sum_{T}{p(V)}}}}{\sum_{Y}{\frac{\sum_{T}{p(V)}}{\sum_{Y}{\sum_{T}{p(V)}}}}}",
r"\frac{\frac{p(V)}{\sum_{Y}{p(V)}}}{\sum_{Y}{\frac{p(V)}{\sum_{Y}{p(V)}}}}",
r"\frac{\sum_{T}{\frac{\sum_{X,Y}{p(V)}*p(V)}{\sum_{Y}{p(V)}}}}{\sum_{Y}{\sum_{T}{\frac{\sum_{X,Y}{p(V)}*p(V)}{\sum_{Y}{p(V)}}}}}",
r"\frac{\frac{p(V)}{\sum_{X}{p(V)}}*\frac{\sum_{X}{p(V)}}{\sum_{Y}{\sum_{X}{p(V)}}}}{\sum_{Y}{\frac{p(V)}{\sum_{X}{p(V)}}*\frac{\sum_{X}{p(V)}}{\sum_{Y}{\sum_{X}{p(V)}}}}}",
r"\frac{\sum_{T}{\frac{\sum_{X,Y}{p(V)}*p(V)}{\sum_{X}{p(V)}}}*\frac{\sum_{X}{p(V)}}{\sum_{Y}{\sum_{X}{p(V)}}}}{\sum_{Y}{\sum_{T}{\frac{\sum_{X,Y}{p(V)}*p(V)}{\sum_{X}{p(V)}}}*\frac{\sum_{X}{p(V)}}{\sum_{Y}{\sum_{X}{p(V)}}}}}",
r"\frac{\frac{\sum_{X,T}{p(V)}*p(V)}{\sum_{X}{p(V)}}}{\sum_{Y}{\frac{\sum_{X,T}{p(V)}*p(V)}{\sum_{X}{p(V)}}}}",
r"\frac{\frac{p(V)}{\sum_{X}{p(V)}}*\sum_{X,T}{p(V)}}{\sum_{Y}{\frac{p(V)}{\sum_{X}{p(V)}}*\sum_{X,T}{p(V)}}}"]

simplified_results = [
    r"\(p(Y)\)",
    r"\(p(Y|X)\)",
    r"\(p(Y|T)\)",
    r"\(p(Y|X,T)\)",
    r"\(p(Y|X,T)\)",
    r"\(p(Y|X)\)",
    r"\(p(Y|X,T)\)",
    r"\(\sum_{t\in\mathcal{T}}p(t)p(Y|X,t)\)",
    r"\(p(Y|X,T)\)",
    r"\(p(Y|X)\)",
    r"\(\frac{p(Y)p(X|Y,T)}{\sum_{y\in\mathcal{Y}}{p(y)p(X|y,T)}}\)",
    r"\(\frac{p(Y)p(X|Y,T)}{\sum_{y\in\mathcal{Y}}{p(y)p(X|y,T)}}\)"]



# PRINT ALL POSSIBLE IDENTIFICATION SCENARIOS
all_identification_scenarios = []
for i in range(len(directed_edges_list)):
    for j in range(len(bidirected_edges_list)):
        # print(directed_edges_name_list[i],bidirected_edges_name_list[j])
        g = create_graph_3(directed_edges_list[i],bidirected_edges_list[j])
        # g.print()
        p = ObservationProbability()
        p.set_all(None, [], ["X","T","Y"], [], ["X","T","Y"])
        q = InterventionQuery()
        q.set_all(g, ["Y"], ["T"], ['X'], p, False)
        newidc = IDC()
        # identification
        # print("identification")
        try:
            identified_p = newidc.id(q)
            latexstr = identified_p.get_latex_expression()
            # print(latexstr)
            identified += 1
            if latexstr in saved_results:
                new_str = simplified_results[saved_results.index(latexstr)]
                all_identification_scenarios.append(new_str)
                if new_str not in identified_results:
                    identified_results.append(new_str)
                # identified_results.append(latexstr)
            # if latexstr not in identified_results:
            #     identified_results.append(latexstr)
        except:
            # print("ERROR")
            not_identified += 1
            all_identification_scenarios.append("Not Identifiable")

for i in range(len(all_identification_scenarios)):
    # every 8 elements, print a new line
    if i % 8 == 0:
        print("------------------",int(i/8)+1,"------------------")
    print(all_identification_scenarios[i])

# print("identified",identified)
# print("not identified",not_identified)
# for i in range(len(identified_results)):
#     print(identified_results[i])
        

# g=create_graph()
# p = ObservationProbability()
# p.set_all(None, [], ["X","T","Y"], [], ["X","T","Y"])
# q = InterventionQuery()
# q.set_all(g, ["Y"], ["T"], ['X'], p, False)
# newidc = ID()
# identifable = True
# # identification
# print("identification")
# identified_p = newidc.id(q)
# latexstr = identified_p.get_latex_expression()
# print(latexstr)

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
# g = create_4_v_loss2() # 4->2->6; ->7->2->1
# p = ObservationProbability()
# p.set_all(None, [], ["X1","X2","T","Y"], [], ["X1","X2","T","Y"])
# p.set_all(None, [], ["X1","X2","X3","X4"], [], ["X1","X2","X3","X4"])
# ----------------------4 VARIABLES----------------------

# ----------------------5 VARIABLES----------------------
# g = create_4_bow_5_v() # line 4->2->6; line 7->2->6; line 2->6
# p = ObservationProbability()
# p.set_all(None, [], ["X1","X2","X3","T","Y"], [], ["X1","X2","X3","T","Y"])
# # ----------------------5 VARIABLES----------------------

# ----------------------identification----------------------
# q = InterventionQuery()
# # q.set_all(g, ["Y"], ["T"], [], p, False)
# q.set_all(g, ["X4"], ["X1"], [], p, False)
# newid = ID()
# identified_p = newid.id(q)
# print("identification result:\n",identified_p.get_latex_expression())
# ----------------------identification----------------------



# chacking all 3 variables
direct_edge = [[0,0,0],[0,0,0],[0,0,0]]
birected_edge = [[0,0,0],[0,0,0],[0,0,0]]
n_nodes = 3

# direct_edge = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
# birected_edge = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
def create_graph(direct_edge, birected_edge, name):
    g = ADMG()
    for i in range(n_nodes):
        g.add_node(name[i])
    for i in range(n_nodes):
        for j in range(n_nodes):
            if direct_edge[i][j] == 1:
                g.add_directed_edge(name[i],name[j])
            if birected_edge[i][j] == 1:
                g.add_birected_edge(name[i],name[j])
    return g

def noselfLoop(direct_edges):
    for i in range(n_nodes):
        if direct_edges[i][i] == 1:
            return False
    return True

def isBirected(birected_edges):
    for i in range(n_nodes):
        for j in range(n_nodes):
            if birected_edges[i][j] == 1 and birected_edges[j][i] == 0:
                return False
    return True

def isDirectedAcyclicGraph(direct_edges):
    g = nx.DiGraph()
    for i in range(n_nodes):
        for j in range(n_nodes):
            if direct_edges[i][j] == 1:
                g.add_edge(i,j)
    return nx.is_directed_acyclic_graph(g)


# # ------------------------------------------checking all 3 variables------------------------------------------
# import numpy as np
# total_admg = 0
# not_identifiable = 0
# identifiable = 0
# identified_results = []
# # for all direct edges
# edge_n = 3*3
# for i in range(2**edge_n): # 3*3
#     tmp_direct_edge = bin(i)[2:].zfill(edge_n)
#     tmp_direct_edge = np.array(list(map(int, tmp_direct_edge))).reshape(n_nodes,n_nodes)
#     if noselfLoop(tmp_direct_edge) is False:
#         continue
#     if isDirectedAcyclicGraph(tmp_direct_edge) is False:
#         continue
#     # g = create_graph(tmp_direct_edge, birected_edge, ["X1","X2","X3","X4"])
#     # x = g.topological_sort()
#     # print("topological sort:",x)
#     # print("direct edge:",noselfLoop(tmp_direct_edge))
#     # for all birected edges
#     for j in range(2**edge_n): # 3*3
#         tmp_birected_edge = bin(j)[2:].zfill(edge_n)
#         tmp_birected_edge = np.array(list(map(int, tmp_birected_edge))).reshape(3,3)
#         # print(tmp_direct_edge)
#         if isBirected(tmp_birected_edge) is False \
#             or noselfLoop(tmp_birected_edge) is False:
#             continue
#         # print("direct",tmp_direct_edge)
#         # print("birected",tmp_birected_edge)
#         total_admg += 1
#         g = create_graph(tmp_direct_edge, tmp_birected_edge, ["X","T","Y"])
#         # print(g.is_d_separated('X','Y','T'))
#         p = ObservationProbability()
#         p.set_all(None, [], ["X","T","Y"], [], ["X","T","Y"])
#         q = InterventionQuery()
#         q.set_all(g, ["Y"], ["T"], ['X'], p, False)
#         newidc = IDC()
#         identifable = True
#         # identification
#         try:
#             print("identification")
#             identified_p = newidc.id(q)
#             identifiable += 1
#             latexstr = identified_p.get_latex_expression()
#             g.print()
#             print("identification result:\n",latexstr)
#             import os
#             os.system("pause")
#             # print(latexstr)
#             # aa = r"\frac{\sum_{X,T}{p(V)}*p(V)}{\sum_{X}{p(V)}}"
#             # if latexstr == aa:
#             #     g.print()
#             #     import os
#             #     os.system("pause")
#             # if latexstr not in identified_results:
#             #     # print(latexstr)
#             #     identified_results.append(latexstr)
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
#     #     print("total:",total_admg)
#     #     print("identifiable:",identifiable)
#     #     print("not identifiable:",not_identifiable)
#     # print("total:",total_admg)
#     for ss in identified_results:
#         print(ss)
#         if identified_p.get_latex_expression() == "\\text{True}":
#             print("direct edge:",direct_edge)
#             print("birected edge:",birected_edge)
#             print("identification result:\n",identified_p.get_latex_expression())
#             print("\n")

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
# #------------------------------------------checking all 3 variables------------------------------------------



# ------------------------------------------checking all 4 variables------------------------------------------
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
# ------------------------------------------checking all 4 variables------------------------------------------
