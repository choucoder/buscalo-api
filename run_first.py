import json
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "food_orders_api.settings")
django.setup()

from core.models import Currency


def load_currencies():
    with open('currencies.json') as file:
        currencies = json.loads(file.read())

        for currency in currencies:
            code = currency['code']
            if not Currency.objects.filter(code=code):
                currency = Currency(
                    code=code,
                    name=currency['name'],
                    country=currency['country'],
                    country_code=currency['country_code']
                )
                currency.save()
                print(f"[INFO] Currency {code} from {currency.country} has been saved")
            else:
                print(f"[INFO] Currency {code} from {currency['country']} is already registered")


if __name__ == '__main__':
    load_currencies()