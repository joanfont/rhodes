from flask import jsonify
from flask.views import MethodView
from flask import request

from api.decorators import login_required
from application.lib.models import DictMixin as ModelDictMixin
from application.services.group import GetUserGroups
import common.status as status
from application.services.subject import GetUserSubjects, GetUserSubject
from common.exceptions import BaseError, CantSerializeArrayError
from common.helper import Helper


class ResponseDictMixin(dict):

    kwargs = {}

    def to_dict(self, data):
        kwargs = self.kwargs
        many = Helper.instance_of(data, list)

        if many:
            can_map_fnx = Helper.array_of
        else:
            can_map_fnx = Helper.instance_of

        can_map = can_map_fnx(data, ModelDictMixin)

        if not can_map:
            raise CantSerializeArrayError()

        if many:
            results = map(lambda x: x.to_dict(**kwargs), data)
            total = len(results)
            response = {
                'total': total,
                'results': results
            }

        else:
            response = data.to_dict(**kwargs)

        return response


class ListAPIViewMixin(ResponseDictMixin, MethodView):

    def get(self, *args, **kwargs):
        try:
            raw_data = self.get_action(*args, **kwargs)
            response = self.to_dict(raw_data)
            status_code = status.HTTP_200_OK
        except BaseError, e:
            response = e.error
            status_code = e.status_code

        return jsonify(response), status_code

    def get_action(self, *args, **kwargs):
        raise NotImplementedError()


class CreateAPIViewMixin(MethodView):

    def post(self, *args, **kwargs):
        pass

    def post_action(self, *args, **kwargs):
        raise NotImplementedError()


class UpdateAPIView(MethodView):

    def put(self, *args, **kwargs):
        pass

    def patch(self, *args, **kwargs):
        pass

    def put_action(self, *args, **kwargs):
        raise NotImplementedError()

    def patch_action(self, *args, **kwargs):
        raise NotImplementedError()


class DeleteAPIView(MethodView):

    def delete(self, *args, **kwargs):
        pass

    def delete_action(self, *args, **kwargs):
        raise NotImplementedError()


class SubjectsView(ListAPIViewMixin):

    def __init__(self):
        self.kwargs = {
            'with_student_group': False,
            'with_groups': False
        }

    @login_required
    def get_action(self, *args, **kwargs):
        user = kwargs.get('user')

        if user.is_teacher():
            self.kwargs['with_groups'] = True
        elif user.is_student():
            self.kwargs['with_student_group'] = True

        get_user_subjects_srv = GetUserSubjects()
        subjects = get_user_subjects_srv.call({'user_id': user.id})
        return subjects


class SubjectDetailView(ListAPIViewMixin):

    def __init__(self):
        self.kwargs = {
            'with_student_group': False,
            'with_groups': False
        }

    @login_required
    def get_action(self, *args, **kwargs):

        user = kwargs.get('user')
        subject_id = kwargs.get('subject_id')

        if user.is_teacher():
            self.kwargs['with_groups'] = True
        elif user.is_student():
            self.kwargs['with_student_group'] = True

        get_subject_srv = GetUserSubject()
        subject = get_subject_srv.call({'id': subject_id, 'user_id': user.id})
        return subject


class GroupsView(ListAPIViewMixin):

    @login_required
    def get_action(self, *args, **kwargs):
        user = kwargs.get('user')
        get_user_groups_srv = GetUserGroups()
        groups = get_user_groups_srv.call({'user_id': user.id})
        return groups


# class SubjectMessagesView(ModelAPIView):
#
#     @login_required
#     def get_action(self, *args, **kwargs):
#         subject_id = kwargs.get('subject_id')
#         get_subject_messages_srv = GetSubjectMessages()
#         messages = get_subject_messages_srv.call({'subject_id': subject_id})
#         return messages, status.HTTP_200_OK
#
#     @staticmethod
#     def get_post_args():
#         req = request.form
#         return {
#             'body': req.get('body')
#         }
#
#     @login_required
#     def post_action(self, *args, **kwargs):
#         params = self.get_post_args()
#         user = kwargs.get('user')
#         subject_id = kwargs.get('subject_id')
#         params.update({
#             'sender_id': user.id,
#             'created_at': datetime.now(),
#             'recipient_id': subject_id,
#         })
#
#         put_subject_message_srv = PutSubjectMessage()
#         message = put_subject_message_srv.call(params)
#         return message, status.HTTP_201_CREATED
#
#
