import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "food_orders_api.settings")
django.setup()

from users.models import User


def main():
    User.objects.filter(username="choujo").delete()


if __name__ == '__main__':
    main()