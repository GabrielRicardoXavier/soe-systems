from flask import Flask
from saie.routes import bp

app = Flask(__name__)
app.register_blueprint(bp)