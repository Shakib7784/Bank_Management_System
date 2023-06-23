from django.contrib import admin
from .models import User,BankAccountType, UserAddress,UserBankAccount

# Register your models here.

admin.site.register(User)
admin.site.register(BankAccountType)
admin.site.register(UserAddress)
admin.site.register(UserBankAccount)

