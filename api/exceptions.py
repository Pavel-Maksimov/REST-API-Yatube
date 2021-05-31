from rest_framework.exceptions import APIException


class ActionDenied(APIException):
    status_code = 400
    default_detail = 'Невозможно совершить запрос.'
    default_code = 'Bad Request'
