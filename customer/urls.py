
from django.urls import path, include

from django.contrib.auth import views as auth_views

from . import views


urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('', views.home, name='home'),
    path('user/', views.userPage, name='user'),

    path('account/', views.accountSetting, name='account'),

    path('products/', views.products, name='products'),
    path('customers/<str:pk>/', views.customers, name='customers'),
    path('delete_customer/<str:pk>/', views.delete_customer, name='delete_customer'),

    
    path('create_order/<str:pk>/', views.create_order, name='create_order'),
    path('update_order/<str:pk>/', views.update_order, name='update_order'),
    path('delete_order/<str:pk>/', views.delete_order, name='delete_order'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="customer/password_reset.html"), name="reset_password"),

    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="customer/password_reset_sent.html"), name="password_reset_done"),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="customer/password_reset_form.html"), name="password_reset_confirm"),

    path('reset_password_complete/', auth_views. PasswordResetCompleteView.as_view(template_name="customer/password_reset_done.html"), name="password_reset_complete"),

]




