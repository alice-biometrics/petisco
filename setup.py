import os

from setuptools import setup, find_packages

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PACKAGE_NAME = "petisco"
VERSION = open("petisco/VERSION", "r").read()

# The text of the README file
with open(os.path.join(CURRENT_DIR, "README.md")) as fid:
    README = fid.read()

with open("requirements/requirements.txt") as f:
    required = f.read().splitlines()

legacy_packages = [
    "petisco/legacy",
    "petisco/legacy/controller",
    "petisco/legacy/controller/errors",
    "petisco/legacy/domain",
    "petisco/legacy/domain/value_objects",
    "petisco/legacy/domain/aggregate_roots",
    "petisco/legacy/domain/errors",
    "petisco/legacy/notifier",
    "petisco/legacy/notifier/config",
    "petisco/legacy/notifier/infrastructure",
    "petisco/legacy/notifier/infrastructure/slack",
    "petisco/legacy/notifier/domain",
    "petisco/legacy/tasks",
    "petisco/legacy/tasks/config",
    "petisco/legacy/tasks/domain",
    "petisco/legacy/tasks/infrastructure",
    "petisco/legacy/fixtures",
    "petisco/legacy/frameworks",
    "petisco/legacy/frameworks/flask",
    "petisco/legacy/frameworks/flask/application",
    "petisco/legacy/http",
    "petisco/legacy/logger",
    "petisco/legacy/persistence",
    "petisco/legacy/persistence/sqlalchemy",
    "petisco/legacy/persistence/pymongo",
    "petisco/legacy/persistence/sql",
    "petisco/legacy/persistence/sql/mysql",
    "petisco/legacy/persistence/sql/sqlite",
    "petisco/legacy/persistence/elastic",
    "petisco/legacy/security/token_decoder",
    "petisco/legacy/security/token_manager",
    "petisco/legacy/tools",
    "petisco/legacy/use_case",
    "petisco/legacy/modules",
    "petisco/legacy/modules/environment",
    "petisco/legacy/modules/environment/application",
    "petisco/legacy/modules/environment/domain",
    "petisco/legacy/modules/healthcheck",
    "petisco/legacy/modules/healthcheck/application",
    "petisco/legacy/modules/healthcheck/domain",
]

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
        "console_scripts": ["petisco = petisco.legacy.application.cli.petisco:main"]
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=find_packages() + legacy_packages,
    include_package_data=True,
    zip_safe=False,
    extras_require={
        "flask": [
            "connexion==2.6.0",
            "swagger-ui-bundle>=0.0.2",
            "Flask-Cors==3.0.7",
            "Flask-Bcrypt==0.7.1",
        ],
        "sqlalchemy": [
            "sqlalchemy==1.4.20",
            "sqlalchemy_utils==0.37.8",
            "PyMySQL==1.0.2",
        ],
        "redis": ["redis >= 3.3.11", "fakeredis>=1.0.5"],
        "rabbitmq": ["pika==1.2.0"],
        "gunicorn": ["gunicorn", "json-logging-py==0.2"],
        "fixtures": ["pytest"],
        "slack": ["slackclient"],
        "pymongo": ["pymongo==3.11.0"],
        "elastic": ["elasticsearch<8.0.0,>=7.13.1"],
        "fastapi": ["fastapi==0.65.2"],
    },
)
