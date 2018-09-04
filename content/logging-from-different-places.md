Title: An attempt on smarter logging
Date: 2018-09-04
Tags: python
Category: HowTo
Status: published


## Motivation

Consider the case where you implement some logic somewhere, and this logic should be used from within several different places.
Think of a logic and two apps using it.
The logic should be yielding logging messages that would be visible as part of the running of the different apps.
And here comes the additional requirement; the first app should use STDOUT for logging and the second should write the log messages to a file.
Or, another possible requirement could be that the logging format should be different depending on the calling app.

In other words, the log messages yielded by the logic should merely be piped to one or more handlers managed by the calling app.
In this example, you will see my workaround this problem.
I hope you will find this solution helpful.
Please comment if you have questions, suggestions etc.

## The solution

### Start with the logic

Here is a dead simple logic:

```
#!python
# package1/package1/foo.py

import logging

logger = logging.getLogger(__name__)


def foo_func():
    logger.info("__name__ = " + __name__)
    logger.info('Info from foo')
```

The key line here is the definition of the logger (line 5); it is associated with `__name__`.
This way, whatever `__name__` might be, `logger` will always be a child of the root logger.
And this is the trick, namely, an app calling this logic should use the root logger.

### The first app

Now we can implement the first app:

```python
#!/usr/bin/env python3

# package1/package1/app1.py

import logging
import foo

logger = logging.getLogger()

logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


def main():
    logger.info('Info from main app1')
    logger.info("__name__ = " + __name__)
    foo.foo_func()


if __name__ == "__main__":
    main()
```

Note that here the `logger` is the root one and we can define the handler to be used.


### The second app

Similarly to the first one, the second should use the root logger as well.
Check this out:

```python
#!/usr/bin/env python3

# package2/package2/app2.py

import logging
import package1.foo as foo


def main():
    logger = logging.getLogger()
    # logger = logging.getLogger('log_example')

    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(levelname)s <-> %(asctime)s - %(name)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    logger.info('Info from main app2')
    logger.info("__name__ = " + __name__)
    foo.foo_func()


if __name__ == "__main__":
    main()
```

## Putting all together

This [git repository](https://gitlab.com/drorata/log-example) holds a complete example, including a `Dockerfile` which allows you to try out this setting.
Clone the repository and build the docker image.
Invoke the following from the project's root.

```bash
docker build -t log-example .
```

Next, you can simply checkout the different output; compare:

```bash
docker run -it --rm log-example /package1/package1/app1.py
```

which yields:

```
2018-08-30 17:08:31,117 - root - INFO - Info from main app1
2018-08-30 17:08:31,117 - root - INFO - __name__ = __main__
2018-08-30 17:08:31,117 - foo - INFO - __name__ = foo
2018-08-30 17:08:31,118 - foo - INFO - Info from foo
```

and

```bash
docker run -it --rm log-example /package2/package2/app2.py
```

which yields:

```
INFO <-> 2018-08-30 17:08:40,143 - root - Info from main app2
INFO <-> 2018-08-30 17:08:40,143 - root - __name__ = __main__
INFO <-> 2018-08-30 17:08:40,144 - package1.foo - __name__ = package1.foo
INFO <-> 2018-08-30 17:08:40,144 - package1.foo - Info from foo
```

### Two things to note

First, pay attention to the different `__name__`'s in use.
Understanding them will help you modify this approach as per your needs.
Secondly, note the different formatting of the messages.
This is governed by the definitions in the apps and not all by the logic!
By defining a different or additional handle, you could, for instance, write the log messages when using the second app to a [rotating file](https://docs.python.org/3/library/logging.handlers.html#logging.handlers.RotatingFileHandler).

Lastly, thanks to [deeplook](https://github.com/deeplook) for his help :)

That's it.
Happy logging!

