from flask import Blueprint

bp = Blueprint('canvas', __name__)

from app.canvas import routes