from .models import Order
from .exceptions import *


def abort_if_order_is_finished(order):
    if order.status != Order.CREATED:
        raise OrderIsFinishedException