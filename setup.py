import os

from setuptools import setup

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
PACKAGE_NAME = "petisco"
VERSION = open("petisco/VERSION", "r").read()

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
    author="ALiCE Biometrics",
    author_email="support@alicebiometrics.com",
    license="MIT",
    install_requires=required,
    entry_points={
        "console_scripts": ["petisco = petisco.application.cli.petisco:main"]
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    packages=[
        "petisco",
        "petisco/application",
        "petisco/application/config",
        "petisco/application/config/events",
        "petisco/application/cli",
        "petisco/controller",
        "petisco/controller/errors",
        "petisco/domain",
        "petisco/domain/value_objects",
        "petisco/domain/aggregate_roots",
        "petisco/domain/errors",
        "petisco/events",
        "petisco/events/rabbitmq",
        "petisco/events/publisher",
        "petisco/events/publisher/domain",
        "petisco/events/publisher/infrastructure",
        "petisco/events/subscriber",
        "petisco/events/subscriber/domain",
        "petisco/events/subscriber/infrastructure",
        "petisco/notifier",
        "petisco/notifier/config",
        "petisco/notifier/infrastructure",
        "petisco/notifier/infrastructure/slack",
        "petisco/notifier/domain",
        "petisco/tasks",
        "petisco/tasks/config",
        "petisco/tasks/domain",
        "petisco/tasks/infrastructure",
        "petisco/fixtures",
        "petisco/frameworks",
        "petisco/frameworks/flask",
        "petisco/frameworks/flask/application",
        "petisco/logger",
        "petisco/persistence",
        "petisco/persistence/sqlalchemy",
        "petisco/security/token_decoder",
        "petisco/security/token_manager",
        "petisco/tools",
        "petisco/use_case",
        "petisco/modules",
        "petisco/modules/environment",
        "petisco/modules/environment/application",
        "petisco/modules/environment/domain",
        "petisco/modules/healthcheck",
        "petisco/modules/healthcheck/application",
        "petisco/modules/healthcheck/domain",
    ],
    include_package_data=True,
    zip_safe=False,
    extras_require={
        "flask": ["connexion==2.6.0", "swagger-ui-bundle>=0.0.2", "Flask-Cors==3.0.7"],
        "sqlalchemy": ["sqlalchemy>=1.3.11", "sqlalchemy_utils", "PyMySQL==0.9.2"],
        "redis": ["redis >= 3.3.11", "fakeredis>=1.0.5"],
        "rabbitmq": ["pika==1.1.0"],
        "gunicorn": ["gunicorn", "json-logging-py==0.2"],
        "fixtures": ["pytest"],
        "slack": ["slackclient"],
    },
)
