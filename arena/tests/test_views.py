from django.test import TestCase, Client
from django.urls import reverse

from arena.factories import USERNAME, PASSWORD, FighterFactory, UserFactory, BattleFactory
from arena.models import Fighter, Battle


class TestCreateBattleView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory(username=USERNAME)
        self.client.login(username=USERNAME, password=PASSWORD)

    def test_create_battle_with_new_figthers(self):
        fighter_one = FighterFactory.build(creator=self.user)
        fighter_two = FighterFactory.build(creator=self.user)

        data = {}
        data['one-name'] = fighter_one.name
        data['one-description'] = fighter_one.description
        data['one-image'] = fighter_one.image

        data['two-name'] = fighter_two.name
        data['two-description'] = fighter_two.description
        data['two-image'] = fighter_two.image

        self.client.post(reverse('new'), data)

        battle = Battle.objects.first()
        self.assertEqual(battle.fighter_one.name, data['one-name'])
        self.assertEqual(battle.fighter_two.name, data['two-name'])

    def test_create_battle_with_one_old_figther_and_one_new_fighter(self):
        battle = BattleFactory(creator=self.user)
        fighter_one = battle.fighter_one
        fighter_two = FighterFactory.build(creator=self.user)

        data = {}
        data['one-name'] = fighter_one.name
        data['one-description'] = None
        data['one-image'] = None

        data['two-name'] = fighter_two.name
        data['two-description'] = fighter_two.description
        data['two-image'] = fighter_two.image

        self.client.post(reverse('new'), data)

        new_battle = Battle.objects.first()
        self.assertEqual(new_battle.fighter_one.name, data['one-name'])
        self.assertEqual(new_battle.fighter_two.name, data['two-name'])

    def test_create_battle_with_both_old_figthers(self):
        battle = BattleFactory(creator=self.user)
        fighter_one = battle.fighter_one
        fighter_two = battle.fighter_two

        data = {}
        data['one-name'] = fighter_one.name
        data['one-description'] = None
        data['one-image'] = None

        data['two-name'] = fighter_two.name
        data['two-description'] = None
        data['two-image'] = None

        self.client.post(reverse('new'), data)

        new_battle = Battle.objects.first()
        self.assertEqual(new_battle.fighter_one.name, data['one-name'])
        self.assertEqual(new_battle.fighter_two.name, data['two-name'])
