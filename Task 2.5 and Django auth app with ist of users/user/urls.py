from django.urls import path
from .views import UserRegistrationView, UserLoginView, UserManagementView, UserBlockView, UserDeleteView, UserUnblockView


urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('users/', UserManagementView.as_view(), name='user-management'),
    path('users/block/<int:pk>/', UserBlockView.as_view(), name='user-block'),
    path('users/unblock/<int:pk>/', UserUnblockView.as_view(), name='user-unblock'),
    path('users/delete/<int:pk>/', UserDeleteView.as_view(), name='user-delete'),
]