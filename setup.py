import os

from setuptools import setup

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PACKAGE_NAME = "petisco"
VERSION = "0.6.0"

# The text of the README file
with open(os.path.join(CURRENT_DIR, "README.md")) as fid:
    README = fid.read()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description="Petisco is a framework for helping Python developers to build clean Applications",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords=["DDD", "Use Case", "Clean Architecture", "REST", "Applications"],
    url="https://github.com/alice-biometrics/petisco",
    author="ALiCE Biometrics",
    author_email="support@alicebiometrics.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=[
        "petisco",
        "petisco/application",
        "petisco/controller",
        "petisco/controller/errors",
        "petisco/controller/tokens",
        "petisco/domain",
        "petisco/domain/entities",
        "petisco/domain/errors",
        "petisco/events",
        "petisco/events/redis",
        "petisco/frameworks/flask",
        "petisco/frameworks/flask/application",
        "petisco/logger",
        "petisco/persistence",
        "petisco/persistence/sqlalchemy",
        "petisco/use_case",
    ],
    zip_safe=False,
    extras_require={
        "flask": ["connexion==2.2.0", "Flask-Cors==3.0.7"],
        "sqlalchemy": ["sqlalchemy>=1.3.11", "sqlalchemy_utils"],
    },
)
