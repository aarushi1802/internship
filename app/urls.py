from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from .views import profile_view

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/profile/', login_required(profile_view), name='profile'),
    path("login/", auth_views.LoginView.as_view(), name="login"), 
    path("profile/", views.profile_view, name="profile"), 
    path("logout/", views.user_logout, name="logout"), 
    path("dashboard/", views.dashboard, name="dashboard"),
    path('search/', views.search_orders, name='search_orders'),  
    path('edit/<str:order_id>/', views.edit_order, name="edit_order"),  
    path("create/", views.create_order, name="create_order"), 
    path('delete/<str:order_id>/', views.confirm_delete, name="delete_order"),  
]
