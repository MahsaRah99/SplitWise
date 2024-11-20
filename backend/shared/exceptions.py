import logging

from django.db import IntegrityError
from django.http import JsonResponse
from django.http.response import Http404
from rest_framework import status
from rest_framework.exceptions import APIException, NotFound
from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler


class APIExceptionWithMetadata(APIException):
    def __init__(self, status_code, code, detail, metadata=None):
        super().__init__(code=code, detail=detail)
        self.status_code = status_code
        self.metadata = metadata


def new_response_for(exception, status_code):
    return Response(
        status=status_code, data={"code": exception.code, "detail": exception.detail}
    )


def exception_handler(e, context):
    response = drf_exception_handler(e, context)
    try:
        if isinstance(e, IntegrityError):
            logging.exception(e)
            return Response(
                status=status.HTTP_409_CONFLICT, data={"code": "integrity_error"}
            )
        if isinstance(e, APIExceptionWithMetadata):
            return Response(
                status=e.status_code,
                data={
                    "code": e.get_codes(),
                    "detail": e.detail,
                    "metadata": e.metadata,
                },
            )
        if isinstance(e, Http404):
            response.data["code"] = NotFound.default_code
            response.data["detail"] = NotFound.default_detail
            return response
        if not isinstance(response.data, dict):
            response.data = {}
        response.data["code"] = e.get_codes()
        response.data["detail"] = "{detail}".format(detail=e.detail)
        if hasattr(e, "metadata"):
            response.data["metadata"] = e.metadata
        return response
    except Exception:
        return response


# It should get replaced by APIExceptionWithMetadata
class JsonError(JsonResponse, Exception):
    def __init__(self, code, message, status=400):
        super().__init__({"code": code, "message": message}, status=status)
