from django.urls import path
from account.views import AccountView

urlpatterns = [
    path('', AccountView.as_view())
]