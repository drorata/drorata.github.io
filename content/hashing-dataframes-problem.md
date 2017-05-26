Title: When trying to hash a data frame
Date: 2017-05-26
Status: published

## TL;DR

The function [`pandas.DataFrame.values`](https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.values.html) is not the inverse of `pd.DataFrame(np.array)`.

## Introduction

An important part of reproducible data science work, is the ability to apply the [DAG](https://en.wikipedia.org/wiki/Directed_acyclic_graph) on the very same dataset.
Simplest option is to commit the datasets to a VCS like `git`.
This has the problem that VCSs are simply not designed for this.
Ultimately, a dataset is the result of an ETL process.
Tracking the ETL process is easy and fits VCSs.
In some sense this is enough; but not quite right.
A hidden assumption in this case, is that the sources from which the ETL process fetches the raw data from are not changing.
This is a rather strong assumption and not necessarily holding in all settings.
A way to verify that the product of the ETL process is the same is to use two hashes:

1. Hash of the code behind the ETL process (you get it for free from `git`)
2. Hash the product of the ETL process; namely, the resulting dataset

Having these two hashes, one can checkout the code of the ETL process, run it and compare the hash of the resulting dataset and the second hash.
If the two are the same, we have a very strong indication that the datasets are the same.
Right, if they are *not* the same we merely know the two datasets are not the same.
Most likely due to changes in the sources which feed the ETL process.
This line of thought made me look into hashing possibilities of `pandas.DataFrame`s.

## Hashing a data frame

[Google](https://stackoverflow.com/a/41715431/671013) suggested that I should represent the data frame in bytes and hash this representation.
Problem is that there's no straightforward way to turn a data frame into bytes stream.
A more-or-less canonical way would be to convert the data frame to an array of `numpy`:

```python
df.values.tobytes()
```

Here's an example which worked nicely:

```python
np.random.seed(42)
arr = np.random.choice([41, 43, 42], size=(3,3))
df = pd.DataFrame(arr)
print(arr)
print(df)
print(hashlib.sha256(arr.tobytes()).hexdigest())
print(hashlib.sha256(df.values.tobytes()).hexdigest())
```

Repeatedly evaluating this code always yield the same hash `ddfee4572d380bef86d3ebe3cb7bfa7c68b7744f55f67f4e1ca5f6872c2c9ba1`.
However, as soon as we introduce a string into the game, things are no longer predictable.
Repeatedly invoking the following shows that the hash of the data frame is not kept:

```python
np.random.seed(42)
arr = np.random.choice(['foo', 'bar', 42], size=(3,3))
df = pd.DataFrame(arr)
print(arr)
print(df)
print(hashlib.sha256(arr.tobytes()).hexdigest())
print(hashlib.sha256(df.values.tobytes()).hexdigest())
```

The reason here is that `df.values != arr`.
As a matter of fact, it seems like each time we evaluate `df.value` we get a new object.
Annoyingly enough, `np.array_equal(df.values, arr)` is **true** because it compares the values.

### Workaround

The workaround I can suggest is to use some string representation of the data frame, and hash the bytes representation of the string representation.
For example:

```python
np.random.seed(42)
arr = np.random.choice(['foo', 'bar', 42], size=(3,3))
df = pd.DataFrame(arr)
print(arr)
print(df)
print(hashlib.sha256(arr.tobytes()).hexdigest())
print(hashlib.sha256(df.values.tobytes()).hexdigest())
print(hashlib.sha256(df.to_json().encode()).hexdigest())
print(hashlib.sha256(df.to_csv().encode()).hexdigest())
```

Obviously the downsides are:

1. The hash won't be the same as the one of the original array
2. If the data frame is big, this can be very lengthy

But, it works.
You can find a summarizing [notebook here](https://gist.github.com/drorata/bfc5d956c4fb928dcc77510a33009691).
In addition, I have also opened a [ticket on the matter](https://github.com/pandas-dev/pandas/issues/16517).


## Solution

Well, it turns out, that opening the bug was helpful.
As of 0.20.1, it is possible to [hash data frames](https://github.com/pandas-dev/pandas/issues/16517#issuecomment-304364225)!
