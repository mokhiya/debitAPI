from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('login/', views.login_user, name='login'),
    path('loans/add/', views.add_loan, name='add_loan'),
    path('loans/my/', views.my_loans, name='my_loans'),
    path('loans/owed/', views.loans_owed, name='loans_owed'),
    path('loans/close/<int:pk>/', views.close_loan, name='close_loan'),
    path('admin/users/', views.admin_get_users, name='admin_users'),
    path('admin/search/', views.admin_search_users, name='search_users'),
]
