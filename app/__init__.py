from flask import Flask


app = Flask(__name__)
from app import views ## put this after to avoid circular import error
