from django.contrib.auth import get_user_model
from django.test import TestCase

from table_groups.models import Table

# Create your tests here.
UserModel = get_user_model()

class TestTableModel(TestCase):
    def test__str_method__returns_table_name(self):
        user = UserModel.objects.create_user(
            username="TableCreator",
            email="creator@example.com",
            password="password123",
            age=30
        )
        table_name = "My Table"
        table = Table.objects.create(
            name=table_name,
            created_by=user
        )
        result = str(table)
        self.assertEqual(result, table_name)