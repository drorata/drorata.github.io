Title: Moving from local machine to Dask cluster using Terraform
Date: 2018-01-05
Status: published
Category: HowTo
Tags: python, dask, cluster, settings
Summary: Tutorial on how to start a cluster of dask instances on AWS (EC2). Using this cluster execute an expansive grid search.

## Introduction

As part of the never-ending effort to improve reBuy and turn it into a market leader, we recently decided to tackle the challenges of our customer services agents.
As a first step, a dump of tagged emails was created and the first goal was set: build a POC that tags the emails automatically.
To that end, NLP had to be used and a lengthy (and greedy) [grid search](http://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html) had to be executed.
So lengthy, that 4 cores of a notebook were working for couple of hours with no results.
This was the point when I decided to explore [`dask`](http://dask.pydata.org/en/latest/) and its sibling [`distributed`](https://distributed.readthedocs.io/en/latest/).
In this tutorial/post we shall discuss how to take a local code doing grid search using Scikit-Learn to a cluster of AWS (EC2) nodes.

The full tutorial, including source files, can be found [here](https://github.com/drorata/ds-dask_cluster_example), where the [README](https://github.com/drorata/ds-dask_cluster_example/blob/master/README.md) is the entrypoint.
