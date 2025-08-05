from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from accounts.forms import UserRegistrationForm
from accounts.models import Profile, CustomUser
from accounts.validators import UsernameAlphaNumericUnderscoreValidator

# Create your tests here.
UserModel = get_user_model()

class TestUserModel(TestCase):
    def test__str_method__returns_username(self):
        username = "TestUser"
        user = UserModel.objects.create_user(username=username,
                                             email="testuser@test.com",
                                             password="12admin34",
                                             age=22)
        result = str(user)
        self.assertEqual(result, username)

class TestUsernameAlphaNumericUnderscoreValidator(TestCase):
    def test__valid_usernames(self):
        valid_usernames = [
            "User123",
            "a_bc",
            "Zebra_99",
            "A1B2C3",
            "JohnDoe",
            "user_",
            "A",
            "A_1234567890"
        ]
        for username in valid_usernames:
            try:
                UsernameAlphaNumericUnderscoreValidator(username)
            except ValidationError:
                self.fail(f"Validator raised ValidationError for valid username '{username}'")

    def test__invalid_usernames(self):
        invalid_usernames = [
            "123User",
            "_User",
            "User-Name",
            "User.Name",
            "User Name",
            "User@",
            "user$",
            "",
        ]
        for username in invalid_usernames:
            with self.assertRaises(ValidationError):
                UsernameAlphaNumericUnderscoreValidator(username)

class TestProfileModel(TestCase):
    def test__str_method__returns_username_profile(self):
        user = UserModel.objects.create_user(
            username="TestUser",
            email="testuser@example.com",
            password="12admin34",
            age=22
        )
        profile = Profile.objects.get(user=user)
        expected = "TestUser's profile"
        result = str(profile)
        self.assertEqual(result, expected)

class ProfileSignalTests(TestCase):
    def test__profile_created_on_user_creation(self):
        user = UserModel.objects.create_user(username='testuser',
                                             email="testuser@test.com",
                                             password='testpass',
                                             age=22)
        profile = Profile.objects.get(user=user)
        self.assertEqual(profile.user, user)

class UserRegistrationFormTests(TestCase):
    def test__save_creates_user_with_hashed_password(self):
        form_data = {
            "username": "TestUser",
            "email": "testuser@example.com",
            "age": 22,
            "first_name": "Test",
            "last_name": "User",
            "password1": "StrongPassword!123",
            "password2": "StrongPassword!123",
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)

        user = form.save()
        self.assertIsInstance(user, CustomUser)
        self.assertEqual(user.username, "TestUser")
        self.assertEqual(user.email, "testuser@example.com")
        self.assertEqual(user.age, 22)
        self.assertEqual(user.first_name, "Test")
        self.assertEqual(user.last_name, "User")
        self.assertNotEqual(user.password, form_data["password1"])
        self.assertTrue(user.check_password(form_data["password1"]))
        self.assertTrue(CustomUser.objects.filter(username="TestUser").exists())