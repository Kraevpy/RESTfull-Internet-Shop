from django.urls import path, include

from .routers import router

urlpatterns = [
    path('accounts/', include('rest_registration.api.urls')),
]

urlpatterns.extend(router.urls)
