from django.urls import path
from .import views

urlpatterns = [
   
    path('property/<str:slug>', views.category, name='category'),
    path('property/', views.buyPage, name='buy'),
    path('detail/edit/<str:pk>', views.edit, name='edit'),
    path('detail/<str:pk>/', views.detailPage, name='detail'),
    path('detail/delete/<str:pk>/', views.deletePage, name='delete'),
    path('sell/', views.addPage, name='add'),
    path('property/rate/<int:pk>/', views.rating, name='property.rating'),
    path('recommendation/',views.recommendation,name='recommendation'),
 
    
]