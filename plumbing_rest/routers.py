from rest_framework.routers import DefaultRouter

from .views import CategoryView, SubcategoryView, CompanyView, ProductView, CommentView, ProductInstanceView, \
    BasketView, OrderView

router = DefaultRouter()

router.register(r'categories', CategoryView, basename='categories')
router.register(r'subcategories', SubcategoryView, basename='subcategories')
router.register(r'companies', CompanyView, basename='companies')
router.register(r'products', ProductView, basename='products')
router.register(r'product_instances', ProductInstanceView, basename='instances')
router.register(r'comments', CommentView, basename='comments')
router.register(r'baskets', BasketView, basename='baskets')
router.register(r'orders', OrderView, basename='orders')
