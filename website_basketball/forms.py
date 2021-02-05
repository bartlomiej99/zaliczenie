from .models import Player, Team, Stadium
import django.forms as forms
from django.core.validators import EmailValidator, ValidationError
from .validators import validate_login, validate_last_name, validate_first_name

YEARS = [1970, 1971, 1972, 1973, 1974, 1975, 1976, 1977, 1978, 1979, 1980,
         1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990,
         1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000,
         2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
         2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020,
         2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030,
         2031, 2032, 2033, 2034, 2035, 2036, 2037, 2038, 2039, 2040,
         2041, 2042, 2043, 2044, 2045, 2046, 2047, 2048, 2049, 2050]


class UserAddForm(forms.Form):
    login = forms.CharField(validators=[validate_login], label="Login")
    password = forms.CharField(widget=forms.PasswordInput, label='Hasło')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Powtórz hasło')
    first_name = forms.CharField(validators=[validate_first_name],label='Imię')
    last_name = forms.CharField(validators=[validate_last_name], label='Nazwisko')
    email = forms.CharField(validators=[EmailValidator()], label='Email')
    date_of_birth = forms.DateField(widget=forms.widgets.SelectDateWidget(years=YEARS), label='Data urodzin')

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password2']:
            raise ValidationError('Hasło nie jest takie same!')
        else:
            return cleaned_data


class LoginForm(forms.Form):
    login = forms.CharField(label='Login')
    password = forms.CharField(widget=forms.PasswordInput, label='Hasło')


class StatisticsCreateForm(forms.Form):
    team = forms.ModelChoiceField(queryset=Team.objects.all(), label='Drużyna')
    matches_played = forms.IntegerField(label='Liczba rozegranych meczy')
    total_points = forms.IntegerField(label='Liczba zdobytych punktów')
    total_wins = forms.IntegerField(label='Liczba wygranych meczy')


class TeamCreateForm(forms.Form):
    team_name = forms.CharField(max_length=64, label="Nazwa drużyny")
    players = forms.ModelMultipleChoiceField(queryset=Player.objects.all(), label="Wybierz członków drużyny")


class UserEditForm(forms.Form):
    first_name = forms.CharField(label='Nowe imię')
    last_name = forms.CharField(label='Nowe nazwisko')
    password = forms.CharField(widget=forms.PasswordInput, label='Nowe hasło')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Powtórz nowe hasło')

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password2']:
            raise ValidationError('Hasło nie jest takie same!')
        else:
            return cleaned_data


class TournamentCreateForm(forms.Form):
    name = forms.CharField(max_length=64, label="Nazwa turnieju")
    team = forms.ModelMultipleChoiceField(queryset=Team.objects.all(), label="Drużyna")


class TeamWinsAddForm(forms.Form):
    team = forms.ModelChoiceField(queryset=Team.objects.all(), label="Wybierz drużynę")


class TeamPlayerDeleteForm(forms.Form):
    team = forms.ModelChoiceField(queryset=Team.objects.all(), label="Wybierz drużynę")
    delete_player = forms.ModelMultipleChoiceField(queryset=Player.objects.all(), label="Usuń z drużyny")


class TeamPlayerAddForm(forms.Form):
    team = forms.ModelChoiceField(queryset=Team.objects.all(), label="Wybierz drużynę")
    add_player = forms.ModelMultipleChoiceField(queryset=Player.objects.all(), label="Dodaj do drużyny")


class StadiumCreateForm(forms.Form):
    name = forms.CharField(max_length=100, label='Stadion')


class MatchCreateForm(forms.Form):
    name = forms.ModelChoiceField(queryset=Stadium.objects.all().order_by('name'), label='Stadion')
    team1 = forms.ModelChoiceField(queryset=Team.objects.all().order_by('team_name'), label='Drużyna')
    date = forms.DateField(widget=forms.widgets.SelectDateWidget(), label="Data rozegrania meczu")


class StadiumHistoryFinder(forms.Form):
    name = forms.ModelChoiceField(queryset=Stadium.objects.all().order_by('name'), label='Stadion')
    team = forms.ModelChoiceField(queryset=Team.objects.all().order_by('team_name'), label='Drużyna')
    date = forms.DateField(widget=forms.widgets.SelectDateWidget(), label="Data rozegrania meczu")