Title: Experiment with Jupyter
Date: 2017-01-18
Category: HowTo
Tags: python, jupyter, pelican, blogging
Status: published
Summary: Outline how to utilize Jupyter notebooks.

Using the [liquid_tags](https://github.com/getpelican/pelican-plugins/tree/master/liquid_tags) plugin, it seems to be very simple to include Jupyter notebooks. You have to add the plugin in `pelicanconf.py`; e.g.:

```python
PLUGIN_PATHS = ["plugins"]
PLUGINS = ["render_math", "liquid_tags.notebook"]
```

Where in my case the plugins are located in `[site's root]/plugins`.
Next, create a directory `[site's root]/content/notebooks` and add a notebook in there.
Lastly, create a new Markdown post and include the following:

```
{% notebook factorial-sample.ipynb %}
```
where `factorial-sample.ipynb` is the notebook's filename.
Don't forget to include in the post (`.md`) the needed metadata like `Title`, `Date` etc.

$\cos(x) = y^2$

## Example

The next line till the end of the post is coming from a notebook:

{% notebook factorial-sample.ipynb %}
