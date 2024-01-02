from django.conf import settings
from django.shortcuts import redirect

from content.models import Like, Dislike
from users.models import User

import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


def toggle_like(like: Like):
    """
    Функция переключающая активность лайка
    :param like: Объект модели Like
    :return: None
    """
    if like.is_active:
        like.is_active = False
        like.save()
    else:
        like.is_active = True
        like.save()


def toggle_dislike(dislike: Dislike):
    """
    Функция переключающая активность лайка
    :param dislike: Объект модели Dislike
    :return: None
    """
    if dislike.is_active:
        dislike.is_active = False
        dislike.save()
    else:
        dislike.is_active = True
        dislike.save()


def create_product(instance: User):
    """
    Функция, создающая продукт
    :param instance: Объект User
    :return: Объект stripe.Product
    """
    product = stripe.Product.create(
        name=f'{instance.username}'
    )
    return product


def create_price(instance: User):
    """
    Функция, создающая сущность стоимости продукта
    :param instance: Объект User
    :return: Объект stripe.Price
    """
    product = create_product(instance)
    price = stripe.Price.create(
        unit_amount=100,
        currency="usd",
        recurring={"interval": "month"},
        product=f"{product.id}",
    )
    return price


def create_session(instance: User):
    """
    Функция, создающая сессию оплаты товара
    :param instance: Объект User
    :return: Ссылка на страницу оплаты
    """
    price = create_price(instance)
    checkout_session = stripe.checkout.Session.create(
        line_items=[
            {
                'price': f'{price.id}',
                'quantity': 1,
            },
        ],
        mode='subscription',
        success_url=f"http://127.0.0.1:8000/user/subscribe/{instance.pk}",
        cancel_url=f"http://127.0.0.1:8000/user/profile/{instance.pk}",
    )

    return redirect(checkout_session.url, code=303)
