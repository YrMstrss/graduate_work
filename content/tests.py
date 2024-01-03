from django.test import TestCase, Client

from content.models import Publication
from users.models import User


class PublicationTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user_1 = User.objects.create(first_name='Test', last_name='Testov', phone='89998887766', username='test')
        user_1.set_password('12345')
        user_1.save()
        cls.data = {"title": "test_title", "content": "test_content", 'is_paid': False}
        cls.post = Publication.objects.create(title='title', content='content', is_paid=True, author=user_1)

    def test_create_post(self):
        client = Client()
        client.login(phone="89998887766", password="12345")
        response = client.post("/publication/create/",
                               data={"title": "test_title", "content": "test_content", 'is_paid': False})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/publication/2/')

    def test_read_post(self):
        client = Client()
        client.login(phone="89998887766", password="12345")
        response = client.get(f"/publication/{self.post.pk}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn('title', response.content.decode())
        self.assertIn('content', response.content.decode())
