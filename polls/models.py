import datetime

from django.db import models
from django.utils import timezone
from django import forms

# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=50)
    pDate = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pDate <= now

    was_published_recently.admin_order_field = 'pDate'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=30)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class User(models.Model):
    username = models.CharField(max_length=16, unique=True)
    password = models.CharField(max_length=16)
    join_date = models.DateTimeField()

    def __str__(self):
        return self.username
    
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + " --------> " + self.question.question_text

class Session(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lastUsed = models.DateTimeField()