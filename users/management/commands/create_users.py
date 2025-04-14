from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Создание нового пользователя"

    def handle(self, *args, **options):
        users = [
            ("user1", "password1"),
            ("user2", "password2")
        ]

        for user in users:
            instance = User.objects.create(username=user[0])
            instance.set_password(user[1])
            instance.save()

        self.stdout.write(self.style.SUCCESS(f"{len(users)} пользователя успешно добавлены!"))
