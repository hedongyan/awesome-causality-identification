# Introduction

This repository implement all kinds of identification algorithm of causal inference, including causal graph with hidden common causes. 

1. ID and IDC algorithm of Ilya Shpitser and Judea Pearl. This algorithm is complete for Directed Acyclic Graph with hidden common causes. 

Warning: Identification results of Ilya's algorithm are not unique due to different topological orderings and different fixing functions! You should notice that before you use it. The fixing function in this work is the individual's certain value. 

In future, I will add more automatic identification algorithms! If the other identification algorithm can be to the same algorithms. I will add an explaination of it rather than implement it repeatly.

# Identification Process

The identification process is very easy to understand. 

1. Create an ADMG which represent the data generation assumptions. The ADMG is DAG with hidden common cause. The three steps are add node names, add directed edges, and add bidirected edges to represent the hidden common causes. 
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
python test_idc.py
```

In order to verify the correctness of our algorithm, I checked many graphs in the file test_many_id.py. 

```python
python test_many_id.py
```

In the output, "Not identifiable" means we can not identfy the causal effect from treatment to outcome. "V" denote the union of all variables (I use it to shorten the length of output latex code).

# Application

I directly plot the [identification table](https://hedongyan.github.io/files/id3.html) of all 200 DAG with abitrary hidden common causes (three measured variables) for quick (conditional) causal query. I firstly identify the 200 graphs mannully and then check the correctness of the program. 

I directly list all [51 identification results](https://hedongyan.github.io/files/id4.pdf) of 34752 cases for 4 observed variables with hidden confounders for query Pr(Y(T)). The program to automatically identify the 34752 graphs is test_id_all4v.py. 

```python
pip install networkx
python test_id_all4v.py
```

# Reference

[JUDEA PEARL, Causal diagrams for empirical research, Biometrika, Volume 82, Issue 4, December 1995, Pages 669–688, https://doi.org/10.1093/biomet/82.4.669](https://www.jstor.org/stable/2337329?seq=1)

[Ilya Shpitser and Judea Pearl. 2006. Identification of joint interventional distributions in recursive semi-Markovian causal models. In Proceedings of the 21st national conference on Artificial intelligence - Volume 2 (AAAI'06). AAAI Press, 1219–1226.](https://dl.acm.org/doi/abs/10.5555/1597348.1597382)
