from flask import Flask, jsonify

from application.services.message import GetMessage

app = Flask(__name__)

@app.route('/message/<message_id>')
def get_message(message_id):
    gm = GetMessage()
    message = gm.call({'id': message_id})
    return jsonify(message.to_dict())