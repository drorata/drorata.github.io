Title: Expose an API for a trained prediction model
Date: 2018-05-08
Category: DS
Tags: python, docker, model, sklearn, IT
Status: published
Summary: You will build a RESTful API exposing a trained prediction model.

## Why?

This is rather clear.
As a data scientist, you worked hard.
You got the data, you explored it, and identified the important features.
Next, you spent days wondering in the mighty hyper-parameters space.
Bottom line, you have trained the best model which can now become part of the production environment.
Alas, to that end you need to turn your model into something more interactive.
In this post, you will learn how to get started with [Flask](http://flask.pocoo.org/) and expose a RESTful API that can communicate with the trained model.

## Training the model

This is out of the scope of this post.
In what follows I assume you have something like:

```python
from sklearn.externals import joblib
pipeline.fit(X, y)
joblib.dump(pipeline, 'pipeline.pkl')
```

Where `pipeline` is a Scikit-learn pipeline.
Pay attention to the nature of the unseen data points that you would like to feed into the pipeline using the API.
You should make sure that the pipeline can handle the unseen data points; for example take care of preprocessing steps.
If this is not the case, you have to take care and enable the application to preprocess the data.

## Flask application

Include the following snippet in a file `app.py`:

```python
# app.py
from flask import Flask, jsonify, request
from sklearn.externals import joblib
import pandas as pd
import train_model as tm # Implementation of preprocessing steps outside of
                         # the pipeline's scope
app = Flask(__name__)


@app.route('/predict', methods=['POST'])
def predict():
    json_ = request.get_json()

    query_df = pd.DataFrame(json_)

    query = tm.prepare_data(query_df, train=False)

    prediction = clf.predict(query)
    prediction = [int(x) for x in prediction]

    return jsonify({'prediction': prediction})


if __name__ == '__main__':
    clf = joblib.load('pipeline.pkl')
    app.run(debug=True, host='0.0.0.0')
```

This is it.
Execute `python app.py` and send unseen data points to `0.0.0.0:5000`.

## Asking the application for predictions

Assume you have `data.json` having the following JSON with unseen data points:

```json
{
    "feat1": {
        "0": 1,
        "1": 3
    },
    "feat2": {
        "0": 3.14,
        "1": 2.71
    }
}
```

You can send this JSON to your already running using [`curl`](https://curl.haxx.se/):

```bash
curl -H "Content-Type: application/json" --data @data.json http://0.0.0.0:5000/predict
```

or using [`httpie`](https://httpie.org/):

```bash
http POST http://0.0.0.0:5000/predict < data.json
```

It is as simple as that.
Of course, you are likely to need way more, but I am sure this will serve as a good start.

## Minimal working example

Simplest way to experience a prediction model API is to run the docker image I prepared:

```bash
docker run -p 5000:5000 drorata/pm_api:v1
```

Once the container is running you can throw at it the following JSON:

```json
{
  "Age": {
    "53": 28,
    "111": null
  },
  "Cabin": {
    "53": "C23 C25 C27",
    "111": null
  },
  "Embarked": {
    "53": "S",
    "111": "Q"
  },
  "Fare": {
    "53": 263,
    "111": 7.7792
  },
  "Name": {
    "53": "Fortune, Miss. Ethel Flora",
    "111": "Shine, Miss. Ellen Natalia"
  },
  "Parch": {
    "53": 2,
    "111": 0
  },
  "PassengerId": {
    "53": 945,
    "111": 1003
  },
  "Pclass": {
    "53": 1,
    "111": 3
  },
  "Sex": {
    "53": "female",
    "111": "female"
  },
  "SibSp": {
    "53": 3,
    "111": 0
  },
  "Ticket": {
    "53": "19950",
    "111": "330968"
  }
}
```

If you want to see more details, this image is built using the sources available in [this repository](https://github.com/drorata/pm_api).
You can create a local python environment, install the requirements and enjoy the example.
