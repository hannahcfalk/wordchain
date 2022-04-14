from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect

from .forms import UserForm
from .models import *
from django.contrib.auth.models import User
from django.db.models import Max, Avg
import json

@login_required
def play(request):
    chain = Chain.objects.order_by('?').first()
    if chain:
        chain_dict = chain.__dict__
    else:
        # Makes sure there isn't an error when the db is empty
        chain_dict = {'first_word': 'TRAIN', 'second_word': 'TRACK', 'third_word': 'TEAM', 'fourth_word': 'BUILDING', 'fifth_word': 'BLOCK', 'sixth_word': 'HEAD'}

    if not SetView.objects.filter(user=request.user).exists():
        display_name = Display.objects.get(display_id=1)
        display = SetView.objects.create(user=request.user, display=display_name)
        font = display_name.accessibility
        mode = display_name.visual_mode
    else:
        display = SetView.objects.get(user=request.user)
        display_name = display.display
        font = display_name.accessibility
        mode = display_name.visual_mode

    if (mode == "Dark" and font == "Normal"):
        file=open("wordchain_app/static/wordchain_app/mode.css", "wt")
        file.write("""#body { background-color: #121213; }
            #game { color: #ffffff; } label { color: #ffffff; }""")
        file.close()
    elif (mode == "Light" and font == "Normal"):
        file=open("wordchain_app/static/wordchain_app/mode.css", "wt")
        file.write("""#body { background-color: #ffffff; }
            #game { color: #000000; } label { color: #000000; }""")
        file.close()
    elif (mode == "Dark" and font == "Bigger"):
        file=open("wordchain_app/static/wordchain_app/mode.css", "wt")
        file.write("""#body { background-color: #121213; }
            #game { color: #ffffff; font-size: 40px; } label { color: #ffffff; } .navbar { font-size: 30px; } .button4 { font-size: 25px; height: 65px; }""")
        file.close()
    else:
        file=open("wordchain_app/static/wordchain_app/mode.css", "wt")
        file.write("""#body { background-color: #ffffff; }
            #game { color: #000000; font-size: 40px; } label { color: #000000; } .navbar { font-size: 30px; } .button4 { font-size: 25px; height: 65px; }""")
        file.close()

    return render(request, "wordchain_app/play.html", chain_dict)

@login_required
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
def account(request):
    user = request.user.username
    first_name = request.user.first_name
    last_name = request.user.last_name

    if not SetView.objects.filter(user=request.user).exists():
        display_name = Display.objects.get(display_id=1)
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

    if (mode == "Dark" and font == "Normal"):
        file=open("wordchain_app/static/wordchain_app/mode.css", "wt")
        file.write("""#body { background-color: #121213; }
            #game { color: #ffffff; } label { color: #ffffff; }""")
        file.close()
    elif (mode == "Light" and font == "Normal"):
        file=open("wordchain_app/static/wordchain_app/mode.css", "wt")
        file.write("""#body { background-color: #ffffff; }
            #game { color: #000000; } label { color: #000000; }""")
        file.close()
    elif (mode == "Dark" and font == "Bigger"):
        file=open("wordchain_app/static/wordchain_app/mode.css", "wt")
        file.write("""#body { background-color: #121213; }
            #game { color: #ffffff; font-size: 40px; } label { color: #ffffff; } .navbar { font-size: 30px; } .button4 { font-size: 25px; height: 65px; }""")
        file.close()
    else:
        file=open("wordchain_app/static/wordchain_app/mode.css", "wt")
        file.write("""#body { background-color: #ffffff; }
            #game { color: #000000; font-size: 40px; } label { color: #000000; } .navbar { font-size: 30px; } .button4 { font-size: 25px; height: 65px; }""")
        file.close()
    
    context = {
        "user": user,
        "first_name": first_name,
        "last_name": last_name,
        "font": font,
        "mode": mode
    }

    return render(request, "wordchain_app/account.html", context)

@login_required
def stats(request):
    user = request.user
    highest_score = get_highest_score(user, 0)
    average_score = get_average_score(user, 0)
    all_scores = get_all_scores(user, 0)
    download = create_download(highest_score, average_score, all_scores)
    all_scores = json.dumps(all_scores)
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
    all_scores = list(all_results.values_list('chain__first_word', 'chain__sixth_word', 'score__value'))
    return 0 if all_scores is None else all_scores

def create_download(high_score, average_score, all_scores):
    download = {}
    download['high score'] = high_score
    download['average score'] = average_score
    download['all scores'] = []
    for score in all_scores:
        s = {}
        s['first word'] = score[0]
        s['sixth word'] = score[1]
        s['score'] = score[2]
        download['all scores'].append(s)
    download = json.dumps(download)
    return download

