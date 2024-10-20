from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import user_list, user_create, user_update, user_delete, appointment_detail

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('users/', views.user_list, name='user_list'),
    path('service/', views.services, name='services'),
    path('service/create/', views.service_create, name='service_create'),
    path('service/update/<int:service_id>/', views.service_update, name='service_update'),
    path('service/delete/<int:service_id>/', views.service_delete, name='service_delete'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/update/<int:user_id>/', views.user_update, name='user_update'),
    path('users/delete/<int:user_id>/', views.user_delete, name='user_delete'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'), 
    path('appointment/make/', views.make_appointment, name='make_appointment'),
    path('appointment/', appointment_detail, name='appointment_detail'),
    path('appointment/update/<int:appointmentid>', views.update_appointment, name='update_appointment'),
    path('', views.home_view, name='home'),  # Adjust the home view name as needed
    path('report/<int:appointment_id>/', views.appointment_detail_report, name='appointment_detail_report'),
    path('appointments/delete/<int:appointment_id>/', views.delete_appointment, name='delete_appointment'),
    



]