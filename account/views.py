import json,bcrypt,random,re

from django.http  import JsonResponse
from django.views import View
from django.db    import transaction

from users.models   import User
from account.models import Account,Transaction,TransactionType
from users.utils    import login_decorator

class AccountView(View):
    @login_decorator
    def post(self,request):
        try:
            data           = json.loads(request.body)
            user           = request.user
            password       = data['password']
            balance        = data.get('balance',0)
            account_number = random.randint(0, 999999999)

            while True:
                if Account.objects.filter(account_number=account_number).exists():
                    account_number = random.randint(0, 999999999)
                else:
                    break

            if not re.match(r'^[0-9]{4}$',password):
                return JsonResponse({"MESSAGE" : "숫자 4자리를 입력해주세요."}, status=400)

            hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            Account.objects.create(
                user           = user,
                name           = user.name,
                password       = hash_password,
                account_number = account_number,
                balance        = balance,
                )

            return JsonResponse({"MESSAGE" : "SUCCESS"}, status=201)
        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)
        