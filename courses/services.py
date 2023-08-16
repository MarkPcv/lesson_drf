import stripe   # library to handle payments
from django.conf import settings


def create_payment(amount):
    stripe.api_key = settings.STRIPE_API_KEY
    response = stripe.PaymentIntent.create(
                    amount=amount,
                    currency="usd",
                    automatic_payment_methods={"enabled": True},
                )
    return response['id']


def retrieve_payment(payment_id):
    stripe.api_key = settings.STRIPE_API_KEY
    response = stripe.PaymentIntent.retrieve(
                    payment_id,
                )
    if response['amount'] - response['amount_received'] > 0:
        return 'paid'
    return 'unprocessed'