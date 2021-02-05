import pytest
from django.contrib.auth.models import Permission
from website_basketball.models import Player, Team, Stadium


@pytest.fixture
def player():
    player = Player.objects.create_user(username='mistrzunio', password='hotel', email='panda@onet.pl',
                                        first_name='Radek', last_name='Cholipka')
    return player


@pytest.fixture
def test_player():
    player = Player.objects.create_user(username='wisienka', password='plebania', email='nerf0@o2.pl',
                                        first_name='Bartek', last_name='Kot')
    return player


@pytest.fixture
def second_test_player():
    player = Player.objects.create_user(username='bolek', password='lolek', email='rafi@onet.pl',
                                        first_name='Sebastian', last_name='Wardęga')
    return player


@pytest.fixture
def test_stadium():
    stadium = Stadium.objects.create(name='W Ełku')
    return stadium


@pytest.fixture
def test_stadium_with_date():
    stadium = Stadium.objects.create(name='W Warszawie', date='1999-01-10')
    return stadium


@pytest.fixture
def auth_player_with_perm_add_stats():
    authorized_player = Player.objects.create_user("Felipe")
    perm = Permission.objects.get(codename="add_statistics")
    authorized_player.user_permissions.add(perm)
    return authorized_player


@pytest.fixture
def auth_player_with_perm_add_tournament():
    authorized_player = Player.objects.create_user("Felipe")
    perm = Permission.objects.get(codename="add_tournament")
    authorized_player.user_permissions.add(perm)
    return authorized_player


@pytest.fixture
def auth_player_add_wins():
    authorized_player = Player.objects.create_user("Felipe")
    perm = Permission.objects.get(codename="add_wins")
    authorized_player.user_permissions.add(perm)
    return authorized_player


@pytest.fixture
def auth_player_add_stadium():
    authorized_player = Player.objects.create_user("Felipe")
    perm = Permission.objects.get(codename="add_stadium")
    authorized_player.user_permissions.add(perm)
    return authorized_player


@pytest.fixture
def auth_player_add_match():
    authorized_player = Player.objects.create_user("Felipe")
    perm = Permission.objects.get(codename="add_match")
    authorized_player.user_permissions.add(perm)
    return authorized_player


@pytest.fixture
def unauthorized_player():
    unauthorized_player = Player.objects.create_user("Felipe")
    return unauthorized_player


@pytest.fixture
def test_team():
    team = Team.objects.create(team_name='KoxTV')
    return team


@pytest.fixture
def second_test_team():
    team = Team.objects.create(team_name='Kominiarze')
    return team
