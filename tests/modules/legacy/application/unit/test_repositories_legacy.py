from typing import Dict

import pytest

from petisco.legacy import Repositories, Repository
from tests.modules.legacy.application.mother.repository_mother import RepositoryMother


@pytest.mark.unit
def test_should_execute_lifecycle_of_repositories_adding_repository():

    repositories = Repositories()

    repository = RepositoryMother.valid()

    repositories.add("repo", repository)

    assert isinstance(Repositories.get("repo"), repository.__class__)
    assert Repositories.info() == {"repo": {"name": "MyRepository"}}
    Repositories.clear()


@pytest.mark.unit
def test_should_execute_lifecycle_of_repositories_from_provider():

    repository = RepositoryMother.valid()

    def provider() -> Dict[str, Repository]:
        return {"repo": repository}

    Repositories.from_provider(provider)

    assert isinstance(Repositories.get("repo"), repository.__class__)
    assert Repositories.info() == {"repo": {"name": "MyRepository"}}

    Repositories.clear()
