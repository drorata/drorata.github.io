Title: Averages, sums and counts when grouping by
Date: 2017-08-28
Category: HowTo
Tags: python, pandas
Status: published
Summary: A gotcha when aggregated time series data involving hourly based counts.

(Original notebook can be found in [this gist](https://gist.github.com/drorata/bb63e87c9baa3d5bc1fc088d43bee8f3))

# Averages, sums and counts when grouping by


```python
import pandas as pd
import numpy as np
```

Assume we have a table where each row corresponds to a transaction and indexed by timestamp.
By re-sampling this table by `1H` frequency and counting the number of transaction per hour, we get a new aggregated view when each row corresponds to an hour and the value is the count of transaction happened within that hour.

As an example, we start with the following table.
This demonstrates the result of the re-sampling mentioned above.


```python
np.random.seed(42)
idx = pd.date_range('2017-01-01', '2017-01-14', freq='1H')
df = pd.DataFrame(np.random.choice([1,2,3,4,5,6], size=idx.shape[0]), index=idx, columns=['count'])
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
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2017-01-01 00:00:00</th>
      <td>4</td>
    </tr>
    <tr>
      <th>2017-01-01 01:00:00</th>
      <td>5</td>
    </tr>
    <tr>
      <th>2017-01-01 02:00:00</th>
      <td>3</td>
    </tr>
    <tr>
      <th>2017-01-01 03:00:00</th>
      <td>5</td>
    </tr>
    <tr>
      <th>2017-01-01 04:00:00</th>
      <td>5</td>
    </tr>
  </tbody>
</table>
</div>



The objective is to measure behavior as depending on the day of the week (Mo., Tue. etc.)
First, let us count how many events happened during each weekday.
This can be achieved in couple of ways:


```python
df.pivot_table('count', index=df.index.dayofweek, aggfunc='sum')
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
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>161</td>
    </tr>
    <tr>
      <th>1</th>
      <td>170</td>
    </tr>
    <tr>
      <th>2</th>
      <td>164</td>
    </tr>
    <tr>
      <th>3</th>
      <td>133</td>
    </tr>
    <tr>
      <th>4</th>
      <td>169</td>
    </tr>
    <tr>
      <th>5</th>
      <td>98</td>
    </tr>
    <tr>
      <th>6</th>
      <td>172</td>
    </tr>
  </tbody>
</table>
</div>



or:


```python
df.groupby(df.index.dayofweek).sum()
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
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>161</td>
    </tr>
    <tr>
      <th>1</th>
      <td>170</td>
    </tr>
    <tr>
      <th>2</th>
      <td>164</td>
    </tr>
    <tr>
      <th>3</th>
      <td>133</td>
    </tr>
    <tr>
      <th>4</th>
      <td>169</td>
    </tr>
    <tr>
      <th>5</th>
      <td>98</td>
    </tr>
    <tr>
      <th>6</th>
      <td>172</td>
    </tr>
  </tbody>
</table>
</div>



Lastly, being more explicit (and less Pythonic):


```python
pd.DataFrame(
    [
        df[df.index.dayofweek==i].sum()[0] for i in range(7)
    ],
    columns=['count']
)
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
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>161</td>
    </tr>
    <tr>
      <th>1</th>
      <td>170</td>
    </tr>
    <tr>
      <th>2</th>
      <td>164</td>
    </tr>
    <tr>
      <th>3</th>
      <td>133</td>
    </tr>
    <tr>
      <th>4</th>
      <td>169</td>
    </tr>
    <tr>
      <th>5</th>
      <td>98</td>
    </tr>
    <tr>
      <th>6</th>
      <td>172</td>
    </tr>
  </tbody>
</table>
</div>



Next, we want to compute the *average* number of transaction per weekday.
First, let's do it explicitly, for Monday (day 0).
The total number of transactions is:


```python
df[df.index.dayofweek == 0].sum()
```




    count    161
    dtype: int64



In the dates range used, there are two Mondays, therefore, the average is:


```python
((df.resample('1d').sum()).index.dayofweek == 0).sum()
```




    2



Therefore, the average is:


```python
df[df.index.dayofweek == 0].sum() / ((df.resample('1d').sum()).index.dayofweek == 0).sum()
```




    count    80.5
    dtype: float64



One may think the following syntax is a quicker way:


```python
df.pivot_table('count', index=df.index.dayofweek, aggfunc='mean')
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
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>3.354167</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3.541667</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3.416667</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2.770833</td>
    </tr>
    <tr>
      <th>4</th>
      <td>3.520833</td>
    </tr>
    <tr>
      <th>5</th>
      <td>3.920000</td>
    </tr>
    <tr>
      <th>6</th>
      <td>3.583333</td>
    </tr>
  </tbody>
</table>
</div>



But this returns the wrong average.
To be more precise, it divides the number of transactions per day-of-week by the number of hours that occurred in this day-of-week in the time range, given by:


```python
df.groupby(df.index.dayofweek).count()
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
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>48</td>
    </tr>
    <tr>
      <th>1</th>
      <td>48</td>
    </tr>
    <tr>
      <th>2</th>
      <td>48</td>
    </tr>
    <tr>
      <th>3</th>
      <td>48</td>
    </tr>
    <tr>
      <th>4</th>
      <td>48</td>
    </tr>
    <tr>
      <th>5</th>
      <td>25</td>
    </tr>
    <tr>
      <th>6</th>
      <td>48</td>
    </tr>
  </tbody>
</table>
</div>



Or, put together:


```python
df.groupby(df.index.dayofweek).sum() / df.groupby(df.index.dayofweek).count()
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
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>3.354167</td>
    </tr>
    <tr>
      <th>1</th>
      <td>3.541667</td>
    </tr>
    <tr>
      <th>2</th>
      <td>3.416667</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2.770833</td>
    </tr>
    <tr>
      <th>4</th>
      <td>3.520833</td>
    </tr>
    <tr>
      <th>5</th>
      <td>3.920000</td>
    </tr>
    <tr>
      <th>6</th>
      <td>3.583333</td>
    </tr>
  </tbody>
</table>
</div>



A way around it, would be:


```python
count_per_day_df = df.resample('1d').sum()
count_per_day_df.groupby(count_per_day_df.index.dayofweek).mean()
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
      <th>count</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>80.5</td>
    </tr>
    <tr>
      <th>1</th>
      <td>85.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>82.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>66.5</td>
    </tr>
    <tr>
      <th>4</th>
      <td>84.5</td>
    </tr>
    <tr>
      <th>5</th>
      <td>49.0</td>
    </tr>
    <tr>
      <th>6</th>
      <td>86.0</td>
    </tr>
  </tbody>
</table>
</div>



I mentioned this maybe counter intuitive behavior on [SO](https://stackoverflow.com/q/45922291/671013).
