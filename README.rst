.. image:: https://travis-ci.org/modelbrouwers/modelbrouwers.png?branch=master   :target: https://travis-ci.org/modelbrouwers/modelbrouwers

######################################
Modelbrouwers Apps & phpBB integration
######################################

Modelbrouwers.nl is a scale modelling community. We couple a phpBB3 board with
custom developed apps in `Django`_:

* Album software, integrated with the board
* Awards, allowing nomination and voting of topics
* Secret Santa app
* Builds overview, add your build topic with metadata to a personal database.
* phpBB3 administration through the Django admin.

.. _Django: https://www.djangoproject.com/

**************************************
Setting up the development environment
**************************************

For new developers, setting up the environment can be overwhelming at first. Don't
hesitate to contact BBT on the Modelbrouwers.nl IRC chat.

Installing ``Python``
=====================
Python is the programming language Django is written in.
Python 2.6 is the minimum required Python version, but 2.7 is recommended,
as the server runs this version.

On Windows, get Python 2.7 here: `Python installer`_.

.. note:: A 64-bit version exists, but often causes problems with third party libraries.
          It's advisory to install a 32-bit Python version.

.. note:: Often problems arise with the $PATH variable and the 'python' command
          not being available in a shell. See `stackoverflow`_ for a resolution.


On Linux Python mostly comes with the distro and should be a recent version.


.. _Python installer: http://www.python.org/ftp/python/2.7.6/python-2.7.6.msi
.. _stackoverflow: http://stackoverflow.com/questions/3701646/how-to-add-to-the-pythonpath-in-windows-7


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

    [user@host]$ mkvirtualenv brouwers

And activate it::

    [user@host]$ workon brouwers

``cd`` to your project folder, e.g.::

    (brouwers)[user@host]$ cd C:\User\my-user\brouwers

Clone the repository with your favorite tool, e.g. on the commandline::

    (brouwers)[user@host]$ git clone https://github.com/modelbrouwers/modelbrouwers.git C:\User\my-user\brouwers

or use the Windows Git client (recommended for inexperienced users)


Installing ``django`` and the project dependencies
==================================================
All dependencies are in `requirements.txt`. Install with::

    (brouwers)[user@host]$ pip install -r requirements.txt

These will be installed in your virtualenv.

Create the settings
===================
The settings module is still WIP and needs proper testing. For now you can create
the required settings this way::

    (brouwers)[user@host]$ cd C:\User\my-user\brouwers\brouwers
    (brouwers)[user@host]$ python create_local_settings.py
    (brouwers)[user@host]$ python create_settings.py

And verify the files ``settings.py`` and ``local_settings.py``. Make sure to use
the ``sqlite3`` database backend if you have no MySQL or Postgres database running.

Only the 'default' database is required, unless you need to test the phpBB3 integration.

Creating the database
=====================
Run::

    (brouwers)[user@host]$ python manage.py syncdb --migrate

This creates the database and runs all required migrations.

Load the testdata by executing::

    (brouwers)[user@host]$ python manage.py loaddata testdata.json

Finally, create a superuser account::

    (brouwers)[user@host]$ python manage.py createsuperuser

Fill out the prompts. You now have a user with all access.

Starting the development server
===============================

Django comes with a development server included.

Start it by invoking::

    (brouwers)[user@host]$ python manage.py runserver

Point your browser to http://127.0.0.1:8000. You should see a homepage.

Setting up local ``phpBB3``-installation
========================================
(TODO)

Tests
=====
WIP