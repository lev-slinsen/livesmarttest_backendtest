from django.urls import path

from .views import TestApiView

urlpatterns = [
    path('test/<str:code>', TestApiView.as_view(), name='test_results'),
]
