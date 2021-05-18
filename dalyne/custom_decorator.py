from django.conf import settings
from rest_framework.response import Response

'''::::::::::: RESPONSE MODIFY DECORATOR FOR COMMON :::::::::::'''


def response_modify_decorator_list(func):
    def inner(self, request, *args, **kwargs):
        response = super(self.__class__, self).list(request, args, kwargs)

        data_dict = {}
        data_dict['result'] = response.data
        if response.data:
            data_dict['request_status'] = 1
            data_dict['msg'] = settings.MSG_SUCCESS
        elif len(response.data) == 0:
            data_dict['request_status'] = 1
            data_dict['msg'] = settings.MSG_NO_DATA
        else:
            data_dict['request_status'] = 0
            data_dict['msg'] = settings.MSG_ERROR
        response.data = data_dict
        return response
    return inner


def response_modify_decorator_get(func):
    def inner(self, request, *args, **kwargs):
        response = super(self.__class__, self).get(self, request, args, kwargs)

        data_dict = {}
        data_dict['result'] = response.data
        if response.data:
            data_dict['request_status'] = 1
            data_dict['msg'] = settings.MSG_SUCCESS
        elif len(response.data) == 0:
            data_dict['request_status'] = 1
            data_dict['msg'] = settings.MSG_NO_DATA
        else:
            data_dict['request_status'] = 0
            data_dict['msg'] = settings.MSG_ERROR
        response.data = data_dict
        return response
    return inner


def response_modify_decorator_get_single(func):
    def inner(self, request, *args, **kwargs):
        response = super(self.__class__, self).get(self, request, args, kwargs)
        data_dict = {}
        if response.data:
            data_dict['request_status'] = 1
            data_dict['result'] = response.data[0]
            data_dict['msg'] = settings.MSG_SUCCESS
        elif len(response.data) == 0:
            data_dict['request_status'] = 1
            data_dict['result'] = ""
            data_dict['msg'] = settings.MSG_NO_DATA
        else:
            data_dict['request_status'] = 0
            data_dict['result'] = ""
            data_dict['msg'] = settings.MSG_ERROR

        response.data = data_dict
        return response
    return inner


'''RESPONSE MODIFY DECORATOR FOR COMMON AFTER EXECUTION'''


def response_modify_decorator_list_after_execution(func):
    def inner(self, request, *args, **kwargs):

        response = func(self, request, *args, **kwargs)
        data_dict = {}
        data_dict['result'] = response.data
        if response.data:
            data_dict['request_status'] = 1
            data_dict['msg'] = settings.MSG_SUCCESS
        elif len(response.data) == 0:
            data_dict['request_status'] = 1
            data_dict['msg'] = settings.MSG_NO_DATA
        else:
            data_dict['request_status'] = 0
            data_dict['msg'] = settings.MSG_ERROR
        response.data = data_dict
        return response
    return inner


def response_modify_decorator_get_after_execution(func):
    def inner(self, request, *args, **kwargs):
        response = func(self, request, *args, **kwargs)
        data_dict = {}
        data_dict['result'] = response.data
        if response.data:
            data_dict['request_status'] = 1
            data_dict['msg'] = settings.MSG_SUCCESS
        elif len(response.data) == 0:
            data_dict['request_status'] = 1
            data_dict['msg'] = settings.MSG_NO_DATA
        else:
            data_dict['request_status'] = 0
            data_dict['msg'] = settings.MSG_ERROR
        response.data = data_dict
        return response
    return inner


def response_modify_decorator_get_single_after_execution(func):
    def inner(self, request, *args, **kwargs):
        response = func(self, request, *args, **kwargs)
        data_dict = {}
        if response.data:
            data_dict['request_status'] = 1
            data_dict['result'] = response.data[0]
            data_dict['msg'] = settings.MSG_SUCCESS
        elif len(response.data) == 0:
            data_dict['request_status'] = 1
            data_dict['result'] = ""
            data_dict['msg'] = settings.MSG_NO_DATA
        else:
            data_dict['request_status'] = 0
            data_dict['result'] = ""
            data_dict['msg'] = settings.MSG_ERROR

        response.data = data_dict
        return response
    return inner


'''RESPONSE MODIFY DECORATOR FOR PAGINATION AND AFTER EXECUTION'''


def response_decorator_list_or_get_after_execution_for_pagination(func):
    def inner(self, request, *args, **kwargs):
        response = func(self, request, *args, **kwargs)
        data_dict = {}
        if response.data:
            data_dict['request_status'] = 1
            data_dict['msg'] = settings.MSG_SUCCESS
        elif len(response.data) == 0:
            data_dict['request_status'] = 1
            data_dict['msg'] = settings.MSG_NO_DATA
        else:
            data_dict['request_status'] = 0
            data_dict['msg'] = settings.MSG_ERROR
        response.data = data_dict
        return response
    return inner


def response_decorator_list_or_get_before_execution_for_pagination(func):
    def inner(self, request, *args, **kwargs):
        response = super(self.__class__, self).get(self, request, args, kwargs)
        data_dict = {}
        data_dict = response.data
        if response.data:
            data_dict['request_status'] = 1
            data_dict['msg'] = settings.MSG_SUCCESS
        elif len(response.data) == 0:
            data_dict['request_status'] = 1
            data_dict['msg'] = settings.MSG_NO_DATA
        else:
            data_dict['request_status'] = 0
            data_dict['msg'] = settings.MSG_ERROR
        response.data = data_dict
        return response
    return inner


def response_modify_decorator_post(func):
    def inner(self, request, *args, **kwargs):
        response = func(self, request, *args, **kwargs)
        data_dict = {}
        if response.data:
            data_dict['request_status'] = 1
            data_dict['result'] = response.data
            data_dict['msg'] = settings.MSG_SUCCESS
        elif len(response.data) == 0:
            data_dict['request_status'] = 1
            data_dict['result'] = ""
            data_dict['msg'] = settings.MSG_NO_DATA
        else:
            data_dict['request_status'] = 0
            data_dict['result'] = ""
            data_dict['msg'] = settings.MSG_ERROR
        return Response(data_dict)
    return inner


def response_modify_decorator_update(func):
    def inner(self, request, *args, **kwargs):
        response = func(self, request, *args, **kwargs)
        data_dict = {}
        if response.data:
            data_dict['request_status'] = 1
            data_dict['result'] = response.data
            data_dict['msg'] = settings.MSG_SUCCESS
        elif len(response.data) == 0:
            data_dict['request_status'] = 1
            data_dict['result'] = ""
            data_dict['msg'] = settings.MSG_NO_DATA
        else:
            data_dict['request_status'] = 0
            data_dict['result'] = ""
            data_dict['msg'] = settings.MSG_ERROR
        return Response(data_dict)
    return inner


'''RESPONSE MODIFY DECORATOR FOR ON OR OFF PAGINATION AND AFTER EXECUTION'''


def response_decorator_list_or_get_after_execution_onoff_pagination(func):
    def inner(self, request, *args, **kwargs):
        response = func(self, request, *args, **kwargs)
        data_dict = {}
        if 'results' in response.data:
            response.data.update({'profile_data': update_element})
            data_dict = response.data
        else:
            data_dict['results'] = response.data

        if response.data:
            data_dict['request_status'] = 1
            data_dict['msg'] = settings.MSG_SUCCESS
        elif len(response.data) == 0:
            data_dict['request_status'] = 1
            data_dict['msg'] = settings.MSG_NO_DATA
        else:
            data_dict['request_status'] = 0
            data_dict['msg'] = settings.MSG_ERROR

        response.data = data_dict
        return response
    return inner


def response_decorator_list_or_get_before_execution_onoff_pagination(func):
    def inner(self, request, *args, **kwargs):
        response = super(self.__class__, self).\
            list(self, request, args, kwargs)
        data_dict = {}
        if 'results' in response.data:
            data_dict = response.data
        else:
            data_dict['results'] = response.data

        if response.data:
            data_dict['request_status'] = 1
            data_dict['msg'] = settings.MSG_SUCCESS
        elif len(response.data) == 0:
            data_dict['request_status'] = 1
            data_dict['msg'] = settings.MSG_NO_DATA
        else:
            data_dict['request_status'] = 0
            data_dict['msg'] = settings.MSG_ERROR

        response.data = data_dict
        return response
    return inner
