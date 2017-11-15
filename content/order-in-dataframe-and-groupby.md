Title: The importance of order
Date: 2017-11-14
Status: published
Category: HowTo
Tags: python, pandas
Summary: When grouping by DataFrame the order does matter and may be surprising.

Consider the following simply table:

```python
df = pd.DataFrame(
    {
        "cat": [1,1,1,3,2,2,2,3],
        "val": [1,2,3,4,3,2,5,1]
    }
)
```

and the following three different grouping by:

```python
df.groupby('cat')['val'].apply(tuple)
df.sort_values('val').groupby('cat')['val'].apply(tuple)
df.sort_values('val', ascending=False).groupby('cat')['val'].apply(tuple)
```

If you'd try it out, you will find that each yields a different order in the generated tuple for each group.
This should not come as a surprise, but one *should* be aware of it!
