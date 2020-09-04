import datetime
from django.shortcuts import get_object_or_404, render, redirect

from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.template import loader
from django.utils import timezone

from .models import Choice, Question, User, Vote
from .forms import SignUpForm, LoginForm, AskForm

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        pDate__lte = timezone.now()
        return Question.objects.filter().order_by('-pDate')[:100]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        return Question.objects.filter(pDate__lte = timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

    def get_context_data(self, **kwargs):
        context = super(ResultsView, self).get_context_data(**kwargs)
        context['data'] = list(context['question'].choice_set.all().values_list("votes", flat=True))
        context['labels'] = list(context['question'].choice_set.all().values_list("choice_text", flat=True))
        return context

class AskView(generic.FormView):
    template_name = 'polls/ask.html'
    form_class = AskForm
    success_url = '.'

    def get_form(self, form_class=None):
        askform = super(AskView, self).get_form(form_class)
        askform.setID(self.request.session['user_ID'])
        return askform
    #def form_valid(self, form):
     #   form.save_poll()
      #  return super().form_valid(form)

class SignUpView(generic.FormView):    
    template_name = 'polls/signup.html'
    form_class = SignUpForm
    success_url = 'login'

    
    #def form_valid(self, form):
     #   form.save_user()
      #  return super().form_valid(form)

class LoginView(generic.FormView):
    template_name = 'polls/login.html'
    form_class = LoginForm
    success_url = '.'

    def form_valid(self, form):
        u = User.objects.filter(
            username = form.cleaned_data['username'],
            password = form.cleaned_data['password'],
        )

        user = u[0]
        self.request.session['user_ID'] = user.id
        self.request.session['username'] = user.username
        self.request.session.set_expiry(1800)
        return super().form_valid(form)
       
def LogoutView(request):
    request.session.flush()
    return HttpResponseRedirect('login')

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        try:
            old_vote = Vote.objects.filter(
                question = question,
                user = User.objects.get(pk=request.session['user_ID']),
            )[0]
            if old_vote.choice.id != selected_choice.id:
                selected_choice.votes += 1
                selected_choice.save()

                old_vote.choice.votes -= 1
                old_vote.choice.save()
                old_vote.choice = selected_choice

            old_vote.save()
        except:      
            vote = Vote(
                question = question, 
                user = User.objects.get(pk=request.session['user_ID']),
                choice = selected_choice
            )
            selected_choice.votes += 1
            selected_choice.save()
            vote.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

def get_name_and_password(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/')
    else:
        form = SignUpForm()

    return render(request, 'signup.html', {'form': form})