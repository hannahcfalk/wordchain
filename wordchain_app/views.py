from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):
    return render(request, "home.html")

def sign_up(request):
    return render(request, "sign_up.html")

def password_reset(request):
    return render(request, "password_reset.html")

def update_account_details(request):
    return render(request, "update_account_details.html")

# def home(request):
#     return render(request, "home.html")

def play(request):
    return render(request, "play.html")