from flask import Blueprint, request, abort, make_response, Response
from app.models.task import Task
from ..db import db

tasks_bp = Blueprint("task_bp", __name__,url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json() 

    # Check if "title" or "description" keys are missing in the request body
    if "title" not in request_body or "description" not in request_body:
        return {"details": "Invalid data"}, 400

    title = request_body["title"]
    description = request_body["description"]
    completed_at = request_body.get("completed_at") # Use .get() since "completed_at" is optional
    
    new_task = Task(title=title, description=description, completed_at=completed_at)

    db.session.add(new_task)
    db.session.commit()

    response = {
        Task.__tablename__: 
            {
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": bool(new_task.completed_at) # Convert to boolean for completeness
        }
            }
    return response, 201

@tasks_bp.get("")
def get_all_tasks():
    #execute the query statement and retrieve the models
    query = db.select(Task) #select records from db Model

    # Check for sorting parameter and apply
    sorting_param = request.args.get("sort", "asc").lower() #asc is default if not provided
    
    # If sort=desc, order by title descending
    if sorting_param.lower() == "desc":
        query = query.order_by(Task.title.desc())
    else:
        query = query.order_by(Task.title)
    # else:
    #     # No sorting parameter provided, default to ordering by id
    #     query = query.order_by(Task.id)
    
    #query = query.order_by(Task.id)#select records
    tasks = db.session.scalars(query) #retrieve the records
    
    response = []
    for task in tasks:
        response.append(
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            }
        )
    return response 

@tasks_bp.get("/<task_id>")
def get_one_task_by_id(task_id):
    task = validate_task_id(task_id)

    return {
        Task.__tablename__: {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_complete": bool(task.completed_at)
        }
    }

def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except:
        response = {"message": f"Task {task_id} invalid"}
        abort(make_response(response, 400))

    #execute the query statement and retrieve the models
    query = db.select(Task).where(Task.id == task_id) #select records with an id = task_id
    task = db.session.scalar(query) #retrieve only one record task_id
    
    if not task:
        response = {"message": f"Task {task_id} not found"}
        abort(make_response(response, 404))

    return task

@tasks_bp.put("/<task_id>")
def update_one_task_by_id(task_id):
    task = validate_task_id(task_id) #record with id = task_id
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit() #save the changes to db

    return {
        Task.__tablename__: {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_complete": bool(task.completed_at)
        }
    }

@tasks_bp.delete("/<task_id>")
def delete_task_by_id(task_id):
    task = validate_task_id(task_id)
    
    #Delete the task
    db.session.delete(task)
    db.session.commit()
    
    response = {
        "details": f"Task {task.id} \"{task.title}\" successfully deleted"
    }
    return response, 200