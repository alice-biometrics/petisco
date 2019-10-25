petisco
=======

Petisco is a framework for helping Python developers to build clean Applications

#### Installation 

~~~
pip install petisco
~~~

#### Getting Started

**petisco** provides us some sort of interfaces and decorators to help on the development of clean architecture Applications.

## Developers

##### Install requirements

```console
pip install -r requirements/dev.txt
```

##### Test

```console
pip install -e . && pytest
```

##### Upload to PyPi 

```console
python setup.py sdist bdist_wheel
twine check dist/*
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
```
