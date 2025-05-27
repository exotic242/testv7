
from flask import Flask
from routes.auth import auth_bp
from routes.student import student_bp
from routes.admin import admin_bp
from routes.public import public_bp
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "fallback-secret")

app.register_blueprint(auth_bp)
app.register_blueprint(student_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(public_bp)

if __name__ == "__main__":
    app.run(debug=True)
