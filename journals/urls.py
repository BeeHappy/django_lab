from django.urls import path
from . import views


urlpatterns = [
    path('', views.Index.as_view(), name='index'),
    path('journal/<int:journal_id>/', views.Info.as_view(), name='journal'),
    path('cart/', views.Cart.as_view(), name='cart'),
]
