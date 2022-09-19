from django.http import JsonResponse
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import exception_handler

from uo_core.global_message import GlobalMessage


def get_error_message(error_dict):
    field = next(iter(error_dict))
    response = error_dict[next(iter(error_dict))]
    if isinstance(response, dict):
        response = get_error_message(response)
    elif isinstance(response, list):
        response_message = response[0]
        if isinstance(response_message, dict):
            response = get_error_message(response_message)
        else:
            response = response[0]
    return response


def handle_exception(exc, context):
    error_response = exception_handler(exc, context)
    if error_response is not None:
        error = error_response.data

        if isinstance(error, list) and error:
            if isinstance(error[0], dict):
                error_response.data = CustomResponse.get_response_body(
                    message=get_error_message(error),
                    status_code=error_response.status_code,
                )

            elif isinstance(error[0], str):
                error_response.data = CustomResponse.get_response_body(
                    message=error[0],
                    status_code=error_response.status_code
                )

        if isinstance(error, dict):
            error_response.data = CustomResponse.get_response_body(
                message=get_error_message(error),
                status_code=error_response.status_code
            )
    if error_response and error_response.status_code == 400:
        error_response.status_code = status.HTTP_208_ALREADY_REPORTED
    return error_response


class ExceptionMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        if response.status_code == 500:
            response = CustomResponse.get_response_body(
                message="Internal server error, please try again later",
                status_code=response.status_code
            )
            return JsonResponse(response, status=response['status_code'])

        if response.status_code == 404 and "Page not found" in str(response.content):
            response = CustomResponse.get_response_body(
                message="Page not found, invalid url",
                status_code=response.status_code
            )
            return JsonResponse(response, status=response['status_code'])

        return response


class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if not 'status_code' in data:
            response_data = {'message': '', 'status_code': 200, 'result': data, 'status': True}
            getattr(renderer_context.get('view').get_serializer(), 'resource_name', 'objects')
            # call super to render the response
            response = super(CustomJSONRenderer, self).render(response_data, accepted_media_type, renderer_context)
        else:
            print('CustomJSONRenderer data', data)
            response = super(CustomJSONRenderer, self).render(data, accepted_media_type, renderer_context)
        return response


class CustomResponse(Response):
    def __init__(self, result=None, status=True, message=GlobalMessage.SUCCESS, status_code=200, extra_data=None,
                 tapa_code=0):
        self.data = CustomResponse.get_response_body(message, result, status, status_code, extra_data, tapa_code)
        super().__init__(self.data, status=self.data['status_code'])

    @staticmethod
    def get_response_body(message="", result=None, status=False, status_code=200, extra_data=None, error_code=0):

        return {
            "message": message,
            "result": result,
            "extra_data": extra_data,
            "status": status,
            "status_code": status_code,
            "error_code": error_code,
        }
