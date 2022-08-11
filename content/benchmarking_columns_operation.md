Title: Benchmarking Columns Operations
Date: 2017-06-27
Category: DS
Tags: python, pandas
Status: published
Summary: Benchmarking different ways to process two columns simultaneously.

(Original notebook can be found in [this gist](https://gist.github.com/drorata/3716f915ffc020bfbb109b5d4d5952c0))

I recently ran the following experiment.
The reason was my need to perform operations on two columns.
Think for example in terms of features engineering; you want to produce an new feature (i.e. column) which is the ratio of the some other two columns.


```python
import pandas as pd
import numpy as np
```


```python
df = pd.DataFrame(np.random.random(size=(10000,2)), columns=['foo', 'bar'])
```


```python
df.head()
```




<div>
<style>
    .dataframe thead tr:only-child th {
        text-align: right;
    }

    .dataframe thead th {
        text-align: left;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>foo</th>
      <th>bar</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.065648</td>
      <td>0.593402</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.592051</td>
      <td>0.123502</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.621030</td>
      <td>0.629470</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.210630</td>
      <td>0.462535</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.263708</td>
      <td>0.807304</td>
    </tr>
  </tbody>
</table>
</div>



## Iterating over the rows

Here we iterate over the rows, and access the indexes of the `pd.Series` which represents the row.


```python
%%timeit
pd.Series([
    x[1]['foo'] * x[1]['bar'] for x in df.iterrows()
])
```

    518 ms ± 60 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)


## Applying a function

Here we use `pd.DataFrame.apply` and provide the axis.
This is actually, the solution I had to use in a case which I now longer remember its details.


```python
%%timeit
df.apply(lambda x: x['foo'] * x['bar'], axis=1)
```

    299 ms ± 43.1 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)


## Columns operations

Best and fastest approach; at least for this simple case.


```python
%%timeit
df.foo.mul(df.bar)
```

    97.2 µs ± 11.9 µs per loop (mean ± std. dev. of 7 runs, 10000 loops each)


## Summary

Obviously, for the simple multiplication, the last option is the most pythonic (and the fastest as well).
But, still due to an edge case I decided to run this test.
Maybe someone would find it helpful.
