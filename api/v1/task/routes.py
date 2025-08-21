from uuid import UUID

from fastapi import APIRouter, HTTPException

from db.database import session_depend
from api.v1.task.crud import TaskCRUD
from api.v1.task.schemas import TaskCreate, TaskUpdate, TaskRead


router = APIRouter(tags=["v1/tasks"])
task_crud = TaskCRUD()

@router.get("/task/{task_id}",
            response_model=TaskRead,
            status_code=200,
            summary="Получение задачи",
            description="Получить задачу по id"
            )
async def get_task(task_id: UUID, session: session_depend):
    result = await task_crud.get(task_id, session)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return result


@router.get("/task/title/{title}",
            response_model=list[TaskRead],
            status_code=200,
            summary="Получение задачи",
            description="Получить все задачи с таким названием"
            )
async def get_task(title: str, session: session_depend):
    result = await task_crud.get_by_title(title, session)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return result


@router.get("/task",
            response_model=list[TaskRead],
            status_code=200
            )
async def get_tasks(session: session_depend):
    result = await task_crud.get_list(session)
    if not result:
        raise HTTPException(status_code=404, detail="Task not found")
    return result


@router.post("/task", 
             response_model=TaskRead,
             status_code=201,
             )
async def create_task(task_body: TaskCreate, session: session_depend):
    task_id = await task_crud.create(task_body, session)
    if task_id:
        return await task_crud.get(task_id, session)
    else:
        raise HTTPException(status_code=404, detail="Task not created")


@router.put("/task/{task_id}", 
             response_model=TaskRead,
             status_code=200,
             )
async def update_task(task_id: UUID, task_body: TaskUpdate, session: session_depend):
    old_task = await task_crud.get(task_id, session)
    if old_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return await task_crud.update(old_task, task_body, session)


@router.delete("/task/{task_id}", 
             status_code=204,
             response_description="No Content"
             )
async def delete_task(task_id: UUID, session: session_depend):
    task = await task_crud.get(task_id, session)
    if task:
        return await task_crud.delete(task, session)
    else:
        raise HTTPException(status_code=404, detail="Task not found")