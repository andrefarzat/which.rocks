from django.test import TestCase

from arena.factories import FighterFactory, UserFactory
from arena.forms import BattleForm


class TestBattleForm(TestCase):

    def test_with_full_data(self):
        fighter_one = FighterFactory()
        fighter_two = FighterFactory()

        data = {}
        data['fighter_one_name'] = fighter_one.name
        data['fighter_one_image'] = fighter_one.image
        data['fighter_one_description'] = fighter_one.description
        data['fighter_two_name'] = fighter_two.name
        data['fighter_two_image'] = fighter_two.image
        data['fighter_two_description'] = fighter_two.description

        form = BattleForm(data)
        self.assertTrue(form.is_valid())


