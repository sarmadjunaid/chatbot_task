from flask import Blueprint, render_template
from utils import login_required

chat_app = Blueprint('chat_app', __name__, template_folder='templates')


@chat_app.route('/', methods=['GET'])
@login_required
def home():
    return render_template('chat.html')
