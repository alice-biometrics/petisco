# petisco 🍪  

[![version](https://img.shields.io/github/release/alice-biometrics/petisco/all.svg)](https://github.com/alice-biometrics/petisco/releases) 
[![ci](https://github.com/alice-biometrics/petisco/workflows/ci/badge.svg)](https://github.com/alice-biometrics/petisco/actions) 
[![pypi](https://img.shields.io/pypi/dm/petisco)](https://pypi.org/project/petisco/) 
[![codecov](https://codecov.io/gh/alice-biometrics/petisco/branch/main/graph/badge.svg?token=YHXAYKX0VO)](https://codecov.io/gh/alice-biometrics/petisco)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![license](https://img.shields.io/github/license/alice-biometrics/petisco.svg)](https://github.com/alice-biometrics/petisco/blob/main/LICENSE)
[![versions](https://img.shields.io/pypi/pyversions/petisco.svg)](https://github.com/alice-biometrics/petisco)

<img src="https://github.com/alice-biometrics/custom-emojis/blob/master/images/alice_header.png?raw=true" width=auto>

---

**Documentation**: <a href="https://alice-biometrics.github.io/petisco/" target="_blank">https://alice-biometrics.github.io/petisco/</a>

**Source Code**: <a href="https://github.com/alice-biometrics/petisco" target="_blank">https://github.com/alice-biometrics/petisco</a>

---

Petisco is a framework for helping Python developers to build clean Applications in Python.

> **Warning**
> Disclaimer:
> Current version now is v1 (not stable yet). 
> v0 is now deprecated (legacy branc)


## Installation 💻

```console
pip install petisco
```

Installation with Extras 

```console
pip install petisco[fastapi,sqlalchemy,elastic,rabbitmq,slack,redis]
```

## Getting Started 📈
    
### Model your Domain

Doc  

#### Message Broker 

petisco 🍪 provides several classes to help on the construction of Message publishers and consumers using a message broker.

Please, find more information in [doc/message_broker/MessageBroker.md](doc/message_broker/rabbitmq.md).

## Development

### Using lume

```console
pip install lume
```

Then:

```console 
lume -install -all
```


## Contact 📬

support@alicebiometrics.com
