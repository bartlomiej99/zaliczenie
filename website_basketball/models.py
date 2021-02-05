from django.db import models
from django.contrib.auth.models import AbstractUser


class Tournament(models.Model):
    name = models.CharField(max_length=64, verbose_name="Nazwa turnieju")

    def __str__(self):
        return self.name


class Team(models.Model):
    team_name = models.CharField(max_length=64, unique=True, verbose_name="Nazwa drużyny")
    points_in_tournament = models.IntegerField(verbose_name="Liczba punktów", default=0)
    wins = models.IntegerField(verbose_name="Wygrane mecze w turnieju", default=0)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, null=True)

    class Meta:
        permissions = (
            ("add_wins", "Can add wins for Team"),
        )

    def __str__(self):
        return self.team_name


class Player(AbstractUser):
    date_of_birth = models.DateField(null=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name="Drużyna", null=True)

    def __str__(self):
        return self.first_name


class Statistics(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, verbose_name="Drużyna")
    matches_played = models.IntegerField(verbose_name="Liczba zagranych meczy")
    total_points = models.IntegerField(verbose_name="Liczba zdobytych punktów")
    total_wins = models.IntegerField(verbose_name="Liczba wygranych meczy")


class Stadium(models.Model):
    name = models.CharField(max_length=100, verbose_name='Nazwa stadionu')
    team = models.ManyToManyField(Team, null=True)
    date = models.DateField(null=True)
    statistics = models.ForeignKey(Statistics, on_delete=models.CASCADE, null=True, verbose_name='Statystyki')

    class Meta:
        permissions = (
            ("add_match", "Can add matches to the history"),
        )

    def __str__(self):
        return self.name
