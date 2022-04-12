from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect

from .forms import UserForm
from .models import *
from django.contrib.auth.models import User
from django.db.models import Max

@login_required
def play(request):
    chain = Chain.objects.order_by('?').first()
    if chain:
        chain_dict = chain.__dict__
    else:
        # Makes sure there isn't an error when the db is empty
        chain_dict = {'first_word': 'TRAIN', 'second_word': 'TRACK', 'third_word': 'TEAM', 'fourth_word': 'BUILDING', 'fifth_word': 'BLOCK', 'sixth_word': 'HEAD'}
    return render(request, "wordchain_app/play.html", chain_dict)

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

@login_required
def settings(request):
    return render(request, "wordchain_app/settings.html")

@login_required
def account(request):
    return render(request, "wordchain_app/account.html")

@login_required
def stats(request):
    user = request.user
    highest_score = get_highest_score(user)
    context = {
        "user": user,
        "highest_score": highest_score
        }
    return render(request, "wordchain_app/stats.html", context)

def get_highest_score(user):
    user_scores = ReceiveScore.objects.all()
    highest_score = 10
    return 0 if highest_score is None else highest_score

def get_average_score(user, level):
    pass

def get_all_scores(user):
    pass