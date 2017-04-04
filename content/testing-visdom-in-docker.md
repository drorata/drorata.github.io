Title: Running Visdom examples within a Docker container
Date: 2017-04-04
Status: published
Tags: docker, visualization
Category: HowTo

Docker could be a great tool when you want to try out new technologies without taking the risk of breaking your own system.
I decided to use Docker when having a quick look into [Visdom](https://github.com/facebookresearch/visdom) the new toy from Facebook.
I'll outline the steps I took.

## Start a minimal container

Here I decided to use the readymade [continuumio/anaconda3](https://hub.docker.com/r/continuumio/anaconda3/).
I started a container:

```bash
docker run -i -t -p 8097:8097 -v ~/tmp:/opt/notebooks --name visdom-test continuumio/anaconda3 /bin/bash
```

Next, I installed `Visdom`:

```bash
pip install visdom
```

Lastly, I could run the server:

```bash
python -m visdom.server
```

At this point I could open [`http://localhost:8097`](http://localhost:8097) and see the empty visualization.

## Running some examples

### Basic example

I placed a file `fb-visdom-example.py` in `~/tmp` containing the example:

```python
import visdom
import numpy as np
vis = visdom.Visdom()
vis.text('Hello, world!')
vis.image(np.ones((3, 10, 10)))
```

Then, I started another `bash` process on my container:

```bash
docker exec -it visdom-test /bin/bash
```

From the new console I could run the example `python /opt/notebooks/fb-visdom-example.py`

### Running `demo.py`

Now, I wanted to run [`demo.py`](https://github.com/facebookresearch/visdom/blob/master/example/demo.py).
To that end I simply cloned the repository:

```bash
cd /
git clone https://github.com/facebookresearch/visdom.git
```

and ran the example `python /visdom/example/demo.py`.
As a matter of fact, this example breaks on this setting with the following error:

```python
Traceback (most recent call last):
  File "visdom/example/demo.py", line 232, in <module>
    viz.mesh(X=X, Y=Y, opts=dict(opacity=0.5))
AttributeError: 'Visdom' object has no attribute 'mesh'
```

It is almost the end of the demo, but still a little annoying; I opened a [bug](https://github.com/facebookresearch/visdom/issues/59).
It turns out that you'd have to install `Visdom` from the sources and not using `pip` in order to avoid this problem.
