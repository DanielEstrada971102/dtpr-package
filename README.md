# Base Tools for Pattern Recognition in DTs

This package provides a set of base tools for implementing pattern recognition algorithms using
input data in NTuple format. It also includes visualization tools for DT Ntuples, taking into account
the geometrical features of the CMS DT system.

If you are a developer please start with reading the [Contributor][contributing]'s  and [Developers][developers]  guides to be updated...

## Installation

First, download the source files or clone the repository:

You can install the package with pip by running:

```shell
git clone https://github.com/DanielEstrada971102/dtpr-package.git
cd dtpr-package
```

You can then install the package with pip by running:

```shell
pip install .
```

To check if the package was installed successfully, run:

```shell
pip show dtpr
```

> [!IMPORTANT]
> Be aware that the package requires PyROOT, so you should have it installed. If you are working in a Python virtual environment, ensure to include ROOT in it. To do this, use the command:
> ```shell
> python -m venv --system-site-packages ROOT ENV_DIR[ENV_DIR ...]
> ```

## Usage

Web documentation is going to be produced. At the moment, you can see it locally by opening the index file from `docs/_build/html/src/index.html`.

[contributing]: CONTRIBUTING.md
[developers]: DEVELOPERS.md