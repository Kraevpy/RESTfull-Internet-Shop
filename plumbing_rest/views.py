from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet

from plumbing import services
from .serializers import CategoriesSerializer, CompanySerializer, ProductSerializer, CommentsSerializer, \
    ProductInstanceSerializer, BasketsSerializer, OrdersSerializer


class CategoryView(ReadOnlyModelViewSet):
    serializer_class = CategoriesSerializer

    def get_queryset(self):
        order_by = self.request.query_params.get('order_by', 'name')
        queryset = services.get_all_categories(order_by)
        return queryset


class SubcategoryView(ReadOnlyModelViewSet):
    serializer_class = CategoriesSerializer

    def get_queryset(self):
        order_by = self.request.query_params.get('order_by', 'name')
        queryset = services.get_all_subcategories(order_by)
        return queryset


class CompanyView(ReadOnlyModelViewSet):
    serializer_class = CompanySerializer

    def get_queryset(self):
        order_by = self.request.query_params.get('order_by', 'name')
        queryset = services.get_all_companies(order_by)
        return queryset


class ProductView(ReadOnlyModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        order_by = self.request.query_params.get('order_by', 'name')
        queryset = services.get_all_products(order_by)
        return queryset


class ProductInstanceView(ReadOnlyModelViewSet):
    serializer_class = ProductInstanceSerializer

    def get_queryset(self):
        order_by = self.request.query_params.get('order_by', 'product')
        queryset = services.get_all_instances(order_by)
        return queryset


class CommentView(ReadOnlyModelViewSet):
    serializer_class = CommentsSerializer

    def get_queryset(self):
        order_by = self.request.query_params.get('order_by', 'send_data_time')
        queryset = services.get_all_comments(order_by)
        return queryset


class BasketView(ReadOnlyModelViewSet):
    serializer_class = BasketsSerializer

    def get_queryset(self):
        order_by = self.request.query_params.get('order_by', 'user')
        queryset = services.get_all_baskets(order_by)
        return queryset


class OrderView(ModelViewSet):
    serializer_class = OrdersSerializer

    def get_queryset(self):
        order_by = self.request.query_params.get('order_by', 'customer')
        queryset = services.get_all_orders(order_by)
        return queryset
