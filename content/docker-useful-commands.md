Title: Useful Docker hints
Date: 2017-04-04
Category: HowTo
Tags: docker, reproducible, research, jupyter
Status: published

Recently, I started to use and get to know [Docker](https://www.docker.com/).
One of my central motivations is to utilize this technology for the creation of reproducible research/work.
The first minimal working example I came up with contains a notebook which loads the data from a CSV file which is part of the image.
You can see the details [here](https://github.com/drorata/mwe-jupyter-docker).
While preparing this image, I came across many useful items; I collected some of them in this post.

## Connecting two containers over network [^7e76b2d7]

[^7e76b2d7]: [source](http://stackoverflow.com/questions/25324860/how-to-create-a-bidirectional-link-between-containers/35577068#35577068)

First, start a new network:

```bash
docker network create new-network
```

Next, start the two containers as follow:

```bash
docker run -i -t --name cont1 --net=new-network --net-alias=cont1 drorata/base-image /bin/bash
docker run -i -t --name cont2 --net=new-network --net-alias=cont2 drorata/base-image /bin/bash
```

## Stop / Remove all running containers [^15cde0e3]

[^15cde0e3]: [source](https://coderwall.com/p/ewk0mq/stop-remove-all-docker-containers)

```bash
docker stop $(docker ps -a -q)
```

The last part generates a list of IDs and in turn this list is passed to the `stop` command.
Similarly,
```bash
docker rm $(docker ps -a -q)
```

will remove all the stoped containers.
You can use the `-f` option for the `rm` for (brutally) stopping and removing all containers.

## Leave a container and keep in alive

If you start a new container in interactive mode and enter the shell, like in `docker run -i -t ubuntu`, and exit it, Docker will stop the container.
You can check it using `docker ps -a`.
The reason is that the process you asked has terminated and the container is stopped.
To avoid it, you can hit `CTRL+P CTRL+Q`.
See this short and excellent [answer](http://stackoverflow.com/questions/25267372/correct-way-to-detach-from-a-container-without-stopping-it) and don't forget to read also [this one](http://stackoverflow.com/a/25268154/671013).

## Using Anaconda from Docker

First, you can run a simple container having full–fledged Anaconda installation.
It is as simple as

```bash
docker run -i -t --name conda-base continuumio/anaconda3 /bin/bash
```

Once running, you can python in the container as much as you want.
As Jupyter is an important part of the work, let's discuss how to use it.
From the container's terminal you can start Jupyter but that won't be enough.
The `localhost` of the container is not the same as of the host OS.
We'd have to enable port forwarding:

```bash
docker run -i -t -p 8888:8888 --name conda-base continuumio/anaconda3 /bin/bash
```

Next, in the new container's shell run

```bash
jupyter notebook --ip='*' --port=8888 --no-browser
```

Go to the address where the notebook is served and enjoy.
There's one thing missing still, the nice notebooks don't have a place to be saved.
They can be saved of course in the container, but they won't persists once you stop it.
You should mount a local directory (on the host) as a data volume:

```
docker run -i -t -p 8888:8888 --name conda-base -v ~/tmp:/opt/notebooks continuumio/anaconda3 /bin/bash
```

and inside the container, execute:

```bash
jupyter notebook --notebook-dir=/opt/notebooks --ip='*' --port=8888 --no-browser
```

Now, what ever notebook you save from within the container, it will be also available on `~/tmp`.
If, for some reason, the container stopped, you can reuse it: `docker exec -it conda-base /bin/bash`.
Lastly, putting everything together, you can instantiate a new container as follow:

```bash
docker run -i -t -p 8888:8888 -v ~/tmp:/opt/notebooks --name conda-base continuumio/anaconda3 /bin/bash -c "/opt/conda/bin/jupyter notebook --notebook-dir=/opt/notebooks --ip='*' --port=8888 --no-browser"
```

### References
* [Mounting local directory](https://docs.docker.com/engine/tutorials/dockervolumes/#mount-a-host-directory-as-a-data-volume)
* [Running notebook from a container](https://www.continuum.io/blog/developer-blog/anaconda-and-docker-better-together-reproducible-data-science)

## Location of images [^167a330e]

[^167a330e]: [source](https://forums.docker.com/t/where-are-images-stored-on-mac-os-x/17165/2)

On Mac images are stored in a file

```bash
$HOME/Library/Containers/com.docker.docker/Data/com.docker.driver.amd64-linux/Docker.qcow2
```

## Running PySpark within Jupyter

The [pyspark-notebook](https://github.com/jupyter/docker-stacks/tree/master/pyspark-notebook) image seems to be a simple and straightforward way to get started with Spark.
Simply run:

```bash
docker run -it --rm -p 8888:8888 jupyter/pyspark-notebook
```

Naturally, you can also mount a local directory for persiting the generated notebooks.
