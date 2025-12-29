from flask import Flask
from dotenv import load_dotenv
from backend.routes.admin_routes import admin_bp
import os

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
from backend.routes.contact_routes import contact_bp
app.register_blueprint(contact_bp)
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    app.run(debug=True)
