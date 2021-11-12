import json, bcrypt, random, re

from django.http           import JsonResponse
from django.views          import View
from django.db             import transaction
from django.core.paginator import Paginator

from users.utils           import login_decorator
from account.models        import Account, Transaction
from account.filtering     import (
    check_date_range, 
    check_sorting, 
    check_transaction_type, 
    arrange_filter
)


class TransationView(View):
    @login_decorator
    def get(self, request, account_id):
        user_id = request.user.id
        page = request.GET.get('page', 1)
        start_date                = request.GET.get('startPeriod', '')
        end_date                  = request.GET.get('endPeriod', '')
        search_by_ordering        = request.GET.get('order-by','')
        search_by_tansaction_type = request.GET.get('transaction_type', 'all')
 
        start_date, end_date      = check_date_range(start_date, end_date)
        sorting                   = check_sorting(search_by_ordering)
        transaction_type          = check_transaction_type(search_by_tansaction_type)
        if transaction_type == 0:
            return JsonResponse({"Message": "Invalid Transaction Format"}, status=404)
        
        q_filter                  = arrange_filter(start_date, end_date, transaction_type)
        
        if not Account.objects.filter(id = account_id).exists():
            return JsonResponse({"Message": "Account Does Not Exist"}, status=404)
        
        account = Account.objects.get(id = account_id)

        if account.user_id != user_id:
            return JsonResponse({"Message": "Not Authorized"}, status=403)

        transactions = Transaction.objects.select_related(
            'user', 
            'account', 
            'transaction_type'
        ).filter(q_filter).order_by(sorting)
        
        transaction_list = Paginator(transactions, 5).get_page(page)
        
        result = [{
            "transaction_date": transaction.created_at.strftime(r"%Y.%m.%d %H:%M:%S"),
            "amount": transaction.amount,
            "balance": transaction.balance,
            "transaction_type": transaction.transaction_type.type,
            "description": transaction.description,
            "transaction_counterparty": transaction.account.account_number[:5] + len(transaction.account.account_number[5:]) * '*' 
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

            if account.user_id != data['user_id']:
                return JsonResponse({'message': '본인의 계좌가 아닙니다.'}, status=404)

            if not bcrypt.checkpw(data['password'].encode('utf-8'), account.password.encode('utf-8')):
                return JsonResponse({'message': '비밀번호가 틀렸습니다.'}, status=404)

            Account.objects.filter(id=data['account_id']).update(balance=account.balance + int(data['amount']))
            Transaction.objects.create(
                amount=data['amount'],
                balance=account.balance + int(data['amount']),
                account_id=data['account_id'],
                user_id=data['user_id'],
                transaction_type_id=1
            )
            
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

            if account.user_id != data['user_id']:
                return JsonResponse({'message': '본인의 계좌가 아닙니다.'}, status=404)

            if not bcrypt.checkpw(data['password'].encode('utf-8'), account.password.encode('utf-8')):
                return JsonResponse({'message': '비밀번호가 틀렸습니다.'}, status=404)

            if account.balance < int(data['amount']):
                return JsonResponse({'message': '금액이 부족합니다.'}, status=404)

            Account.objects.filter(id=data['account_id']).update(balance=account.balance - int(data['amount']))
            Transaction.objects.create(
                amount=data['amount'],
                balance=account.balance - int(data['amount']),
                account_id=data['account_id'],
                user_id=data['user_id'],
                transaction_type_id=2
            )

            return JsonResponse({'message': '출금 성공'}, status=200)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'},status=400)
