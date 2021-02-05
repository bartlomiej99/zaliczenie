from django.core.exceptions import ValidationError
from .models import Player


def validate_login(login):
    if Player.objects.filter(username=login):
        raise ValidationError('Podany użytkownik już istnieje!')


def validate_first_name(first_name):
    if first_name != first_name.capitalize():
        raise ValidationError('Podane imię nie może zaczynać się małą literą')


def validate_last_name(last_name):
    if last_name != last_name.capitalize():
        raise ValidationError('Podane nazwisko nie może zaczynać się małą literą')