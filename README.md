==========
# Practice implementations of various algorithms
==========


Description
===========

From basic, textbook to advanced

Python, C++, and others


Typical Python module file layout from this [StackOverFlow](http://stackoverflow.com/questions/15237806/python-modules-hierarchy-naming-convention)

```python
/some-parent-directory # This needs to be on sys.path, the name doesnot matter indeed
    /module
        __init__.py  # import module
        # init is loaded when you `import module` or anything below it
        some.py  # import module.some
        implementation.py  # import module.implementation
        files.py  # import module.files
        /submodule
            __init__.py  # import module.submodule
            # init is loaded when you `import module.submodule` or anything below it
            submodule_impl.py  # import module.submodule.submodule_impl
            goes.py  # import module.submodule.goes
            here.py  # import module.submodule.here
```

Note
====

This project has been set up using PyScaffold 2.5.7. For details and usage
information on PyScaffold see http://pyscaffold.readthedocs.org/.

Add to the `[files]` command in `setup.cfg` the following:

```
namespace_packages =
	top_namespace
```

to add `top_namespace` to the top of your packages

More about [namespace_packages](http://stackoverflow.com/questions/1675734/how-do-i-create-a-namespace-package-in-python) and directory structure.

More about using `setup.cfg` [here](http://stackoverflow.com/questions/27077355/how-to-use-setup-cfg-instead-of-setup-py-with-python-2-7), which basically says that `setup.cfg` file does not provide parameters to the `setup.py` function. It is used to supply parameters to the commands that `setup.py` makes available.
Sample of a fully annotated `setup.cfg` [here](https://www.stsci.edu/svn/ssb/stsci_python/stsci.samplepackage/trunk/setup.cfg.sample)

Toolsets
=======

On mastering the following tools, I am pretty much preapared for my endevour:

- [Python](https://python.org) for scripting, building, sketching, prototyping, i.e. lightly weighing - heavily *abstrative* computing tasks. Applications: Data Analytics, Machine Learning, Services, Backend systems
- [C/C++](https://en.wikipedia.org/wiki/C%2B%2B) for *performance*, under-the-hood engine that powers abstractive calculation. Application: Physics modelling, CFD, time-critical algorithms, extensions for Python functionalities.
- [JavaScript](https://www.javascript.com), currently ES5, for any *front end*, web app related. Great for building tools to allow platform independent, web based user interface. Applications: Data visulizations for algorithms and simulations, learning techniques.
- [Pycallgraph](http://pycallgraph.slowchop.com/en/master/) is pretty cool for analyzing and optimizing Python codes, visually. A great addition to cProfile.
- [Diagram drawing tool - Draw.io](http://draw.io): nice and powerful diagram drawing tool, highly customizable and numerous export options.
- [BFG Repo-Cleaner](https://rtyley.github.io/bfg-repo-cleaner/): a tool to cleanly remove a file AND its history in the repo. [Tutorial](https://github.com/IBM/BluePic/wiki/Using-BFG-Repo-Cleaner-tool-to-remove-sensitive-files-from-your-git-repo). Basically you need: 1) clone the repo 2) from outside the repo (for ex cloned_repo.git) directory use BFG to doctor the repo (most likely `--delete-files` to delete files and their histories). BFG will then modify the repo to make sure that it reflects the changes we made 3) `cd` to the cloned_repo.git, prune it, see tutorial. 4) `git push`

System Design
=============

SQLite can be used for small and medium sites with, emperically less than 100.000 hits / day, more definitely possible but with increasingly struggling performance.

SQLite: < **100.000 / day** ~ **1 hit / second**

Toolkits
========
- [curl](http://www.codingpedia.org/ama/how-to-test-a-rest-api-from-command-line-with-curl/)