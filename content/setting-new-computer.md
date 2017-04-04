Title: Setting new computer
Date: 2017-03-16
Modified: 2017-04-04
Category: General
Tags: IT, computer, apps, settings, superuser, python
Status: published
Summary: Mostly notes for myself on what items I installed on a new machine. You might be interested as well.

# Straightforward

* `Docker` Time to start using it, right?
* `DropboxInstaller`
* `Franz` a universal messenger
* `Spotify`
* `LibreOffice`
* `MacPorts` For this one you'd need to install XCode related stuff
* `Skim` Much better than the built in Preview
* `Skype`
* `Slack`
* `Spectacle` Super useful for windows management using the keyboard
* `atom` Well, this is my editor of choice for the past 4 months. I'm not going to change it.
* `Chrome`
* `iTerm2`. However, I'm going to try out `Hyper`
* Google drive
* `mactex`
* `nteract`
* `vlc`
* Anaconda python distribution
* In addition I installed [`json_resume`](https://github.com/prat0318/json_resume) which I use to build my CV.

# Some more remarks

## Setting of Atom
For this I discovered the wonderful plugin [sync-settings](https://atom.io/packages/sync-settings).
This allowed easy copying of the settings and packages from my other box.

## Improved commandline
To that end I use [powerline-shell](https://github.com/banga/powerline-shell) which I strongly recommend.

## Enabling Pelican
Pelican is easy to install using `pip`.
However, in addition I had to install the `Markdown` module.

## Mapping `§` to `` ` ``
I got an international English keyboard.
This means that the upper left key (right under the `ESC`) is mapped to `§` and `±`.
I lived so long without using these symbols on a regular basis, and thus I decided to map this key to the regular backtick and tilde (`~`).
To that end I used the [Karabiner-Elements](https://github.com/tekezo/Karabiner-Elements).

## `vim` syntax highlighting
I'm using `vim` as the editor in the console (mostly when it comes to commit messages for git).
Still, coloring the editor is nice.
I Simply added `syntax on` to `~/.vimrc`.

## N.B. 1

After couple of days, as always, there are some additional items to mention:

* [nb conda kernels](https://github.com/Anaconda-Platform/nb_conda_kernels) to treat Conda environments as Jupyter kernels
* For [decision trees visualization](http://scikit-learn.org/stable/modules/tree.html#classification) I had to install `GraphViz` and `pydotplus`. The former using MacPorts and the latter using `conda install -c conda-forge pydotplus`.
* [`pandoc`](http://pandoc.org/) is a nice to have around
* Similarly, [`jq`](https://github.com/stedolan/jq/wiki/Installation) is very important to have around; simply using MacPorts. In addition, [`ack`](https://beyondgrep.com/) is worthy installing

## N.B. 2

How could I forget, spell checking for Jupyter notebooks and other extensions are a must. This is rather straightforward as described [here](https://github.com/ipython-contrib/jupyter_contrib_nbextensions).

## N.B. 3

When inspecting a file from the console, it is nice to see it colored properly.
A nice way to go about it is to install `Pygments`.
This can be easily done: `conda install Pygments`.
Next, in `~/.bash_profile` I added the following alias `alias catc='pygmentize -g'`.
