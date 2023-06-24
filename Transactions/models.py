from django.db import models

# Create your models here.
from Accounts.models import UserBankAccount
from .constants import TRANSACTION_TYPE_CHOICE

class Transaction(models.Model):
    account = models.ForeignKey(UserBankAccount,on_delete=models.CASCADE,null=True,blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=12, null=True)
    blance_after_transaction = models.DecimalField(decimal_places=2, max_digits=12, null=True)
    transaction_type = models.CharField(choices=TRANSACTION_TYPE_CHOICE, null=True,max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
    # loan_approved = models.BooleanField(default=False)
    
    class Meta:
        ordering=["timestamp"]



class LoanTransaction(Transaction):
    loan_approved = models.BooleanField(default=False)