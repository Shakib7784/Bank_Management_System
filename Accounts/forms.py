from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, BankAccountType,UserBankAccount,UserAddress
from .constants import GENDER_CHOICE


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        fields=["street","city","postal_code","country"] 
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs) # we are using it to overide our changes in Model
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    "form-control"
                )
            })
        
        
        

class UserRegistrationForm(UserCreationForm):
    account_type = forms.ModelChoiceField(queryset=BankAccountType.objects.all())
    first_name = forms.CharField(max_length=250) # we have to define these value because usercreation don't have first-name,
    last_name = forms.CharField(max_length=250)
    gender = forms.ChoiceField(choices=GENDER_CHOICE)
    birth_date = forms.DateField(widget=forms.DateInput(attrs={"type":"date"}))
    class Meta:
        model = User
        fields = ["first_name","last_name","email","password1","password2"]
        
        
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        
        #adding bootstrap class from bootstrap form
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    "form-control"
                )
            })
        
    def save(self, commit=True):
        user = super().save(commit=False) #while accessing user data that time we are not saving. just storing.
        #The returned value of super().save(commit=False) is the User instance that has been created but not yet saved. By assigning it to the user variable, you can perform further modifications or validations before saving it to the database.
        user.set_password(self.cleaned_data["password1"])
        
        if commit:
            user.save() # when commit true that time we need to save the user
            account_type = self.cleaned_data["account_type"]
            gender = self.cleaned_data["gender"]
            birth_date = self.cleaned_data["birth_date"]
            
            
            UserBankAccount.objects.create(
               user = user,
               gender = gender ,
               birth_date = birth_date,
               account_type = account_type,
               account_no = (
                   user.id+10000000
               )
            )
        return user
        
        
        
    
    