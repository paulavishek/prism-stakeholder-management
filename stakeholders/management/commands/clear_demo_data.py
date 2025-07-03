from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from stakeholders.models import Stakeholder, Engagement, StakeholderRelationship, DemoSession


class Command(BaseCommand):
    help = 'Clear demo data from the stakeholder management system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user',
            type=str,
            help='Username to clear demo data for (default: all demo users)'
        )
        parser.add_argument(
            '--confirm',
            action='store_true',
            help='Confirm deletion without prompting'
        )

    def handle(self, *args, **options):
        username = options.get('user')
        confirm = options.get('confirm')

        if username:
            try:
                users = [User.objects.get(username=username)]
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'User {username} does not exist')
                )
                return
        else:
            # Get all users with demo sessions
            users = User.objects.filter(demo_session__is_demo_mode=True)

        if not users:
            self.stdout.write(
                self.style.WARNING('No demo users found')
            )
            return

        # Confirm deletion
        if not confirm:
            user_list = ', '.join([user.username for user in users])
            confirm_msg = f"This will delete ALL data for users: {user_list}. Are you sure? (yes/no): "
            confirmation = input(confirm_msg)
            if confirmation.lower() not in ['yes', 'y']:
                self.stdout.write('Operation cancelled')
                return

        total_deleted = {
            'stakeholders': 0,
            'engagements': 0,
            'relationships': 0,
            'demo_sessions': 0
        }

        for user in users:
            # Count before deletion
            stakeholder_count = Stakeholder.objects.filter(created_by=user).count()
            engagement_count = Engagement.objects.filter(created_by=user).count()
            relationship_count = StakeholderRelationship.objects.filter(created_by=user).count()
            
            # Delete data
            Stakeholder.objects.filter(created_by=user).delete()
            Engagement.objects.filter(created_by=user).delete()
            StakeholderRelationship.objects.filter(created_by=user).delete()
            
            # Update demo session
            try:
                demo_session = user.demo_session
                demo_session.is_demo_mode = False
                demo_session.save()
                total_deleted['demo_sessions'] += 1
            except DemoSession.DoesNotExist:
                pass

            # Update totals
            total_deleted['stakeholders'] += stakeholder_count
            total_deleted['engagements'] += engagement_count
            total_deleted['relationships'] += relationship_count

            self.stdout.write(
                f'Cleared data for user {user.username}: '
                f'{stakeholder_count} stakeholders, '
                f'{engagement_count} engagements, '
                f'{relationship_count} relationships'
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully cleared demo data:\n'
                f'- {total_deleted["stakeholders"]} stakeholders\n'
                f'- {total_deleted["engagements"]} engagements\n'
                f'- {total_deleted["relationships"]} relationships\n'
                f'- {total_deleted["demo_sessions"]} demo sessions updated'
            )
        )
