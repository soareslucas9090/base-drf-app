from django.urls import path, include

app_name = 'auth'

urlpatterns = [
    path('token_jwt/', include('Auth.auth.urls')),
]
