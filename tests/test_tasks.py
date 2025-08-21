import pytest
from httpx import AsyncClient

from api.v1.task.schemas import TaskCreate, TaskUpdate

@pytest.mark.asyncio
async def test_create_task(client: AsyncClient):
    data = {
        "title": "Test task",
        "description": "This is a test task",
        "status": "СОЗДАНО"
    }
    response = await client.post("api/v1/task", json=data)
    assert response.status_code == 201
    result = response.json()
    assert result["title"] == data["title"]
    assert result["description"] == data["description"]
    assert result["status"] == "СОЗДАНО"
    return result["id"]


@pytest.mark.asyncio
async def test_get_task(client: AsyncClient):
    # Создаем задачу
    create_resp = await client.post("api/v1/task", json={
        "title": "Task 1",
        "description": "Task to get",
        "status": "СОЗДАНО"
    })
    task_id = create_resp.json()["id"]

    # Получаем задачу
    response = await client.get(f"api/v1/task/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id


@pytest.mark.asyncio
async def test_get_task_by_title(client: AsyncClient):
    title = "Unique Task"
    # Создаем задачу
    await client.post("api/v1/task", json={
        "title": title,
        "description": "Task to search",
        "status": "СОЗДАНО"
    })

    # Поиск по названию
    response = await client.get(f"api/v1/task/title/{title}")
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    assert result[0]["title"] == title


@pytest.mark.asyncio
async def test_get_all_tasks(client: AsyncClient):
    # Создаем пару задач
    for i in range(2):
        await client.post("api/v1/task", json={
            "title": f"Task {i}",
            "description": "For list test",
            "status": "СОЗДАНО"
        })

    # Получаем список
    response = await client.get("api/v1/task")
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    assert len(result) >= 2


@pytest.mark.asyncio
async def test_update_task(client: AsyncClient):
    # Создаем задачу
    create_resp = await client.post("api/v1/task", json={
        "title": "Task to update",
        "description": "Old description",
        "status": "СОЗДАНО"
    })
    task_id = create_resp.json()["id"]

    # Обновляем задачу
    update_data = {
        "title": "Updated Task",
        "description": "Updated description",
        "status": "В РАБОТЕ"
    }
    response = await client.put(f"api/v1/task/{task_id}", json=update_data)
    assert response.status_code == 200
    result = response.json()
    assert result["title"] == update_data["title"]
    assert result["description"] == update_data["description"]
    assert result["status"] == "В РАБОТЕ"


@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient):
    # Создаем задачу
    create_resp = await client.post("api/v1/task", json={
        "title": "Task to delete",
        "description": "Will be removed",
        "status": "СОЗДАНО"
    })
    task_id = create_resp.json()["id"]

    # Удаляем задачу
    response = await client.delete(f"api/v1/task/{task_id}")
    assert response.status_code == 204

    # Проверяем, что ее больше нет
    get_resp = await client.get(f"api/v1/task/{task_id}")
    assert get_resp.status_code == 404
