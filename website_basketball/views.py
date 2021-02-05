from django.shortcuts import render, redirect
from django.views import View
from .models import Team, Tournament, Statistics, Player, Stadium
from django.contrib.auth import authenticate, login, logout
from .forms import UserAddForm, LoginForm, StatisticsCreateForm, TeamCreateForm, UserEditForm, TournamentCreateForm,\
    TeamWinsAddForm, TeamPlayerDeleteForm, TeamPlayerAddForm, StadiumCreateForm, StadiumHistoryFinder, MatchCreateForm
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.db import IntegrityError


class HomePageView(View):
    def get(self, request):
        return render(request, "home_page.html")
    """ Strona główna wyświetla linki z przekierowaniami do różnych widoków """


class UserAddView(View):
    def get(self, request):
        form = UserAddForm()
        return render(request, "user_add.html", {'form': form})

    def post(self, request):
        form = UserAddForm(request.POST)
        if form.is_valid():
            try:
                Player.objects.create_user(username=form.cleaned_data['login'],
                                           password=form.cleaned_data['password'],
                                           email=form.cleaned_data['email'],
                                           first_name=form.cleaned_data['first_name'],
                                           last_name=form.cleaned_data['last_name'],
                                           date_of_birth=form.cleaned_data['date_of_birth'])
                return redirect('/login/')
            except IntegrityError:
                return render(request, "user_add.html", {'form': form, 'info': 'Użytkownik o podanym loginie istnieje!'})
        else:
            return render(request, "user_add.html", {'form': form, 'info': 'Wypełnij poprawnie wszystkie pola!'})

    """ Wchodząc metodą GET pokazuje pusty formularz rejestracyjny,
    a metodą POST wysyła formularz i zapisuje do bazy danych jeżeli jest poprawny """


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['login'],
                                password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect('/')
            else:
                return render(request, "login.html", {'form': form, 'info': "Błędny login lub hasło!"})

    """ Po wejściu na stronę logowania metodą GET wyświetla pusty formularz,
     a po wejściu metodą POST wysyła dane z formularza i po wpisaniu poprawnych danych loguje użytkownika na stronę """


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('/')

    """ Po wciśnięciu przycisku wyloguj, wyloguje użytkownika ze strony i przekierowuje na stronę główną"""


class StatisticsCreateView(PermissionRequiredMixin, View):
    permission_required = 'website_basketball.add_statistics'
    permission_denied_message = 'Nie masz odpowiednich uprawnień!'

    def get(self, request):
        form = StatisticsCreateForm()
        return render(request, "statistics_create.html", {'form': form})

    def post(self, request):
        form = StatisticsCreateForm(request.POST)
        if form.is_valid():
            user = request.user
            if user.has_perm('website_basketball.add_statistics'):
                Statistics.objects.create(team=form.cleaned_data['team'],
                                          matches_played=form.cleaned_data['matches_played'],
                                          total_points=form.cleaned_data['total_points'],
                                          total_wins=form.cleaned_data['total_wins'])
                return redirect('/statistics/')
            else:
                return render(request, "403.html")
        else:
            return render(request, "statistics_create.html", {'form': form, 'info': "Wypełnij poprawnie formularz!"})

    """ Aby móc wejść na tą podstronę trzeba mieć uprawnienie, po wejściu metodą GET wyświetla pusty formularz,
     a po wejściu metodą POST wysyła formularz gdy jest poprawny i zapisuje dane do bazy """


class StatisticsShowView(View):
    def get(self, request):
        statistics = Statistics.objects.all().order_by('team')
        return render(request, "statistics_show.html", {'statistics': statistics})

    """ Wyświetla Wszystkie zapisane statystyki ułożone po kolei nazwami drużyn """


class TeamShowView(View):
    def get(self, request):
        team = Team.objects.all().order_by('team_name')
        return render(request, "team_show.html", {'team': team})

    """ Wyświetla stworzone drużyny ułożone po kolei poprzez ich nazwy """


class TeamCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = TeamCreateForm()
        return render(request, "team_create.html", {'form': form})

    def post(self, request):
        form = TeamCreateForm(request.POST)
        if form.is_valid():
            team = Team.objects.create(team_name=form.cleaned_data['team_name'])
            players = form.cleaned_data['players']
            for p in players:
                p.team = team
                p.save()
            return redirect("/team/")
        else:
            return render(request, "team_create.html", {'form': form, 'info': "Wypełnij poprawnie formularz!"})
    """ Po wejściu metodą GET wyświetla pusty formularz dodania drużyny,
        a po wejściu metodą POST zapisuje drużynę i graczy do bazy danych """


class TeamPlayerDeleteView(LoginRequiredMixin, View):
    def get(self, request):
        form = TeamPlayerDeleteForm()
        return render(request, "team_player_delete.html", {'form': form})

    def post(self, request):
        form = TeamPlayerDeleteForm(request.POST)
        if form.is_valid():
            team = Team.objects.get(team_name=form.cleaned_data['team'])
            delete_player = form.cleaned_data['delete_player']
            for p in delete_player:
                p.team = None
                p.save()
            return redirect('/team/', {'info': 'Gracz pomyślnie usunięty!'})
        else:
            return render(request, "team_player_delete.html", {'form': form, 'info': 'Wypełnij poprawnie formularz!'})

    """ Po wejściu na stronę wyświetla formularz,
        a gdy wyślę się formularz zp oprawnymi danymi usuwa gracza z danej drużyny """


class TeamPlayerAddView(LoginRequiredMixin, View):
    def get(self, request):
        form = TeamPlayerAddForm()
        return render(request, "team_player_add.html", {'form': form})

    def post(self, request):
        form = TeamPlayerAddForm(request.POST)
        if form.is_valid():
            add_player = form.cleaned_data['add_player']
            team = Team.objects.get(team_name=form.cleaned_data['team'])
            for p in add_player:
                p.team = team
                p.save()
            return redirect('/team/', {'info': 'Gracz pomyślnie dodany!'})
        else:
            return render(request, "team_player_add.html", {'form': form, 'info': 'Wypełnij poprawnie formularz!'})

    """ Po wejściu metodą GET wyświetli formularz dodania gracza do drużyny,
        a po wejściu POST wyśle formularz i doda gracza do odpowiedniej drużyny"""


class PlayerEditView(LoginRequiredMixin, View):
    def get(self, request):
        form = UserEditForm()
        return render(request, "user_edit.html", {'form': form})

    def post(self, request):
        user = request.user
        form = UserEditForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            password = form.cleaned_data['password']
            player = Player.objects.get(id=user.id)
            player.first_name = first_name
            player.last_name = last_name
            player.set_password(password)
            player.save()
            return redirect("/login/")
        else:
            return render(request, "user_edit.html", {'form': form, 'info': "Wypełnij poprawnie formularz!"})

    """ Po wejściu na stronę metodą GET wyświetli formularz edycji profilu,
        a po wejściu POST wyśle formularz i zapisze dane do bazy o ile będą poprawne"""


class TournamentsListView(View):
    def get(self, request):
        tournament = Tournament.objects.all()
        team = Team.objects.all()
        return render(request, "tournament_list.html", {'tournament': tournament, 'team': team})

    """ Pokazuje listę Turniejów oraz drużyn biorących w nim udział"""


class TournamentCreateView(PermissionRequiredMixin, View):
    permission_required = 'website_basketball.add_tournament'

    def get(self, request):
        form = TournamentCreateForm()
        return render(request, "tournament_create.html", {'form': form})

    def post(self, request):
        form = TournamentCreateForm(request.POST)
        if form.is_valid():
            user = request.user
            if user.has_perm('website_basketball.add_tournament'):
                tournament = Tournament.objects.create(name=form.cleaned_data['name'])
                team = form.cleaned_data['team']
                for t in team:
                    t.tournament = tournament
                    t.save()
                return redirect('/tournament/')
            else:
                return render(request, "403.html")
        else:
            return render(request, "tournament_create.html", {'form': form, 'info': "Wypełnij poprawnie formularz!"})

    """ Aby wejść potrzebne jest uprawnienie, po wejściu GET Wyświetli pusty formularz,
        a po wejściu POST wyślę formularz doda turniej do bazy danych oraz drużyny przypisane do tego turnieju"""


class TournamentTableView(View):
    def get(self, request):
        team = Team.objects.all().order_by('team_name')
        team_stage_2 = Team.objects.filter(wins=1)
        team_stage_3 = Team.objects.filter(wins=2)
        team_final = Team.objects.filter(wins=3)
        team_win = Team.objects.filter(wins=4)
        return render(request, "table_new.html", {'team': team,
                                                  'team_stage_2': team_stage_2,
                                                  'team_stage_3': team_stage_3,
                                                  'team_final': team_final,
                                                  'team_win': team_win})


class TeamWinsAddView(PermissionRequiredMixin, View):
    permission_required = 'website_basketball.add_wins'

    def get(self, request):
        form = TeamWinsAddForm()
        return render(request, "team_wins_add.html", {'form': form})

    def post(self, request):
        form = TeamWinsAddForm(request.POST)
        user = request.user
        if form.is_valid():
            if user.has_perm('website_basketball.add_wins'):
                team = Team.objects.get(team_name=form.cleaned_data['team'])
                team.wins += 1
                team.save()
                return redirect('/team/')
            else:
                return render(request, "403.html")
        else:
            return render(request, "team_wins_add.html", {'form': form, 'info': 'Wypełni poprawnie pole!'})

    """ Potrzebne uprawnienie aby wejść, po wejściu GET wyświetli formularz dodania zwycięstwa drużyny,
        a po wejściu post zwiększy liczbę wygranych drużyny o 1"""


class StadiumCreate(PermissionRequiredMixin, View):
    permission_required = 'website_basketball.add_stadium'

    def get(self, request):
        form = StadiumCreateForm()
        return render(request, "stadium_create.html", {'form': form})

    def post(self, request):
        form = StadiumCreateForm(request.POST)
        if form.is_valid():
            user = request.user
            if user.has_perm('website_basketball.add_stadium'):
                Stadium.objects.create(name=form.cleaned_data['name'])
                return redirect('/stadium-history/')
            else:
                return render(request, "403.html")
        else:
            return render(request, "stadium_create.html", {'form': form,
                                                           'info': 'Wypełnij poprawnie formularz!'})

    """ Wymagane uprawnienie, po wejściu GET wyświetli formularz stworzenia stadion,
        a po wejściu POST doda stadion i zapisze w bazie danych"""


class MatchCreateView(PermissionRequiredMixin, View):
    permission_required = 'website_basketball.add_match'

    def get(self, request):
        form = MatchCreateForm()
        return render(request, "match_create.html", {'form': form})

    def post(self, request):
        form = MatchCreateForm(request.POST)
        user = request.user
        if form.is_valid():
            if user.has_perm('website_basketball.add_match'):
                date = form.cleaned_data['date']
                stadium_name = form.cleaned_data['name']
                team = Team.objects.get(team_name=form.cleaned_data['team1'])
                stadium = Stadium.objects.get(name=stadium_name)
                stadium.team.add(team)
                stadium.save()
                stadium.date = date
                stadium.save()
                return redirect('/stadium-history/')
            else:
                return render(request, "403.html")
        else:
            return render(request, "match_create.html", {'form': form, 'info': 'Wypełnij poprawnie formularz!'})

    """ Wymagane uprawnienie, po wejściu GET wyświetli formularz dodanie meczu do history rozgrywek na danym stadionie,
        a po wejściu POST wyśle formularz i zapisze drużynę która grała na tym stadionie"""


class HistoryMatchesView(LoginRequiredMixin, View):
    def get(self, request):
        form = StadiumHistoryFinder()
        return render(request, "history_matches.html", {'form': form})

    def post(self, request):
        form = StadiumHistoryFinder(request.POST)
        if form.is_valid():
            date = form.cleaned_data['date']
            name = form.cleaned_data['name']
            team = Team.objects.get(team_name=form.cleaned_data['team'])
            stadium = Stadium.objects.get(name=name, date=date)
            return render(request, "history_matches.html", {'team': team, 'stadium': stadium})
        else:
            return render(request, "history_matches.html", {'form': form, 'info': 'Wypełnij poprawnie wszystkie pola!'})

    """ Po wejściu GET wyświetli formularz wyszukania meczu który odbył się na danym stadionie określonego dnia,
        a po wejściu POST wyszukane dane z bazy danych które zostały przekazane w formularzu,
        oraz wyświetli znaleziony mecz"""
