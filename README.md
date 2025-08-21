# Why you may need causal identification?

## 💰 Find Your Growth Levers: Cut Through the Data Noise!

Is your business leaving money on the table?  
- That "successful" campaign—did it **really drive profit**, or just attract existing buyers?  
- Your new UX redesign—is it a **true upgrade** or just a placebo?  
- Is churn caused by **pricing**... or **poor support**?  

📈 **Guessing = Wasted budget + Missed opportunities!**  
Correlation tricks you. Causation empowers you.  

**Causal identification** is your **ROI magnifying glass**. It lets you:  
- 🎯 **Pinpoint drivers**: Discover what *truly* moves metrics (revenue, retention, costs).  
- ⚖️ **Optimize resources**: Invest time/money where it *actually* generates returns.  
- 📊 **Quantify value**: Measure the *exact dollar impact* of every change.  

**Stop optimizing blind. Start growing smart. 🚀 Star now to turn data into dollars!**  
*ACI delivers lightning-fast causal insights*.  

# Motivation

The motivation to create this repository at Janurary of 2022 and rewrite the identification code is that existed causal package can not implement the complete identification algorithms of Ilya Shpitser correctly, including [CausalEffect](https://github.com/santikka/causaleffect)(Santtu Tikka), [CausalML](https://causalml.readthedocs.io/en/latest/about.html)(Uber), [Ananke](https://ananke.readthedocs.io/en/latest/)(Ilya Shpitser), [dowhy](https://github.com/py-why/dowhy)(Microsoft), [CEE](https://github.com/L-F-Z/CEE)(Fengzhi Li), [Dagitty](https://www.dagitty.net/)(Johannes Textor), [YLearn](https://github.com/DataCanvasIO/YLearn)(CSDN). If I did not implement it, I can not identify the graph automaticlly in my following works. 

1. CausalEffect.
The understanding of causaleffect of line 7 of ID algorithm is wrong in their [paper](https://www.jstatsoft.org/article/view/v076i12/0). 

2. CEE.
The understanding of CEE of line 6 of ID algorithm is wrong. It confused the fixed value v and variable V. And I got a wrong result after I run the program. 

3. Dowhy.
I did not find complete ID and IDC algorithm in their source code after searching in their source code. 

4. Ananke.
They use fixing operation in nest forms and do not give final expression. 

5. Dagitty.
It only support adjustment and instrument variable.

6. YLearn.
I did not find complete ID and IDC algorithm in their source code after searching in their source code. 

7. CausalML.
I did not find complete ID and IDC algorithm in their source code after searching in their source code. 

# Introduction

This repository implement all kinds of identification algorithm of causal inference, including causal graph with hidden common causes. The post-intervention distribution of `p(V)=\prod_{i}p(v_i|pa_i)` is defined by `p(V(T))=\prod_{i|V_i\notin T}p(v_i|pa_i)` where `V` is the measured variables, `pa_i` is parents of `v_i`. Those identification is mainly based on Judea Pearl's three theorems of identification on structural causal model. 

1. Intervention query. ID and IDC algorithm of Ilya Shpitser and Judea Pearl. This algorithm is complete for causal query with observation data on Directed Acyclic Graph with hidden common causes. The interested quantities are Pr(Y(T)), Pr(Y(T)|X(T)). 
2. Mediator Analysis. The path-specific effect is the causal effect from treatment T to outcome Y by the path of mediater M. When someone use a causal model to intervene the outcome Y by the T, you can terminate its effect if you found a mediater M of T on Y and you can intervene the mediater M. The interested quantity is total effect Pr(Y(T)), natural direct effect Pr(Y(T)|M), natural indirect effect Pr(Y(M)|T). 
3. Surrogate experiments. When you can not internve the treatment directly, you may can intervene other variable. Such intervention is called surrogate experiment. IDZ algorithm of Elias Bareinboim and Judea Pearl is complete for causal query with surrogate experiments and observation data on Directed Acyclic Graph with hidden common causes. (update soon)

Warning: Identification results of Ilya's algorithm are not unique due to different topological orderings and different fixing functions! You should notice that before you use it. The fixing function in this work is the individual's certain value. 

In future, it will support more automatic identification algorithms! If the other identification algorithm can be to the same algorithms, we will add an explaination of it rather than implement it repeatly. Please feel free to let me know your demands by issues. 

The following figure is the decision tree of identification algorithm choosing. 

![Decision Tree of Identification Algorithm](figs/因果效应识别流程图.png)

# Identification Process

The identification process is very easy to understand. 

1. Create an ADMG which represent the data generation assumptions. The ADMG is DAG with hidden common cause. The three steps are add node names to represent variable name, add directed edges to represent dependency, and add bidirected edges to represent the hidden common causes. 
2. Create ObservationProbability to represent a distribution. 
3. Create InterventionQuery to represent a causal query. 
4. Create identification algorithms (such as ID, IDC) for the identification.
5. Identify the causal query by the identification algorithm and return the identified ObservationProbability for the InterventionQuery. 
6. Print the identification result (ObservationProbability) by latex code. 

# Example

I checked many exmaples of the identification result mannuly. 

If you want to run the examples of ID algorithm and IDC algorithm, please run the examples of ID and IDC by following orders:

```python
python test_id.py
```

```python
python test_idc.py
```

In order to verify the correctness of our algorithm, we checked many graphs in the file test_many_id.py. 

```python
python test_many_id.py
```

In the output, "Not identifiable" means we can not identfy the causal effect from treatment to outcome. "V" denote the union of all variables (I use it to shorten the length of output latex code).

# Application

I directly plot the [identification table](https://hedongyan.github.io/files/id3.html) of all 200 DAG with abitrary hidden common causes (three measured variables) for quick (conditional) causal query. I firstly identify the 200 graphs [mannully](https://hedongyan.github.io/files/myuai2022.pdf) and then check the correctness of the program. 

I directly list all [51 identification results](https://hedongyan.github.io/files/id4.pdf) of 34752 cases for 4 observed variables with hidden confounders for query Pr(Y(T)). The program to automatically identify the 34752 graphs is test_id_all4v.py. The result is stored in the **identified_results.txt**.

```python
pip install networkx
python test_id_all4v.py
```

# Citation

If you find this repo useful, please cite me as follows:
```
@misc{causalid,
  author={Hedong YAN},
  title={Awesome Causality Identification},
  howpublished={https://github.com/hedongyan/awesome-causality-identification},
  note={Version 0.x},
  year={2025}
}
```

# Reference

[JUDEA PEARL, Causal diagrams for empirical research, Biometrika, Volume 82, Issue 4, December 1995, Pages 669–688, https://doi.org/10.1093/biomet/82.4.669](https://www.jstor.org/stable/2337329?seq=1)

[Ilya Shpitser and Judea Pearl. 2006. Identification of joint interventional distributions in recursive semi-Markovian causal models. In Proceedings of the 21st national conference on Artificial intelligence - Volume 2 (AAAI'06). AAAI Press, 1219–1226.](https://dl.acm.org/doi/abs/10.5555/1597348.1597382)

[Bareinboim E, Pearl J. Causal inference by surrogate experiments: z-identifiability. InProceedings of the Twenty-Eighth Conference on Uncertainty in Artificial Intelligence 2012 Aug 14 (pp. 113-120).](https://dl.acm.org/doi/abs/10.5555/3020652.3020668)
