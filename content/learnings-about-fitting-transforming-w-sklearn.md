Title: Some learnings from implementing a transformer
Date: 2017-06-22
Category: ML
Tags: python, sklearn
Status: published

I had to (or at least I thought I had to) implement a transformer to be used in a [`sklearn.pipeline.Pipeline`](http://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html).
In a nutshell, I implemented badly the `transform` method.
The original version can be found in [this gist](https://gist.github.com/drorata/b25547d5f5ed01411658b46f30dfc140/c5c02e4f6e8d5c2b5cf838f53a7d0177b038ed1c).
In the [following version](https://gist.github.com/drorata/b25547d5f5ed01411658b46f30dfc140/9e7193262d1509063ccf984c731e101e854837e2) I fixed it.
Furthermore, I left some comments on the gist's page.
