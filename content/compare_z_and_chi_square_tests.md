Title: Comparing $z$ and $\chi^2$ tests
Date: 2018-02-19
Category: Stats
Tags: hypothesis, testing, z-test, chi2-test
Status: published
Summary: Showing that at least in one certain case the two tests are the same

This post is a snapshot of a notebook that can be found here: [(fd870a6)](https://github.com/drorata/z-vs-ch2-tests/blob/fd870a67cbe3b9e44d397e50a8883919d676e8bf/compare%20z%20and%20chi%20square%20tests.ipynb).
You can also enjoy the binder version of this notebook [![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/drorata/z-vs-ch2-tests/master)

<hr>

```python
import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.stats import proportion

from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

%matplotlib inline
import seaborn as sns
import matplotlib.pyplot as plt
plt.style.use('ggplot')
```

## Preface

The motivation for this tutorial is to better understand the methods to assess the results of A/B(/C...) tests.
There are so many common pitfalls when it comes to A/B tests; make sure you avoid them!
For example, [this check list](https://blog.hubspot.com/marketing/a-b-test-checklist) might be a good reference.

A common and repeating question is how to check the significance of the results of an A/B test.
[Matt Brems](https://stats.stackexchange.com/a/178860/54320) provided a very nice summary.
I wanted to compare two of the tests suggested:

- [$z$-test](https://en.wikipedia.org/wiki/Z-test)
- [$\chi^2$-test](https://en.wikipedia.org/wiki/Chi-squared_test)


### The plan

Let us define $N$ to be a set of $u$ integers and $\Delta$ to be a set of $v$ real numbers.
For each $n \in N$ and $\delta \in \Delta$ we generate a synthetic results of an A/B test.
In particular the control and variant groups would have $\sim n$ observations.
The reason is that in real results of A/B tests, the groups sizes are normally not identical; they are close but not equal.
Furthermore, the control set would have a fixed $\mathrm{CTR}$ (click through rate) and the variant will have conversion rate of $\mathrm{CTR} + \delta$.

As the null hypothesis we take that the CTR of the control and variant groups is the same, independently of the treatment.
Thus a small $p$-value should suggest to reject the null hypothesis.
For each synthetic result we will compute the $p$-value using a $z$-test and a $\chi^2$-test.
In general, we expect that the smaller $n$ is and the larger $\delta$, the resulting $p$-value would be larger.

## Generate data

### Groups' sizes

In reality, even though we assume the users are split randomly and evenly, the final groups' sizes are not identical.
Therefore, we randomize the group size:


```python
def rand_group_size(N, tol=0.05):
    return N + np.random.randint(
        min(-tol * N, -1),
        max(tol * N, 1) + 1)
```

### Event's value

For each successful event we assign a value.
To that end we use a truncated uniform distribution providing the `low` and `up` values, together with the mean (`mu`) and standard deviation (`sigma`).


```python
def rand_values(low, up, mu, sigma, N):
    return stats.truncnorm(
        (low - mu) / sigma,
        (up  - mu) / sigma,
        loc=mu, scale=sigma).rvs(N)
```

### Generating the data for a group

When generating an observation, the following features are randomized:

* The group size; controlled by `N` (~size) and `N_tol`. See `rand_group_size`
* Name of the group. Normally `control` or `var`. Configured by `treat`.
* Randomly assign `1` is the event was converted and `0` otherwise. The randomness is controlled by the weight`ctr`
* In case of conversion what was the value; controlled by: `min_val`, `max_val`, `mean_val` and `std_val`
* What day of the test is it; controlled by number of `days` and the distribution `days_dist`
* `seed` can help you reproduce the results.


```python
def generate_group_observations(N=1000, N_tol=0.05,
                                treat='control',
                                ctr=0.2,
                                min_val=None, max_val=None,
                                mean_val=None, std_val=None,
                                days=7, days_dist=[1/7] * 7,
                                verbose=True,
                                seed=42
                               ):
    if verbose:
        print('Generating ~{N} samples with tolerance {tol}'.format(N=N, tol=N_tol))
        print('CTR: {ctr}'.format(ctr=ctr))
        print('Min value: {min_val} / Max value: {max_val}'.format(min_val=min_val,
                                                                   max_val=max_val))
        print('Value mean: {mean_val} / Value STD: {std_val}'.format(mean_val=mean_val,
                                                                     std_val=std_val))
        print('Generating observation over {days} days with {dist} as the distribution'.format(
            days=days, dist=days_dist
        ))
    if seed is not None:
        np.random.seed(seed)
    N = rand_group_size(N=N, tol=N_tol)
    converts = np.random.choice([0, 1], size=N, p=[1 - ctr, ctr])
    values = np.multiply(rand_values(min_val, max_val, mean_val, std_val, N), converts)
    day = np.random.choice(np.arange(0, days), p=days_dist, size=N)
    return pd.DataFrame(
        {
            "Treat": [treat] * N,
            "Day": day,
            "Converted": converts,
            "Value": values
        }
    )
```

Here is an example of ~10 observation (for a single group) spread along two days


```python
generate_group_observations(
    N=10, days=2, days_dist=[0.4, 0.6],
    min_val=30, max_val=100, mean_val=60, std_val=20, seed=314)
```

    Generating ~10 samples with tolerance 0.05
    CTR: 0.2
    Min value: 30 / Max value: 100
    Value mean: 60 / Value STD: 20
    Generating observation over 2 days with [0.4, 0.6] as the distribution





<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Converted</th>
      <th>Day</th>
      <th>Treat</th>
      <th>Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>1</td>
      <td>control</td>
      <td>58.682799</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0</td>
      <td>1</td>
      <td>control</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>1</td>
      <td>control</td>
      <td>83.425302</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0</td>
      <td>0</td>
      <td>control</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>0</td>
      <td>control</td>
      <td>37.115954</td>
    </tr>
    <tr>
      <th>5</th>
      <td>1</td>
      <td>0</td>
      <td>control</td>
      <td>85.991153</td>
    </tr>
    <tr>
      <th>6</th>
      <td>0</td>
      <td>1</td>
      <td>control</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>7</th>
      <td>0</td>
      <td>1</td>
      <td>control</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>8</th>
      <td>1</td>
      <td>1</td>
      <td>control</td>
      <td>53.225721</td>
    </tr>
  </tbody>
</table>
</div>



We are now ready to generate a synthetic results set of an A/B test, using the following function.


```python
def generate_observations(N=1000,
                          control_ctr=0.2,
                          control_min_value=50,
                          control_max_value=150,
                          control_mean_sale=80,
                          control_std_sale=20,
                          var_ctr=0.15,
                          var_min_value=50,
                          var_max_value=150,
                          var_mean_sale=90,
                          var_std_sale=30,
                          days=7, days_dist=[1/7] * 7,
                          seed=42,
                          verbose=True
                         ):
    np.random.seed(seed)
    control = generate_group_observations(N=N, days=days, days_dist=days_dist,
                                          ctr=control_ctr, min_val=control_min_value, max_val=control_max_value,
                                          mean_val=control_mean_sale, std_val=control_std_sale,
                                          treat='control',
                                          seed=None, verbose=verbose
                                         )
    var = generate_group_observations(N=N, days=days, days_dist=days_dist,
                                      ctr=var_ctr, min_val=var_min_value, max_val=var_max_value,
                                      mean_val=var_mean_sale, std_val=var_std_sale,
                                      treat='var',
                                      seed=None, verbose=verbose
                                     )

    results = pd.concat([control, var]).reset_index(drop=True)
    return results
```

Here's a ~10 days X 2 (for *control* and *variation* groups) results set


```python
generate_observations(N=10, seed=262, verbose=False)
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Converted</th>
      <th>Day</th>
      <th>Treat</th>
      <th>Value</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>1</td>
      <td>control</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>6</td>
      <td>control</td>
      <td>90.575667</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0</td>
      <td>2</td>
      <td>control</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0</td>
      <td>0</td>
      <td>control</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0</td>
      <td>3</td>
      <td>control</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>5</th>
      <td>0</td>
      <td>6</td>
      <td>control</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>6</th>
      <td>0</td>
      <td>3</td>
      <td>control</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>7</th>
      <td>1</td>
      <td>5</td>
      <td>control</td>
      <td>88.962021</td>
    </tr>
    <tr>
      <th>8</th>
      <td>0</td>
      <td>2</td>
      <td>control</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>9</th>
      <td>0</td>
      <td>3</td>
      <td>control</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>10</th>
      <td>0</td>
      <td>6</td>
      <td>var</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>11</th>
      <td>0</td>
      <td>6</td>
      <td>var</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>12</th>
      <td>1</td>
      <td>6</td>
      <td>var</td>
      <td>61.830611</td>
    </tr>
    <tr>
      <th>13</th>
      <td>0</td>
      <td>2</td>
      <td>var</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>14</th>
      <td>0</td>
      <td>1</td>
      <td>var</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>15</th>
      <td>0</td>
      <td>6</td>
      <td>var</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>16</th>
      <td>0</td>
      <td>6</td>
      <td>var</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>17</th>
      <td>1</td>
      <td>4</td>
      <td>var</td>
      <td>74.639051</td>
    </tr>
    <tr>
      <th>18</th>
      <td>0</td>
      <td>0</td>
      <td>var</td>
      <td>0.000000</td>
    </tr>
  </tbody>
</table>
</div>



## Conversion rate

At this point we want to aggregate the results and compute the metric (a.k.a. proportion) we are after.
In this example we consider the conversion rate.


```python
def agg_conversion(results):
    conversions = results.groupby('Treat')['Converted'].agg(['count', 'sum'])
    conversions.rename(columns={'count': 'Visitors', 'sum': 'Converted'}, inplace=True)
    conversions['Not_converted'] = conversions.Visitors - conversions.Converted
    conversions['CR'] = conversions.Converted / conversions.Visitors
    return conversions
```

For the conversion rate we aggregate the raw events into a *contingency* matrix.
Here is the resulting aggregation of the data generated previously.


```python
agg_conversion(generate_observations(N=10, seed=262, verbose=False))
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>Visitors</th>
      <th>Converted</th>
      <th>Not_converted</th>
      <th>CR</th>
    </tr>
    <tr>
      <th>Treat</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>control</th>
      <td>10</td>
      <td>2</td>
      <td>8</td>
      <td>0.200000</td>
    </tr>
    <tr>
      <th>var</th>
      <td>9</td>
      <td>2</td>
      <td>7</td>
      <td>0.222222</td>
    </tr>
  </tbody>
</table>
</div>



### Conversion rate and sample size

In this example (you have to run the notebook interactively) you can witness how the smaller the sample size is the further off the conversion rate is from the one prescribed in the generation function.

1. Fix the conversion rate for the control and variation groups
2. Play around with $N$. Note that the larger $N$ is the aggregation of the results gets closers to the values set.

For every value of $N$ we generate a synthetic data set and aggregate it to get the observed *conversion rate*.
The synthetic


```python
interact(
    lambda N, control_ctr, var_ctr: print(
        agg_conversion(
            generate_observations(
                seed=None, verbose=False,
                N=N,
                control_ctr=control_ctr,
                var_ctr=var_ctr
            ))['CR']
        ),
    control_ctr=widgets.FloatSlider(value=0.2, min=0, max=1, step=0.05, description='Control CR'),
    var_ctr=widgets.FloatSlider(value=0.15, min=0, max=1, step=0.05, description='Variation CR'),
    N=widgets.IntSlider(min=10,max=5000,step=100,value=1000)
);
```


<p>Failed to display Jupyter Widget of type <code>interactive</code>.</p>
<p>
  If you're reading this message in the Jupyter Notebook or JupyterLab Notebook, it may mean
  that the widgets JavaScript is still loading. If this message persists, it
  likely means that the widgets JavaScript library is either not installed or
  not enabled. See the <a href="https://ipywidgets.readthedocs.io/en/stable/user_install.html">Jupyter
  Widgets Documentation</a> for setup instructions.
</p>
<p>
  If you're reading this message in another frontend (for example, a static
  rendering on GitHub or <a href="https://nbviewer.jupyter.org/">NBViewer</a>),
  it may mean that your frontend doesn't currently support widgets.
</p>



## Experimenting with different statistical tests

First, here is a simple utility to plot a heat map of the the resulting $p$-values.


```python
def plot_experiment(df):
    """
    Utility function to plot a heatmap of the resulting p-values
    """
    plt.figure(figsize=(10,10))
    ax = sns.heatmap(df, cmap=plt.cm.Blues, linecolor='gray',
                     xticklabels=df.columns.values.round(2),
                     linewidths=.02
                    )
    ax.set(xlabel='CR delta', ylabel='N')
    ax.set_yticklabels(rotation=0, labels=Ns);
```

As discussed in the outline, we generate results for various $n$'s and various CTRs of the variant group.


```python
def generate_data(control_ctr, deltas, Ns, seeds_seed=None):
    """
    Generate data for len(Ns)*len(deltas) experiment.
    Each experiment has ~N observation in each group and
    the CTR of the variation is control_ctr+delta
    """
    if seeds_seed is not None:
        np.random.seed(seeds_seed)
    seeds = np.random.randint(0, 2**32 - 1, size=(len(Ns), len(deltas)))
    experiments = [
        [
            generate_observations(
                N=N, control_ctr=control_ctr,
                var_ctr = control_ctr + delta,
                seed=seeds[i][j] if seeds_seed is not None else None,
                verbose=False
            ) for j, delta in enumerate(deltas)
        ] for i, N in enumerate(Ns)
    ]
    return pd.DataFrame(experiments, index=Ns, columns=deltas)
```

*Finally*, generating the data:


```python
deltas = np.linspace(-0.15, 0.15, num=31)
Ns = np.round(np.linspace(10, 10000, num=40)).astype('int64')

data = generate_data(seeds_seed=262, control_ctr=0.2,
                     deltas=deltas, Ns=Ns,
                    )
```

For each A/B test we aggregate the data:


```python
data_agg = data.applymap(agg_conversion)
```

Utility function to element-wise $p$-value computation:


```python
def compute_proportions_pvals(data_agg, test):
    """
    Compute the p-value of a single A/B test.
    `test` is assumed to be from `statsmodels.stats.proportion`
    """
    return data_agg.applymap(lambda x: test(x['Converted'], x['Visitors'])[1])
```

#### $\chi^2$ independence test


```python
pvals_chi2 = compute_proportions_pvals(data_agg, proportion.proportions_chisquare)
plot_experiment(pvals_chi2)
```

    /Users/drorata/anaconda3/envs/z-vs-ch2-tests/lib/python3.6/site-packages/scipy/stats/stats.py:4554: RuntimeWarning: invalid value encountered in true_divide
      terms = (f_obs - f_exp)**2 / f_exp




![png]({static}/images/compare_z_and_chi_square_tests_32_1.png)



### $z$ test


```python
pvals_z = compute_proportions_pvals(data_agg, proportion.proportions_ztest)
plot_experiment(pvals_z)
```

    /Users/drorata/anaconda3/envs/z-vs-ch2-tests/lib/python3.6/site-packages/statsmodels/stats/weightstats.py:670: RuntimeWarning: invalid value encountered in double_scalars
      zstat = value / std_diff




![png]({static}/images/compare_z_and_chi_square_tests_34_1.png)



## Comparing $z$-test and $\chi^2$ test

The results of the element-wise $z$ and $\chi^2$ tests yields an expected visualization.
The smaller the number of samples per group $N$ is and the smaller $\delat$ is we have $p$-values that are larger.
But, and it is not a huge surprise, the visuals for the two different tests seems similar.
Let us check how close are they.


```python
pvals_diffs_close = pd.DataFrame(np.isclose(pvals_chi2, pvals_z))
```


```python
pvals_diffs = (pvals_chi2 - pvals_z).abs()
```


```python
plot_experiment(pvals_diffs)
```



![png]({static}/images/compare_z_and_chi_square_tests_38_0.png)




```python
plot_experiment(pvals_diffs_close.applymap(lambda x: 0 if x else 1))
```



![png]({static}/images/compare_z_and_chi_square_tests_39_0.png)



So we see that except a single(!) case, all $p$-values are the same!
