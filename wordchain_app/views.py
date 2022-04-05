from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect

from .forms import UserForm

@login_required
def play(request):
    return render(request, "wordchain_app/play.html")

def about(request):
    return render(request, "wordchain_app/about.html")

def sign_up(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('wordchain:play')

    else:
        form = UserForm()
    return render(request, "registration/sign_up.html", {'form': form})


def password_reset(request):
    return render(request, "wordchain_app/password_reset.html")


@login_required
def update_account_details(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('wordchain:home')
    else:
        form = UserForm(instance=request.user)
    return render(request, "wordchain_app/update_account_details.html", {'form': form})

