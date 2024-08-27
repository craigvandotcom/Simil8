from flask import Flask
from flask_cors import CORS
from .config import Config

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(Config)

    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app