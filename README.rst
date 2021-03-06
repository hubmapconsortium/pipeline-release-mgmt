.. image:: https://travis-ci.com/hubmapconsortium/salmon-rnaseq.svg?branch=master
    :target: https://travis-ci.com/hubmapconsortium/pipeline-release-mgmt
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

HuBMAP pipeline release management
==================================

Overview
--------

This package provides a convenience script which automates some aspects of
tagging and releasing production-ready versions of HuBMAP computational
analysis pipelines.

Installation
------------

Run ``python3 -m pip install hubmap-pipeline-release-mgmt``.

Usage
-----

Once the package is installed, navigate to a repository containing a
pipeline, and ensure that the ``master`` branch is what you would like
to release as a new tagged version (including the state of any
submodules).

Choose a new version number (preferably starting with ``v``), like ``v1.0``,
and run::

  tag_release_pipeline v1.0

Most of the script is automated, but Git will ask you for a tag message (by
opening a text editor) unless a tag message is given as an argument to this
script via the ``--tag-message`` argument.

To sign Git tags with GPG, append ``--sign`` (and if you want to sign with
a non-default key, add ``--sign=preferred@email.address``).

(Your local ``master`` branch can be behind or ahead of ``origin/master``
-- if behind, it will be updated with ``git pull``, and if ahead
``origin/master`` will be updated with ``git push``. Your ``master`` branch
and ``origin/master`` cannot have *diverged*, however; ``tag_release_pipeline``
will abort if this is the case.)

The ``tag_release_pipeline`` script makes several assumptions about the state
of your repository, and if these assumptions are violated, the script will
probably fail loudly and leave your local copy in an arbitrary state. Make sure
you have no local modifications for best results (though you shouldn't anyway,
if preparing a release version of a pipeline).

At a high level, ``tag_release_pipeline`` does:

* Checkout the ``master`` branch, pull/push so it and ``origin/master`` match
* Checkout or create a ``release`` branch
* Merge ``master`` into ``release``
* Update the content of all submodules to match the versions committed in ``master``
* Build all Docker containers in ``docker_images.txt``, using the
  ``multi-docker-build`` package
* Tag all containers as ``latest`` and with the new tag name
* Push all Docker containers/tags to Docker Hub
* Update all CWL files to use tagged versions of any containers built from the
  pipeline repository (*i.e.* those listed in ``docker_images.txt``)
* Commit the updated CWL files
* Tag the new commit, signed or not
* Push the ``master`` and ``release`` branches, and the new tag

Options:

--pretend   Don't run anything that would make any modifications to any Git
            repositories or Docker images. This will still run
            ``git branch -a`` to obtain the list of Git branches, however.
            This will print all commands which would be run.

--tag-message  (alias: ``-m``) Use this string as the tag message. This is
               given to Git as the ``-m`` argument to ``git tag``, which stops
               Git from asking for a tag message interactively.

--sign      Sign the new tag with GPG using your default identity.

--sign=identity    Sign the new tag with GPG, using the specified
                   identity (email address).

--no-push     Don't push anything to Docker Hub or the Git remote repository.
              Everything will be committed, tagged, and built locally.

Requirements
------------

* Python 3.6 or newer.
* Version 0.3 or newer of the ``multi-docker-build`` PyPI package (which
  should be installed automatically).
