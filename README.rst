================
Modelbrouwers.nl
================

:Version: 2.6.2
:Source: https://github.com/modelbrouwers/modelbrouwers
:Keywords: scale modeling, phpBB3, forum, albums, community

Modelbrouwers.nl is a scale modeling community. The website hosts a phpBB3 board,
albums software and a webshop.

|build| |coverage| |python-versions| |black|

.. |build| image:: https://github.com/modelbrouwers/modelbrouwers/workflows/Run%20CI/badge.svg
    :target: https://github.com/modelbrouwers/modelbrouwers/actions?query=workflow%3A%22Run+CI%22

.. |coverage| image:: https://codecov.io/github/modelbrouwers/modelbrouwers/coverage.svg?branch=main
    :target: https://codecov.io/github/modelbrouwers/modelbrouwers?branch=main

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code style
    :target: https://github.com/psf/black

.. |python-versions| image:: https://img.shields.io/badge/python-3.12-blue.svg
    :alt: Supported Python versions


Introduction
============

This repository contains the majority of software powering the modelbrouwers.nl domain.

The main parts are the phpBB3 board and various apps built in `Django`_, such as:

* album software, tightly integrated in the phpBB3 board
* Kit database with reviews
* Member projects portfolio
* phpBB3 administration through the Django admin.

.. _Django: https://www.djangoproject.com/

Code organization
=================

There are three major parts involved in the modelbrouwers.nl website, each backed by
their own containers and/or databases and interacting with each other.

See ``docker-compose.yml`` to see how the services interact.

phpBB3 forum
------------

phpBB3 is an open-source forum built in PHP, and our choice or even origin story
for the community. See the ``Dockerfile-forum`` for more details.

Django project
--------------

The Django project implements the user accounts, album software and any extra additions
that are not available in phpBB3. Generally we avoid extensions to phpBB3 due to the
increase in maintenance and challenges in quality control.

The idea is rather to implement the necessary functionality in the Django backend,
expose it through the API and consume it with (modern) Javascript in the phpBB3 pages.

The backend build is specified in ``Dockerfile``.

Webshop
-------

The webshop is (for now) based on OpenCart. Modelbrouwers.nl does use some closed source
extensions which live in a private repository. This is orchestrated via the
``opencart-extensions`` git submodule.

You need access to this repository to be able to build the ``Dockerfile-shop`` image,
which is only given to trusted people directly involved with the project.

Setting up the development environment
======================================

Ensure you have the prerequisites installed on your system:

* PostgreSQL database server (django project)
* MySQL/MariaDB database server (phpBB3 and django project)
* Python 3.12
* NodeJS 20+/npm 8+

It is recommended to use a virtualenv.

Advanced users may also find inspiration in the Github CI configuration in
``.github/workflows/ci.yml``.

Installing the dependencies
---------------------------

Install the backend dependencies using pip:

.. code-block:: bash

   pip install -r requirements/dev.txt

Frontend dependencies:

.. code-block:: bash

   npm install

Configuring your environment
----------------------------

Configuration is mostly done through environment variables, which you can specify
in a ``.env`` file in the root of the project/repository.

For all available settings, check ``src/brouwers/conf/base.py`` and look for the
``config`` function calls.

Synchronizing the database(s)
-----------------------------

Run:

.. code-block:: bash

    src/manage.py migrate

You should also create a superuser for local development:

.. code-block:: bash

   src/manage.py createsuperuser

Starting the development server
-------------------------------

**Frontend**

You can either build the frontend once:

.. code-block:: bash

   npm run build

or have the dev server watch for file changes and rebuild the frontend on every change:

.. code-block:: bash

   npm start

**Backend**

Django comes with a development server included.

Start it by invoking:

.. code-block:: bash

   src/manage.py runserver

Point your browser to http://127.0.0.1:8000. You should see a homepage.

For the frontend tooling, you can invoke ``npm start`` which will watch for file changes
and compile the bundles.

Setting up local ``phpBB3``-installation
----------------------------------------

We're currently on the 3.0.x branch. The 3.1.x versions have major backwards
incompatible changes that our code needs adoption for.

The easiest way is probably to run this through the docker setup:

.. code-block:: bash

   docker-compose up phpbb

Tests
-----

Run all tests by executing:

.. code-block:: bash

    src/manage.py test src

Docker
------

The entire stack can be run with docker compose, recommended for local development of
the Javascript/CSS bundles that are used outside of Django.

.. code-block:: bash

    docker-compose -f docker-compose.yml -f docker-compose.dev.yml up

This setup uses your locally installed ``node_modules`` and has the Django dev server
handle static files/assets, while reloading Python code when it changes.

Point your browser at http://localhost/phpBB3/ to view the forum, for example.
