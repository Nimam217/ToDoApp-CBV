from django.core.management.base import BaseCommand
from faker import Faker
from accounts.models import User, Profile
from task.models import Task
import random


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__()
        self.fake = Faker()

    def handle(self, *args, **options):
        user = User.objects.create_user(
            email=self.fake.email(), password="@ASDF!@#"
        )
        profile = Profile.objects.get(user=user)
        profile.first_name = str(self.fake.first_name())
        profile.last_name = str(self.fake.last_name())
        profile.description = str(self.fake.paragraph(nb_sentences=3))
        profile.save()

        for _ in range(10):
            Task.objects.create(
                user=user,
                title=str(self.fake.sentence(nb_words=3)),
                description=str(self.fake.paragraph(nb_sentences=3)),
                done=random.choice([True, False]),
            ),
