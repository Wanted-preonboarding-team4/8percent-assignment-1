from django.urls import path
from account.views import DepositView

urlpatterns = [
    path('/deposit', DepositView.as_view())
]