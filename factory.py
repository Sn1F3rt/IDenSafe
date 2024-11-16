import click
from web3 import Web3
from flask import Flask, flash
from flask_wtf import CSRFProtect
from flask_cors import CORS
from flask_login import LoginManager, current_user

from utils.crud import get_kyc_status, reset_kyc_status, pending_notification
from utils.models import Base
from utils.database import engine

csrf: CSRFProtect
w3: Web3


def setup_db():
    Base.metadata.create_all(bind=engine)


def create_app() -> Flask:
    app = Flask(__name__, static_url_path="/assets", static_folder="assets")
    CORS(app, allow_origin="*")
    app.config.from_pyfile("config.py")

    global csrf
    csrf = CSRFProtect()
    csrf.init_app(app)

    global w3
    w3 = Web3(Web3.HTTPProvider(app.config["WEB3_PROVIDER"]))

    setup_db()

    login_manager = LoginManager()
    login_manager.init_app(app)

    with app.app_context():

        @login_manager.user_loader
        def _load_user(address: str):
            from utils.models import User
            from utils.database import create_session

            session = create_session()
            return session.query(User).filter(User.address == address).first()

        @login_manager.unauthorized_handler
        def _unauthorized():
            from flask import flash, url_for, redirect

            flash("You must be logged in to access this page.", "warning")
            return redirect(url_for("meta._index"))

        @app.before_request
        def _before_request():
            from utils.models import User

            if isinstance(current_user, User) and pending_notification(
                current_user.address
            ):
                if get_kyc_status(current_user.address) == -1:
                    flash("Your KYC has been rejected.", "error")
                else:
                    flash(f"Your KYC has been verified and approved.", "success")

                reset_kyc_status(current_user.address)

        @app.template_filter("format")
        def _format(dt):
            return dt.strftime("%Y-%m-%d %H:%M:%S")

        @app.cli.command("make_admin")
        @click.argument("username")
        def _make_admin(username: str):
            from utils.models import User
            from utils.database import create_session

            session = create_session()
            user = session.query(User).filter(User.username == username).first()

            if not user:
                click.echo("User not found.")
                return

            user.admin = True
            session.commit()

            click.echo(f"User {username} is now an admin.")

        @app.cli.command("remove_admin")
        @click.argument("username")
        def _remove_admin(username: str):
            from utils.models import User
            from utils.database import create_session

            session = create_session()
            user = session.query(User).filter(User.username == username).first()

            if not user:
                click.echo("User not found.")
                return

            user.admin = False
            session.commit()

            click.echo(f"User {username} is no longer an admin.")

        @app.before_request
        def _check_username():
            from flask import request, url_for, redirect
            from flask_login import current_user

            if request.endpoint in ["auth._username", "auth._logout", "static"]:
                return

            if current_user.is_authenticated and not current_user.username:
                return redirect(url_for("auth._username"))

    from blueprints.app import app_bp
    from blueprints.auth import auth_bp
    from blueprints.meta import meta_bp
    from blueprints.admin import admin_bp

    app.register_blueprint(admin_bp)
    app.register_blueprint(app_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(meta_bp)

    csrf.exempt("blueprints.auth.routes._message")
    csrf.exempt("blueprints.auth.routes._verify")
    csrf.exempt("blueprints.admin.routes._record")

    return app
