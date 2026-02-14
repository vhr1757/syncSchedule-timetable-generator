from django.apps import AppConfig
from django.db.models.signals import post_migrate

class GeneratorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'generator'

    def ready(self):
        from django.contrib.auth import get_user_model

        def create_default_users(sender, **kwargs):
            User = get_user_model()

            # Create Admin
            if not User.objects.filter(username='admin').exists():
                User.objects.create_superuser(
                    username='admin',
                    password='vedansh17052007',
                    email='admin@example.com',
                    role='ADMIN'
                )

            # Create HOD
            if not User.objects.filter(username='hod').exists():
                User.objects.create_user(
                    username='hod',
                    password='hod123',
                    email='hod@example.com',
                    role='HOD'
                )

        post_migrate.connect(create_default_users, sender=self)
