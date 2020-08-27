from django import forms, db
from .models import User, Choice, Question
from datetime import datetime


class SignUpForm(forms.Form):
    username = forms.CharField(label = 'Your username', max_length=16)
    password = forms.CharField(widget=forms.PasswordInput, max_length=16)
    
    def clean(self):
        super(SignUpForm, self).clean()
        newUser = User(
            username = self.cleaned_data['username'],
            password = self.cleaned_data['password'],
            
            join_date = datetime.now()
            
        )
        try:
            newUser.save()
        except db.IntegrityError:
            self._errors['username'] = self.error_class([
                'Your username has been taken already'
            ])
        return self.cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(label = 'Your username', max_length=16)
    password = forms.CharField(widget=forms.PasswordInput, max_length=16)
    
    def clean(self):
        super(LoginForm, self).clean()
        u = User.objects.filter(username = self.cleaned_data['username'], password = self.cleaned_data['password'])

        if not u:
            self._errors['username'] = self.error_class([
                'Your username and password did not match'
            ])

        return self.cleaned_data

class AskForm(forms.Form):
    text = forms.CharField(label = 'Question text', max_length=200, min_length=1)
    choice1 = forms.CharField(label = 'Choice text 1', max_length=200, min_length=1, required=True)
    choice2 = forms.CharField(label = 'Choice text 2', max_length=200, min_length=1, required=True)
    choice3 = forms.CharField(label = 'Choice text 3', max_length=200, required=False)
    choice4 = forms.CharField(label = 'Choice text 4', max_length=200, required=False)
    choice5 = forms.CharField(label = 'Choice text 5', max_length=200, required=False)

    def clean(self):
        super(AskForm, self).clean()

        if len(self._errors) > 0:
            return self.cleaned_data()
            
        newQuestion = Question(
            question_text = self.cleaned_data['text'], 
            pDate = datetime.now()
        )
        newQuestion.save()

        newChoice1 = Choice(
            question = newQuestion, 
            choice_text = self.cleaned_data['choice1'],
            votes = 0
        )
        newChoice1.save()
        newChoice2 = Choice(
            question = newQuestion, 
            choice_text = self.cleaned_data['choice2'],
            votes = 0
        )
        newChoice2.save()

        if self.cleaned_data['choice3'] != '':
            newChoice3 = Choice(
                question = newQuestion, 
                choice_text = self.cleaned_data['choice3'],
                votes = 0
            )
            newChoice3.save()

        if self.cleaned_data['choice4'] != '':
            newChoice4 = Choice(
                question = newQuestion, 
                choice_text = self.cleaned_data['choice4'],
                votes = 0
            )
            newChoice4.save()
        
        if self.cleaned_data['choice5'] != '':
            newChoice5 = Choice(
                question = newQuestion, 
                choice_text = self.cleaned_data['choice5'],
                votes = 0
            )
            newChoice5.save()

        return self.cleaned_data