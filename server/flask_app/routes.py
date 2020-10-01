from flask import current_app as app
from flask import request, json
from flask_app.database import save_to_base


@app.route('/')
def home():
    return 'hi'


@app.route('/climat_save', methods=['POST'])
def climat_save():

    # TODO Провести тест запроса

    data = json.loads(request.json)
    if save_to_base(data) == 0:
        return 'ok'
    else:
        return "error"
