from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('add/<int:journal_id>/', views.add_to_cart, name='add'),
]
