python-urlsync
==============

Ever get caught downloading large files from a public location in a script that gets
run a lot? If that seems like a waste of time, `urlsync` is for you! It's very simple
and easy to use from the command line or within a python script.

Installation
------------

From an activated virtual environment, simply type:

```pip install git+https://github.com/ajk8/fencepy```

Usage
-----

From the command line:

```urlsync URL```

The above command will download the file at URL to a file of the same name in the cwd.
More usages can be found by typing:

```urlsync -h```
