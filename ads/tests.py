from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from ads.models import Ad
from table_groups.models import Table

# Create your tests here.
User = get_user_model()

class TestAdModelClean(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="AdOwner",
            email="adowner@example.com",
            password="12admin34",
            age=25
        )
        self.table = Table.objects.create(
            name="Ad Table",
            created_by=self.user
        )

    def test__clean_raises_if_no_players_or_dm(self):
        ad = Ad(
            owner=self.user,
            table=self.table,
            description="Test ad",
            looking_for_players=False,
            looking_for_dm=False
        )
        with self.assertRaises(ValidationError):
            ad.clean()

    def test__clean_sets_num_players_none_if_not_looking_for_players(self):
        ad = Ad(
            owner=self.user,
            table=self.table,
            description="Test ad",
            looking_for_players=False,
            looking_for_dm=True,
            num_players=4
        )
        ad.clean()
        self.assertIsNone(ad.num_players)

    def test_clean_passes_if_looking_for_players(self):
        ad = Ad(
            owner=self.user,
            table=self.table,
            description="Test ad",
            looking_for_players=True,
            looking_for_dm=False,
            num_players=3
        )
        try:
            ad.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly when looking_for_players=True")