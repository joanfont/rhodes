from collections import OrderedDict

from flask import jsonify
from flask.views import MethodView
from flask import request

from api.decorators import login_required
from application.services.group import GetUserGroups
from application.services.message import PutSubjectMessage, GetSubjectMessages
import common.status as status
from application.services.subject import GetUserSubjects
from application.lib.models import DictMixin
from common.exceptions import BaseError, CantSerializeArrayError
from common.helper import Helper

from datetime import datetime


class ModelAPIView(MethodView):
    def get(self, *args, **kwargs):

        try:
            data, code = self.get_action(*args, **kwargs)
            response = ModelAPIView.to_dict(data)
        except BaseError, e:
            response = e.error
            code = e.status_code

        return jsonify(response), code

    def post(self, *args, **kwargs):
        try:
            data, code = self.post_action(self, *args, **kwargs)
            response = ModelAPIView.to_dict(data)
        except BaseError, e:
            response = e.error
            code = e.status_code

        return jsonify(response), code

    def get_action(self, *args, **kwargs):
        raise NotImplementedError()

    def post_action(self, *args, **kwargs):
        raise NotImplementedError()

    @staticmethod
    def to_dict(data):

        many = Helper.instance_of(data, list)

        if many:
            can_map_fnx = Helper.array_of
        else:
            can_map_fnx = Helper.instance_of

        can_map = can_map_fnx(data, DictMixin)

        if not can_map:
            raise CantSerializeArrayError()

        if many:
            results = map(lambda x: x.to_dict(), data)
            total = len(results)
            response = {
                'total': total,
                'results': results
            }

        else:
            response = data.to_dict()

        return response


class SubjectsView(ModelAPIView):

    @login_required
    def get_action(self, *args, **kwargs):
        user = kwargs.get('user')
        get_user_subjects_srv = GetUserSubjects()
        subjects = get_user_subjects_srv.call({'user_id': user.id})
        return subjects, status.HTTP_200_OK

    def post_action(self, *args, **kwargs):
        pass


class GroupsView(ModelAPIView):
    @login_required
    def get_action(self, *args, **kwargs):
        user = kwargs.get('user')
        get_user_groups_srv = GetUserGroups()
        groups = get_user_groups_srv.call({'user_id': user.id})
        return groups, status.HTTP_200_OK

    def post_action(self):
        pass


class SubjectMessagesView(ModelAPIView):

    @login_required
    def get_action(self, *args, **kwargs):
        subject_id = kwargs.get('subject_id')
        get_subject_messages_srv = GetSubjectMessages()
        messages = get_subject_messages_srv.call({'subject_id': subject_id})
        return messages, status.HTTP_200_OK

    @staticmethod
    def get_post_args():
        req = request.form
        return {
            'body': req.get('body')
        }

    @login_required
    def post_action(self, *args, **kwargs):
        params = self.get_post_args()
        user = kwargs.get('user')
        subject_id = kwargs.get('subject_id')
        params.update({
            'sender_id': user.id,
            'created_at': datetime.now(),
            'recipient_id': subject_id,
        })

        put_subject_message_srv = PutSubjectMessage()
        message = put_subject_message_srv.call(params)
        return message, status.HTTP_201_CREATED


