Title: Custom Enums and tests
Date: 2018-11-22
Status: published
Category: General
Tags: python, superuser
Summary: Somehow advanced usage of python's enums. Including a discussion on testing of those custom entities.

(Original notebook can be found in [this gist](https://gist.github.com/drorata/ab47b78dc5ad5cf681909b054ea51c4c))

## Motivation

Assume you want to share across your application a smart list of constants.
For example, a list of colors supported by your application.
One way probably could be a `list` in some module along with some replated logic implemented.
In this post, you will learn how I tackled this issue.

## Enums in Python

There are a lot of resources about Enums in Python and probably the best place to start are the [docs](https://docs.python.org/3/library/enum.html).
Let us start with a simple example.


```python
from enum import Enum
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
```

This is great; you can check the value of `RED`:


```python
Color.RED
```




    <Color.RED: 1>



Recall, that the objective is to come up with a solution enabling a little more logic.
In particular, you want to have two functionalities:

1. Nice printout of the supported colors
1. Checking whether a given color is supported

## Customizing `Color`

Here is the definition of the customized class.


```python
from enum import EnumMeta


class MyEnumMeta(EnumMeta):
    def __str__(cls):
        lines = [f"Members of `{cls.__name__}` are:"]
        for member in cls:
            lines.append(f"- {member}")
        return '\n'.join(lines)

    def _contains(self, member):
        return member in self._member_map_ \
            or member in set(
                map(lambda x: x.value, self._member_map_.values()))

    def is_valid(self, member):
        if self._contains(member):
            return True
        else:
            return False


class Color(Enum, metaclass=MyEnumMeta):
    RED = 1
    GREEN = 2
    BLUE = 3
```

Now, your `Color` can do much more:


```python
print(Color)
```

    Members of `Color` are:
    - Color.RED
    - Color.GREEN
    - Color.BLUE


or, alternatively:


```python
Color.is_valid('RED'), Color.is_valid('YELLOW')
```




    (True, False)



I am sure you can take it from here, improve and modify the implementation as per your needs.
But, before doing so, you might want to see how the custom `Color` can be used, and, more importantly, tested.

## Using the custom `Color`

Here is an example of how we can use the custom `Color`:


```python
def foo(type):
    if Color.is_valid(type):
        print(f"Wonderful! we will use the wonderful {type} color")
        return "valid"
    else:
        print(f"{type} is not supported color. The supported colors are:\n{str(Color)}")
        return "invalid"
```

And here are some examples:


```python
foo('RED')
```

    Wonderful! we will use the wonderful RED color





    'valid'




```python
foo('BLUE')
```

    Wonderful! we will use the wonderful BLUE color





    'valid'




```python
foo('YELLOW')
```

    YELLOW is not supported color. The supported colors are:
    Members of `Color` are:
    - Color.RED
    - Color.GREEN
    - Color.BLUE





    'invalid'



## Testing `foo`

Next, you want to test `foo`.
But, as you want it to be a proper unit test, you don't want to refer to the values of `Color`.
That is, you want to patch `Color` and use some value defined within the scope of the test.
Here is the way to do that.


```python
import unittest
from unittest.mock import patch


class DummyColor(Enum, metaclass=MyEnumMeta):
    TEST_TYPE1 = 1
    TEST_TYPE2 = 10


class MyTest(unittest.TestCase):

    def test_a(self):
        # Without any patch, you are depending on the
        # values of `Color`
        assert foo('RED') == 'valid'
        assert foo('YELLOW') == 'invalid'

    @patch('__main__.Color', DummyColor)  # Make sure you patch the right `Color`
                                          # it should be within the class you want to test
    def test_b(self):
        assert foo('TEST_TYPE1') == 'valid'
        assert foo('TEST_TYPE10') == 'invalid'
```


```python
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
```

    ..

    Wonderful! we will use the wonderful RED color
    YELLOW is not supported color. The supported colors are:
    Members of `Color` are:
    - Color.RED
    - Color.GREEN
    - Color.BLUE
    Wonderful! we will use the wonderful TEST_TYPE1 color
    TEST_TYPE10 is not supported color. The supported colors are:
    Members of `DummyColor` are:
    - DummyColor.TEST_TYPE1
    - DummyColor.TEST_TYPE2



    ----------------------------------------------------------------------
    Ran 2 tests in 0.002s

    OK


## Summary

I hope you found it useful.
As a bonus, here is more or less the same example, given in scripts.
You can save the three of theme somewhere and run `pytest` to see how everything works together.

### `special_enum.py`

```python
# Implementation of the customized enum
from enum import Enum, EnumMeta


class MyEnumMeta(EnumMeta):
    def __str__(cls):
        lines = [f"Members of `{cls.__name__}` are:"]
        for member in cls:
            lines.append(f"- {member}")
        return '\n'.join(lines)

    def _contains(self, member):
        return member in self._member_map_ \
            or member in set(
                map(lambda x: x.value, self._member_map_.values()))

    def is_valid(self, member):
        if self._contains(member):
            return True
        else:
            return False


class SpecialEnum(Enum, metaclass=MyEnumMeta):
    TYPE1 = 1
    TYPE2 = 10
```

### `foo.py`

```python
# Your amazing logic!
from special_enum import SpecialEnum


def bar(type):
    print(SpecialEnum)  # Just for debugging
    if SpecialEnum.is_valid(type):
        return "valid"
    else:
        return "invalid"
```

### `test_foo.py`

```python
# The testing script
import unittest
from unittest.mock import patch
import foo
from special_enum import MyEnumMeta
from enum import Enum


class SpecialEnumTest(Enum, metaclass=MyEnumMeta):
    TEST_TYPE1 = 1
    TEST_TYPE2 = 10


class MyTest(unittest.TestCase):

    def test_a(self):
        # Passes as it is ussing the original SpecialEnum
        assert foo.bar('TYPE1') == 'valid'
        assert foo.bar('TYPE10') == 'invalid'

    @patch('foo.SpecialEnum', SpecialEnumTest)
    def test_b(self):
        assert foo.bar('TEST_TYPE1') == 'valid'
        assert foo.bar('TEST_TYPE10') == 'invalid'
```
