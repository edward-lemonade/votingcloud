from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'), #/polls/
    path('<int:pk>/', views.DetailView.as_view(), name = 'detail'), #/polls/4/
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'), #/polls/4/results/
    path('<int:question_id>/vote/', views.vote, name='vote'), #/polls/4/vote/
    path('ask', views.AskView.as_view(), name='ask'), #/polls/ask
    path('signup', views.SignUpView.as_view(), name='signup'), #/polls/signup
    path('login', views.LoginView.as_view(), name='login'), #/polls/login
    path('logout', views.LogoutView, name='logout'),
]