from django.db.models import QuerySet

from plumbing.models import Order, Basket, ProductInstance, Comments, Company, Product, Category


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

