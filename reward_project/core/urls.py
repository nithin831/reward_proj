from django.urls import path
from . import views

urlpatterns = [
    path('admi/login/', views.admin_login, name='admin_login'),
    path('admi/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admi/add_app/', views.admin_add_app, name='admin_add_app'),
    path('admi/update_app/<int:app_id>/', views.admin_update_app, name='admin_update_app'),
    path('admi/delete_app/<int:app_id>/', views.admin_delete_app, name='admin_delete_app'),
    path('admi/logout/', views.admin_logout, name='admin_logout'),

    path('', views.signup, name='signup'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('submit_task/<int:app_id>/', views.submit_task, name='submit_task'),
    path('profile/', views.user_profile, name='user_profile'),
]
