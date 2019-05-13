
.. image:: https://travis-ci.org/modelbrouwers/modelbrouwers.svg?branch=master
    :target: https://travis-ci.org/modelbrouwers/modelbrouwers

.. image:: https://coveralls.io/repos/modelbrouwers/modelbrouwers/badge.png
    :target: https://coveralls.io/r/modelbrouwers/modelbrouwers

.. image:: https://codecov.io/github/modelbrouwers/modelbrouwers/coverage.svg?branch=master
    :target: https://codecov.io/github/modelbrouwers/modelbrouwers?branch=master

.. image:: https://landscape.io/github/modelbrouwers/modelbrouwers/master/landscape.svg?style=plastic
    :target: https://landscape.io/github/modelbrouwers/modelbrouwers/master
    :alt: Code Health

.. image:: https://requires.io/github/modelbrouwers/modelbrouwers/requirements.svg?branch=master
     :target: https://requires.io/github/modelbrouwers/modelbrouwers/requirements/?branch=master
     :alt: Requirements Status

######################################
Modelbrouwers Apps & phpBB integration
######################################

Modelbrouwers.nl is a scale modelling community. We couple a phpBB3 board with
custom developed apps in `Django`_:

* Album software, integrated with the board
* Groupbuilds managed and integrated in the board
* Awards, allowing nomination and voting of topics
* Kit database with reviews
* Builds overview, add your build topic with metadata to a personal database.
* phpBB3 administration through the Django admin.

.. _Django: https://www.djangoproject.com/

**************************************
Setting up the development environment
**************************************

For new developers, setting up the environment can be overwhelming at first. Don't
hesitate to contact BBT on the Modelbrouwers.nl IRC chat or forum itself.

Installing ``Python``
=====================

Python is the programming language Django is written in. You need Python 3.6 to
run the project.

Installing ``virtualenv`` and ``virtualenvwrapper``
===================================================
``virtualenv`` creates isolated Python environments on your system, allowing
multiple versions of libraries to be installed without interfering each other.

``virtualenvwrapper`` provides a more intuitive interface to use these environments.

Both are optional, but highly recommended!

On Linux, consult distro specific guides. For windows, the installer is available
on `Pypi`_.

.. _Pypi: https://pypi.python.org/pypi/virtualenvwrapper-win


Initializing the project
========================
You only need to do this once to configure the project environment.

Start with creating a virtualenv::

    $ mkvirtualenv brouwers

Or with regular ``virtualenv``::

    $ virtualenv myenv

And activate it::

    $ workon brouwers

(regular virtualenv, Linux/OSX)::

    $ source myenv/bin/activate

``cd`` to your project folder, e.g.::

    $ cd /home/me/code

Fork the repository on GitHub (button is above) and clone the fork with your
favorite tool, e.g. on the commandline::

    $ git clone https://github.com/<my-github-account>/modelbrouwers.git

or use the Windows Git client (recommended for inexperienced users)


Installing ``django`` and the project dependencies
==================================================
All dependencies are in the `requirements` folder, grouped by the environment type (development, staging, production). Install with::

    $ pip install -r requirements/development.txt

These will be installed in your virtualenv.


Installing front-end dependencies
=================================

Make sure npm is installed globally. Then run::

    $ npm install

This will install all the necessary front-end dependencies.

Create the settings
===================

You need some settings to get the project up. For security reasons, sensitive
data lives in ``secrets.py``

Copy ``src/conf/settings/secrets.py_example`` to ``secrets.py``.

Edit secrets.py to include your own settings. You can generate a secret key here: `SecretKey`_.

.. _SecretKey: http://www.miniwebtool.com/django-secret-key-generator/

The base file is base.py, and is included by ``settings/development.py`` for instance.


All available database backends are in the example file, for local development
it's easiest if everything is changed to sqlite3 (like the
``DATABASES['sqlite3']`` example). Both the 'default' and 'mysql' database must
be present.

In production the Django tables live in a postgresql database, while the phpBB3
tables live in MySQL. Replicating this environment is probably the most robust
during development.

Creating the database
=====================

Run::

    $ python src/manage.py migrate

This creates the database if you're running sqlite and runs all required migrations.

Finally, create a superuser account::

    $ python src/manage.py createsuperuser

Fill out the prompts. You now have a user with all permissions.

Starting the development server
===============================

Django comes with a development server included.

Start it by invoking::

    $ python src/manage.py runserver

Point your browser to http://127.0.0.1:8000. You should see a homepage.

Setting up local ``phpBB3``-installation
========================================

We're currently on the 3.0.x branch. The 3.1.x versions have major backwards
incompatible changes that our code needs adoption for.

To install phpBB3, you'll need a full fledged PHP stack with a (MySQL) database.

The `docker forum setup`_ makes this available using Docker.

Tests
=====

Run all tests by executing::

    $ python src/manage.py test src


Thanks
======

Thanks to `browserstack`_ to make cross browser testing a breeze.

.. _browsersstdack: https://www.browserstack.com

.. _docker forum setup: https://github.com/modelbrouwers/forum
