from flask import Blueprint, request, abort, make_response, Response
from app.models.goal import Goal
from ..db import db
goals_bp = Blueprint("goals_bp",__name__,url_prefix="/goals")

@goals_bp.post("")
def create_goal():
    request_body = request.get_json() 

    if "title" not in request_body:
        return {"details": "Invalid data"}, 400
    
    title = request_body["title"]
    new_goal = Goal(title=title)

    db.session.add(new_goal)
    db.session.commit()

    response = {
        Goal.__tablename__: 
            {
            "id": new_goal.id,
            "title": new_goal.title,
        }
            }
    return response, 201

@goals_bp.get("")
def get_all_goals():
    #execute the query statement and retrieve the models
    query = db.select(Goal) #select records from db Model
    
    query = query.order_by(Goal.id)
    goals = db.session.scalars(query) #retrieve the records
    
    response = []
    for goal in goals:
        response.append(
            {
                "id": goal.id,
                "title": goal.title
            }
        )
    return response 

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        response = {"message": f"goal {goal_id} invalid"}
        abort(make_response(response, 400))

    #execute the query statement and retrieve the models
    query = db.select(Goal).where(Goal.id == goal_id) #select records with an id = goal_id
    goal = db.session.scalar(query) #retrieve only one record goal_id
    
    if not goal:
        response = {"message": f"Goal {goal_id} not found"}
        abort(make_response(response, 404))

    return goal

@goals_bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)

    return {
        Goal.__tablename__: {
        "id": goal.id,
        "title": goal.title,
        }
    }

@goals_bp.put("/<goal_id>")
def update_one_goal_by_id(goal_id):
    goal = validate_goal(goal_id) #record with id = goal_id
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit() #save the changes to db

    return {
        Goal.__tablename__: {
        "id": goal.id,
        "title": goal.title,
        }
    }

@goals_bp.delete("/<goal_id>")
def delete_goal_by_id(goal_id):
    goal = validate_goal(goal_id)
    
    #Delete the goal
    db.session.delete(goal)
    db.session.commit()
    
    response = {
        "details": f"Goal {goal.id} \"{goal.title}\" successfully deleted"
    }
    return response, 200