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
        data['one-slug'] = ''

        data['two-name'] = fighter_two.name
        data['two-description'] = fighter_two.description
        data['two-image'] = fighter_two.image
        data['two-slug'] = ''

        self.client.post(reverse('new'), data)

        new_battle = Battle.objects.last()
        self.assertEqual(new_battle.fighter_one.name, data['one-name'])
        self.assertEqual(new_battle.fighter_two.name, data['two-name'])

    def test_create_battle_with_one_old_figther_and_one_new_fighter(self):
        battle = BattleFactory(creator=self.user)
        fighter_one = battle.fighter_one                            #Old
        fighter_two = FighterFactory.build(creator=self.user)       #New

        data = {}
        data['one-name'] = ''
        data['one-description'] = ''
        data['one-image'] = ''
        data['one-slug'] = fighter_one.slug

        data['two-name'] = fighter_two.name
        data['two-description'] = fighter_two.description
        data['two-image'] = fighter_two.image
        data['two-slug'] = ''

        self.client.post(reverse('new'), data)

        new_battle = Battle.objects.last()
        self.assertEqual(new_battle.fighter_one.slug, fighter_one.slug)
        self.assertEqual(new_battle.fighter_two.name, data['two-name'])

    def test_create_battle_with_both_old_figthers(self):
        battle1 = BattleFactory(creator=self.user)
        battle2 = BattleFactory(creator=self.user)
        fighter_one = battle1.fighter_one
        fighter_two = battle2.fighter_two

        data = {}
        data['one-name'] = ''
        data['one-description'] = ''
        data['one-image'] = ''
        data['one-slug'] = fighter_one.slug

        data['two-name'] = ''
        data['two-description'] = ''
        data['two-image'] = ''
        data['two-slug'] = fighter_two.slug

        self.client.post(reverse('new'), data)

        new_battle = Battle.objects.last()
        self.assertEqual(new_battle.fighter_one.slug, fighter_one.slug)
        self.assertEqual(new_battle.fighter_two.slug, fighter_two.slug)
