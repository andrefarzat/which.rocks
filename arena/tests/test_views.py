from django.test import TestCase, Client
from django.urls import reverse

from arena.factories import USERNAME, PASSWORD, FighterFactory, UserFactory, BattleFactory
from arena.models import Fighter, Battle


class TestCreateBattleView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.client.login(username=USERNAME, password=PASSWORD)

    def test_create_battle_with_new_figthers(self):
        fighter_one = FighterFactory.build(creator=self.user)
        fighter_two = FighterFactory.build(creator=self.user)

        data = {}
        data['fighter_one_name'] = fighter_one.name
        data['fighter_one_creator'] = fighter_one.creator
        data['fighter_one_description'] = fighter_one.description
        data['fighter_one_image'] = fighter_one.image

        data['fighter_two_name'] = fighter_two.name
        data['fighter_two_creator'] = fighter_two.creator
        data['fighter_two_description'] = fighter_two.description
        data['fighter_two_image'] = fighter_two.image

        self.client.post(reverse('new'), data)

        battle = Battle.objects.first()
        self.assertEqual(battle.fighter_one.name, data['fighter_one_name'])
        self.assertEqual(battle.fighter_two.name, data['fighter_two_name'])

    def test_create_battle_with_one_old_figther_and_one_new_fighter(self):
        battle = BattleFactory(creator=self.user)
        fighter_one = battle.fighter_one
        fighter_two = FighterFactory.build(creator=self.user)

        data = {}
        data['fighter_one_name'] = fighter_one.name
        data['fighter_one_creator'] = None
        data['fighter_one_description'] = None
        data['fighter_one_image'] = None

        data['fighter_two_name'] = fighter_two.name
        data['fighter_two_creator'] = fighter_two.creator
        data['fighter_two_description'] = fighter_two.description
        data['fighter_two_image'] = fighter_two.image

        self.client.post(reverse('new'), data)

        new_battle = Battle.objects.first()
        self.assertEqual(new_battle.fighter_one.name, data['fighter_one_name'])
        self.assertEqual(new_battle.fighter_two.name, data['fighter_two_name'])

    def test_create_battle_with_both_old_figthers(self):
        battle = BattleFactory(creator=self.user)
        fighter_one = battle.fighter_one
        fighter_two = battle.fighter_two

        data = {}
        data['fighter_one_name'] = fighter_one.name
        data['fighter_one_creator'] = None
        data['fighter_one_description'] = None
        data['fighter_one_image'] = None

        data['fighter_two_name'] = fighter_two.name
        data['fighter_two_creator'] = None
        data['fighter_two_description'] = None
        data['fighter_two_image'] = None

        self.client.post(reverse('new'), data)

        new_battle = Battle.objects.first()
        self.assertEqual(new_battle.fighter_one.name, data['fighter_one_name'])
        self.assertEqual(new_battle.fighter_two.name, data['fighter_two_name'])
