Installation is as simple as:

<div class="termy">
```console
$ pip install petisco
---> 100%
Successfully installed petisco
```
</div>

This will install the latest version of petisco package ✌️ [![version](https://img.shields.io/github/release/alice-biometrics/petisco/all.svg)](https://github.com/alice-biometrics/petisco/releases) 

## Base Requirements

* [meiga](https://alice-biometrics.github.io/meiga/): A Python µframework that provides a simple, fully typed, monad-based result type.
* [pydantic](https://pydantic-docs.helpmanual.io/): Data validation and settings management using Python type annotations.
* [requests](https://requests.readthedocs.io/en/latest/): An elegant and simple HTTP library for Python, built for human beings.
* [pyjwt[crypto]](https://pyjwt.readthedocs.io/en/stable/): A Python library which allows you to encode and decode JSON Web Tokens (JWT). JWT is an open, industry-standard (RFC 7519) for representing claims securely between two parties.
* [validators](https://validators.readthedocs.io/en/latest/): Python Data Validation for Humans
* [pyyaml](https://pyyaml.org/): A full-featured YAML framework for the Python programming language.
* [loguru](https://loguru.readthedocs.io/en/stable/index.html): Loguru is a library which aims to bring enjoyable logging in Python.


## Extras

To install extras:

<div class="termy">
```console
$ pip install petisco[sqlalchemy, redis, rabbitmq, slack, elastic, elastic-apm, fastapi, rich]
---> 100%
Successfully installed petisco
```
</div>

