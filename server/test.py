from flask import request, jsonify
from flask_app import init_app
from flask_app.database import get_last_row
import json

app = init_app()

with app.test_client() as c:
    rv = c.post('/climat_save', json=json.dumps({
        'temp': 22.85,
        'hum': 35.12,
        'pres': 576.2,
        'lux': 97.92,
    }))
    lr = get_last_row()
    print(lr.temp, lr.hum, lr.pres, lr.lux)
    lr.delete_instance()
