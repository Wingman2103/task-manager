import uuid
import pytest

from httpx import AsyncClient
from models.task import TaskStatus


@pytest.mark.asyncio
async def test_create_task(client: AsyncClient):
    
    data = {
        "title": "Test task",
        "description": "This is a test task",
        "status": TaskStatus.created.value
    }
    response = await client.post("api/v1/task", json=data)
    assert response.status_code == 201
    result = response.json()
    assert result["title"] == data["title"]
    assert result["description"] == data["description"]
    assert result["status"] == TaskStatus.created.value
    return result["id"]


@pytest.mark.asyncio
async def test_get_task(client: AsyncClient):

    create_resp = await client.post("api/v1/task", json={
        "title": "Task 1",
        "description": "Task to get",
        "status": TaskStatus.created.value
    })
    task_id = create_resp.json()["id"]

    response = await client.get(f"api/v1/task/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id


@pytest.mark.asyncio
async def test_get_task_by_title(client: AsyncClient):

    title = "Unique Task"

    await client.post("api/v1/task", json={
        "title": title,
        "description": "Task to search",
        "status": TaskStatus.created.value
    })

    response = await client.get(f"api/v1/task/title/{title}")
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    assert result[0]["title"] == title


@pytest.mark.asyncio
async def test_get_all_tasks(client: AsyncClient):

    for i in range(2):
        await client.post("api/v1/task", json={
            "title": f"Task {i}",
            "description": "For list test",
            "status": TaskStatus.created.value
        })

    response = await client.get("api/v1/task")
    assert response.status_code == 200
    result = response.json()
    assert isinstance(result, list)
    assert len(result) >= 2


@pytest.mark.asyncio
async def test_update_task(client: AsyncClient):
  
    create_resp = await client.post("api/v1/task", json={
        "title": "Task to update",
        "description": "Old description",
        "status": TaskStatus.created.value
    })
    task_id = create_resp.json()["id"]

    update_data = {
        "title": "Updated Task",
        "description": "Updated description",
        "status": TaskStatus.in_progress.value
    }
    response = await client.patch(f"api/v1/task/{task_id}", json=update_data)
    assert response.status_code == 200
    result = response.json()
    assert result["title"] == update_data["title"]
    assert result["description"] == update_data["description"]
    assert result["status"] == TaskStatus.in_progress.value


@pytest.mark.asyncio
async def test_delete_task(client: AsyncClient):

    create_resp = await client.post("api/v1/task", json={
        "title": "Task to delete",
        "description": "Will be removed",
        "status": TaskStatus.created.value
    })
    task_id = create_resp.json()["id"]

    response = await client.delete(f"api/v1/task/{task_id}")
    assert response.status_code == 204

    get_resp = await client.get(f"api/v1/task/{task_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_full_loop_task(client: AsyncClient):

    data = {
        "title": "Test task",
        "description": "This is a test task",
        "status": TaskStatus.created.value
    }
    create_resp = await client.post("api/v1/task", json=data)
    assert create_resp.status_code == 201
    result = create_resp.json()
    assert result["title"] == data["title"]
    assert result["description"] == data["description"]
    assert result["status"] == TaskStatus.created.value
    
    task_id = result["id"]

    update_data = {
        "description": "Updated description",
        "status": TaskStatus.in_progress.value
    }
    update_response = await client.patch(f"api/v1/task/{task_id}", json=update_data)
    assert update_response.status_code == 200
    result = update_response.json()
    assert result["description"] == update_data["description"]
    assert result["status"] == TaskStatus.in_progress.value

    update_data = {
        "description": "Complete description",
        "status": TaskStatus.completed.value
    }
    update_response = await client.patch(f"api/v1/task/{task_id}", json=update_data)
    assert update_response.status_code == 200
    result = update_response.json()
    assert result["description"] == update_data["description"]
    assert result["status"] == TaskStatus.completed.value

    response = await client.delete(f"api/v1/task/{task_id}")
    assert response.status_code == 204

    get_resp = await client.get(f"api/v1/task/{task_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_bad_get_task(client: AsyncClient):

    task_id = uuid.uuid4()
    
    response = await client.get(f"api/v1/task/{task_id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_bad_update_task(client: AsyncClient):

    task_id = uuid.uuid4()

    update_data = {
        "title": "Updated Task",
        "description": "Updated description",
        "status": TaskStatus.in_progress.value
    }
    
    response = await client.patch(f"api/v1/task/{task_id}", json=update_data)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_bad_delete_task(client: AsyncClient):

    task_id = uuid.uuid4()
    
    response = await client.delete(f"api/v1/task/{task_id}")
    assert response.status_code == 404