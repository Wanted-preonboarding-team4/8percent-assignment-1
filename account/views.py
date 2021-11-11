import json
from datetime             import date, datetime, timedelta

from django.http.response import JsonResponse
from django.shortcuts     import render
from django.views         import View
from django.db.models     import Q

from users.utils          import login_decorator
from account.models       import Account, Transaction
from account.filtering    import check_filter

class TransationView(View):
    @login_decorator
    def get(self, request, account_id):
        '''
            거래 일시, 거래금액, 잔액, 거래종류, 적요 
        '''
        user_id = request.user.id
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
        

        transaction_list = [{
            "transaction_date": transaction.created_at.strftime(r"%Y.%m.%d.%m.%s"),
            "amount": transaction.ammount,
            "balance": transaction.balance,
            "transaction_type": transaction.transaction_type.type,
            "description": transaction.description,
            "transaction_counterparty": transaction.account.account_number[:5] + (transaction.account.account_number[5:]) * '*' 
        }for transaction in transactions]

        return JsonResponse({"Result": transaction_list}, status=200)
        
