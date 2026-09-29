from flask import Blueprint, request
from src.app import User, db
from http import HTTPStatus
from sqlalchemy import inspect

app = Blueprint('users', __name__, url_prefix='/users')


def _list_users():
    query =db.select(User)
    users =db.session.execute(query).scalars()
    
    return [ 
        {
            "id": user.id,
            "username": user.username
        }
        for user in users

     ]



def _create_user():
    data = request.json
    username = data['username']

    if db.session.execute(db.select(User).where(User.username == username)).scalar():
        return {"message": f"User '{username}' already exists"}, HTTPStatus.CONFLICT

    user = User(username=username)
    db.session.add(user)
    db.session.commit()
    return {"message": "User created"}, HTTPStatus.CREATED


@app.route('/', methods=["GET", "POST"])
def handle_users():
    if request.method == 'POST':
        return _create_user()
    else:
        return {"users": _list_users()}, HTTPStatus.OK

@app.route('<int:user_id>')
def get_user(user_id):        
    user=db.get_or_404(User, user_id)
    return {
        "id": user.id,
        "username": user.username
    }
@app.route('<int:user_id>', methods=["PATCH"])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    data=request.json   
    
    mapper = inspect(User)
    for column in mapper.attrs:
        if column.key in data:
            setattr(user, column.key, data[column.key])
    db.session.commit()

    return {"message": "User updated"}, HTTPStatus.OK

@app.route("<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    db.session.delete(user)
    db.session.commit()
    
   
    return {"message": "User deleted"}, HTTPStatus.NO_CONTENT
