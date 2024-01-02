from django.test import TestCase, Client

from users.models import User


class UserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_1 = User.objects.create(first_name='Test', last_name='Testov',phone='89998887766', username='test')
        user_1.set_password('12345')
        user_1.save()
        user_2 = User.objects.create(first_name='Test2', last_name='Testov', phone='81112223344', username='test2')
        user_2.subscriptions.add(user_1)
        user_2.set_password('54321')
        user_2.save()

    def test_login(self):
        client = Client()
        response = client.post("/user/login/", {"phone": "89998887766", "password": "12345"})
        self.assertEqual(response.status_code, 200)

    def test_my_profile(self):
        client = Client()
        client.login(phone="89998887766", password="12345")
        response = client.get("/user/my-profile")
        self.assertEqual(response.status_code, 200)
        self.assertIn('89998887766', response.content.decode())
        self.assertIn('test', response.content.decode())
        self.assertIn('Test Testov', response.content.decode())
        self.assertIn('нет подписок', response.content.decode())
        self.assertIn('Testov Test2', response.content.decode())

    def test_other_profile(self):
        client = Client()
        client.login(phone="89998887766", password="12345")
        response = client.get("/user/profile/2")
        self.assertEqual(response.status_code, 200)
        self.assertIn('81112223344', response.content.decode())
        self.assertIn('test2', response.content.decode())
        self.assertIn('Test2 Testov', response.content.decode())
        self.assertIn('Testov Test', response.content.decode())
        self.assertIn('нет подписчиков', response.content.decode())
