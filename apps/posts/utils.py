from typing import Text
from .models import Post
from .exceptions import *

def has_text_or_photo(data, fields=['text', 'photo']):
    times = 0

    for field in fields:
        if field in data:
            times += 1

    if times > 0:
        return True
    else:
        raise TextOrPhotoException()


def is_allowed_to_post(data, user):
    notify_type = data.get('notify_type', Post.FEED)

    if notify_type == Post.PUSH:
        if user.push_post_amount <= 0:
            raise PostDeniedException()

    return True

