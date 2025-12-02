"""
Custom createsuperuser command that sets role to 'admin'
"""
from django.contrib.auth.management.commands import createsuperuser
from django.core.management import CommandError


class Command(createsuperuser.Command):
    help = 'Create a superuser with admin role'

    def handle(self, *args, **options):
        # Store the username before calling parent
        database = options.get('database')
        username = options.get(self.UserModel.USERNAME_FIELD)

        # Call parent's handle to create the user
        super().handle(*args, **options)

        # If username wasn't in options, get the last created superuser
        UserModel = self.UserModel
        if not username:
            # Get the most recently created superuser
            user = UserModel._default_manager.db_manager(database).filter(
                is_superuser=True
            ).order_by('-date_joined').first()
        else:
            user = UserModel._default_manager.db_manager(database).get(**{
                UserModel.USERNAME_FIELD: username
            })

        if user:
            user.role = 'admin'
            user.is_onboarded = True  # Admins don't need onboarding
            user.save()

            self.stdout.write(self.style.SUCCESS(
                f'Successfully set role to "admin" for user "{user.username}"'
            ))
