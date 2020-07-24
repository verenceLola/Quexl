"""Add paypal payments to the db"""
from quexl.apps.orders.models import PaypalPayment


def save_payment_details(**kwargs):
    obj = PaypalPayment(
        order=kwargs.get("order"), paypal_id=kwargs.get("paypal_id")
    )
    obj.save()
