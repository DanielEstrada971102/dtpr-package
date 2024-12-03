# Developers' guide

[[_TOC_]]

## Development setup

The recommended way of development is under a virtual environment. Bear in mind that you will need PyROOT.

### Quick start

1. Clone the repository
    ```shell
    git clone https://github.com/DanielEstrada971102/dtpr-package.git && cd cmsgemos-analysis
    ```
2. Install the `dtpr-package` project along with all its dependencies in a virtual environment with the commands
    ```shell
    python -m venv --system-site-package ROOT ENV_DIR[ENV_DIR ...]
    source [ENV_DIR]/bin/activate
    # being in the main directory
    pip install -e .
    ```

## Development guidelines
### Coding style

You can check and fix your code formatting through the usage of `Black`:

``` shell
black --check -l 100 dtpr
```

### Documentation writing

We use the [sphinx](https://www.sphinx-doc.org/en/master/usage/quickstart.html) with read-the-docs theme for `python` code documentation.

Complete as necesary the documentation in `docs/src` and generate it using the command:

```shell
cd /docs
make html 
```

Generated files are placed in `docs/_build` and main `index.html` can be found in `docs/_build/index.html`.

## Tips
...