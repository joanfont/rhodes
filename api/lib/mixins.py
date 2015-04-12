from flask import jsonify, request
from flask.views import MethodView
from api.exceptions.response import CantSerializeArrayError
from common import status
from common.helper import Helper
from application.lib.models import DictMixin


class APIDict(dict):
    pass


class ResponseDict(dict):

    def __init__(self, data, **options):
        many = Helper.instance_of(data, list)
        is_api_dict = False

        if many:
            can_map_fnx = Helper.array_of
        else:
            can_map_fnx = Helper.instance_of

        can_map = can_map_fnx(data, DictMixin)

        # workaround
        if not can_map and not many:
            can_map = Helper.instance_of(data, APIDict)
            is_api_dict = can_map

        if not can_map:
            raise CantSerializeArrayError()
        if not is_api_dict:
            if many:
                results = map(lambda x: x.to_dict(**options), data)

                total = len(results)
                response = {
                    'total': total,
                    'results': results
                }

            else:
                response = data.to_dict(**options)
        else:
            response = data

        super(ResponseDict, self).__init__(response)


class APIView(MethodView):

    def __init__(self, **kwargs):
        super(APIView, self).__init__(**kwargs)
        self.response_args = {}

    @staticmethod
    def get_data():
        return request.args

    @staticmethod
    def post_data():
        return dict(
            (key, request.form.getlist(key) if len(request.form.getlist(key)) > 1 else request.form.getlist(key)[0]) for
            key in request.form.keys())


class ListAPIViewMixin(APIView):

    def get(self, *args, **kwargs):
        raw_data = self.get_action(*args, **kwargs)
        response = ResponseDict(raw_data, **self.response_args)
        status_code = status.HTTP_200_OK
        return jsonify(response), status_code

    def get_action(self, *args, **kwargs):
        raise NotImplementedError()


class CreateAPIViewMixin(APIView):

    def post(self, *args, **kwargs):
        raw_data = self.post_action(*args, **kwargs)
        response = ResponseDict(raw_data, **self.response_args)
        status_code = status.HTTP_201_CREATED
        return jsonify(response), status_code

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
