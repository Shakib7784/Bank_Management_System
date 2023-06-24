from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import Transaction,LoanTransaction

# Register your models here.

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display=["account","amount","blance_after_transaction","transaction_type"]



@admin.register(LoanTransaction)
class LoanTransactionAdmin(admin.ModelAdmin):
    # Other admin configurations
    
    def loan_approval_link(self, obj):
        if obj.loan_approved:
            return 'Approved'
        else:
            url = reverse('approve_loan', args=[obj.id])
            return format_html('<a href="{}">Approve</a>', url)
    
    loan_approval_link.short_description = 'Loan Approval'
    loan_approval_link.allow_tags = True

    def get_list_display(self, request):
        transaction_type = request.GET.get('transaction_type')
        if transaction_type == 'LOAN':
            return ['id', 'account', 'amount', 'blance_after_transaction', 'transaction_type', 'loan_approval_link']
        else:
            return []

    def changelist_view(self, request, extra_context=None):
        # Set default transaction_type if not provided in the request
        if 'transaction_type' not in request.GET:
            request.GET = request.GET.copy()
            request.GET['transaction_type'] ='LOAN'
        return super().changelist_view(request, extra_context=extra_context)