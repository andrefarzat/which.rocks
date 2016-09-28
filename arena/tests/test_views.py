from django.test import TestCase, Client
from django.urls import reverse

from arena.factories import USERNAME, PASSWORD, FighterFactory, UserFactory
from arena.models import Fighter, Battle


class TestCreateBattleView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = UserFactory()
        self.client.login(username=USERNAME, password=PASSWORD)

    def test_create_battle_with_new_figthers(self):
        fighter_one = FighterFactory.build(creator=self.user)
        fighter_two = FighterFactory.build(creator=self.user)

        data = {'fighter_one': {'name': fighter_one.name, 'description': fighter_one.description,
                                'image': fighter_one.image, 'creator': fighter_one.creator},
                'fighter_two': {'name': fighter_two.name, 'description': fighter_two.description,
                                'image': fighter_two.image, 'creator': fighter_two.creator}}

        self.client.post(reverse('new'), data)

        battle = Battle.objects.first()
        self.assertEqual(battle.fighter_one.name, data['fighter_one']['name'])
        self.assertEqual(battle.fighter_two.name, data['fighter_two']['name'])



