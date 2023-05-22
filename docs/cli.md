This comprehensive guide aims to provide you with all the necessary information to effectively utilize the command-line 
interface (CLI) tools offered by petisco. Whether you are a beginner or an experienced developer, this documentation 
will help you harness the full potential of our CLI tools and streamline your development process.


You `can check installed version of petisco with:

<div class="termy">
```console
$ petisco --version
petisco 🍪 => 2.X.X
```
</div>

Or generate a random UUID v4 with:

<div class="termy">
```console
$ petisco --uuid
a4161d89-9819-4730-99e3-7d2890fb17bc
```
</div>

And also print the current `utcnow`:

<div class="termy">
```console
$ petisco --utcnow
2023-05-22 13:49:13.243518
```
</div>

## `petisco-dev`

Provides various commands to help you interact with and manage your petisco-based application.

This is what `petisco-dev` provides us:

<div class="termy">
```console
$ petisco-dev --help
petisco dev tools to inspect your application

options:
  -h, --help            show this help message and exit
  -i, --info            show petisco app info.
  -deps, --dependencies
                        show petisco app dependencies.
  -configs, --configurers
                        show petisco app configurers.
  --application APPLICATION
                        Module path (default app.application)
```
</div>

!!! info

    If `rich` package is installed, information will use it to show valuable information in a fancy way.

### Show info

<div class="termy">
```console
$ petisco-dev --info
╭────────── Petisco Application ───────────╮
│ name:          my-petisco-app            │
│ version:       1.0.1                     │
│ organization:  alice                     │
│ deployed_at:   2023-05-16 10:41:39       │
│ dependencies:  1                         │
│ configurers:   2                         │
╰──────────────────────────────────────────╯
```
</div>


### Show dependencies

<div class="termy">
```console
$ petisco-dev --dependencies
┏━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┓
┃        Type┃Default        ┃Implementation        ┃ENV               ┃
┡━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━┩
│MyRepository│SqlMyRepository│fake: FakeMyRepository│MY_REPOSITORY_TYPE│
└────────────┴───────────────┴──────────────────────┴──────────────────┘
```
</div>

### Show configurers

<div class="termy">
```console
$ petisco-dev --configurers
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃                Configurer ┃ execute_after_dependencies ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│     PersistenceConfigurer │           False            │
│ RabbitMqMessageConfigurer │            True            │
└───────────────────────────┴────────────────────────────┘
```
</div>

!!! help

    This information is obtained from instantiating a `petisco.Application`.

    By default, `petisco-dev` searchs this application in the module `app.application`:

    ```python hl_lines="13" title="app/application.py"
    from petisco.extra.fastapi import FastApiApplication

    from app import (
        APPLICATION_LATEST_DEPLOY,
        APPLICATION_NAME,
        APPLICATION_VERSION,
        ORGANIZATION,
    )
    from app.fastapi import fastapi_configurer
    from app.petisco.configurers.configurers import configurers
    from app.petisco.dependencies.dependencies_provider import dependencies_provider
    
    application = FastApiApplication(
        name=APPLICATION_NAME,
        version=APPLICATION_VERSION,
        organization=ORGANIZATION,
        deployed_at=APPLICATION_LATEST_DEPLOY,
        dependencies_provider=dependencies_provider,
        configurers=configurers,
        fastapi_configurer=fastapi_configurer,
    )
    ```
    
    If your application is defined in other file, you can modify it with `petisco-dev --info --application app.other.module.application`. 
    

