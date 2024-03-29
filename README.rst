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
pipeline, and ensure that the main branch is what you would like
to release as a new tagged version, including the *committed* state of any
submodules. (See Configuration_ for setting persistent configuration
parameters globally or for each pipeline, including the name of the "main"
branch.)

Choose a new version number (preferably starting with ``v``), like ``v1.0``,
and run::

  tag_release_pipeline v1.0

Most of the script is automated, but Git will ask you for a tag message (by
opening a text editor) unless a tag message is given as an argument to this
script via the ``--tag-message`` argument.

To sign Git tags with GPG, append ``--sign`` (and if you want to sign with
a non-default key, add ``--sign=preferred@email.address``).

(Your local main branch can be behind or ahead of its remote version
-- if behind, it will be updated with ``git pull``, and if ahead
the remote branch will be updated with ``git push``. Your main branch
and its remote version cannot have *diverged*, however; ``tag_release_pipeline``
will abort if this is the case.)

The ``tag_release_pipeline`` script makes several assumptions about the state
of your repository, and if these assumptions are violated, the script will
probably fail loudly and leave your local copy in an arbitrary state. Make sure
you have no local modifications for best results (though you shouldn't anyway,
if preparing a release version of a pipeline).

At a high level, ``tag_release_pipeline`` does:

* Checkout the main branch, pull/push so it and its remote version match
* Checkout or create a release branch, ``git pull --ff-only`` if checking out
  a local branch that already exists
* Sync the main branch to the release branch -- note that this is *not* a
  merge; the previous contents of the release branch are overwritten entirely
* Update the content of all submodules to match the versions committed in the
  main branch
* Build all Docker images in ``docker_images.txt``, using the
  ``multi-docker-build`` package
* Tag all images as ``latest`` and with the new tag name
* Push all Docker images/tags to Docker Hub
* Update all CWL files to use tagged versions of any images built from the
  pipeline repository (*i.e.* those listed in ``docker_images.txt``)
* Commit the updated CWL files (on the release branch)
* Tag the new commit, signed or not
* Push the main and release branches, and the new tag

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

--main-branch   Name of the main branch. Overrides the default (``master``)
                and anything found in configuration files.

--release-branch   Name of the release branch. Overrides the default (``release``)
                   and anything found in configuration files.

--remote-repository   Name of the remote repository. Overrides the default
                      (``origin``) and anything found in configuration files.

Configuration
-------------

This package uses the `confuse <https://confuse.readthedocs.io/en/latest/>`_
library to read user and pipeline configuration. The default configuration
specifies branch names, the remote repository name, and whether to sign each
release version of a pipeline, via the following contents of
``config_default.yaml``::

  main_branch: master
  release_branch: release
  remote_repository: origin
  sign: false

This configuration can be overridden globally (affecting all usage of this
package) and separately for each repository. These configuration parameters
are read in this order, with each source overriding earlier ones:

1. Package default configuration shown above
2. Global (user) configuration from ``~/.config/hubmap_pipeline_release_mgmt/config.yaml``
   (on Linux)
3. Pipeline configuration options, from ``pipeline_release_mgmt.yaml`` in the
   base directory of the pipeline repository
4. Command-line arguments passed to the ``tag_release_pipeline`` script

For example, to sign all Git tags by default with a specific GPG key, you could
create the user configuration file noted above, containing::

  sign: mruffalo@cs.cmu.edu

The default ``main_branch`` of ``master`` is likely to change in the near future.

Requirements
------------

Python 3.6 or newer.

The following package dependencies should be automatically installed when
installing via ``pip`` or ``python setup.py install``:

* Version 0.7.1 or newer of the ``multi-docker-build`` PyPI package
* `confuse <https://confuse.readthedocs.io/en/latest/>`_, (recent) version
  unimportant
