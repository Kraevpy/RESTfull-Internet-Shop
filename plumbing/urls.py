from django.urls import path, include

from plumbing import views

urlpatterns = [
    path('', views.ProductsListView.as_view(), name='index'),
    path('basket/<int:user_id>', views.BasketView.as_view(), name='basket'),
    path('<int:category_id>/', views.ProductsListView.as_view(), name='categories'),
    path('<int:category_id>/<int:subcategory_id>', views.ProductsListView.as_view(), name='subcategories'),
    path('product/<str:serial_number>/', views.ProductDetail.as_view(), name='show_product'),
    path('product/<str:serial_number>/add_to_card', views.AddToCard.as_view(), name='add_to_card'),
    path('product/<str:serial_number>/remove_from_card', views.RemoveFromCard.as_view(), name='remove_from_card'),
    path('product/<str:serial_number>/to_order', views.CreateOrder.as_view(), name='order'),
    path('user/<int:user_id>/orders', views.OrdersList.as_view(), name='orders'),

    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.RegistrationView.as_view(), name='register'),
]
