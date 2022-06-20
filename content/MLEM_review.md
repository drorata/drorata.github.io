Title: Getting to know MLEM
Date: 2022-06-17
Category: ML
Tags: MLops, workflows
Status: published


_This post is based on the README [here](https://github.com/drorata/mlem-review/blob/main/README.md) where newer versions might be available._

[MLEM](https://mlem.ai/) promises that you:

> Use the same human-readable format for any ML framework

This is a bold promise and in this repo I will explore it a little (and maybe some other features as well).
Note that the machine learning part of the content is only secondary.
In the foreground we put the process and the tools.

## Fetching and preparing the data 👷🏽‍♀️

To keep it simple on the ML front, we use the [Iris data set](https://scikit-learn.org/stable/auto_examples/datasets/plot_iris_dataset.html).
The data is obtained in [`get_data.py`](https://github.com/drorata/mlem-review/blob/3609bd31b65ecbc3623447b8e9608f7fad1845d0/get_data.py); see the comments there for more details.

This script is used in the first stage of the DVC pipeline [`dvc.yaml`](https://github.com/drorata/mlem-review/blob/3609bd31b65ecbc3623447b8e9608f7fad1845d0/dvc.yaml#L3-L10).

## Training the model and persisting it using MLEM 🚀

In [`train_and_persist.py`](https://github.com/drorata/mlem-review/blob/3609bd31b65ecbc3623447b8e9608f7fad1845d0/train_and_persist.py) we, well, train and persist the model.
Again, in [`dvc.yaml`](https://github.com/drorata/mlem-review/blob/3609bd31b65ecbc3623447b8e9608f7fad1845d0/dvc.yaml#L12-L19) this script is used as the second stage.
Here it is important to pay more attention to the `mlem.api.save()` statement:

```python
save(
    rf, "rf", sample_data=X, description="Random Forest Classifier",
)
```

`rf` is the fitted model and it is given a name; the _string_ `"rf"`.
In addition a description is provided (See issue [#279](https://github.com/iterative/mlem/issues/279) for a related topic).
Furthermore, by providing a value to the parameter `sample_data`, MLEM will include the schema of the data in the model's meta data.
Checkout [`.mlem/model/rf.mlem`](https://github.com/drorata/mlem-review/blob/3609bd31b65ecbc3623447b8e9608f7fad1845d0/.mlem/model/rf.mlem#L13-L24).

## What's next? Or how to get predictions using an API? ⚡️

By running `dvc repro` in this project following things will happen:

- Iris data set will be fetched and splitted into train and test sets.
- A model will be train.
- The model will be persisted by MLEM; its metadata ([`.mlem/model/rf.mlem`](https://github.com/drorata/mlem-review/blob/3609bd31b65ecbc3623447b8e9608f7fad1845d0/.mlem/model/rf.mlem)) will be tracked by Git and the model itself (`.mlem/model/rf`) will be tracked by DVC.

Now comes the fun part.
By running:

```bash
mlem build rf docker --conf server.type=fastapi --conf image.name=rf-image-test
```

MLEM will build a docker image that can be used to get predictions from the trained model using an API.
Once the image is built, a container can be ran:

```
docker run --rm -it -p 8080:8080 rf-image-test
```

As soon as it is up and running, the documentation of the endpoints of the new API can be found here: http://0.0.0.0:8080/docs.

To make it easier, [`Taskfile.yml`](https://github.com/drorata/mlem-review/blob/3609bd31b65ecbc3623447b8e9608f7fad1845d0/Taskfile.yml) can help in building and serving the image.
For more details on how to use a `Taskfile`, checkout [`task`](https://taskfile.dev/).

Finally, once MLEM is serving the model, we can get predictions for our test set using [`evaluate.py`](https://github.com/drorata/mlem-review/blob/3609bd31b65ecbc3623447b8e9608f7fad1845d0/evaluate.py).
To that end we simply send a list of dictionaries to the `/predict` end point and get, in return, a list of predictions.
Isn't it really wonderful?

<center>
<img src="https://cdn.pixabay.com/photo/2020/06/04/08/50/awesome-5257905_1280.png" alt="Isn't it awesome?" width=25% height=25%>
</center>

## Summary

So, in [this repository](https://github.com/drorata/mlem-review) you can find an end-to-end example how to bring your ML model to life as an API that can return predictions.
This bridges a huge hurdle that data science teams face.
After completing the hard work related to data fetching, cleaning, feature engineering, models training/evaluation/tuning and so on, the team is ready to deliver great value.
Alas... Now support from DevOps and Data engineers is needed to bring the model to production.
Using MLEM, the team is much closer to be independent and impact directly and quickly.
