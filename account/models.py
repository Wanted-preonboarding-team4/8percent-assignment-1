from django.db import models


class Account(models.Model):
    name           = models.CharField(max_length=50)
    account_number = models.CharField(max_length=50, unique=True)
    password       = models.CharField(max_length=200)
    balance        = models.PositiveIntegerField(default=0)
    user           = models.ForeignKey("users.User", on_delete=models.CASCADE)
    
    class Meta:
        db_table = "accounts"

class TransactionType(models.Model):
    type = models.CharField(max_length=20)

    class Meta:
        db_table = "transaction_types"

class Transaction(models.Model):
    amount                   = models.IntegerField()
    transaction_counterparty = models.CharField(max_length=100, null=True)
    created_at               = models.DateTimeField(auto_now_add=True)
    description              = models.CharField(max_length=100, null=True)
    balance                  = models.PositiveIntegerField(default=0)
    user                     = models.ForeignKey("users.User", on_delete=models.CASCADE)
    account                  = models.ForeignKey("Account", on_delete=models.CASCADE)
    transaction_type         = models.ForeignKey("TransactionType", on_delete=models.CASCADE)

    class Meta:
        db_table = "transactions"
