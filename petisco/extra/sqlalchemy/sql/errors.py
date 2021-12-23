from meiga import Error

from petisco import Uuid


class EntityAlreadyExistError(Error):
    def __init__(
        self,
        repository_name: str = None,
        table_name: str = None,
        entity_id: Uuid = None,
    ):
        entity_id_str = f" ({entity_id.value})" if entity_id else ""
        repository_str = f" (repository: {repository_name})" if repository_name else ""
        table_str = f" (table: {table_name})" if repository_name else ""
        self.message = f"Entity{entity_id_str} already exist{repository_str}{table_str}"


class EntityNotFoundError(Error):
    def __init__(self, repository_name: str = None, entity_id: Uuid = None):
        entity_id_str = f" ({entity_id.value})" if entity_id else ""
        repository_str = f" (repository: {repository_name})" if repository_name else ""
        self.message = f"Entity{entity_id_str} not found{repository_str}"


class EntitiesNotFoundError(Error):
    def __init__(self, repository_name: str = None):
        repository_str = f" (repository: {repository_name})" if repository_name else ""
        self.message = f"Entities not found{repository_str}]"
