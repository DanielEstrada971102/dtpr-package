.. DT Pattern Recognition documentation master file, created by
   sphinx-quickstart on Thu Nov 28 01:21:14 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

DT Pattern Recognition Package
==============================
This package provides a set of base tools for implementing pattern recognition algorithms using 
input data in Ntuple format. It also includes visualization tools for DT Ntuples, taking into account
the geometrical features of the CMS DT system.

Installation
------------

First, download the source files or clone the repository:

.. code-block:: bash

   git clone https://github.com/DanielEstrada971102/dtpr-package.git
   cd dtpr-package

You can then install the package with pip by running:

.. code-block:: bash

   pip install .

To check if the package was installed successfully, run:

.. code-block:: bash

   pip show dtpr

.. important::
   Be aware that the package requires PyROOT, so you should have it installed. If you are working in
   a Python virtual environment, ensure to include ROOT in it. To do this, use the command:

   .. code-block:: bash

      python -m venv --system-site-packages ROOT ENV_DIR[ENV_DIR ...]


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   src/base/main
   src/particles/main
   src/geometry/main
   src/patches/main