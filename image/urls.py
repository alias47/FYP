from django.urls import path
from . import views

urlpatterns = [
    path('property/', views.buyPage, name='buy'),
    path('detail/<str:pk>/', views.detailPage, name='detail'),
    path('add/', views.addPage, name='add'),
]