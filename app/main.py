from fastapi import FastAPI , status ,HTTPException 
from pydantic import BaseModel 
from typing import Optional
from dotenv import load_dotenv
import os
from datetime import datetime
from app.database import connect_to_monogoDB,disconnect_to_monogoDB,__init__database
from app.models.task import Task
load_dotenv()
class TaskCreater(BaseModel):
    
    task: str
    description: str = "" 
    

app = FastAPI(
    title="Personal Task Manager API",
    description="Learning FastAPI by building a task manager",
    version="1.0.0"
)

fake_data = [  
        {"id": 1, "task": "pick all clothes", "completed": False},
        {"id": 2, "task": "finish your homework ?", "completed": False},
        {"id": 3, "task": "20 push ups", "completed": True}
    ]



@app.on_event("startup")
async def startup_event():
    """Connect to MongoDB when app starts"""
    await connect_to_monogoDB()
    from beanie import init_beanie
    from app.database import Database
    await init_beanie(
        database=Database.client[os.getenv("DATABASE_NAME", "task_manager")],
        document_models=[Task]
    )
    print("🚀 App started with MongoDB connection")

@app.on_event("shutdown")
async def shutdown_event():
    """Close MongoDB connection when app shuts down"""
    await disconnect_to_monogoDB()

@app.get("/")
def main():
    print("fastAPI server is running")
    return {"message": "i'm Alive"}

@app.get("/about")
def about():
    print("you are in the about page")
    return {
        "project": "Task Manager API",  
        "version": "1.0.0",
        "description": "Learning FastAPI"  
    }

@app.get("/tasks")
async def get_all_tasks(completed: Optional[bool] = None, search: Optional[str] = None, order: Optional[str]= "asc", sort: Optional[str]=None):
    
    query={}
    if completed is not None:
        query["completed"]=completed

    if search is not None:
        search_regex={"$regex":search,"$options":"i"}
        task_query = Task.find({
            **query,
            "$or":[
                {"task":search_regex},
                 {"description":search_regex}
            ]
        })
        
    else:
        task_query = Task.find(query)
    valid_sort_fields = ["task", "completed", "created_at", "updated_at"]
    if sort is not None:
        if sort not in valid_sort_fields:
            raise HTTPException(status_code=400,detail=f'Invalid sort field "{sort}". Valid options: {valid_sort_fields}')
        sort_direction = -1 if order == "desc" else 1 
        task_query = task_query.sort([(sort,sort_direction)])
    result_task = await task_query.to_list()

    return{
        "tasks":result_task,
        "total":len(result_task),
        "filters":{
            "completed":completed,
            "search":search,
            "order":order,
            "sort":sort
        }
    }
        

@app.get("/tasks/{task_id}")
async def get_single_task(task_id: str):
    task = await Task.get(task_id)
    if not task:
        raise HTTPException(status_code=404 ,detail=f"Task with ID {task_id} is not found")
    return task

@app.post("/add_task",status_code=status.HTTP_201_CREATED)
async def create_task(task_data: TaskCreater):

    new_task = Task(
        task=task_data.task,
        description=task_data.description,
        completed=False  # Always start as incomplete
    )
    await new_task.save()

    return new_task

@app.put("/update_task/{task_id}")
async def update_task(task_id:str,task_data:TaskCreater):

    task = await Task.get(task_id)
    
    if not task :
        raise HTTPException(status_code=404 , detail= f"the task{task_id} is not found !")
    
    task.task = task_data.task
    task.description=task_data.description
    task.updated_at = datetime.utcnow()

    await task.save()

    return task

@app.delete("/remove_task/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id:str):


    try:
        clean_task_id = task_id.strip('"')
        task = await Task.get(clean_task_id)

        if not task:
            raise HTTPException(status_code=404, detail=f"that task id{clean_task_id} is not found")
        
        await task.delete()

        return None
    except HTTPException:
        raise HTTPException(status_code=404, detail=f"that task id {clean_task_id} is not found")
    except Exception as e:
        print(f"error is {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.patch("/task/{task_id}/completed/",status_code=status.HTTP_200_OK)
async def mark_task_completed(task_id:str):
    try:
        clean_task_id = task_id.strip('"')
        task = await Task.get(clean_task_id)

        if not task:
            raise HTTPException(status_code=404 , detail=f"that task id {clean_task_id} is not fount")

        task.completed=True
        task.updated_at = datetime.utcnow() 
        await task.save()

        return {
            "message": f"Task '{task.task}' marked as completed", 
            "task": task
        }
    
    except HTTPException:
        raise HTTPException(status_code=404,detail=f"that task id {clean_task_id} is not found")
    
    except Exception as e:
        print(f"Error in mark_task_completed: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
@app.patch("/task/{task_id}/incompleted/",status_code=status.HTTP_200_OK)
async def mark_task_incompleted(task_id : str):
    try:
        clean_task_id = task_id.strip('"')
        task = await Task.get(clean_task_id)

        if not task:
            raise HTTPException(status_code=404 , detail=f"that task id {clean_task_id} is not found")
        
        task.completed = False
        task.updated_at=datetime.utcnow()

        await task.save()

        return{
            "message":f"Task {task.task} marked as incompleted",
            "task":task
        }
    
    except HTTPException:
        raise HTTPException(status_code=404 , detail=f"that task id {clean_task_id} is not found")
    except Exception as e:
        print(f"Error in mark_task_incompleted: {e}")
        raise Exception(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/task/stats",status_code=status.HTTP_200_OK)
def get_statstic():

    total_tasks = len([task for task in fake_data ])
    completed = len([task for task in fake_data if task["completed"] == True])
    incompleted = len([task for task in fake_data if task["completed"] == False])
    completion_percentage = (completed / total_tasks)*100


    return{
        "total task":total_tasks,
        "total task completed":completed,
        "total task not yet completed":incompleted,
        "percentage of completed task":completion_percentage,
        "summary": f'you completed {completed} out of {total_tasks} tasks!'
    }