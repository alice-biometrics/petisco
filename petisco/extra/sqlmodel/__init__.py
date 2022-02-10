from petisco.extra.sqlmodel.is_sqlmodel_available import is_sqlmodel_available

if is_sqlmodel_available():
    from petisco.extra.sqlmodel.sqlmodel_crud_repository import SQLModelCrudRepository

    __all__ = ["SQLModelCrudRepository"]
else:
    __all__ = []
