from flask import Flask
from quickredtech.extensions import db, migrate, login_manager
from quickredtech.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
migrate.init_app(app, db)
login_manager.init_app(app)


from quickredtech import models
from quickredtech.routes import register_routes
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
