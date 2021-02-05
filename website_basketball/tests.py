import pytest
from website_basketball.models import Player, Team, Tournament, Stadium


@pytest.mark.django_db
def test_player_add(client):
    response = client.post('/add-user/', {'login': 'Gracz12', 'email': 'nerf0_1999@o2.pl', 'password': 'rybak',
                                          'password2': 'rybak', 'first_name': 'Kacper', 'last_name': 'Brzoznowski',
                                          'date_of_birth': '1999-02-10'})
    assert Player.objects.filter(username='Gracz12')


@pytest.mark.django_db
def test_login(client):
    response = client.post('/login/', {'login': 'wisienka', 'password': 'pandemia'})
    assert response.status_code == 200


@pytest.mark.django_db
def test_login_authenticate(client, test_player):
    if not test_player.is_authenticated:
        response = client.post('/login/', {'login': 'wisienka', 'password': 'plebania'})
        assert test_player is None


@pytest.mark.django_db
def test_statistics_create_has_no_perm(client, unauthorized_player, test_team):
    client.force_login(unauthorized_player)
    team = test_team
    response = client.post('/statistics-create/', {'team': team, 'matches_played': 0,
                                                   'total_points': 0, 'total_wins': 0})
    assert response.status_code == 403


@pytest.mark.django_db
def test_statistics_create_has_perm(client, auth_player_with_perm_add_stats, test_team):
    client.force_login(auth_player_with_perm_add_stats)
    team = test_team
    response = client.post('/statistics-create/', {'team': team, 'matches_played': 0,
                                                   'total_points': 0, 'total_wins': 0})
    assert response.status_code == 200


@pytest.mark.django_db
def test_team_create_with_one_player(client, test_player, second_test_player):
    client.force_login(test_player)
    player = second_test_player
    response = client.post('/team-create/', {'team_name': 'Ełczanie', 'players': [player.id]})
    assert Team.objects.filter(team_name='Ełczanie', player=player.id)


@pytest.mark.django_db
def test_team_has_multiple_players(client, test_player):
    client.force_login(test_player)
    player = Player.objects.create_user(username='szymon')
    player2 = Player.objects.create_user(username='bartek')
    response = client.post('/team-create/', {'team_name': 'Sokoliki', 'players': [player.id, player2.id]})
    assert Team.objects.filter(team_name='Sokoliki', player=player.id)
    assert Team.objects.filter(team_name='Sokoliki', player=player2.id)


@pytest.mark.django_db
def test_team_player_delete(client, test_player, test_team, second_test_player):
    client.force_login(test_player)
    team = test_team
    player = second_test_player
    response = client.post('/player-delete/', {'team': [team.id], 'delete_player': [player.id]})
    assert Player.objects.filter(username='bolek', team_id=None)


@pytest.mark.django_db
def test_team_player_delete_when_player_is_unauthorized(client, test_player, test_team, second_test_player):
    team = test_team
    player = second_test_player
    if not test_player.is_authenticated:
        response = client.post('/player-delete/', {'team': [team.id], 'delete_player': [player.id]})
        assert test_player is None


@pytest.mark.django_db
def test_team_one_player_add(client, test_player, test_team, second_test_player):
    client.force_login(test_player)
    team = test_team
    player = second_test_player
    response = client.post('/player-add/', {'team': [team.id], 'add_player': [player.id]})
    assert Player.objects.filter(username='bolek', team_id=team.id)


@pytest.mark.django_db
def test_team_multiple_players_add(client, test_player, second_test_player, test_team, player):
    client.force_login(player)
    player = test_player
    second_player = second_test_player
    team = test_team
    response = client.post('/player-add/', {'team': [team.id], 'add_player': [player.id, second_player.id]})
    assert Player.objects.filter(username=player.username, team_id=team.id)
    assert Player.objects.filter(username=second_player.username, team_id=team.id)


@pytest.mark.django_db
def test_player_edit_profile(client, test_player):
    client.force_login(test_player)
    response = client.post('/edit-account/', {'first_name': 'Szymon', 'last_name': 'Pies',
                                              'password': 'chlebek', 'password2': 'chlebek'})
    assert response.status_code == 302


@pytest.mark.django_db
def test_tournament_create_with_perm(client, auth_player_with_perm_add_tournament, test_team, second_test_team):
    client.force_login(auth_player_with_perm_add_tournament)
    team = test_team
    team2 = second_test_team
    response = client.post('/tournament-create/', {'name': 'Championships', 'team': [team.id, team2.id]})
    assert Tournament.objects.filter(name='Championships', team=team.id)
    assert Tournament.objects.filter(name='Championships', team=team2.id)


@pytest.mark.django_db
def test_tournament_create_without_perm(client, test_team, second_test_team, unauthorized_player):
    client.force_login(unauthorized_player)
    team = test_team
    team2 = second_test_team
    response = client.post('/tournament-create/', {'name': 'Championships', 'team': [team.id, team2.id]})
    assert response.status_code == 403


@pytest.mark.django_db
def test_wins_add_with_perm(client, auth_player_add_wins, test_team):
    client.force_login(auth_player_add_wins)
    team = test_team
    response = client.post('/team-wins-add/', {'team': [team.id]})
    assert Team.objects.filter(team_name='KoxTV', wins=1)


@pytest.mark.django_db
def test_wins_add_without_perm(client, unauthorized_player, test_team):
    client.force_login(unauthorized_player)
    team = test_team
    response = client.post('/team-wins-add/', {'team': [team.id]})
    assert response.status_code == 403


@pytest.mark.django_db
def test_stadium_create_with_perm(client, auth_player_add_stadium):
    client.force_login(auth_player_add_stadium)
    response = client.post('/stadium-create/', {'name': 'Stadion miejski w Ełku'})
    assert Stadium.objects.filter(name='Stadion miejski w Ełku')


@pytest.mark.django_db
def test_stadium_create_without_perm(client, unauthorized_player):
    client.force_login(unauthorized_player)
    response = client.post('/stadium-create/', {'name': 'Stadion miejski w Ełku'})
    assert response.status_code == 403


@pytest.mark.django_db
def test_match_create_with_perm(client, auth_player_add_match, test_stadium, test_team):
    client.force_login(auth_player_add_match)
    team = test_team
    stadium = test_stadium
    response = client.post('/stadium-match-create/', {'name': [stadium.id], 'team1': [team.id], 'date': '1999-01-10'})
    assert Stadium.objects.filter(id=stadium.id, team=team.id, date='1999-01-10')


@pytest.mark.django_db
def test_match_create_without_perm(client, unauthorized_player, test_stadium, test_team):
    client.force_login(unauthorized_player)
    team = test_team
    stadium = test_stadium
    response = client.post('/stadium-match-create/', {'name': [stadium.id], 'team1': [team.id], 'date': '1999-01-10'})
    assert response.status_code == 403
