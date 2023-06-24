from django.shortcuts import render,redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .forms import DepositeForm,WithdrawForm,LoanRequestForm
from .models import Transaction,LoanTransaction
from django.db import transaction
from django.contrib.auth.decorators import login_required
from .constants import TRANSACTION_TYPE_CHOICE
from django.views.generic import ListView

# Create your views here.


class DepositMoney(LoginRequiredMixin,View):
    def get(self,request):
        account = request.user.BankAccount
        form = DepositeForm(account=account)
        return render(request,"deposit.html",{"form":form})
    
    def post(self,request):
        account = request.user.BankAccount
        form = DepositeForm(request.POST, account=account)
        if form.is_valid():
            form.instance.transaction_type =TRANSACTION_TYPE_CHOICE[0][0]
            deposite_amount = form.cleaned_data["amount"]
            with transaction.atomic():
                account.balance += deposite_amount
                account.save()
                form.save()
            messages.success(request,f"Deposite of {deposite_amount} is successfull")
            return redirect("profile")
        return render(request,"deposit.html",{"form":form})
    
    
    
class WithdrawMoney(LoginRequiredMixin,View):
    def get(self,request):
        account = request.user.BankAccount
        form = WithdrawForm(account=account)
        return render(request,"withdraw.html",{"form":form})
    
    def post(self,request):
        account = request.user.BankAccount
        form = WithdrawForm(request.POST, account=account)
        if form.is_valid():
            form.instance.transaction_type =TRANSACTION_TYPE_CHOICE[1][0]
            withdraw_amount = form.cleaned_data["amount"]
            with transaction.atomic():
                account.balance -= withdraw_amount
                account.save()
                form.save()
            messages.success(request,f"Withdraw of {withdraw_amount} is successfull")
            return redirect("profile")
        return render(request,"withdraw.html",{"form":form})



class LoanRequest(LoginRequiredMixin,View):
    def get(self,request):
        account = request.user.BankAccount
        form = LoanRequestForm(account=account)
        return render(request,"loan_request.html",{"form":form})
    
    def post(self,request):
        account = request.user.BankAccount
        
        form = LoanRequestForm(request.POST, account=account)
        if form.is_valid():
            # form.instance.transaction_type =TRANSACTION_TYPE_CHOICE[2][0]
            loan_amount = form.cleaned_data["amount"]
            current_loan_count = LoanTransaction.objects.filter(account = request.user.BankAccount, transaction_type = TRANSACTION_TYPE_CHOICE[2][0], loan_approved=True).count()
            if current_loan_count>=3:
                return HttpResponse("You have crossed the loan limits")
            with transaction.atomic():
                loan_transaction = LoanTransaction.objects.create(
                    account=account,
                    amount=loan_amount,
                    blance_after_transaction=account.balance,
                    transaction_type=TRANSACTION_TYPE_CHOICE[2][0],
                    loan_approved=False
                )
                loan_transaction.save()
            messages.success(request,f"Loan request of {loan_amount} is send successfully")
            return redirect("profile")
        return render(request,"loan_request.html",{"form":form})
    
    
    
    



# def approve_loan(request, transaction_id):
#     try:
#         transaction = Transaction.objects.get(id=transaction_id)
#         amount = transaction.amount
#         # Retrieve the associated user's bank account
#         account = transaction.account
#         if account:
#             # Update the user's balance
#             account.balance += amount
#             transaction.blance_after_transaction = account.balance
#             account.save()
#             transaction.loan_approved = True
#             transaction.save()
#             messages.success(request, 'Loan request approved successfully.')
#         else:
#             messages.error(request, 'Associated bank account not found.')
            
#     except Transaction.DoesNotExist:
#         messages.error(request, 'Loan request not found.')
#     previous_url = request.META.get('HTTP_REFERER')
#     return redirect(previous_url)  # Redirect back to the previous page 



class ApproveLoanView(LoginRequiredMixin, View):
    def get(self, request, transaction_id):
        try:
            transaction = LoanTransaction.objects.get(id=transaction_id)
            amount = transaction.amount
            account = transaction.account
            if account:
                account.balance += amount
                transaction.blance_after_transaction = account.balance
                account.save()
                transaction.loan_approved = True
                transaction.save()
                messages.success(request, 'Loan request approved successfully.')
            else:
                messages.error(request, 'Associated bank account not found.')
        except Transaction.DoesNotExist:
            messages.error(request, 'Loan request not found.')
        previous_url = request.META.get('HTTP_REFERER')
        return redirect(previous_url)  # Redirect back to the previous page
    
    
    
    
    
class LoanList(LoginRequiredMixin,ListView):
        model = LoanTransaction
        template_name = "loanlist.html"
        context_object_name ="loans"
        
        def get_queryset(self):
            user_accouont = self.request.user.BankAccount
            queryset = LoanTransaction.objects.filter(account=user_accouont,transaction_type = TRANSACTION_TYPE_CHOICE[2][0])
            print(queryset)
            return queryset
        
        

class LoanPay(LoginRequiredMixin,View):
    def get(self,request,loan_id):#loan_id comming from urls
        try:
            transaction = LoanTransaction.objects.get(id=loan_id)
            account = transaction.account
            if account:
                amount_to_pay = transaction.amount
                if account.balance >= amount_to_pay:
                    account.balance -=amount_to_pay
                    transaction.transaction_type = TRANSACTION_TYPE_CHOICE[3][0]
                    account.save()
                    transaction.save()
                    messages.success(request, 'Loan Payment Successful', extra_tags='loan-pay-success')
                else:
                    messages.error(request,"Insufficient Balance to pay loan", extra_tags='loan-pay-error')
            else:
                messages.error(request, "Bank account not found",extra_tags='loan-pay-error')
        except:
            messages.error(request,"Loan transaction not found",extra_tags='loan-pay-error')
        
        previous_url = request.META.get("HTTP_REFERER")
        return redirect(previous_url)


