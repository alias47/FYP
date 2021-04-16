from django.urls import path
from account import views

urlpatterns = [
    path('',views.indexPage, name="home"),
    path('register/', views.registerPage, name="register"),
	path('login/', views.loginPage, name="login"),  
	path('logout/', views.logoutUser, name="logout"),
    path('profile/', views.profilePage, name="profile"),
    path('profile/edit/', views.editProfilePage, name="editProfile"),
    path('profile/change-password/', views.changePasswordPage, name="change_password"),
    ] 