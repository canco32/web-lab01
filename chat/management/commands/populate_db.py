import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from faker import Faker

from chat.models import Chat, ChatMember
from message.models import Message

User = get_user_model()
fake = Faker('uk_UA')


class Command(BaseCommand):
    help = 'Populate database with test data'

    def handle(self, *args, **options):
        self.stdout.write('Creating test data...')

        users = []
        for i in range(10):
            user = User.objects.create_user(
                email=f'testuser{i}@example.com',
                username=f'testuser{i}',
                password='Testpass123',
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                gender=random.choice(['M', 'F', 'O']),
                birth_date=fake.date_of_birth(minimum_age=18, maximum_age=65),
            )
            users.append(user)

        chats = []

        for _ in range(5):
            a, b = random.sample(users, 2)
            chat = Chat.objects.create(
                type='private',
                created_by=a,
                title='',
            )
            ChatMember.objects.create(chat=chat, user=a, role='owner')
            ChatMember.objects.create(chat=chat, user=b, role='member')
            chats.append(chat)

        for _ in range(7):
            owner = random.choice(users)
            other_count = random.randint(2, 4)
            members = {owner}
            while len(members) < other_count + 1:
                members.add(random.choice(users))
            members = list(members)
            chat = Chat.objects.create(
                type='group',
                title=fake.sentence(nb_words=5)[:255],
                created_by=owner,
            )
            for u in members:
                role = 'owner' if u == owner else 'member'
                ChatMember.objects.create(chat=chat, user=u, role=role)
            chats.append(chat)

        messages = []
        for _ in range(100):
            chat = random.choice(chats)
            members = list(chat.participants.all())
            sender = random.choice(members)
            message = Message.objects.create(
                chat=chat,
                sender=sender,
                text=fake.text(max_nb_chars=500),
            )
            messages.append(message)

        for message in random.sample(messages, k=min(25, len(messages))):
            same_chat = [m for m in messages if m.chat_id == message.chat_id and m.pk < message.pk]
            if same_chat:
                message.reply_to = random.choice(same_chat)
                message.save(update_fields=['reply_to'])

        self.stdout.write(
            self.style.SUCCESS('Successfully created test data')
        )
