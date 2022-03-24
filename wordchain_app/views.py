from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect

from .forms import SignUpForm

@login_required
def home(request):
    return render(request, "wordchain_app/home.html")


def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('wordchain:home')

    else:
        form = SignUpForm()
    return render(request, "registration/sign_up.html", {'form': form})

def password_reset(request):
    return render(request, "wordchain_app/password_reset.html")

def update_account_details(request):
    return render(request, "wordchain_app/update_account_details.html")

def play(request):
    return render(request, "wordchain_app/play.html")