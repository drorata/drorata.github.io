Title: Parasitic numbers - did you know?
Date: 2017-01-30
Tags: math
Status: published
Summary: Just learned about a new kind of numbers

# Minimal parasitic number

One of the things I like so much about math is that you always get to know a new concept.
Recently, I learned about [parasitic numbers](https://en.wikipedia.org/wiki/Parasitic_number).
I was asked what is the minimal parasitic 4-number.
So, I wrote down the following simple code, and found out:


```python
def new_num(n):
    n_str = str(n)
    res = n_str[-1:] + n_str[:-1]
    return int(res)
```


```python
def is_num(n, k):
    new_n = new_num(n)
    if new_n == k * n:
        return True
    else:
        return False
```


```python
for i in range(1000000):
    if is_num(i,4):
        print(i)
```

    0
    102564
    128205
    153846
    179487
    205128
    230769
