from datetime import date, datetime, timedelta

from django.http.response import JsonResponse

def check_filter(start, end, ordering, trans_type):
    if not start:
            start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    elif not end:
        end = datetime.now() 
    else:
        start = datetime.strptime(start, '%Y.%m.%d')
        end = datetime.strptime(end, '%Y.%m.%d') + timedelta(days=1, seconds=-1)
    
    if end > datetime.now():
        end = datetime.now()
    
    if ordering == 'asc':
        ordering = 'created_now'
    elif ordering == 'desc':
        ordering = '-created_now'
    else:
        return JsonResponse({"Message: Wrong Ordering Filter Format"},status=404)
    if not trans_type:
        return JsonResponse({"Message: Wrong Ordering Transaction Type Format"}, status=404)
    
    return start, end, ordering, trans_type