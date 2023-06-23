from django.db import models

from django.contrib import auth
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager
import datetime
from .constants import GENDER_CHOICE
# Create your models here.

class UserManager(BaseUserManager):
    use_in_migrations = True
    
    def _create_user(self,email,password, **extra_fields):
        if not email: 
            raise ValueError("The given email must to be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using = self._db)
        return user
    
    def create_user(self,email,password, **extra_fields):
        extra_fields.setdefault("is_staff",False)
        extra_fields.setdefault("is_superuser",False)
        return self._create_user(email,password, **extra_fields)
    def create_superuser(self,email,password, **extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        
        if extra_fields.get("is_staff") is not True : 
            raise ValueError("Superuser must have is_staff = True")
        if extra_fields.get("is_superuser") is not True : 
            raise ValueError("Superuser must have is_superuser = True")
        return self._create_user(email,password, **extra_fields)
    
    
    

class User(AbstractBaseUser):
    username = None
    email = models.EmailField(unique=True,null=False,blank=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS=[]
    
    def has_module_perms(self, app_label):
        return self.is_staff

    def has_perm(self, perm, obj=None):
        return self.is_staff

    def get_group_permissions(self, obj=None):
        return set()

    def get_all_permissions(self, obj=None):
        return set()
    
    def __str__(self):
        return self.email
    
    
class BankAccountType(models.Model):
    name = models.CharField(max_length=160)
    maximum_withdrawal_amount = models.DecimalField(decimal_places=2,max_digits=11)
    def __str__(self):
        return self.name
    
    
class UserBankAccount(models.Model):
    user = models.OneToOneField(User, related_name="BankAccount", on_delete=models.CASCADE) #one user will have one account
    account_type = models.ForeignKey(BankAccountType,related_name="accounts",on_delete=models.CASCADE) # one user can have multiple types of account
    account_no = models.PositiveIntegerField(unique=True)
    gender= models.CharField(max_length=10,choices=GENDER_CHOICE)
    birth_date = models.DateField(null=True, blank=True)
    balance = models.DecimalField(default=0,max_digits=11,decimal_places=2)
    initial_deposite_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return str(self.account_no)
    
    
class UserAddress (models.Model):
     user = models.OneToOneField(User, related_name="address", on_delete=models.CASCADE)
     street = models.CharField(max_length=500)
     city = models.CharField(max_length=250)
     postal_code = models.PositiveIntegerField()
     country = models.CharField(max_length=200)
     
     def __str__(self):
         return self.user.email