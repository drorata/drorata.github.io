Title: Installing Spark on macOS (Sierra)
Date: 2017-01-16
Category: HowTo
Tags: spark, jupyter, python
Summary: How did I install Spark on my macOS
Status: published

[TOC]

# Download Spark

- First, download Spark.
I downloaded the binaries given as [`spark-2.1.0-bin-hadoop2.7`](http://d3kbcqa49mib13.cloudfront.net/spark-2.1.0-bin-hadoop2.7.tgz)
- You'd also need to install the JDK; I took it from [here](http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html)

# Set and test

## Tree structure
Simply installing Spark is simple.
All you have to do is extract the archive.
I placed the extracted binaries in `~/Applications`, resulting in the following tree structure:

```
~/Applications
└── spark-2.1.0-bin-hadoop2.7
```

At this point, you can already run Spark.
Look for `~/Applications/spark-2.1.0-bin-hadoop2.7/bin/pyspark`.
For simplifying the settings, I created a symbolic link to `~/Applications/spark`, in particular using `ln -s spark-2.1.0-bin-hadoop2.7 spark`, yielding the following structure:

```
~/Applications
├── spark -> spark-2.1.0-bin-hadoop2.7
└── spark-2.1.0-bin-hadoop2.7
```

## Environment variables

Next step, is to set environment variables.
In particular, I added the following lines to `~/.bash_profile`:

```bash
export SPARK_HOME="/Users/user/Applications/spark"
export PYSPARK_SUBMIT_ARGS="--master local[2]"
# Make pyspark available anywhere
export PATH="$SPARK_HOME/bin:$PATH"
```

_Remark:_ `spark-shell` (i.e. the scala based REPL) should also be accessible at this point.
## Test
Now, it is time fore testing.
Start a new terminal session, or source `/.bash_profile`.
Now, simply run `pyspark`.
You should get a Python REPL console with the `SparkContext` already loaded as `sc`.
Tryout:
```python
x = sc.parallelize([1,2,3])
```
and create a simple RDD.

# Use `IPython` and `Jupyter`

The standard Python REPL is, somehow, crappy.
You probably want to use `IPython` and even better `Jupyter`.
To that end, I added the following to my `./bash_profile`:

```bash
export PYSPARK_PYTHON=/Users/drorata/anaconda3
export PYSPARK_DRIVER_PYTHON=/Users/drorata/anaconda3/bin/ipython
alias pysparknb='PYSPARK_DRIVER_PYTHON="jupyter" PYSPARK_DRIVER_PYTHON_OPTS="notebook" pyspark'
```

This way, whenever I invoke `pyspark` a nice IPython console is started.
In addition `pysparknb` starts a Jupyter server in the current directory.
