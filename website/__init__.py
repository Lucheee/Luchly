import os
from flask import Flask
from .utils import db
from flask_login import LoginManager
from .auth import auth
from .base import base
from .urls import urls
from .models import User, URL
from .account import account
from dotenv import load_dotenv
from flask_migrate import Migrate
from flask_mail import Mail
from flask_mail import Mail
from flask_share import Share
from flask_caching import Cache
load_dotenv() 
BASE_DIR = os.path.dirname(os.path.realpath(__file__))
import os


app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3')
app.config["SECRET_KEY"] = 'dcabc46275bceb98bf55e21c'
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config['CACHE_TYPE'] = 'SimpleCache'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300



mail = Mail(app)
share = Share(app)
cache = Cache(app)

app.register_blueprint(auth, url_prefix="/")
app.register_blueprint(base, url_prefix="/")
app.register_blueprint(urls, url_prefix="/")
app.register_blueprint(account, url_prefix="/")

    
      
db.init_app(app)  
migrate = Migrate(app,db)
mail = Mail(app)

    
    
    
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)
    
    
@login_manager.user_loader
def load_user(user_id):
     return User.query.get(int(user_id))

    


@app.shell_context_processor
def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Url':URL,
            
            
        }

#return app


