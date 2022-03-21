from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def home(request):
    return render(request, "wordchain_app/home.html")

def sign_up(request):
    return render(request, "wordchain_app/sign_up.html")

def password_reset(request):
    return render(request, "wordchain_app/password_reset.html")

def update_account_details(request):
    return render(request, "wordchain_app/update_account_details.html")

def play(request):
    return render(request, "wordchain_app/play.html")