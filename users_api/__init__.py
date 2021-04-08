import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache

db = SQLAlchemy()
migrate = Migrate()
cache = Cache()

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_key',
        SQLALCHEMY_DATABASE_URI = "postgresql://ndznwrwrigkkuz:b7abeadaf312ae61c7a218b2c81d6758ad7f045be2d60651b31ff71007650409@ec2-54-167-168-52.compute-1.amazonaws.com:5432/ddpdk9e41as84r",
        #SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(app.instance_path, 'users.sqlite'), #Developer
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )

    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app, config={'CACHE_TYPE': 'redis', 'CACHE_REDIS_URL': 'redis://localhost:6379/0'})

    from .models.UserModel import User
    from .controllers import userController
    app.register_blueprint(userController.bp)

    return app