from .models import Transaction, LoanTransaction
import datetime
from django.conf import settings
from django import forms 


class TransactionForm(forms.ModelForm):
    class Meta:
        model = LoanTransaction
        fields =["amount","transaction_type"]
        widgets = {
            "transaction_type": forms.HiddenInput(),
        }
        
    def __init__(self, *args, **kwargs):
        #The purpose of extracting the account argument is to associate the transaction being created with a specific account
        self.account = kwargs.pop("account")
        super().__init__(*args,**kwargs)
        self.fields["transaction_type"].disabled = True #we are disabling transaction type from user
        # self.fields["transaction_type"].initial = self.instance.transaction_type
        # self.fields["transaction_type"].widget = forms.HiddenInput()
        self.fields["transaction_type"].required = False
           
    def save(self,commit=True):
        self.instance.account = self.account #here instance.account is coming from Transaction mode. self.account is commig from UserBankAccount model.
        self.instance.blance_after_transaction = self.account.balance # Here,blance_after_transaction cp,omg frp, Transaction model, and account.balance coming from UserBankAccount model 
        return super().save(commit=commit)
    
    

class DepositeForm(TransactionForm):
    
    def clean_amount(self):
        min_deposit_amount = 100
        max_deposit_amount = 1000000000
        amount = self.cleaned_data.get("amount")
        
        balance = self.account.balance
        digits = len(str(balance))
        
        Total_balance_after_deposit = balance+amount
        total_digit = len(str(Total_balance_after_deposit))
        
        if total_digit>15 : # because balance can be at max 15 digits
            raise forms.ValidationError(f"You total balance after deposit will be cross a user's total balance capacity")
        
        else: 
            if amount<min_deposit_amount:
                raise forms.ValidationError(f"You need to deposit at least {min_deposit_amount} $, Thank You")
            elif amount>max_deposit_amount:
                raise forms.ValidationError(f"You can deposit max {min_deposit_amount} $, Thank You")
        return amount
    
    


#The purpose of the clean_amount method is to check if the deposit amount entered by the user meets certain criteria, such as being above a minimum required amount. If the entered amount is not valid, an error is raised using the forms.ValidationError class.

class WithdrawForm(TransactionForm):
    
    def clean_amount(self):
        min_withdraw_amount = 100
        max_withdraw_amount = 10000
        balance = self.account.balance #comming from UserBankAccount model
        amount = self.cleaned_data.get("amount") #coming from transactionfrom
         
        if amount<min_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at least {min_withdraw_amount} $'
            )
            
        if amount>max_withdraw_amount:
            raise forms.ValidationError(
                f'You can withdraw at most {max_withdraw_amount} $'
            )
            
        if amount>balance:
            raise forms.ValidationError(
                f'You have {balance} $ in your account. '
                'You can not withdraw more than your account balance'
            )
            
        return amount
    
    

class LoanRequestForm(TransactionForm):
    def clean_amount(self):
        min_loan_amount = 100
        max_loan_amount = 1000000
        amount = self.cleaned_data.get("amount")
        if amount<min_loan_amount:
            raise forms.ValidationError(
                f'You can request for loan at least {min_loan_amount} $'
            )
        if amount>max_loan_amount:
            raise forms.ValidationError(
                f'You can request for loan at max {max_loan_amount} $'
            )
        return amount
            

        
    
        