from rest_framework.exceptions import APIException

class TextOrPhotoException(APIException):
    status_code = 400
    default_detail = "You should send a text or photo to make a post"


class PostDeniedException(APIException):
    status_code = 400
    default_detail = "You don't have enough push post amount, buy it"