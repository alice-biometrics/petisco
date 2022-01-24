from abc import abstractmethod
from typing import List

from meiga import (
    BoolResult,
    Error,
    Failure,
    NotImplementedMethodError,
    Result,
    Success,
    isSuccess,
)
from meiga.decorators import meiga
from sqlmodel import Session, SQLModel, create_engine, select

from petisco import Uuid
from petisco.base.application.patterns.crud_repository import (
    AggregateRootType,
    CrudRepository,
)
from petisco.base.domain.errors.defaults.already_exists import (
    AggregateAlreadyExistError,
)
from petisco.base.domain.errors.defaults.not_found import AggregateNotFoundError

engine = create_engine("sqlite:///database.db", echo=True)
SQLModel.metadata.create_all(engine)


class SQLModelCrudRepository(CrudRepository[AggregateRootType]):
    @abstractmethod
    def get_aggregate_root(self, sql_model: SQLModel) -> AggregateRootType:
        return NotImplementedMethodError

    @abstractmethod
    def get_sql_model(self, aggregate_root: AggregateRootType) -> SQLModel:
        return NotImplementedMethodError

    @meiga
    def save(self, aggregate_root: AggregateRootType) -> BoolResult:
        with Session(engine) as session:
            Model = self.transformer.InfrastructureModel
            statement = select(Model).where(
                Model.aggregate_id == aggregate_root.aggregate_id
            )
            infrastructure_model = session.exec(statement).first()
            if infrastructure_model:
                return Failure(AggregateAlreadyExistError(aggregate_root.aggregate_id))

            infrastructure_model = self.transformer.get_infrastructure_model(
                aggregate_root
            ).unwrap_or_return()

            session.add(infrastructure_model)
            session.commit()

        # if aggregate_root.aggregate_id in self._data:
        #     return Failure(
        #         AggregateAlreadyExistError(aggregate_root.aggregate_id)
        #     )  # TODO: should we use AlreadyExist
        # infrastructure_model = self.transformer.get_infrastructure_model(
        #     aggregate_root
        # ).unwrap_or_return()
        # self._data[aggregate_root.aggregate_id] = infrastructure_model
        return isSuccess

    @meiga
    def retrieve(self, aggregate_id: Uuid) -> Result[AggregateRootType, Error]:
        infrastructure_model = self._data.get(aggregate_id)
        if infrastructure_model is None:
            return Failure(
                AggregateNotFoundError(aggregate_id)
            )  # TODO: should we use NotFound
        aggregate_root = self.transformer.get_domain_model(
            infrastructure_model
        ).unwrap_or_return()
        return Success(aggregate_root)

    def update(self, aggregate_root: AggregateRootType) -> BoolResult:
        if aggregate_root.aggregate_id not in self._data:
            return Failure(
                AggregateNotFoundError(aggregate_root.aggregate_id)
            )  # TODO: should we use NotFound
        infrastructure_model = self.transformer.get_infrastructure_model(
            aggregate_root
        ).unwrap_or_return()
        self._data[aggregate_root.aggregate_id] = infrastructure_model
        return isSuccess

    def remove(self, aggregate_id: Uuid) -> BoolResult:
        if aggregate_id not in self._data:
            return Failure(
                AggregateNotFoundError(aggregate_id)
            )  # TODO: should we use NotFound
        self._data.pop(aggregate_id)
        return isSuccess

    def retrieve_all(self) -> Result[List[AggregateRootType], Error]:
        all = [
            self.transformer.get_domain_model(infrastructure_model).unwrap_or_return()
            for infrastructure_model in self._data.values()
        ]
        return Success(all)
