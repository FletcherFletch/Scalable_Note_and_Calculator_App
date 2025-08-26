import stripe
from decouple import config 

#Change test

DJANGO_DEBUG=config("DJANGO_DEBUG", default=False, cast=bool)
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default="", cast=str)

stripe.api_key = STRIPE_SECRET_KEY

def create_customer (
        name="",
        email="",
        metadata={},
        raw=False):
    response = stripe.Customer.create(
        name=name,
        email=email,
        metadata=metadata,
    )

    if raw:
        return response
    stripe_id = response.id
    return stripe_id

def create_product (name="",
                    metadata={},
                    raw=False):
    product = stripe.Product.create(
        name=name,
        metadata=metadata
    )

    if raw:
        return product
    product_id = product.id
    return product_id

def create_price ( currency = "usd",
                  product = "",
                  unit_amount = "9999",
                  metadata={},
                  raw=False,):
    if product is None:
        return None
    price = stripe.Price.create(
        currency=currency,
        product=product,
        unit_amount=unit_amount,
        metadata=metadata,
    )

    if raw:
        return price
    price_id = price.id
    return price_id

def start_checkout_session(customer_id,                    
                     success_url="",
                     cancel_url="",
                     price_id="",
                     raw=True,
                     ):
    if not success_url.endswith("?session_id={CHECKOUT_SESSION_ID}"):
        success_url = f"{success_url}" + "?session_id={CHECKOUT_SESSION_ID}"
    session = stripe.checkout.Session.create(
        customer=customer_id,
        success_url=success_url,
        cancel_url=cancel_url,
        line_items=[{"price": price_id, "quantity": 1}],
        mode="payment",
    )
    if raw:
        return session
    return session.url

def get_checkout_session(stripe_id, raw=True):
    response = stripe.checkout.Session.retrieve(
        stripe_id
    )
    if raw:
        return response
    return response.url 