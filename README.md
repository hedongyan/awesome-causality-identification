# Introduction

This repository implement all kinds of identification algorithm of causal inference, including causal graph with hidden common causes. 

1. ID and IDC algorithm of Ilya Shpitser and Judea Pearl. This algorithm is complete for Directed Acyclic Graph with hidden common causes. 

Warning: Identification results of Ilya's algorithm are not unique due to different topological orderings and different fixing functions! You should notice that before you use it. The fixing function in this work is the individual's certain value. 

In future, I will add more automatic identification algorithms!

# Example

Please run the examples of ID and IDC by following orders:
python test_id.py
python test_idc.py

In the output, "Not identifiable" means we can not identfy the causal effect from treatment to outcome. "V" denote the union of all variables (I use it to simply the length of output).

# Application

I directly plot the [identification table](https://hedongyan.github.io/files/id3.html) of all 200 DAG with abitrary hidden common causes (three measured variables) for quick (conditional) causal query. 

I directly list all [51 identification results](https://hedongyan.github.io/files/id4.pdf) of 34752 cases for 4 observed variables with hidden confounders for query Pr(Y(T)). 

# Reference

[Ilya Shpitser and Judea Pearl. 2006. Identification of joint interventional distributions in recursive semi-Markovian causal models. In Proceedings of the 21st national conference on Artificial intelligence - Volume 2 (AAAI'06). AAAI Press, 1219–1226.](https://dl.acm.org/doi/abs/10.5555/1597348.1597382)
