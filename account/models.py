from django.db import models


class Account(models.Model):
    user           = models.ForeignKey("users.User", on_delete=models.CASCADE)
    name           = models.CharField(max_length=50)
    account_number = models.CharField(max_length=50)
    password       = models.IntegerField()
    balance        = models.PositiveIntegerField(default=0)
    
    class Meta:
        db_table = "accounts"

class TransactionType(models.Model):
    type = models.CharField(max_length=20)

    class Meta:
        db_table = "transaction_types"

class Transaction(models.Model):
    user                     = models.ForeignKey("users.User", on_delete=models.CASCADE)
    amount                   = models.IntegerField()
    transaction_counterparty = models.CharField(max_length=100, null=True)
    created_at               = models.DateTimeField(auto_now_add=True)
    description              = models.CharField(max_length=100, null=True)
    account                  = models.ForeignKey("Account", on_delete=models.CASCADE)
    transaction_type         = models.ForeignKey("TransactionType", on_delete=models.CASCADE)

    class Meta:
        db_table = "transactions"
