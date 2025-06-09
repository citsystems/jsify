.. _installation:

.. meta::
   :keywords: Jsify, Python, pip, installation, PyPI, upgrade, setup, install Jsify, Python package
   :description: Learn how to install the Jsify library using pip from PyPI. This guide provides step-by-step instructions for setting up Jsify in your Python environment, verifying the installation, and upgrading to the latest version.

Installation
============

Jsify can be easily installed via pip from PyPI. Follow the instructions below to set up Jsify in your Python environment.

Using pip
---------

To install Jsify using pip, run the following command:

.. code-block:: bash

    pip install jsify

This will install the latest version of Jsify and its dependencies.

**Note:**
If there is no prebuilt wheel available for your Python version or platform, pip will attempt to build Jsify from source.
To compile successfully, you need a working C compiler and Python development headers (e.g. `python3-dev` on Debian/Ubuntu).

.. code-block:: bash

    # On Debian/Ubuntu:
    sudo apt install build-essential python3-dev

    # Then run:
    pip install jsify

If you encounter errors during compilation, please check your compiler setup and ensure your environment is ready for building C extensions.

Verifying the Installation
--------------------------

To verify that Jsify is installed correctly, run a simple Python script to import the library:

.. code-block:: python

    import jsify

    print(jsify.__version__)

If Jsify is installed correctly, this script should output the version number of the installed package.

Upgrading Jsify
---------------

To upgrade Jsify to the latest version, use:

.. code-block:: bash

    pip install --upgrade jsify

This will upgrade Jsify to the most recent version available on PyPI.
