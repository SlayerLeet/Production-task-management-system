from fastapi import APIRouter, Depends, HTTPException, Query
from.schemas import TaskAddSchema
from sqlalchemy import select, delete, update
from storage import engine, Base, TaskModel, SessionDep

router = APIRouter()


@router.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok" : True, "message" : "База данных перезагружена"}



# CRUD TASKS
# -------------------------------------------------------------------------------------------
@router.get("/tasks/")
async def get_tasks(session: SessionDep, task_id : int = Query(None)):
    if task_id == None:
        quarry = select(TaskModel)
    else:
        quarry = select(TaskModel).where(TaskModel.id == task_id)
    result = await session.execute(quarry)
    return result.scalars().all()


@router.get("/tasks/history")
async def get_tasks_history(session: SessionDep):
    quarry = select(TaskModel).where(TaskModel.status == 2)
    result = await session.execute(quarry)
    return result.scalars().all()


@router.post("/tasks")
async def create_task(data: TaskAddSchema, session : SessionDep):
    new_task = TaskModel(
        org_name = data.org_name,
        task = data.task,
        workshop = data.workshop.value,
        status = data.status.value,
        begin_date = data.begin_date,
        dead_line = data.dead_line
    )
    session.add(new_task)
    await session.commit()
    
    return {"ok" : True, "message" : "Задача успешно добавлена"}


@router.put("/tasks/{task_id}")
async def update_task(data: TaskAddSchema, task_id : int, session : SessionDep):
    quarry = (update(TaskModel).
              where(TaskModel.id == task_id).
              values(org_name = data.org_name,
                    task = data.task,
                    workshop = data.workshop.value,
                    status = data.status.value,
                    begin_date = data.begin_date,
                    dead_line = data.dead_line
                    ))
    await session.execute(quarry)
    await session.commit()
    
    return {"ok" : True, "message" : "Задача успешно обновлена"}


@router.patch("/tasks/next/{task_id}")
async def next_status(task_id : int, session: SessionDep):
    quarry = select(TaskModel).where(TaskModel.id == task_id)
    result = await session.execute(quarry)
    task = result.scalar_one_or_none()
    
    if task is None:
        raise HTTPException(404, "Task not found")
    
    if task.status == 2:
        raise HTTPException(404, "Task status cannot be higher")
    
    task.status += 1     
    await session.commit()
    return {"ok" : True, "message" : "Статус задачи успешно обновлен"}


@router.patch("/tasks/prev/{task_id}")
async def prev_status(task_id : int, session: SessionDep):
    quarry = select(TaskModel).where(TaskModel.id == task_id)
    result = await session.execute(quarry)
    task = result.scalar_one_or_none()
    
    if task is None:
        raise HTTPException(404, "Task not found")
    
    if task.status == 0:
        raise HTTPException(404, "Task status cannot be lower")
    
    task.status -= 1     
    await session.commit()
    return {"ok" : True, "message" : "Статус задачи успешно обновлен"}


@router.delete("/tasks/{task_id}")
async def delete_task(task_id : int, session: SessionDep):
    quarry = delete(TaskModel).where(TaskModel.id == task_id)
    await session.execute(quarry)
    await session.commit()
    return {"message" : "Задача успешно удалена"}
# -------------------------------------------------------------------------------------------
