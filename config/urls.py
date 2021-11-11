from django.urls import path, include

urlpatterns = [
    path('user', include('users.urls')),
    path('account', include('account.urls')),
]
