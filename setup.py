import os

from setuptools import find_packages, setup

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PACKAGE_NAME = "petisco"
VERSION = open("petisco/VERSION").read().rstrip()

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
    entry_points={
        "console_scripts": [
            "petisco = petisco.cli.petisco:main",
            "petisco-rabbitmq = petisco.cli.petisco_rabbitmq:main",
            "petisco-dev = petisco.cli.petisco_dev:main",
        ]
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        "sqlalchemy": [
            "sqlalchemy<3.0.0,>=2.0.15",
            "sqlalchemy_utils>=0.40.0",
            "PyMySQL==1.0.3",
        ],
        "redis": ["redis<5.0.0,>=4.5.3"],
        "rabbitmq": ["pika==1.3.2"],
        "slack": ["slack_sdk<4.0.0,>=3.20.2"],
        "elastic": [
            "elasticsearch[async]<9.0.0",
            "elastic-apm<7.0.0,>=6.15.1",
        ],
        "elastic-apm": ["elastic-apm<7.0.0,>=6.15.1"],
        "fastapi": ["fastapi<1.0.0,>=0.100"],
        "rich": ["rich"],
        "dev": ["graphviz"],
    },
)
