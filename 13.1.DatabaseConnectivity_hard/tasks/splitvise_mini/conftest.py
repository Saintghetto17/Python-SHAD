import pytest

from splitvise.models.base import clear_database, Session


@pytest.fixture(scope='function')
def clear_session() -> Session:
    clear_database()

    session = Session()
    yield session
    session.close()
