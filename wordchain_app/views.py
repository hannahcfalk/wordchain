from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.db.models import Q

from .forms import UserForm
from .models import *
import json


@login_required
def play(request):
    if request.method == 'POST':
        request_data = request.body.decode("utf-8")
        data = json.loads(request_data)
        score = Score.objects.create(value=data['score'])
        ReceiveScore.objects.create(user=request.user, score=score)
        chain = Chain.objects.get(chain_id=data['chain'])
        Results.objects.create(chain=chain, score=score)
        PlayGame.objects.create(chain=chain, user=request.user)

    chain = Chain.objects.order_by('?').first()
    if (Chain.objects.count() <= PlayGame.objects.filter(user_id=request.user.id).count()) or (chain is None):
        return render(request, "wordchain_app/play-no-chains.html")
    while PlayGame.objects.filter(chain=chain, user_id=request.user.id).exists():
        chain = Chain.objects.order_by('?').first()

    isassignto = IsAssignedTo.objects.get(chain=chain)
    Selects.objects.update_or_create(user=request.user, defaults={"level":isassignto.level})
    level = isassignto.level.difficulty
    context = {
        "level": level,
        "style": set_style(request.user),
    }
    context.update(chain.__dict__)
    return render(request, "wordchain_app/play.html", context)


@login_required
def about(request):
    return render(request, "wordchain_app/about.html", {"style": set_style(request.user)})


def sign_up(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('wordchain:play')
    else:
        form = UserForm()
    return render(request, "registration/sign_up.html", {'form': form})


@login_required
def update_account_details(request):
    if request.method == 'POST':
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('wordchain:play')
    else:
        form = UserForm(instance=request.user)
    return render(request, "wordchain_app/update_account_details.html", {'form': form, "style": set_style(request.user)})


@login_required
def account(request):
    user = request.user.username
    first_name = request.user.first_name
    last_name = request.user.last_name

    if not SetView.objects.filter(user=request.user).exists():
        display_name, created = Display.objects.get_or_create(display_id=1, accessibility="Normal", visual_mode="Dark")
        display = SetView.objects.create(user=request.user, display=display_name)
        font = display_name.accessibility
        mode = display_name.visual_mode
    else:
        display = SetView.objects.get(user=request.user)
        display_name = display.display
        font = display_name.accessibility
        mode = display_name.visual_mode

    if request.method == 'POST':
        if request.POST.get('font') == "Normal" or request.POST.get('font') == "Bigger":
            font = request.POST.get('font')

        if request.POST.get('mode') == "Light" or request.POST.get('mode') == "Dark":
            mode = request.POST.get('mode')

        display_view = SetView.objects.get(user=request.user)
        display_view.display = Display.objects.get(accessibility=font, visual_mode=mode)
        display_view.save()

    context = {
        "user": user,
        "first_name": first_name,
        "last_name": last_name,
        "font": font,
        "mode": mode,
        "style": set_style(request.user),
    }

    return render(request, "wordchain_app/account.html", context)


@login_required
def stats(request):
    user = request.user
    highest_score_level1 = get_highest_score(user, 1)
    highest_score_level2 = get_highest_score(user, 2)
    highest_score_level3 = get_highest_score(user, 3)

    average_score_level1 = get_average_score(user, 1)
    average_score_level2 = get_average_score(user, 2)
    average_score_level3 = get_average_score(user, 3)

    all_scores = get_all_scores(user)
    download = create_download(highest_score_level1, highest_score_level2, highest_score_level3, average_score_level1, average_score_level2, average_score_level3, all_scores)
    all_scores = json.dumps(all_scores)
    context = {
        "user": user,
        "highest_score_level1": highest_score_level1,
        "highest_score_level2": highest_score_level2,
        "highest_score_level3": highest_score_level3,
        "average_score_level1": average_score_level1,
        "average_score_level2": average_score_level2,
        "average_score_level3": average_score_level3,
        "all_scores": all_scores,
        "download": download,
        "style": set_style(request.user)
    }
    return render(request, "wordchain_app/stats.html", context)


def get_highest_score(user, level):
    try:
        user_id = user.id
        user_scores = ReceiveScore.objects.filter(user_id=user_id)
        user_score_ids = list(user_scores.values_list('score__score_id', flat=True))
        all_results = Results.objects.filter(score__score_id__in=user_score_ids)

        all_results_chains = list(all_results.values_list('chain__chain_id', flat=True))
        all_chains = IsAssignedTo.objects.filter(Q(chain__chain_id__in=all_results_chains) & Q(level__difficulty__exact=level))

        all_chain_ids = list(all_chains.values_list('chain__chain_id', flat=True))
        all_chain_ids_scores = Results.objects.filter(chain__chain_id__in=all_chain_ids)

        highest_score = all_chain_ids_scores.order_by('-score__value').first().score.value
    except:
        return 0
    return 0 if highest_score is None else highest_score


def get_average_score(user, level):
    try:
        user_id = user.id
        user_scores = ReceiveScore.objects.filter(user_id=user_id)
        user_score_ids = list(user_scores.values_list('score__score_id', flat=True))
        all_results = Results.objects.filter(score__score_id__in=user_score_ids)

        all_results_chains = list(all_results.values_list('chain__chain_id', flat=True))
        all_chains = IsAssignedTo.objects.filter(Q(chain__chain_id__in=all_results_chains) & Q(level__difficulty__exact=level))

        all_chain_ids = list(all_chains.values_list('chain__chain_id', flat=True))
        all_chain_ids_scores = Results.objects.filter(chain__chain_id__in=all_chain_ids)

        average_score = list(all_chain_ids_scores.values_list('score__value', flat=True))
        average_score = round(sum(average_score)/len(average_score), 2)
    except:
        return 0
    return 0 if average_score is None else average_score


def get_all_scores(user):
    user_id = user.id
    user_scores = ReceiveScore.objects.filter(user_id=user_id)
    if not user_scores:
        return []
    user_score_ids = list(user_scores.values_list('score__score_id', flat=True))
    all_results = Results.objects.filter(score__score_id__in=user_score_ids)
    all_scores = list(all_results.values_list('chain__first_word', 'chain__sixth_word', 'score__value'))
    return [] if all_scores is None else all_scores


def create_download(highest_score_level1, highest_score_level2, highest_score_level3, average_score_level1, average_score_level2, average_score_level3, all_scores):
    download = {}
    download['Highest Easy Chain Score'] = highest_score_level1
    download['Highest Medium Chain Score'] = highest_score_level2
    download['Highest Hard Chain Score'] = highest_score_level3
    download['Average Easy Chain Score'] = average_score_level1
    download['Average Medium Chain Score'] = average_score_level2
    download['Average Hard Chain Score'] = average_score_level3
    download['All Scores'] = []
    for score in all_scores:
        s = {}
        s['First Word'] = score[0]
        s['Sixth Word'] = score[1]
        s['Score'] = score[2]
        download['All Scores'].append(s)
    download = json.dumps(download)
    return download


def set_style(user):
    if not SetView.objects.filter(user=user).exists():
        display_name, created = Display.objects.get_or_create(display_id=1, accessibility="Normal", visual_mode="Dark")
        display = SetView.objects.create(user=user, display=display_name)
        font = display_name.accessibility
        mode = display_name.visual_mode
    else:
        display = SetView.objects.get(user=user)
        display_name = display.display
        font = display_name.accessibility
        mode = display_name.visual_mode

    if (mode == "Dark" and font == "Normal"):
        style = "#body { background-color: #121213; }#game { color: #ffffff; } label { color: #ffffff; }"
    elif (mode == "Light" and font == "Normal"):
        style = "#body { background-color: #ffffff; }#game { color: #000000; } label { color: #000000; }"
    elif (mode == "Dark" and font == "Bigger"):
        style = "#body { background-color: #121213; }#game { color: #ffffff; font-size: 40px; } label { color: #ffffff; } .navbar { font-size: 30px; } .button4 { font-size: 25px; height: 65px; }"
    else:
        style = "#body { background-color: #ffffff; }#game { color: #000000; font-size: 40px; } label { color: #000000; } .navbar { font-size: 30px; } .button4 { font-size: 25px; height: 65px; }"

    return style