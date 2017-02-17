Title: Thoughts about data science teams
Date: 2017-02-15

One of the positive things about my current situation (read job hunting), is that it provides a good excuse to meet many different people from many different domains.
This is indeed the case for me.
Furthermore, this state makes you think a lot about your domain, what is your position in it and so on.
You know, the kind of *thoughts-about-life* mode.

<center>![thought-about-life]({filename}/images/life-data-thoughts.jpg)</center>

# What is a data scientist?

Probably by now, everyone saw the Venn-diagram by [Drew Conway](http://drewconway.com/zia/2013/3/26/the-data-science-venn-diagram).

<center>![Drew Conway DS Venn-diagram](http://static1.squarespace.com/static/5150aec6e4b0e340ec52710a/t/51525c33e4b0b3e0d10f77ab/1364352052403/Data_Science_VD.png)</center>

Most of its variations (see for example [KDnuggets](http://www.kdnuggets.com/2016/10/battle-data-science-venn-diagrams.html)) are nothing but semantic changes.
One of them however is really different; it adds the secret sauce.
Check it out:

<center>![Stephan Kolassa DS Venn-diagram](https://i.stack.imgur.com/aiQeT.png)</center>

Most of the other diagrams are correct, as long as they are not dealing with a business related setting.
In order to make data science relevant to business, you need an extra pillar; communication skills.
A data scientist, as part of a business organization, has to communicate.
He or she has to talk with various stakeholders; understand their problems; explain his point of view; discuss matters with developers etc.
This, by the way, also relates to visualization skills which are mentioned by many.
visualization is a great, and even mandatory, support tool when it comes to communication.
In this post, I would like to list the central traits which I consider most important when it comes to data science *within* a business organization.

# Data science ingredients

Let's dive deeper into what is needed from a data scientist.
But before doing so, allow me a word of warning.
The traits that I will discuss next are amazingly broad and span across insanely amount of fields.
This means that a single data scientist is, almost by definition, a bad one.
I would argue it is (almost) impossible to find an individual who masters all aspects that are needed in order to have a productive data scientist.
This means that the business would ultimately need a *team*.
Naturally, not all fields that we shall discuss are needed in all cases.
Each business has to identify what are the needed traits of its data science team and find the individuals that will build such a team.

## Theoretical knowledge
If you want to build a predictive model, well, you have to know what a predictive model is.
You will also have to know how to evaluate it and understand whether it is better than tossing a coin.
If the business case requires the deep learning of images, again, you have to know your way.
Still, even if you managed to come up with the best model ever, which manages to find even [Schrödinger's cat](https://en.wikipedia.org/wiki/Schr%C3%B6dinger's_cat) in an image, it is not at all helpful if the running time is $O(n!)$.
In order to be a valuable asset of the organization, a data scientist (or the team) should be familiar with the following fields:

* Mathematics
* Statistics
* Machine/deep learning
* Computer science

Indeed, each of the fields I listed is vast on its own.
It might be that deep knowledge about [Galois Group](http://mathworld.wolfram.com/GaloisGroup.html) won't be the first thing you'd need when tackling a DS problem.
But, have background in these fields can help you a lot.
Furthermore, you can probably argue it is not at all an exhausting list.
And you are probably correct.
Additional fields might be needed depending on (spoiler) business needs.

## Tech-stack know-how
Data science has something to do with [data](https://giphy.com/gifs/you-got-it-dude-aVtdz7iNVPI1W).
As the data is likely not to stored in the form of handwritten laboratories diaries, knowing the technology can be helpful.
Big data and data science go hand in hand, the underlying tech stack is an important part of the trade.
Furthermore, by being on top of the tech-stack one (who masters the theoretical knowledge) can avoid re-inventing the wheel.
Knowing the relevant tech stack is a must when you need to

* access the data
* train scalable models
* master the ETL process
* present the data
* etc. etc. etc.

It is important to note that there are different specializations as well as varying depth that relates to different tech branches and/or tools.
One doesn't necessarily have to be a core contributor to Spark and still be a productive user of the framework.
Depending on the needs of the business the needed stack has to be defined.
Of course, since advances in the data science ecosystem are very rapid, it is super important to keep the finger on the pulse.
Here it is worthy to warn: staying on top of all the changes in the tech-stack related to data science is a task on its own.

## Business understanding
Some people argue that data science is agnostic to the business domain.
And in some cases they are right; a data point is just a data point.
But this is not entirely correct and a sound understanding of the business can make the difference between a mediocre data science and an excelling one.
Here is an example.
One of the standard measures of a model you trained is its [accuracy](https://en.wikipedia.org/wiki/Accuracy_and_precision); what is the ratio between the true positives and negatives with respect to the whole population.
However, if your positive set is very small and valuable, in comparison to the negative set, you are likely to be more interested in the [recall](https://en.wikipedia.org/wiki/Precision_and_recall).
In other words, you want to minimize the number of false negatives (deeming an event as negative event though it is positive).
Being able to state this observation needs business domain understanding.

The message is that those in charge of the data science should (and probably) must be in close contact with business people and make sure they work towards shared goals.
This leads to the next item.

## Communication skills
Data scientists, in smaller organizations for sure, are always in between.
They have to juggle between developers, engineers, management, business people, product and virtually all stakeholders.
It comes as no surprise that all these different facets speak different languages.
On top of all these, the data scientists have to speak data.
Furthermore, the discussions between data people and other stakeholders should happen during all phases of the work.
It starts at the brainstorming phase, when everyones come together and discuss a possible project.
It continuous during the planning phase and the development itself.
Lastly, when results are there to be presented, communication between different stakeholders continues.
Constant communication, free of translation problems, is an important feature of productive and tangible work.
Data scientists are sometimes like Marty McFly trying to explain the world how great Dr. Emmett Brown is or vice versa --- trying to make Doc comprehend what the world is about.

<center>![back to the future](https://c1.staticflickr.com/3/2330/2162754778_9544d707a3.jpg)</center>

# So what?
I believe there are some morals to be taken from the notes above:

* Data science team: Even if you think unicorns (i.e. someone acing in all fields of DS) can be found, you are likely to waste endless amount of time trying to find them.
It is much more reasonable and beneficial to focus on team building.
The team should cover all the fields needed by the business.
* Have well defined objectives: Data science is not black magic and it is not going to solve all problems.
Use the communication skills of the data science *team* and define well-posed problems.
This way you will enable a focused efforts on the data front.
* I believe the above notes can be helpful both to data scientists in turning them into more productive and contributing, and at the same time to different stakeholders who want to utilize the data science capabilities in the company.
