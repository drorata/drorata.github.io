Title: Experiment with Jupyter
Date: 2017-01-18
Modified: 2022-08-11
Category: HowTo
Tags: python, jupyter, pelican, blogging
Status: published
Summary: Outline how to utilize Jupyter notebooks.

**UPDATE:** The `liquid_tags` solution seems to have changed a lot and embedding Jupyter notebooks became a little harder.
Therefore, I'm porting all notebooks to Markdown.
In the future I will try to find a better solution.

The notebook `factorial-sample.ipynb` has been removed.

<hr>

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

## Example

The next line till the end of the post is coming from a notebook:

{% notebook factorial-sample.ipynb %}
