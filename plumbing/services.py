from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from plumbing.models import Category, Product, Comments, Basket, ProductInstance, Order


def get_all_categories():
    return Category.objects.filter(parent=None).all()


def get_categories(category_id):
    return Category.objects.filter(parent_id=category_id).all()


def get_all_products():
    return Product.objects.all()


def get_product(serial_number):
    try:
        return Product.objects.get(serial_number=serial_number)
    except ObjectDoesNotExist:
        return None


def get_comments(product):
    return Comments.objects.filter(product=product)


def get_product_with_category(category_id):
    return Product.objects.filter(category__parent_id=category_id)


def get_product_with_subcategory(subcategory_id):
    return Product.objects.filter(category_id=subcategory_id)


def get_user_products(user_id):
    return Product.objects.filter(basket__user_id=user_id)


def create_basket(username):
    user = User.objects.get(username=username)
    basket = Basket(user_id=user.id)
    basket.save()


def add_to_card(user, serial_number):
    basket = Basket.objects.get(user_id=user.id)
    product = Product.objects.get(serial_number=serial_number)
    basket.products.add(product)
    basket.save()


def remove_from_card(user, serial_number):
    basket = Basket.objects.get(user_id=user.id)
    product = Product.objects.get(serial_number=serial_number)
    basket.products.remove(product)
    basket.save()


def change_instance_status(serial_number):
    try:
        instance = ProductInstance.objects.filter(product__serial_number=serial_number, status='s').first()
        instance.status = 'b'
        instance.save()
        return True
    except ObjectDoesNotExist:
        return None


def get_orders(user_id):
    return Order.objects.filter(customer_id=user_id)
