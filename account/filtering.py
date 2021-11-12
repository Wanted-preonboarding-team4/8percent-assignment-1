from datetime             import datetime

from django.db.models     import Q
from django.http          import JsonResponse


def check_date_range(start, end):
    if start == '': 
        start = str(datetime.now()).split()[0]
        
    if end == '':
        end = str(datetime.now())
    
    return start,end


def check_sorting(sorting):
    if sorting == 'latest':
        sorting = '-created_at'
    else:
        sorting = 'created_at'

    return sorting


def check_transaction_type(search_by_tansaction_type):
    if search_by_tansaction_type not in ['1', '2', 'all']:
        result = 0
    else:
        result = search_by_tansaction_type
    
    return result 


def arrange_filter(start_date, end_date, transaction_type):
    q= Q()

    q &= Q(created_at__range=(start_date, end_date))
    
    if transaction_type == 'all':
        q &= (Q(transaction_type_id = 1) | Q(transaction_type_id = 2))
    else:
        q &= Q(transaction_type_id = transaction_type)
    
    return q