import json, bcrypt, random, re
from datetime              import date, datetime, timedelta

from django.core           import paginator
from django.http           import JsonResponse
from django.shortcuts      import render
from django.views          import View
from django.db             import transaction
from django.db.models      import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from users.utils           import login_decorator
from account.filtering     import check_filter
from users.models          import User
from account.models        import Account, Transaction, TransactionType


class TransationView(View):
    @login_decorator
    def get(self, request, account_id):
        user_id = request.user.id
        page = request.GET.get('page', 1)
        start_date  = request.GET.get('startPeriod', '')
        end_date  = request.GET.get('endPeriod', '')
        search_by_ordering = request.GET.get('order-by', '')
        search_by_tansaction_type = request.GET.get('transaction_type', '')
        

        start_date, end_date, search_by_ordering, search_by_tansaction_type = check_filter(
            start_date, 
            end_date, 
            search_by_ordering, 
            search_by_tansaction_type
        )
        
        if not Account.objects.filter(id = account_id).exists():
            return JsonResponse({"Message": "Account Does Not Exist"}, status=404)
        
        account = Account.objects.filter(id = account_id)

        if account.user_id != user_id:
            return JsonResponse({"Message": "Not Authorized"}, status=403)

        transactions = Transaction.select_related('user', 'account', 'transactiontype').filter(
            account_id = account_id,
            created_at__range=(start_date, end_date),
            transaction_type_id = search_by_tansaction_type
        ).order_by(search_by_ordering)

        paginator = Paginator.page(transactions, 5)
        
        try:
            transaction_list = paginator.page(page)
        except PageNotAnInteger:
            transaction_list = paginator.page(1)
        except EmptyPage:
            transaction_list = paginator.page(paginator.num_pages)
        
        result = [{
            "transaction_date": transaction.created_at.strftime(r"%Y.%m.%d.%m.%s"),
            "amount": transaction.ammount,
            "balance": transaction.balance,
            "transaction_type": transaction.transaction_type.type,
            "description": transaction.description,
            "transaction_counterparty": transaction.account.account_number[:5] + (transaction.account.account_number[5:]) * '*' 
        }for transaction in transaction_list]

        return JsonResponse({"Result": result}, status=200)
        

class AccountView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = request.user
            password = data['password']
            balance = data.get('balance', 0)
            account_number = random.randint(0, 999999999)

            while True:
                if Account.objects.filter(account_number=account_number).exists():
                    account_number = random.randint(0, 999999999)
                else:
                    break

            if not re.match(r'^[0-9]{4}$', password):
                return JsonResponse({"MESSAGE": "숫자 4자리를 입력해주세요."}, status=400)

            hash_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            Account.objects.create(
                user=user,
                name=user.name,
                password=hash_password,
                account_number=account_number,
                balance=balance,
            )

            return JsonResponse({"MESSAGE": "SUCCESS"}, status=201)
        except KeyError:
            return JsonResponse({"MESSAGE": "KEY_ERROR"}, status=400)
        


class DepositView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            account = Account.objects.get(id=data['account_id'])

            if not account:
                return JsonResponse({'message': '일치하는 계좌가 없습니다.'}, status=404)

            if not bcrypt.checkpw(data['password'].encode('utf-8'), account.password.encode('utf-8')):
                return JsonResponse({'message': '비밀번호가 틀렸습니다.'}, status=404)

            Account.objects.filter(id=data['account_id']).update(balance=account.balance + int(data['amount']))
            return JsonResponse({'message': '입금 성공'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)


class WithdrawView(View):
    @login_decorator
    def post(self, request):
        try:
            data = json.loads(request.body)
            account = Account.objects.get(id=data['account_id'])

            if not account:
                return JsonResponse({'message': '일치하는 계좌가 없습니다.'}, status=404)

            if not bcrypt.checkpw(data['password'].encode('utf-8'), account.password.encode('utf-8')):
                return JsonResponse({'message': '비밀번호가 틀렸습니다.'}, status=404)

            if account.balance < int(data['amount']):
                return JsonResponse({'message': '금액이 부족합니다.'}, status=404)

            Account.objects.filter(id=data['account_id']).update(balance=account.balance - int(data['amount']))
            return JsonResponse({'message': '입금 성공'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)
