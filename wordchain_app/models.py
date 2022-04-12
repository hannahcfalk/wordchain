from django.db import models
from django.contrib.auth.models import User


class Chain(models.Model):
    chain_id = models.AutoField(primary_key=True)
    first_word = models.CharField(max_length=13)
    second_word = models.CharField(max_length=13)
    third_word = models.CharField(max_length=13)
    fourth_word = models.CharField(max_length=13)
    fifth_word = models.CharField(max_length=13)
    sixth_word = models.CharField(max_length=13)


class Score(models.Model):
    score_id = models.AutoField(primary_key=True)
    value = models.IntegerField()


class Results(models.Model):
    score = models.ForeignKey('Score', on_delete=models.CASCADE)
    chain = models.ForeignKey('Chain', on_delete=models.CASCADE)


class Level(models.Model):
    difficulty = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=20)


class Selects(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    level = models.ForeignKey('Level', on_delete=models.CASCADE)


class Display(models.Model):
    display_id = models.AutoField(primary_key=True)
    visual_mode = models.CharField(max_length=20)
    accessibility = models.CharField(max_length=20)

class SetView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    display = models.ForeignKey('Display', on_delete=models.CASCADE)


class ReceiveScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.ForeignKey('Score', on_delete=models.CASCADE)


class IsAssignedTo(models.Model):
    chain = models.ForeignKey('Chain', on_delete=models.CASCADE)
    level = models.ForeignKey('Level', on_delete=models.CASCADE)


class PlayGame(models.Model):
    chain = models.ForeignKey('Chain', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
