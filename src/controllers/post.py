from flask import Blueprint, request
from src.app import User, Post, db
from http import HTTPStatus
from sqlalchemy import inspect

app = Blueprint('post', __name__, url_prefix='/posts')

#função que cria um novo usuário no banco de dados, recebendo os dados via request.
def _create_post():
    data = request.get_json(silent=True) or {}

    missing = [field for field in ('autor_id', 'title', 'body') if field not in data]
    if missing:
        return {"message": f"Missing fields: {', '.join(missing)}"}, HTTPStatus.BAD_REQUEST

    
    title = data['title']
    body = data['body']
    autor_id = data['autor_id']
    id=data["id"]
    id=db.get_or_404(User, id)
    if id is None:
        return {"message": f"User with id '{id}' not found"}, HTTPStatus.NOT_FOUND
    
    post = Post( title=title, body=body,  autor_id=id.id)
    db.session.add(post)
    db.session.commit()
    return {"message": "Post created"}, HTTPStatus.CREATED

def _list_posts():
    query =db.select(Post)
    posts =db.session.execute(query).scalars()
    
    return [ 
        {
            "id": post.id,
            "autor_id": post.autor_id,
            "title": post.title,
            "body": post.body,
            "created": post.created
        }
        for post in posts

     ]


@app.route('/', methods=["GET", "POST"])
def handle_posts():
    if request.method == 'POST':
        return _create_post()
    else:
        return {"posts": _list_posts()}, HTTPStatus.OK

@app.route('<int:autor_id>')
def get_post(autor_id):        
    post=db.get_or_404(Post, autor_id)
    return {
        "id": post.id,
        "autor_id": post.autor_id,
        "title": post.title,
        "body": post.body,
        "created": post.created
    }

@app.route('<int:post_id>', methods=["PATCH"])
def update_post(post_id):
    post = db.get_or_404(Post, post_id)
    data=request.json   
    
    mapper = inspect(Post)
    for column in mapper.attrs:
        if column.key in data:
            setattr(post, column.key, data[column.key])
    db.session.commit()

    return {"message": "Post updated"}, HTTPStatus.OK

@app.route("<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    post = db.get_or_404(Post, post_id)
    db.session.delete(post)
    db.session.commit()
    
   
    return {"message": "Post deleted"}, HTTPStatus.NO_CONTENT
