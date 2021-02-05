"""basketball_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from website_basketball.views import UserAddView, LoginView, LogoutView, HomePageView, StatisticsCreateView,\
    StatisticsShowView, TeamShowView, TeamCreateView, PlayerEditView, TournamentsListView, TournamentCreateView,\
    TeamWinsAddView, TournamentTableView, TeamPlayerDeleteView, TeamPlayerAddView, MatchCreateView,\
    HistoryMatchesView, StadiumCreate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomePageView.as_view(), name="home_page"),
    path('add-user/', UserAddView.as_view(), name="add_user"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('statistics/', StatisticsShowView.as_view(), name="statistics"),
    path('statistics-create/', StatisticsCreateView.as_view(), name="statistics_create"),
    path('team/', TeamShowView.as_view(), name="team_show"),
    path('team-create/', TeamCreateView.as_view(), name="team_create"),
    path('edit-account/', PlayerEditView.as_view(), name="user_edit"),
    path('tournament/', TournamentsListView.as_view(), name="tournament"),
    path('tournament-create/', TournamentCreateView.as_view(), name="tournament_create"),
    path('team-wins-add/', TeamWinsAddView.as_view(), name="team_winds_add"),
    path('table/', TournamentTableView.as_view(), name='table'),
    path('player-delete/', TeamPlayerDeleteView.as_view(), name='player_delete_team'),
    path('player-add/', TeamPlayerAddView.as_view(), name='player_add_team'),
    path('stadium-match-create/', MatchCreateView.as_view(), name='stadium_history_create'),
    path('stadium-history/', HistoryMatchesView.as_view()),
    path('stadium-create/', StadiumCreate.as_view()),
]
