from flask import Flask, jsonify, request
from flask.views import MethodView

from application.services.subject import GetStudentSubjects


app = Flask(__name__)


class SubjectsView(MethodView):

    def get(self):
        user_id = request.headers.get('X-UIB-User')
        get_student_subjects_srv = GetStudentSubjects()
        subjects = get_student_subjects_srv.call({'student_id': user_id})
        subjects_dict = map(lambda x: x.to_dict(), subjects)
        return jsonify(subjects=subjects_dict)


app.add_url_rule('/subjects/', view_func=SubjectsView.as_view('subjects'))
