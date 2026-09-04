# Plato-Helper-Py

Plato-Helper-Py is an auxiliary Python helper library that provides interaction with the Plato API. 
It is compatible with Python versions 3.8 through 3.14.

## Usage ##

1. Install the library with your preferred dependency manager:
``` shell
pip install plato-helper-py
``` 

2. Initialize the Plato Helper object with your plato Host and optionally, the maximum number of retries you want 
in case of connection error. The default value for retries is 3.
``` python
plato = PlatoHelper(<PLATO_HOST>, <MAX_TRIES>)
```
3. Create a new plato template by using a zipfile with the template data directory structure and assets for Amazon S3, as well as
your new template JSON schema.
``` python
plato = PlatoHelper(<PLATO_HOST>)
template = plato.create_template(file_stream=<zip_file>, template_details=<template_schema>)
```
4. You can also fetch all the registered templates and search by tag.
``` python
plato = PlatoHelper(<PLATO_HOST>)
template = plato.templates(tags=["tag1", "tag2"])
```

5. For creating a new file using the template you created, you can compose it by sending the intended compose data. There
are some optional parameters you can pass in, such as the mime type of the final file, the number of the page that 
should be printed (in case of a multipage template), and size of the template.
``` python
plato = PlatoHelper(<PLATO_HOST>)
file = plato.compose(template_id=<template_id>, 
                     compose_data={"name": "Carlos", "course": "Advanced Python"},
                     mime_type="application/pdf")
```

## Development ##

### Prerequisites ###

- Pyenv
- Python 3.8+, up to 3.14 (included)
- Python Poetry

### Setup environment for development ###

1. Setup a Python version on your local environment
```shell
pyenv install 3.8.13
pyenv install 3.9.8
pyenv install 3.10.4
pyenv install 3.11.14
pyenv install 3.12.12
pyenv install 3.13.9
pyenv install 3.14.0
pyenv local 3.8.13 3.9.8 3.10.4 3.11.14 3.12.12 3.13.9 3.14.0
``` 
2. Install dependencies
```shell
poetry install
``` 

### Running the tests ###

A Tox configuration has been created, which runs all the tests in the compatible Python versions, linter and type 
checking for you. To do so, run:
```shell
tox -p
``` 
Feel free to add '-v' for more verbose logs while running the tests.

However, if you want to run any of these configurations individually, for ease of debugging, then use the following commands:
* Unit tests, and to check coverage:
```shell
coverage run --source=plato_helper_py -m unittest
coverage report
``` 
* Mypy:
```shell
mypy --config-file conf/mypy.ini plato_helper_py
```
* Pylint:
```shell
pylint --rcfile=conf/.pylintrc plato_helper_py
```

## Continuous Integration ##

CI runs on GitHub Actions (see `.github/workflows/`): `test.yml` runs the unit tests across every supported Python 
version, plus mypy, pylint, coverage and a SonarQube scan, on every push/PR. `publish.yml` builds and publishes to 
PyPI whenever a version tag (e.g. `2.1.1`) is pushed.

## Authors ##

* **Tiago Santos** - *Initial work* - [Vizidox](https://vizidox.com)
* **Joana Teixeira** - *Additional work* - [Vizidox](https://vizidox.com)
* **Rita Mariquitos** - *Additional work* - [Vizidox](https://vizidox.com)


