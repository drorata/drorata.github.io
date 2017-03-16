Title: Pillars of reproducible data science work
Date: 2017-03-16
Summary: What does it take to have reproducible data science work? Present a minimal example using Docker.
Status: published
Tags: docker, jupyter, reproducible, research
Category: DS

# Bare minimum of reproducible work

The output of software development is naturally a software.
However, when a software developer presents his or her work the compiled binaries are not the whole story.
It is important to present also the source code, which has to be readable, meet the coding conventions of the team, testable, etc. etc.
As software engineering dates back to the 60s of the previous century[^7d3740b4] the industry has well established methods, paradigms and processes that enable successful software development.
Reproducible work in the context of software development means that the binaries can be recompiled by someone who is not the original developer.


[^7d3740b4]: Paul Niquette (1995). ["Softword: Provenance for the Word 'Software'"](http://www.niquette.com/books/softword/tocsoft.html). adapted from Sophisticated: The Magazine ISBN 1-58922-233-4

However, in the context of output of data science work, reproducibility depends on slightly different set of elements:

1. *Result:* It goes without saying that you need to have results if you want to present your work.
One should be able to compare the reproduced result to the original one.
In the case of data science result may be an analysis, report, dashboard, trained and tested model, etc.
Having software development in mind, this part is equivalent to the compiled binaries provided by a developer.
2. *Source code:*  By merely presenting the result of the work, the deliverable is not complete.
Just like in software development, the binaries on their own are not enough to account as a complete work.
It is important to show the way; how the results were achieved.
In other words, sharing the the source code together with the results is crucial.
3. *Data:* Source code alone is not enough.
For data science related work, the source code is not enough as it has to crunch some numbers.
The numbers are available in the data set which was considered when the scientist worked on the task.
Without the data the sources cannot be evaluated and the result cannot be reproduced.
Let me stress it, for real reproduction the very same data set(s) has to be provided alongside the code.
4. *Environment:* Even if you have the sources and the data that the scientist used for generating the results, you might still be lightyears away from being able to reproduce them.
For example, results were generated using the development branch version of Pandas and you only have the stable version installed.

In other words, if you want to enable someone to reproduce your work, you have to provide a complete package consisting of all the above items.
The result (or results) must be there, otherwise there's no way of introducing a deliverable.
Next, it might be argued that the simplest item is the source code.
To that end one can harness the rich experience from the world of software development.
But what about the rest?
How do you put everything into one "software" which can be provided for things like

- peer reviewing
- knowledge sharing
- result reproduction
- versioning control
- etc.

If you [google related keywords](http://lmgtfy.com/?q=reproducible+research+data+science) you will find lots of stuff.
I recently read about [Pachyderm](http://pachyderm.io/); I didn't have the chance to check it.
You can look in the direction of [knowledge-repo](https://github.com/airbnb/knowledge-repo), and probably endless amount of other possibilities.
I decided to start and play with [Docker](http://docker.io/) when trying to tackle this issue.
True, you might see people  write that this is a [bad solution](https://blog.wearewizards.io/why-docker-is-not-the-answer-to-reproducible-research-and-why-nix-may-be), but there are always pros and cons.
You can read more about my first attempt [here](https://github.com/drorata/mwe-jupyter-docker).

One warning light I see with this approach is the size of the resulting Docker image.
[At first](https://github.com/drorata/mwe-jupyter-docker/blob/230b683ff0d9c2aed4b632185de5af6015bf92c3/Dockerfile), I used `jupyter/minimal-notebook` as the base of the image.
This resulted in a 3.4GB image.
As per the [related discussion](https://github.com/jupyter/docker-stacks/issues/205), I switched to `jupyter/base-notebook` and this was a significant improvement.
Still, the size of the resulting image might be a hurdle when it comes to easily share and distribute the results of data science work.
[This post](https://blog.replicated.com/engineering/refactoring-a-dockerfile-for-image-size/) seems like a good place to look for further size optimization tips.
