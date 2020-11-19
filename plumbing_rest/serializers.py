from rest_framework.serializers import ModelSerializer
from plumbing.models import Category, Product, Company, Comments, ProductInstance, Basket, Order


class CategoriesSerializer(ModelSerializer):
    """This serializer is used for categories and subcategories"""

    class Meta:
        model = Category
        fields = ('id', 'name', 'parent',)


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = ('type', 'name', 'address')


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name', 'category', 'serial_number', 'photo', 'maker',
            'importer', 'country', 'barcode', 'certificate', 'cost',
            'delivery_date', 'description'
        )


class ProductInstanceSerializer(ModelSerializer):
    class Meta:
        model = ProductInstance
        fields = ('product', 'status')


class CommentsSerializer(ModelSerializer):
    class Meta:
        model = Comments
        fields = ('sender', 'text', 'send_data_time', 'product')


class BasketsSerializer(ModelSerializer):
    class Meta:
        model = Basket
        fields = ('user', 'products')


class OrdersSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ('cost', 'customer', 'data_time', 'address', 'phone_number', 'status', 'product_name')
