from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect

from .forms import UserForm
from .models import *
from django.contrib.auth.models import User
from django.db.models import Max, Avg

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
    highest_score = get_highest_score(user, 0)
    average_score = get_average_score(user, 0)
    all_scores = get_all_scores(user, 0)
    download = 0
    context = {
        "user": user,
        "highest_score": highest_score,
        "average_score": average_score,
        "all_scores": all_scores,
        "download": download
        }
    return render(request, "wordchain_app/stats.html", context)

def get_highest_score(user, level):
    user_id = user.id
    try:
        user_scores = ReceiveScore.objects.filter(user_id=user_id)
    except ReceiveScore.DoesNotExist:
        return 0
    highest_score = user_scores.order_by('-score__value').first().score.value
    return 0 if highest_score is None else highest_score

def get_average_score(user, level):
    user_id = user.id
    try:
        user_scores = ReceiveScore.objects.filter(user_id=user_id)
    except ReceiveScore.DoesNotExist:
        return 0
    average_score = list(user_scores.values_list('score__value', flat=True))
    average_score = round(sum(average_score)/len(average_score), 2)
    return 0 if average_score is None else average_score

def get_all_scores(user, level):
    user_id = user.id
    try:
        user_scores = ReceiveScore.objects.filter(user_id=user_id)
    except ReceiveScore.DoesNotExist:
        return 0
    user_score_ids = list(user_scores.values_list('score__score_id', flat=True))
    all_results = Results.objects.filter(score__score_id__in=user_score_ids)
    all_scores = list(all_results.values_list('score__value', 'chain__first_word', 'chain__sixth_word'))
    return 0 if all_scores is None else all_scores
