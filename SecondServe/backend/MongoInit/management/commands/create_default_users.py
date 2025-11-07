# backend/app/management/commands/create_default_users.py
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from User.models import User


class Command(BaseCommand):
    help = "Create default users"

    def handle(self, *args, **kwargs):
        users = [
            {
                "username": "user",
                "email": "user@example.com",
                "password": "user123",
                "role": "user",
            },
            {
                "username": "org",
                "email": "org@example.com",
                "password": "org123",
                "role": "organization",
            },
            {
                "username": "driver",
                "email": "driver@example.com",
                "password": "driver123",
                "role": "driver",
            },
        ]

        for u in users:
            if not User.objects.filter(email=u["email"]).exists():
                User.objects.create(
                    username=u["username"],
                    email=u["email"],
                    password=make_password(u["password"]),
                    role=u["role"],
                )
                self.stdout.write(self.style.SUCCESS(f"Created user {u['email']}"))
            else:
                self.stdout.write(f"User {u['email']} already exists")
