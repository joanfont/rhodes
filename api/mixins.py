from flask import jsonify, request
from flask.views import MethodView
from common import status
from common.exceptions import CantSerializeArrayError, BaseError
from common.helper import Helper
from application.lib.models import DictMixin


class ResponseDict(dict):

    def __init__(self, data, **options):
        many = Helper.instance_of(data, list)

        if many:
            can_map_fnx = Helper.array_of
        else:
            can_map_fnx = Helper.instance_of

        can_map = can_map_fnx(data, DictMixin)

        if not can_map:
            raise CantSerializeArrayError()

        if many:
            results = map(lambda x: x.to_dict(**options), data)

            total = len(results)
            response = {
                'total': total,
                'results': results
            }

        else:
            response = data.to_dict(**options)

        super(ResponseDict, self).__init__(response)


class APIView(MethodView):

    def __init__(self, *args, **kwargs):
        super(APIView, self).__init__(*args, **kwargs)
        self.response_args = {}


class ListAPIViewMixin(APIView):

    def get(self, *args, **kwargs):
        try:
            raw_data = self.get_action(*args, **kwargs)
            response = ResponseDict(raw_data, **self.response_args)
            status_code = status.HTTP_200_OK
        except BaseError, e:
            response = e.error
            status_code = e.status_code

        return jsonify(response), status_code

    def get_action(self, *args, **kwargs):
        raise NotImplementedError()


class CreateAPIViewMixin(APIView):

    def post(self, *args, **kwargs):
        try:
            raw_data = self.post_action(*args, **kwargs)
            response = ResponseDict(raw_data, **self.response_args)
            status_code = status.HTTP_201_CREATED
        except BaseError, e:
            response = e.error
            status_code = e.status_code

        return jsonify(response), status_code

    @staticmethod
    def post_data():
        return dict(
            (key, request.form.getlist(key) if len(request.form.getlist(key)) > 1 else request.form.getlist(key)[0]) for
            key in request.form.keys())

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
