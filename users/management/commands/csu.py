from django.core.management import BaseCommand
from django.db import IntegrityError

from users.models import User


class Command(BaseCommand):
    """
    Команда для создания суперпользователя
    """

    def handle(self, *args, **options):
        try:
            user = User.objects.create(
                phone='88008008080',
                first_name='Admin',
                last_name='Content',
                username='admin',
                is_staff=True,
                is_superuser=True
            )

            user.set_password('password')
            user.save()
        except IntegrityError:
            pass
