!!! note "" 
    
    The `ElasticDatabase` is an specific implementation of a `Database` using the elastic python client.
    This object encapsulates some specific Elastic stuff and provides it as a scoped session.

## Connections

When you define a `ElasticDatabase` you have to specify the connection. Petisco already provides the `ElasticConnection`
object.

````python
from petisco.extra.elastic import ElasticConnection, ElasticDatabase

connection = ElasticConnection.create_local()
database = ElasticDatabase(name="elastic_test", connection=connection)
````

## Session

The `ElasticDatabase` implements the `get_session_scope` method to get a context manager with a pre-configured 
`ElasticSearch` client.

```python
from petisco.extra.elastic import ElasticConnection, ElasticDatabase

connection = ElasticConnection.create_local()
database = ElasticDatabase(name="elastic_test", connection=connection)
database.initialize()

session_scope = database.get_session_scope()
with session_scope() as es:
    document = {
        "title": "Example Document",
        "content": "This is the content of the document.",
    }
    index_name = "my-index"
    response = es.index(index=index_name, document=document)
```

## Async

Petisco also provides an async implementation, the `AsyncElasticDatabase`. To run it with async/await pattern, you could
run the following:

```python
from petisco.extra.elastic import ElasticConnection, AsyncElasticDatabase

connection = ElasticConnection.create_local()
database = AsyncElasticDatabase(name="elastic_test", connection=connection)
database.initialize()

session_scope = database.get_session_scope()

async with session_scope() as es:
    document = {
        "title": "Example Document",
        "content": "This is the content of the document.",
    }
    index_name = "my-index"
    response = await es.index(index=index_name, document=document)
    assert response.get("result") == "created"
```
