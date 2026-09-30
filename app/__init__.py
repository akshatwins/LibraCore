from flask import Flask, render_template
from .config import Config
from .extensions import db, login_manager, migrate

def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    app.config["SQLALCHEMY_DATABASE_URI"] = app.config.get("DATABASE_URL", "sqlite:///library.db")

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from .routes.auth import auth_bp
    from .routes.dashboard import dashboard_bp
    from .routes.books import books_bp
    from .routes.members import members_bp
    from .routes.circulation import circulation_bp
    from .routes.api import api_bp
    from .routes.reservations import reservations_bp
    from .routes.notifications import notifications_bp
    from .routes.analytics import analytics_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(books_bp)
    app.register_blueprint(members_bp)
    app.register_blueprint(circulation_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(reservations_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(analytics_bp)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("errors/403.html"), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template("errors/500.html"), 500

    with app.app_context():
        db.create_all()

    return app
