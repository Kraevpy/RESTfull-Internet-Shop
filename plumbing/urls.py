from django.urls import path, include

from plumbing import views

urlpatterns = [
    path('', views.index, name='index'),
    path('basket/<int:user_id>', views.basket, name='basket'),
    path('<int:category_id>/', views.categories, name='categories'),
    path('<int:category_id>/<int:subcategory_id>', views.categories, name='subcategories'),
    path('product/<str:serial_number>/', views.product, name='show_product'),
    path('product/<str:serial_number>/add_to_card', views.add_to_card, name='add_to_card'),
    path('product/<str:serial_number>/remove_from_card', views.remove_from_card, name='remove_from_card'),
    path('product/<str:serial_number>/to_order', views.order, name='order'),
    path('user/<int:user_id>/orders', views.orders, name='orders'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name='register'),
]
