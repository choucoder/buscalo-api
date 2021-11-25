from rest_framework.exceptions import APIException

class OrderIsFinishedException(APIException):
    status_code = 400
    default_detail = "You can not remove the item because the order is already completed/canceled"