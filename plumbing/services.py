from typing import Optional

from django.core.exceptions import ObjectDoesNotExist
from plumbing.models import Category, Product, Comments, Basket, ProductInstance, Order, Company
from django.contrib.auth.models import User
from django.db.models import QuerySet
from django.core.mail import send_mail
from plumbingShop import settings


def get_all_categories(field: str = 'name') -> QuerySet[Category]:
    if field not in Category.__dict__:
        field = 'name'
    return Category.objects.filter(parent=None).order_by(field)


def get_all_subcategories(field: str = 'name') -> QuerySet[Category]:
    if field not in Category.__dict__:
        field = 'name'
    return Category.objects.filter(parent_id__isnull=False).order_by(field)


def get_all_products(field: str = 'name') -> QuerySet[Product]:
    if field not in Product.__dict__:
        field = 'name'
    return Product.objects.all().order_by(field)


def get_all_companies(field: str = 'name') -> QuerySet[Company]:
    if field not in Company.__dict__:
        field = 'name'
    return Company.objects.all().order_by(field)


def get_all_comments(field: str = 'send_data_time') -> QuerySet[Comments]:
    if field not in Comments.__dict__:
        field = 'send_data_time'
    return Comments.objects.all().order_by(field)


def get_all_instances(field: str = 'product') -> QuerySet[ProductInstance]:
    if field not in ProductInstance.__dict__:
        field = 'product'
    return ProductInstance.objects.all().order_by(field)


def get_all_baskets(field: str = 'user') -> QuerySet[Basket]:
    if field not in Basket.__dict__:
        field = 'user'
    return Basket.objects.all().order_by(field)


def get_all_orders(field: str = 'customer') -> QuerySet[Order]:
    if field not in Basket.__dict__:
        field = 'customer'
    return Order.objects.all().order_by(field)


def add_to_card(user: User, serial_number: str) -> None:
    basket = Basket.objects.get(user_id=user.id)
    product = Product.objects.get(serial_number=serial_number)
    basket.products.add(product)
    basket.save()


def get_subcategories(category_id: int) -> QuerySet[Category]:
    return Category.objects.filter(parent_id=category_id).all()


def get_product(serial_number: str) -> Optional[Product]:
    """Returns a product object by serial number. Returns None if no such object exists"""
    try:
        return Product.objects.get(serial_number=serial_number)
    except ObjectDoesNotExist:
        return None


def get_comments(product: Product) -> QuerySet[Comments]:
    """Returns all product comments"""
    return Comments.objects.filter(product=product)


def get_product_with_category(category_id: int) -> QuerySet[Product]:
    """Returns all products belonging to the subcategory"""
    return Product.objects.filter(category__parent_id=category_id)


def get_product_with_subcategory(subcategory_id: int) -> QuerySet[Product]:
    """Returns all products belonging to a category"""
    return Product.objects.filter(category_id=subcategory_id)


def get_user_products(user_id: int) -> QuerySet[Product]:
    """Returns all items in the user's cart"""
    return Product.objects.filter(basket__user_id=user_id)


def create_basket(username: str) -> None:
    """Creating a shopping cart for a user"""
    user = User.objects.get(username=username)
    basket = Basket(user_id=user.id)
    basket.save()


def remove_from_card(user: User, serial_number: str) -> None:
    basket = Basket.objects.get(user_id=user.id)
    product = Product.objects.get(serial_number=serial_number)
    basket.products.remove(product)
    basket.save()


def change_instance_status(serial_number: str) -> Optional[bool]:
    """Changes the status of the instance to booked"""
    try:
        instance = ProductInstance.objects.filter(product__serial_number=serial_number, status='s').first()
        instance.status = 'b'
        instance.save()
        return True
    except (ObjectDoesNotExist, AttributeError):
        return None


def get_orders(user_id: int) -> QuerySet[Order]:
    """Get all user orders"""
    return Order.objects.filter(customer_id=user_id)


def send_email_successful_registration(email: str):
    html_message = '<em> На нашем сайте Вы можете ознакомится и купить сантехнику наиболее известных производителей.' \
                   'Продажа в комплексе с услугами по установке и производству подготовительных работ. ' \
                   'Обязательное гарантийное и послегарантийное обслуживание.' \
                   ' Консультации опытных специалистов-установщиков.' \
                   'Помощь в подборе оптимального решения </em>' \
                   f'<em><html><head><body><a href="{settings.ALLOWED_HOSTS[0]}":{settings.PORT}>' \
                   'Вы успешно зарегестрировались на сайте PlumbingShop'
    send_mail(
        'Добро пожаловать в мир "PlumbingShop"',
        '',
        settings.EMAIL_HOST_USER,
        [email],
        html_message=html_message
    )


def send_email_create_order(email, product_name, cost):
    html_message = f"""
    <em>
        Вы успешно заказали {product_name} стоимость: {cost} BYN.
        Благодарим за то что выбрали наш магазин.
    </em>
     """
    send_mail(
        '"PlumbingShop" заказ успешно оформлен',
        '',
        settings.EMAIL_HOST_USER,
        [email],
        html_message=html_message
    )

