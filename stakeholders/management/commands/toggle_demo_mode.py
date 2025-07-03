from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from stakeholders.models import DemoSession


class Command(BaseCommand):
    help = 'Toggle demo mode for a user'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=str,
            required=True,
            help='Username to toggle demo mode for'
        )
        parser.add_argument(
            '--scenario',
            type=str,
            default='standard',
            choices=['standard', 'tech_startup', 'enterprise_project', 'product_launch'],
            help='Demo scenario (only used when enabling demo mode)'
        )

    def handle(self, *args, **options):
        username = options['user']
        scenario = options['scenario']

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'User {username} does not exist')
            )
            return

        # Get or create demo session
        demo_session, created = DemoSession.objects.get_or_create(
            user=user,
            defaults={'demo_scenario': scenario}
        )

        if demo_session.is_demo_mode:
            # Disable demo mode
            demo_session.is_demo_mode = False
            demo_session.save()
            
            self.stdout.write(
                self.style.SUCCESS(f'Demo mode disabled for user {username}')
            )
            
            # Ask if user wants to clear demo data
            clear_data = input('Clear demo data as well? (yes/no): ')
            if clear_data.lower() in ['yes', 'y']:
                from django.core.management import call_command
                call_command('clear_demo_data', user=username, confirm=True)
        else:
            # Enable demo mode
            demo_session.is_demo_mode = True
            demo_session.demo_scenario = scenario
            demo_session.save()
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'Demo mode enabled for user {username} with scenario: {scenario}'
                )
            )
            
            # Ask if user wants to load demo data
            load_data = input('Load demo data? (yes/no): ')
            if load_data.lower() in ['yes', 'y']:
                from django.core.management import call_command
                call_command('load_demo_data', user=username, scenario=scenario)
