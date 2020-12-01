from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
app = Flask(__name__)

def create_app():
    app.config['SECRET_KEY'] = 'skurczybonk'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['JWT_TOKEN_LOCATION'] = 'headers'
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    app.config['JWT_IDENTITY_CLAIM'] = 'sub'
    app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379'
    app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379'
    from . import main as main_bp
    app.register_blueprint(main_bp.mainbp)
    from . import authorization as auth_bp
    app.register_blueprint(auth_bp.authbp)
    from . import api as api_bp
    app.register_blueprint(api_bp.apibp)
    JWTManager(app)
    db.init_app(app)
    Migrate(app, db)
    return app


def get_db():
    return db
