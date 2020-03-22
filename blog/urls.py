from django.urls import path
from .views import my_blog

urlpatterns = [
    path('', my_blog, name='my_blog')
]