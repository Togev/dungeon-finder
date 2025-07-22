from django.urls import path
from common import views

urlpatterns = [
    path('', views.home, name='landing_page'),
]