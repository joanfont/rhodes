from flask import Flask, jsonify

from application.services.message import GetMessage
from application.lib.validators import ValidationError

import status

app = Flask(__name__)


@app.route('/message/<message_id>')
def get_message(message_id):
    gm = GetMessage()
    try:
        message = gm.call({'id': message_id})
    except ValidationError, e:
        return jsonify(e.get_errors()), status.HTTP_400_BAD_REQUEST
    return jsonify(message.to_dict()), status.HTTP_200_OK