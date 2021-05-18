from rest_framework.exceptions import APIException
from rest_framework import exceptions


def custom_exception_message(self, field_name: str, msg: str = None):
    if msg:
        raise APIException({
                    "error": {
                        'request_status': 0,
                        'msg': msg
                        }
                    })
    else:
        raise APIException({
                    "error": {
                        'request_status': 0,
                        'msg': field_name + " already exist"
                        }
                    })


class CustomAPIException(exceptions.APIException):
    status_code = None
    default_code = 'error'

    def __init__(self, detail: str, msg: str = None, status_code=None):
        if msg:
            self.detail = {
                            'request_status': 0,
                            'msg': msg
                        }

        if status_code is not None:
            self.status_code = status_code
