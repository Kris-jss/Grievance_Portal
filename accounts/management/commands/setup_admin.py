from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help = 'Create admin user if not exists'

    def handle(self, *args, **kwargs):
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@example.com',
                password='admin123',  # Change this!
                role='admin'
            )
            self.stdout.write(self.style.SUCCESS('Admin user created!'))
        else:
            admin = User.objects.get(username='admin')
            admin.role = 'admin'
            admin.save()
            self.stdout.write(self.style.SUCCESS('Admin role updated!'))
