from flask import request, Response
from flask.views import MethodView
from common import status
from common.helper import Helper
import json


class JSONResponse(Response):

    mimetype = 'application/json'
    content_type = 'application/json'

    def __init__(self, response=None, status_code=None):
        response = json.dumps(response)
        super(JSONResponse, self).__init__(response, status_code, mimetype=self.mimetype, content_type=self.content_type)


class ModelResponse(JSONResponse):

    def __init__(self, data, **options):
        many = Helper.instance_of(data, list)

        if many:
            response = map(lambda x: x.to_dict(**options), data)
        else:
            response = data.to_dict(**options)

        super(ModelResponse, self).__init__(response=response)


class BaseResponseMixin(object):

    response_class = None
    response_args = {}


class ModelResponseMixin(BaseResponseMixin):

    response_class = ModelResponse


class APIView(MethodView, BaseResponseMixin):

    status_code = 0

    def __init__(self, **kwargs):
        super(APIView, self).__init__(**kwargs)

    @staticmethod
    def get_data():
        return request.args

    @staticmethod
    def post_data():
        return dict(
            (key, request.form.getlist(key) if len(request.form.getlist(key)) > 1 else request.form.getlist(key)[0]) for
            key in request.form.keys())


class ListAPIViewMixin(APIView):

    status_code = status.HTTP_200_OK

    def get(self, *args, **kwargs):
        response_data = self.get_action(*args, **kwargs)
        response = self.response_class(response_data, **self.response_args)
        response.status_code = self.status_code
        return response

    def get_action(self, *args, **kwargs):
        raise NotImplementedError()


class CreateAPIViewMixin(APIView):

    status_code = status.HTTP_201_CREATED

    def post(self, *args, **kwargs):
            response_data = self.post_action(*args, **kwargs)
            response = self.response_class(response_data, **self.response_args)
            response.status_code = self.status_code
            return response

    def post_action(self, *args, **kwargs):
        raise NotImplementedError()


class UpdateAPIView(APIView):

    def put(self, *args, **kwargs):
        pass

    def patch(self, *args, **kwargs):
        pass

    def put_action(self, *args, **kwargs):
        raise NotImplementedError()

    def patch_action(self, *args, **kwargs):
        raise NotImplementedError()


class DeleteAPIView(APIView):

    def delete(self, *args, **kwargs):
        pass

    def delete_action(self, *args, **kwargs):
        raise NotImplementedError()