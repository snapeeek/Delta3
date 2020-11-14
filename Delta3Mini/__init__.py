from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'skurczybonk'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    from . import main as main_bp
    app.register_blueprint(main_bp.app)
    from . import delta3authorization as auth_bp
    app.register_blueprint(auth_bp.bp)
    db.init_app(app)
    migrate = Migrate(app,db)
    return app

def get_db():
    return db