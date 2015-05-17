from flask import request, Response
from flask.views import MethodView
from api.lib.decorators import copy_params
from application.services.media import GetMediaBytes
from common import status
from common.helper import Helper
import json


class JSONResponse(Response):
    mimetype = 'application/json'
    content_type = 'application/json'

    def __init__(self, response=None, status_code=None):
        response = json.dumps(response)
        super(JSONResponse, self).__init__(response, status_code, mimetype=self.mimetype,
                                           content_type=self.content_type)


class ModelResponse(JSONResponse):
    def __init__(self, data, **options):
        many = Helper.instance_of(data, list)

        if many:
            response = map(lambda x: x.to_dict(**options), data)
        else:
            response = data.to_dict(**options)

        super(ModelResponse, self).__init__(response=response)


class PaginatedResponse(JSONResponse):
    def __init__(self, data, **options):
        response = data.to_dict(**options)
        super(PaginatedResponse, self).__init__(response=response)


class MediaResponse(Response):

    def __init__(self, media, **options):

        get_media_bytes_srv = GetMediaBytes()
        media_bytes = get_media_bytes_srv.call({
            'media': media
        })
        super(MediaResponse, self).__init__(response=media_bytes, status=status.HTTP_200_OK, mimetype=media.mime,
                                            content_type=media.mime)


class BaseResponseMixin(object):
    response_class = JSONResponse

    def __init__(self):
        super(BaseResponseMixin, self).__init__()
        self.response_args = {}


class ModelResponseMixin(BaseResponseMixin):

    response_class = ModelResponse


class PaginatedResponseMixin(BaseResponseMixin):

    response_class = PaginatedResponse


class MediaResponseMixin(BaseResponseMixin):

    response_class = MediaResponse


class APIView(BaseResponseMixin, MethodView):
    PARAM_URL = 1
    PARAM_GET = 2
    PARAM_POST = 3
    PARAM_FILES = 4

    status_code = 0

    def __init__(self, **kwargs):
        super(BaseResponseMixin, self).__init__()
        super(APIView, self).__init__(**kwargs)

    def params(self):
        return {}

    @staticmethod
    def get_data():
        return request.args

    @staticmethod
    def post_data():
        return dict(
            (key, request.form.getlist(key) if len(request.form.getlist(key)) > 1 else request.form.getlist(key)[0]) for
            key in request.form.keys())

    @staticmethod
    def files_data():
        return dict(
            (key, request.files.getlist(key) if len(request.files.getlist(key)) > 1 else request.files.getlist(key)[0])
            for key in request.files.keys())


class ListAPIViewMixin(APIView):

    status_code = status.HTTP_200_OK

    @copy_params
    def get(self, *args, **kwargs):
        response_data = self.get_action(*args, **kwargs)
        response = self.response_class(response_data, **self.response_args)
        response.status_code = self.status_code
        return response

    def get_action(self, *args, **kwargs):
        raise NotImplementedError()


class CreateAPIViewMixin(APIView):
    status_code = status.HTTP_201_CREATED

    @copy_params
    def post(self, *args, **kwargs):
        response_data = self.post_action(*args, **kwargs)
        response = self.response_class(response_data, **self.response_args)
        response.status_code = self.status_code
        return response

    def post_action(self, *args, **kwargs):
        raise NotImplementedError()


class UpdateAPIViewMixin(APIView):

    status_code = status.HTTP_202_ACCEPTED

    @copy_params
    def put(self, *args, **kwargs):
        response_data = self.put_action(*args, **kwargs)
        response = self.response_class(response_data, **self.response_args)
        response.status_code = self.status_code
        return response

    def put_action(self, *args, **kwargs):
        raise NotImplementedError()


class PartialUpdateAPIViewMixin(APIView):

    status_code = status.HTTP_202_ACCEPTED

    @copy_params
    def patch(self, *args, **kwargs):
        response_data = self.patch_action(*args, **kwargs)
        response = self.response_class(response_data, **self.response_args)
        response.status_code = self.status_code
        return response

    def patch_action(self, *args, **kwargs):
        raise NotImplementedError()


class DeleteAPIViewMixin(APIView):
    def delete(self, *args, **kwargs):
        pass

    def delete_action(self, *args, **kwargs):
        raise NotImplementedError()