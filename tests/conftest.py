import pytest
import pytest_asyncio
from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from fastapi.testclient import TestClient

from app.core.config import settings
from typing import AsyncGenerator

from app.core.database import get_async_session
from app.main import app
from app.models.base import Base

test_engine = create_async_engine(settings.TEST_DB_URL(), future=True, poolclass=NullPool,)
test_async_session_maker = async_sessionmaker(test_engine, expire_on_commit=False)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with test_async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = override_get_async_session

@pytest_asyncio.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def department(client):
    create_department = client.post("/api/v1/departments",
                                    json={
                                        'name': 'test_department'
                                    })
    assert create_department.status_code == 201
    return create_department.json()

@pytest.fixture
def author(client, department):
    create_author = client.post('/api/v1/employees',
                                json={
                                    'fullname': 'test_author',
                                    'position': 'test_department',
                                    'department_id': department['id']
                                })
    assert create_author.status_code == 201
    return create_author.json()

@pytest.fixture
def executor(client, department):
    create_executor = client.post('/api/v1/employees',
                                  json={
                                      'fullname': 'test_executor',
                                      'position': 'test',
                                      'department_id': department['id']
                                  })
    assert create_executor.status_code == 201
    return create_executor.json()

@pytest.fixture
def created_request(client, author, executor):
    create_request = client.post('/api/v1/requests',
                                 json={
                                     'description': 'test_description',
                                     'deadline': '2011-11-11',
                                     'author_id': author['id'],
                                     'executor_id': executor['id']
                                 })
    assert create_request.status_code == 201
    return create_request.json()

@pytest_asyncio.fixture(scope="session",
                        loop_scope="session",
                        autouse=True)
async def prepare_test_database():
    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield

@pytest_asyncio.fixture(autouse=True)
async def close_database():
    async with test_engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    yield

    await test_engine.dispose()

