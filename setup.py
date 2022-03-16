import os

from setuptools import find_packages, setup

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PACKAGE_NAME = "petisco"
VERSION = open("petisco/VERSION", "r").read().rstrip()

# The text of the README file
with open(os.path.join(CURRENT_DIR, "README.md")) as fid:
    README = fid.read()

with open("requirements/requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    description="Petisco is a framework for helping Python developers to build clean Applications",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords=["DDD", "Use Case", "Clean Architecture", "REST", "Applications"],
    url="https://github.com/alice-biometrics/petisco",
    author="Alice Biometrics",
    author_email="support@alicebiometrics.com",
    license="MIT",
    install_requires=required,
    entry_points={"console_scripts": ["petisco = petisco.cli.petisco:main"]},
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        "sqlalchemy": [
            "sqlalchemy==1.4.31",
            "sqlalchemy_utils==0.38.2",
            "PyMySQL==1.0.2",
        ],
        "redis": ["redis==4.1.1"],
        "rabbitmq": ["pika==1.2.0"],
        "slack": ["slack_sdk==3.13.0"],
        "elastic": ["elasticsearch<8.0.0,>=7.13.1", "elastic-apm==6.8.1"],
        "fastapi": ["fastapi==0.73.0"],
    },
)
