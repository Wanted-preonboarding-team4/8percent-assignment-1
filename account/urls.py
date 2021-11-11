from django.urls import path
from account.views import AccountView, DepositView

urlpatterns = [
    path('', AccountView.as_view()),
    path('/deposit', DepositView.as_view())
]