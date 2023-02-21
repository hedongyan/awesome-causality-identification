
import torch
import torch.distributions as dist

# structure causal model
class SCM:
    def __init__(self, observed_node_names: list, confounded_cliques: list, observed_parents_dict: dict):  
        # --------------------------------------names/keys of variables and mechanisms--------------------------------------start

        # --------------variable name--------------start
        # Name: observed_node_names
        # Type: list
        # Example: ['X', 'Y', 'T']
        # Note: 
        #   observed variable names
        #   no symbol "->" in all node names
        self.observed_node_names = []

        # Name: hidden_node_names
        # Type: dict
        # Example: {'Z1':['X1','X2'], 'Z2':['X','T','Y']}
        # Note: 
        #   common causes clique (sub complete graph) between observed variables
        #   no redundant clique, for example, if Z1=['X1','X2'] and Z2=['X1','X2','X3'], then Z1 is redundant
        #   no symbol "->" in all node names
        self.hidden_node_names = {}
        
        self.all_node_names = []

        # Name: treatment_node_names
        # Type: list
        # Example: ['T']
        # Note:
        #   treatment variable names
        # self.treatment_node_names = []

        # Name: outcome_node_names
        # Type: list
        # Example: ['Y']
        # Note:
        #   outcome variable names
        # self.outcome_node_names = []

        # Name: pre_treat_node_names
        # Type: list
        # Example: ['X1', 'X2']
        # Note:
        #   pre-treatment variable names, including observed and hidden variables
        # self.pre_treat_node_names = []

        # Name: post_treat_node_names
        # Type: list
        # Example: ['X1', 'X2']
        # self.post_treat_node_names = []
        # --------------variable name--------------end
        
        # --------------mechanism names--------------start
        # Name: hidden_mechanism_names
        # Type: dict
        # Example: {'Z1->X1': ['Z1','X1'], 'Z1->X2': ['Z1','X2'], 'Z2->X': ['Z2','X'], 'Z2->T': ['Z2','T'], 'Z2->Y': ['Z2','Y']}
        # Note:
        #   hidden mechanism names
        #   all hidden mechanisms are pre-treatment mechanisms
        self.hidden_mechanism_names = {}

        # Name: observed_mechanism_names
        # Type: dict
        # Example: {'X->T': ['X','T'], 'Y->X': ['Y','X']}
        # Note:
        #   observed mechanism names
        self.observed_mechanism_names = {}

        # Name: fusion_mechanism_names
        # Type: list
        # Example: ['X','T','Y']
        # Note:
        #   fusion mechanism names
        #   every variable has a fusion mechanism
        #   fusion mechanism is a mechanism whose input is processed parent values and output is the value of this variable
        self.fusion_mechanism_names = []

        # Name: pre_treat_mechanism_names
        # Type: dict
        # Example: {'Z1->X1': ['Z1','X1']}
        # Note:
        #   pre-treatment mechanism names, including observed and hidden mechanisms
        # self.pre_treat_mechanism_names = {}

        # Name: post_treat_mechanism_names
        # Type: dict
        # Example: {'Z1->X1': ['Z1','X1']}
        # Note:
        #   post-treatment mechanism names, including observed and hidden mechanisms
        # self.post_treat_mechanism_names = {}
        # --------------mechanism names--------------end
        
        # --------------------------------------names/keys of variables and mechanisms--------------------------------------end


        # --------------------------------------distributions of hidden variables and independent observed variables--------------------------------------start
        # Name: hidden_distributions
        # Type: dict
        # Example: {'Z1': Bernoulli(probs: tensor([0.5000])), 'Z2': Bernoulli(probs: tensor([0.5000]))}
        # Note: 
        #   hidden variable distributions
        #   all hidden distributions are pre-treatment distributions
        self.hidden_distributions = {}
        # --------------------------------------distributions of hidden variables and independent observed variables--------------------------------------end


        # --------------------------------------mechanisms--------------------------------------
        
        # --------------mechanisms--------------start
        # Name: hidden_mechanisms
        # Type: dict
        # Example: {'Z1->X1': lambda Z1: 2*Z1}
        # Note:
        #   hidden mechanism functions
        #   all hidden mechanisms are pre-treatment mechanisms
        self.hidden_mechanisms = {}

        # Name: observed_mechanisms
        # Type: dict
        # Example: {'X->T': lambda X: 2*X}
        # Note:
        #   observed mechanism functions
        self.observed_mechanisms = {}

        # Name: fusion_mechanisms
        # Type: dict
        # Example: {'X': lambda X, T: 2*X-2*T}
        # Note:
        #   fusion mechanism functions
        #   every variable has a fusion mechanism
        #   fusion mechanism is a mechanism whose input is processed parent values and output is the value of this variable
        self.fusion_mechanisms = {}
        self.all_mechanism_names = {}
        self.all_mechanisms = {}

        # Name: pre_treat_mechanisms
        # Type: dict
        # Example: {'Z1->X1': lambda Z1: 2*Z1}
        # Note:
        #   pre-treatment mechanism functions, including observed and hidden mechanisms
        # self.pre_treat_mechanisms = {}

        # Name: post_treat_mechanisms
        # Type: dict
        # Example: {'Z1->X1': lambda Z1: 2*Z1}
        # Note:
        #   post-treatment mechanism functions, including observed and hidden mechanisms
        # self.post_treat_mechanisms = {}

        # --------------mechanism names--------------end

        # --------------------------------------mechanisms--------------------------------------end

        # --------------------------------------set names--------------------------------------start
        self.set_names(observed_node_names, confounded_cliques, observed_parents_dict)
        # --------------------------------------set names--------------------------------------end

        # --------------------------------------set parameters--------------------------------------start
        self.set_parameters()
        # --------------------------------------set mechanism functions--------------------------------------end

    
    # --------------------------------------set name functions--------------------------------------start
    # Input Example:
    #   observation_node_names = ['X', 'Y', 'T']
    #   confounded_cliques = [['X', 'Y'], ['T']]
    #   observed_parents = {'T': None, 'X': ['T'], 'Y': ['X', 'T']}
    # Output Example:
    #   self.observed_node_names = ['X', 'Y', 'T']
    #   self.hidden_node_names = {'(X,Y)': ['X', 'Y'], '(T)': ['T']}
    #   self.all_node_names = ['X', 'Y', 'T', '(X,Y)', '(T)']
    #   self.hidden_mechanism_names = {'(X,Y)->X': ['(X,Y)', 'X'], '(X,Y)->Y': ['(X,Y)', 'Y'], '(T)->T': ['(T)', 'T']}
    #   self.observed_mechanism_names = {'T->X': ['T', 'X'], 'X->Y': ['X', 'Y'], 'T->Y': ['T', 'Y']}
    #   self.fusion_mechanism_names = {'T': ['(T)'], 'X': ['(X,Y)', 'T'], 'Y': ['X', 'T', '(X,Y)'], '(X,Y)': None, '(T)': None}
    def set_names(self, observed_node_names: list, confounded_cliques: list, observed_parents_dict: dict):
        # set node names
        self.observed_node_names = observed_node_names.copy()
        for nodes in confounded_cliques:
            name = "("
            for node in nodes:
                name += node + ','
            name = name[:-1] + ")"
            self.hidden_node_names[name] = nodes.copy()
        self.all_node_names = self.observed_node_names.copy() + list(self.hidden_node_names.keys())
        print("self.all_node_names: ", self.all_node_names)
        # set mechanism names
        for hidden_parent in self.hidden_node_names: # hidden_node_names is a dict: {'X<->T': ['X', 'T']}
            for observed_node in self.hidden_node_names[hidden_parent]:
                self.hidden_mechanism_names[hidden_parent + '->' + observed_node] = [hidden_parent, observed_node]
        for (node, observed_parents) in observed_parents_dict.items(): 
            for parent in observed_parents:
                self.observed_mechanism_names[parent + '->' + node] = [parent, node]
        
        for node in self.all_node_names:
            if node in self.observed_node_names:
                self.fusion_mechanism_names.append(node)
        # print("self.fusion_mechanism_names: ", list(self.fusion_mechanism_names.keys()))
        # print("self.hidden_mechanism_names: ", self.hidden_mechanism_names)
        # print("self.observed_mechanism_names: ", self.observed_mechanism_names)
        self.all_mechanism_names = list(self.hidden_mechanism_names.keys()) + list(self.observed_mechanism_names.keys()) + self.fusion_mechanism_names.copy()
        print("self.all_mechanism_names: ", self.all_mechanism_names)
    
    # Input Example:
    #   distributions: dict, {'Z1': dist.Bernoulli(torch.tensor([0.5])), 'Z2': dist.Bernoulli(torch.tensor([0.5]))}
    #   fusion_mechanisms: dict, {'X': lambda X, T: 2*X-2*T}
    #   hidden_mechanisms: dict, {'Z1->X1': lambda Z1: 2*Z1}
    #   observed_mechanisms: dict, {'Z1->X1': lambda Z1: 2*Z1}
    #   fusion_mechanism: dict, {'Z1->X1': lambda Z1: 2*Z1}
    # Output Example:
    #   self.hidden_distributions: dict, {'Z1': dist.Bernoulli(torch.tensor([0.5])), 'Z2': dist.Bernoulli(torch.tensor([0.5]))}
    #   self.fusion_mechanisms: dict, {'X': lambda X, T: 2*X-2*T}
    #   self.hidden_mechanisms: dict, {'Z1->X1': lambda Z1: 2*Z1}
    #   self.observed_mechanisms: dict, {'Z1->X1': lambda Z1: 2*Z1}
    def set_parameters(self, distributions: dict = None, fusion_mechanisms: dict = None, hidden_mechanisms: dict = None, observed_mechanisms: dict = None):
        # set hidden distributions (including hidden variables and independent variables)
        for hidden_node in self.hidden_node_names:
            z_dist = distributions[hidden_node] if distributions is not None else dist.Bernoulli(torch.tensor([0.5]))
            self.hidden_distributions[hidden_node] = z_dist
        # set mechanisms
        for key in self.all_mechanism_names:
            # for hidden mechanisms
            if key in self.hidden_mechanism_names:
                self.hidden_mechanisms[key] = hidden_mechanisms[key] if hidden_mechanisms is not None else lambda x: 2 * x + 1
            # for observed mechanisms
            elif key in self.observed_mechanism_names:
                self.observed_mechanisms[key] = observed_mechanisms[key] if observed_mechanisms is not None else lambda x: x + 1.5
            # for fusion mechanisms
            elif key in self.fusion_mechanism_names:
                self.fusion_mechanisms[key] = fusion_mechanisms[key] if fusion_mechanisms is not None else lambda x: sum(x) + 0.5
            else:
                raise Exception("Error: no mechanism named " + key)
        self.all_mechanisms = self.hidden_mechanisms.copy()
        self.all_mechanisms.update(self.observed_mechanisms)
        self.all_mechanisms.update(self.fusion_mechanisms)
        # print("all_mechanisms: ", self.all_mechanisms)
        # print("self.hidden_distributions: ", self.hidden_distributions)
        # print("self.fusion_mechanisms: ", self.fusion_mechanisms)
        # print("self.hidden_mechanisms: ", self.hidden_mechanisms)
    # --------------------------------------sampling functions--------------------------------------start   
    # Input: 
    #   n_samples: the number of samples, for example, 5
    #   variables_sampled: a dict: {'X': False, 'Y': False}
    #   mechanisms: a dict: {'X<->Y->X': ['X<->Y', 'X'], 'X<->Y->Y': ['X<->Y', 'Y']}
    # Output:
    #  observed_data: a dict: {'X': [1.3, 2.1, -0.2, 4, 5], 'Y': [0.1, 0.2, 0.3, 0.4, 0.5]}
    #  hidden_data: a dict: {'X<->Y': [0, 1, 1, 0, 1]}
    # Note:
    #   sampling
    #   this is a start function
    def sampling(self, n_samples):
        observed_data = {}
        hidden_data = {}
        variables_sampled = {}
        for i in range(n_samples):
            # initialize variables_sampled as False
            for key in self.all_node_names:
                variables_sampled[key] = False
            # sampling a data point
            data, variables_sampled = self.recusive_one_sample({}, variables_sampled)
            # classify data into observed_data and hidden_data
            for key in data:
                if key in self.observed_node_names:
                    if key not in observed_data:
                        observed_data[key] = []
                    observed_data[key].append(data[key])
                else:
                    if key not in hidden_data:
                        hidden_data[key] = []
                    hidden_data[key].append(data[key])
        return observed_data, hidden_data

    # Input:
    #   data: a dict: {'X<->Y': 0.2, 'X': None, 'Y': None}
    #   variables_sampled: a dict: {'X<->Y': True, 'X': False, 'Y': False}
    #   mechanisms: a dict: ('X<->Y', 'X'): function, ('X<->Y', 'Y'): function, ('X', 'Y'): function}
    # Output:
    #   data: a dict: {'X<->Y': 0.2, 'X': 1.3, 'Y': None}
    #   variables_sampled: a dict: {'X<->Y': True, 'X': True, 'Y': 0.1}
    #   mechanisms: the same as input
    # Note:
    #   this is a recursive function
    def recusive_one_sample(self, data, variables_sampled):
        while True:
            for variable in variables_sampled:
                # if this variable has been sampled, then we continue
                if variables_sampled[variable] == True:
                    continue
                # if this variable is a hidden variable or an independent observed variable then we sample it by its own distribution
                if variable in self.hidden_distributions:
                    data[variable] = self.hidden_distributions[variable].sample()
                    variables_sampled[variable] = True
                    continue
                
                # if this variable is an observed variable, then we sample it by its mechanism
                num_mechanism = 0
                ready_to_sample = True
                for mechanism in self.observed_mechanisms:
                    print("mechanism",mechanism)
                    if mechanism[1] == variable: # check whether this variable is the output of a mechanism
                        if variables_sampled[mechanism[0]] == True: # check whether the input of this mechanism has been sampled, if not, it is not ready to be sampled
                            num_mechanism += 1
                        else:
                            ready_to_sample = False
                            break
                if ready_to_sample == False:
                    continue
                # print("ready to sample!:",variable)
                # print("num_mechanism",num_mechanism)
                # print("data",data)
                # if this variable should be sampled, then we sample it
                # first, we use mechanism to sample the input of this variable
                # tmp_data shape is [num_mechanism, 1]
                # import numpy as np
                tmp_data = {}
                print("self.observed_mechanisms",self.observed_mechanisms)
                for name in self.observed_mechanism_names:
                    # print("mechanism[1]",mechanism[1])
                    mechanism = self.observed_mechanisms[name]
                    print("name",name)
                    from_name = self.observed_mechanism_names[name][0]
                    to_name = self.observed_mechanism_names[name][1]
                    print("from_name",from_name)
                    print("to_name",to_name)
                    if to_name == variable:
                        print("data[from_name]",data[from_name])
                        tmp_data[to_name] = mechanism(data[from_name])

                # then, we use the fusion mechanism to sample the output of this variable
                print("tmp_data",tmp_data)
                # print("data",data)
                # print("variable",variable)
                # print("self.fusion_mechanisms[variable]",self.fusion_mechanisms)

                t_data = self.fusion_mechanisms[variable](tmp_data.values())
                print("t_data",t_data)
                data[variable] = self.fusion_mechanisms[variable](tmp_data.values())
                variables_sampled[variable] = True
            
            # check whether all variables have been sampled
            all_sampled = True
            for variable in variables_sampled:
                if variables_sampled[variable] == False:
                    all_sampled = False
                    break
            if all_sampled == True:
                break
        return data, variables_sampled

observed_node_names = ['X','T','Y']
confounded_cliques = [['X','Y']]
observed_parents_dict = {'Y':['X','T']}

scm = SCM(observed_node_names,confounded_cliques,observed_parents_dict)

# distributions = {'X': None, 'Y': None, 'T': None}
# fusion_mechanisms = {'Y': lambda x: x[0]*0.1+x[1]+1}
# observed_mechanisms = {'X': lambda x: x*0.1, 'T': lambda x: x+1}
scm.set_parameters(distributions = None, fusion_mechanisms = None, observed_mechanisms = None, hidden_mechanisms=None)

ob_data, hidden_data = scm.sampling(10)


print("hidden data",hidden_data)
print("observed data",ob_data)