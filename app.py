from extensions import mail

from flask import Flask
from itsdangerous import URLSafeTimedSerializer
from routes.auth import auth_bp_bp
from routes.student import student_bp
from routes.admin import admin_bp
from routes.public import public_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
mail.init_app(app)
app.secret_key = os.getenv("SECRET_KEY", "fallback-secret")
serializer = URLSafeTimedSerializer(os.getenv('SECRET_KEY'))
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')

app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(public_bp)

if __name__ == "__main__":
    app.run(debug=True)
