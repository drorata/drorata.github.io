Title: Group by date from a column
Date: 2017-07-03
Category: HowTo
Tags: python, pandas
Status: published

(Original notebooks can be found in [this gist](https://gist.github.com/drorata/315da662702ba82cb70b75d275314ac9))

Assume you have data set as follows:

| ID  | Date | Value |
| --- | ---- | ----- |
| x   | x    | x     |

where each row contains an ID, a date (given as `pd.Datetime`) and a value.
The objective is to count how many rows occur in each day.


```python
import pandas as pd
import numpy as np
import datetime
import random
```


```python
def random_date(start, end):
    """Generate a random datetime between `start` and `end`

    Thanks to https://stackoverflow.com/a/8170651/671013
    """
    return start + datetime.timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int((end - start).total_seconds())),
    )
```

Let's generate a random data set:


```python
N = 100
df = pd.DataFrame(
    {
        "date": [random_date(datetime.datetime(2017,5,1), datetime.datetime(2017,7,1)) for x in range(N)],
        "val": np.random.choice([0,1], size=N)
    }
)
```

**Magic:**

(Based on [this answer](https://stackoverflow.com/a/11397052/671013))


```python
df.groupby(
    [df['date'].map(lambda x: x.month),
     df['date'].map(lambda x: x.day)]
).size()
```



```
    date  date
    5     1       4
          2       2
          3       2
          4       1
          5       4
          6       2
          7       1
          9       1
          10      2
          11      1
          12      1
          13      2
          14      2
          15      1
          16      1
          17      4
          19      4
          20      2
          21      1
          22      1
          24      1
          25      1
          26      3
          27      1
          28      2
          29      1
          31      1
    6     1       2
          2       2
          3       2
          4       3
          5       2
          6       1
          7       1
          9       4
          10      2
          11      1
          12      1
          13      1
          15      1
          16      2
          18      1
          19      5
          20      3
          21      2
          23      3
          24      3
          26      2
          27      3
          29      1
          30      3
    dtype: int64
```
