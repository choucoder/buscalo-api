from uuid import uuid4
import re, locale


def get_filename(instance, filename):
    extension = filename.split('.')[-1]
    new_filename = "%s.%s" % (str(uuid4()).replace('-', ''), extension)

    return '/'.join(['images', new_filename])


def generate_random_uuid():
    return str(uuid4())


def clean_str(text: str) -> str:
    cleaned = ' '.join(re.findall('\w+', text))
    return cleaned
