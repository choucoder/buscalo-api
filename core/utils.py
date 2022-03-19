from datetime import datetime, timedelta
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


def get_time_ago(d1: datetime, d2: datetime) -> str:
    """
    minutos, horas, dias, semanas, meses, años
    """
    diff = d2 - (d1 - timedelta(hours=4))
    years = diff.days // 365
    months = diff.days // 30
    weeks = diff.days // 7
    days = diff.days
    hours = diff.seconds // 3600
    minuts = diff.seconds // 60

    ago_number = 0
    ago_string = ""

    if years:
        ago_string = "año" if years == 1 else "años"
        ago_number = years
    elif months:
        ago_string = "mes" if months == 1 else "meses"
        ago_number = months
    elif weeks:
        ago_string = "semana" if weeks == 1 else "semanas"
        ago_number = weeks
    elif days:
        ago_string = "dia" if days == 1 else "dias"
        ago_number = days
    elif hours:
        ago_string = "hora" if hours == 1 else "horas"
        ago_number = hours
    elif minuts:
        ago_string = "minuto" if minuts == 1 else "minutos"
        ago_number = minuts
    else:
        ago_string = "ahora"
        ago_number = diff.seconds

    if ago_string != "ahora":
        return f"hace {ago_number} {ago_string}"

    return "ahora"