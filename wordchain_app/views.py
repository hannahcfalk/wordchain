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