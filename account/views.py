import json, re, bcrypt, jwt

from django.http import JsonResponse
from django.views import View
from account.models import Account, Transaction
from users.utils import login_decorator


class DepositView(View):
    # @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            account = Account.objects.get(account_number=data['account_number'])

            if not account:
                return JsonResponse({'message': '일치하는 계좌가 없습니다.'}, status=404)

            if account.user.email != data['user']['email']:
                return JsonResponse({'message': '본인 계좌가 아닙니다.'}, status=404)

            if not bcrypt.checkpw(data['password'].encode('utf-8'), account.password.encode('utf-8')):
                return JsonResponse({'message': '비밀번호가 틀렸습니다.'}, status=404)

            # if account.user.password != data['user']['password']:
            #     return JsonResponse({'message': '비밀번호가 틀렸습니다.'}, status=404)
            Account.objects.filter(account_number=data['account']).update(balance=account.balance + int(data['account_number']))
            return JsonResponse({'message': '입금 성공'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)