from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    
    path("deposit",views.DepositMoney.as_view(),name="deposit"),
    path("withdraw",views.WithdrawMoney.as_view(),name="withdraw"),
    path("loanrequest",views.LoanRequest.as_view(),name="loanrequest"),
    path('approve_loan/<int:transaction_id>/', views.ApproveLoanView.as_view(), name='approve_loan'),
    path("loanlist",views.LoanList.as_view(),name="loanlist"),
    path("payloan/<int:loan_id>/",views.LoanPay.as_view(),name="payloan"),
    
]