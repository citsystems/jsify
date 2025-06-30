Installation
============

Requirements
------------

- **Python 3** (any supported version) is required.
- **C compiler and Python development headers are required** on all platforms, as Jsify includes a C extension and is usually built from source during installation.
  - **Linux:** GCC and Python dev headers (`build-essential python3-dev` on Debian/Ubuntu)
  - **Windows:** Microsoft Visual Studio Build Tools (Desktop development with C++)
  - **macOS:** Xcode command line tools (`xcode-select --install`)
- **pip** and **setuptools** must be installed and up to date.

Quick Install
-------------

Install the latest release from PyPI (pip will build the C extension automatically):

.. code-block:: bash

   pip install jsify

Troubleshooting
---------------

If you see errors like ``Failed building wheel for jsify`` or ``Could not find a version that satisfies the requirement jsify``, check that:

- You have Python 3.x (check with ``python --version``)
- Your C compiler and Python development headers are installed and properly configured for your OS
- pip and setuptools are up to date:

  .. code-block:: bash

     python -m pip install --upgrade pip setuptools

- On Windows, use the "x64 Native Tools Command Prompt for VS" for installation.

Notes
-----

- Jsify will be built and installed in a single step using pip.
- No manual build steps are needed for most users, but you must have the appropriate build environment for your platform.

See Also
--------

- :doc:`jsify_unjsify` for usage and conversion
