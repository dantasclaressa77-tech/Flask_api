import os
from datetime import datetime
from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from flask_migrate import Migrate

import click

class Base(DeclarativeBase):
    pass

db=SQLAlchemy(model_class=Base)
migrate=Migrate()


class User(db.Model):
    id : Mapped[int]=mapped_column( primary_key=True)   
    username : Mapped[str]=mapped_column( unique=True, nullable=False)
    active: Mapped[bool]=mapped_column( default=True)

    def __repr__(self):
        return f"<User {self.username}>, id={self.id}, active={self.active}>"
    

class Post(db.Model):
    id : Mapped[int]=mapped_column( primary_key=True)
    title : Mapped[str]=mapped_column( nullable=False)
    body : Mapped[str]=mapped_column( nullable=False)
    created : Mapped[datetime]=mapped_column(db.DateTime, server_default=db.func.current_timestamp())
    autor_id :  Mapped[int]=mapped_column( db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Post {self.title}, id={self.id}>"

 # CORRIGIDO: O correto é command (com dois 'm') -> @click.command
@click.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    global db
    with current_app.app_context():
        db.create_all()
    click.echo("Initialized the database.")  

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=f"sqlite:///{os.path.join(app.instance_path, 'blog_dio.sqlite')}",
    )
    

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)    
    else:
        app.config.from_mapping(test_config)    
    try: 
        os.makedirs(app.instance_path)
    except OSError:
        pass 

    app.cli.add_command(init_db_command)
    db.init_app(app)
    migrate.init_app(app, db)              
    
    from src.controllers import users    
    app.register_blueprint(users.app)

    from src.controllers import post
    app.register_blueprint(post.app)

    return app
     