from flask import jsonify
from flask.views import MethodView

from api.decorators import login_required
import common.status as status
from application.services.subject import GetStudentSubjects
from application.lib.models import DictMixin

from common.exceptions import BaseError, CantSerializeArrayError
from common.helper import Helper

from collections import OrderedDict


class ModelAPIView(MethodView):

    def get(self, *args, **kwargs):

        try:
            data = self.get_data(*args, **kwargs)
            response = ModelAPIView.to_dict(data)
            code = status.HTTP_200_OK
        except BaseError, e:
            response = {'errors': e.errors}
            code = e.status_code

        return jsonify(response), code

    def get_data(self):
        raise NotImplementedError()

    @staticmethod
    def to_dict(array_of_models):
        can_map = Helper.array_of(array_of_models, DictMixin)

        if not can_map:
            raise CantSerializeArrayError()

        results = map(lambda x: x.to_dict(), array_of_models)

        return OrderedDict(
            (('total', len(results)),
             ('results', results)
            ))


class SubjectsView(ModelAPIView):

    @login_required
    def get_data(self, *args, **kwargs):
        user = kwargs.get('user')
        get_student_subjects_srv = GetStudentSubjects()
        subjects = get_student_subjects_srv.call({'student_id': user.id})
        return subjects
