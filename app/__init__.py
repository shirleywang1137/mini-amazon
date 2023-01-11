from flask import Flask
from flask_login import LoginManager
from .config import Config
from .db import DB


login = LoginManager()
login.login_view = 'users.login'


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.db = DB(app)
    login.init_app(app)

    from .index import bp as index_bp
    app.register_blueprint(index_bp)

    from .users import bp as user_bp
    app.register_blueprint(user_bp)

    from .api import bp as api_bp
    app.register_blueprint(api_bp)

    from .loginview import bp as loginview_bp
    app.register_blueprint(loginview_bp)

    from .productsearch import bp as productsearch_bp
    app.register_blueprint(productsearch_bp)

    from .addcart import bp as addcart_bp
    app.register_blueprint(addcart_bp)

    from .addorder import bp as addorder_bp
    app.register_blueprint(addorder_bp)

    from .reviewHome import bp as reviewHome_bp
    app.register_blueprint(reviewHome_bp)

    from .sellerview import bp as sellerview_bp
    app.register_blueprint(sellerview_bp)

    from .wishlistitem import bp as wishlistitem_bp
    app.register_blueprint(wishlistitem_bp)


    return app
