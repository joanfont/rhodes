from flask import Flask, jsonify

from application.services.message import GetMessage
from application.lib.validators import ValidationError

app = Flask(__name__)


@app.route('/message/<message_id>')
def get_message(message_id):
    gm = GetMessage()
    try:
        message = gm.call({'id': message_id})
    except ValidationError, e:
        return jsonify(e.get_errors()), 400
    return jsonify(message.to_dict()), 200