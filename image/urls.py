from django.urls import path
from . import views

urlpatterns = [
    path('property/<str:slug>', views.category, name='category'),
    path('property/', views.buyPage, name='buy'),
    path('detail/<str:pk>/', views.detailPage, name='detail'),
    path('sell/', views.addPage, name='add'),
]