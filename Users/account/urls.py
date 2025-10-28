from django.urls import path

from .views import (
    CreateAccountPostView,
    CreateAccountConfirmCodePostView,
    ConfirmPasswordAccountPostView,
    PasswordResetRequestPostView,
    PasswordResetConfirmCodePostView,
    PasswordResetNewPasswordPostView
)

app_name = 'account'

urlpatterns = [
    path('create/', CreateAccountPostView.as_view(), name='create-account'),
    path('create/confirm-code/', CreateAccountConfirmCodePostView.as_view(), name='create-account-confirm-code'),
    path('create/confirm-password/', ConfirmPasswordAccountPostView.as_view(), name='create-account-confirm-password'),
    path('password-reset/request/', PasswordResetRequestPostView.as_view(), name='password-reset-request'),
    path('password-reset/confirm-code/', PasswordResetConfirmCodePostView.as_view(), name='password-reset-confirm-code'),
    path('password-reset/new-password/', PasswordResetNewPasswordPostView.as_view(), name='password-reset-new-password'),
]
