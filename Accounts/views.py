from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model,login,logout
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView,RedirectView
from .forms import UserRegistrationForm, UserAddressForm, ProfileForm
from django.contrib.auth.views import LoginView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Create your views here.

User = get_user_model()
# def Registration(request):
#     form = UserRegistrationForm(request.POST)
#     form_2 = UserAddressForm(request.POST)
#     res = {
#         "form":form,
#         "form2":form_2
#     }
#     return render(request,"registration.html",res)

class UserRegistrationView(TemplateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "registration.html"
    
    #if user try to access registraion after being authenticated then he will redirect profile
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("profile")
        
        return super().dispatch(request, *args, **kwargs)

    
    
   
    def post(self,request, *args, **kwargs):
        registration_form = UserRegistrationForm(self.request.POST,request.FILES)
        address_form = UserAddressForm(self.request.POST)
        
        # if not registration_form.is_valid():
        #     print("error from register form : ",registration_form.errors)
 

        # if not address_form.is_valid():
        #     print("error from addrress form : ", address_form.errors)
            
        # print(registration_form.cleaned_data)
        # print(address_form.cleaned_data)


        if registration_form.is_valid() and address_form.is_valid():
            user = registration_form.save()
          
            address = address_form.save(commit=False)
            address.user =user
            address.save()
            messages.success(self.request,"Registration is successfull",extra_tags="regsuccess")
            return HttpResponseRedirect(
                reverse_lazy("login")
            )
            
        # if there is any form validation errors, the user is presented with the registration form again, including the error messages, so they can correct their input.
        
        # print("there is error")  
        return self.render_to_response(
            self.get_context_data(
                registration_form = registration_form,
                address_form = address_form,
                
                
            )
        )

    
    # def get_context_data(self, **kwargs):
    #     kwargs["registration_form"] = UserRegistrationForm()
    #     kwargs["address_form"] = UserAddressForm()
    #     return super().get_context_data(**kwargs)
    
    def get_context_data(self, **kwargs):
        if 'registration_form' not in kwargs:
            kwargs['registration_form'] = UserRegistrationForm()
        if 'address_form' not in kwargs:
            kwargs['address_form'] = UserAddressForm()

        return super().get_context_data(**kwargs)


            




# def user_login(request):
#     return render(request,"login.html")


class UserLogin(LoginView):
    template_name="login.html"
    redirect_authenticated_user=False
    
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("profile")
        
        return super().dispatch(request, *args, **kwargs)
    
    
    def get_success_url(self):
        # Customize the redirect URL here
        return reverse_lazy('profile')
    


class UserLogout(RedirectView):
    pattern_name="home"
    
    def get_redirect_url(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            logout(self.request)
        return super().get_redirect_url(*args,**kwargs) 
 
 
   
def Profile(request):
    if request.user.is_authenticated:
        return render(request,"profile.html")
    else:
        return redirect("login")
    
    
    


class EditProfileView(LoginRequiredMixin,View):
    def get(self, request):
        user = request.user
        form = ProfileForm(instance=user)
        return render(request, 'edit_profile.html', {'form': form})

    def post(self, request):
        user = request.user
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(self.request,"Profile Edit is successfull",extra_tags="editsuccess")
            return redirect('profile')
        return render(request, 'edit_profile.html', {'form': form})
    
    
class ChangePassword(LoginRequiredMixin,View):
    def get(self, request):
        form = PasswordChangeForm(user=request.user)
        context={"form":form}
        return render(request,"changepass.html",context)
    def post(selg,request):
        form = PasswordChangeForm(user=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request,"your password has been changed",extra_tags="passchange")
            return redirect("profile")
        else :
            context={"form":form}
            return render(request,"changepass.html",context)
    

