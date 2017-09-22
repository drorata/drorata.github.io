Title: Messages taken home from "AI in Data Science presented by RecdoTech"
Status: published
Category: DS
Summary: Some remarks and highlights from taken from a meetup I attended.

On September 14th (2017) I attended the first meet organized by RecdoTech[^b5d84a8f].
Although organized by be a recruitment agency, it turned out to be a real meetup.
There should have been three talks, but eventually there were only two.

The first talk, by [Luba Weissmann](https://www.linkedin.com/in/luba-weissmann-47b7757/), introduce the basics concepts and ideas from the world of credit scoring.
In particular, Luba discussed how FinTech harnesses data science to understand behavioral aspects of individuals asking for credit.
The speaker tried to make a very clear distinction between *machine learning* and *AI*; for her the main differentiator is the way the decision is made.
Personally, I was not convinced, and I think primary reason to use the term AI in this context, is to create more hype.
It is often the case, that AI is considered an umbrella of different automated decision making approaches.
Many of them are employing machine learning, but not only.[^5fa6e1e7]

An interesting point raised by Luba is that regulators are introducing hurdles to the integration of AI (in the broader sense) into credit scoring.
The reason might be a little surprising: in a nutshell, when credit is denied, the customer (let it be an individual or a company) has the right to know why the rejection happened.
However, assuming the reason for rejection is due to an algorithm which returned some value, it is not necessarily clear and trivial to explain why and in turn it may be hard to explain this to the customer.
Have deep learning in mind, as a clear example where the algorithm may suggest rejection, but understanding *why* is very complicated.

[^5fa6e1e7]: Nice summary on [Quora](https://www.quora.com/What-are-the-main-differences-between-artificial-intelligence-and-machine-learning-Is-machine-learning-a-part-of-artificial-intelligence)

[^b5d84a8f]: This is a brand of Darwin Recruitment. See [profile](https://www.meetup.com/RecdoTech/members/230799589/)

The second talk, by [Sébastien Foucaud](https://www.linkedin.com/in/sfoucaud/), was more high level, and provided ideas and insights into the meaning of having data science as part of business landscape.
In the business world, the results of data science work have to have impact.
The needle has to move!

![VU meter]({filename}/images/VU_Meter.gif)

The data scientist who wishes to survive and strive in the business world, has to add value to the operations.
Even research labs ran by big players are, at the end of the day, about adding value to the company.
This holds for sure when it comes to small/medium size companies and startups, where the impact has to be present.
Sébastien used the term *business driven data scientist*; I liked it especially when there is so much noise around the data drivenness approach.
It is impossible to be data driven without, first, be business driven.
Along this line of thought, Sébastien also mentioned that the model does not matter; it is its integration and impact that count.
To that end, if you have a model which delivers then no one cares about its beauty, complexity or how ingenious it is.
As a scientist this is sometimes hard to accept; you are trained to deliver perfection, because otherwise your paper will not be accepted.

Another point discussed during the talk was related to data quality.
"Not all data is useful" and you need your data to be "smart".
Having big data does not necessarily imply it is smart.
Sometimes, the overhead derived by big data is so much bigger, that at the end of the day the impact is marginal.
The most important key to *smart data* is to have it labeled or flagged.
This is the only way that the data scientist can really derive insights out of it.
Facebook, Google, Airbnb and all the others are releasing technologies like crazy.
They are much more cautious when it comes to sharing labeled data[^9f4e79c9].
Companies are trying to improve their data quality all the time and user feedback is a central ingredient.
For instance, think of all the thumbs-up/down icons that turned into a little epidemic.
They are all there as part of the effort of companies to label, tag and flag their data.

![Thumbs up]({filename}/images/thumbs-up.jpg)

[^9f4e79c9]: There are [exceptions](https://quickdraw.withgoogle.com/data) of course.

Lastly, the composition of a data science team was briefly discussed during the Q&A part.
In contrast to the vibe around the [full stack data scientist](http://lmgtfy.com/?q=full+stack+data+scientist), Sébastien advocated the need of a cross functional team in order to address the needs.
The team should consist of:

- Data scientist and engineer (assuming these are two different things): I guess these two are kind of self-explanatory.
- Product manager: this guy should fill in the gap between the data scientist in the team and the "business driven" data scientist that should be there. But not only for that; he should take care of all the coordination and the project management.
- Software developer/engineer: enable easier streamlining of the data science products into the business and to production environments.
- User interface: remember the thumbs-up/down, this guys is needed to make user feedback more accessible.

All in all, the teams size should be between 5-8 people, depending on the plate's size, the capacity of each team member and its availability.
I believe that during an initial phase of integration of the team(s) in the organization,  some of the manpower may be shared with other parts of the tech team.
