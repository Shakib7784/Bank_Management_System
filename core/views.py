from django.shortcuts import render,redirect

# Create your views here.


def home(request):
    if not request.user.is_authenticated:
        return render(request,"home.html")
    else:
        return redirect("profile")
