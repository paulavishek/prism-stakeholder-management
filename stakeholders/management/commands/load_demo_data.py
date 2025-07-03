from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime, timedelta
import random

from stakeholders.models import Stakeholder, Engagement, StakeholderRelationship, DemoSession


class Command(BaseCommand):
    help = 'Load comprehensive demo data for stakeholder management system'

    def add_arguments(self, parser):
        parser.add_argument(
            '--scenario',
            type=str,
            default='standard',
            choices=['standard', 'tech_startup', 'enterprise_project', 'product_launch'],
            help='Demo scenario to load'
        )
        parser.add_argument(
            '--user',
            type=str,
            help='Username to load demo data for (default: create demo user)'
        )

    def handle(self, *args, **options):
        scenario = options['scenario']
        username = options.get('user')

        # Get or create demo user
        if username:
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'User {username} does not exist')
                )
                return
        else:
            user, created = User.objects.get_or_create(
                username='demo',
                defaults={
                    'email': 'demo@example.com',
                    'first_name': 'Demo',
                    'last_name': 'User',
                    'is_active': True,
                }
            )
            if created:
                user.set_password('password')
                user.save()

        # Clear existing demo data for this user
        self.stdout.write('Clearing existing data...')
        Stakeholder.objects.filter(created_by=user).delete()
        Engagement.objects.filter(created_by=user).delete()
        
        # Create or update demo session
        demo_session, _ = DemoSession.objects.get_or_create(
            user=user,
            defaults={'demo_scenario': scenario}
        )
        demo_session.is_demo_mode = True
        demo_session.demo_scenario = scenario
        demo_session.save()

        # Load scenario-specific data
        if scenario == 'tech_startup':
            self.load_tech_startup_data(user)
        elif scenario == 'enterprise_project':
            self.load_enterprise_data(user)
        elif scenario == 'product_launch':
            self.load_product_launch_data(user)
        else:
            self.load_standard_data(user)

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully loaded {scenario} demo data for user {user.username}'
            )
        )

    def load_standard_data(self, user):
        """Load standard demo data showcasing all features"""
        stakeholders_data = [
            # Executive Level
            {
                'name': 'Sarah Chen',
                'title': 'Chief Executive Officer',
                'organization': 'TechCorp Inc.',
                'department': 'Executive',
                'email': 'sarah.chen@techcorp.com',
                'phone': '+1-555-0101',
                'influence': 'very_high',
                'interest': 'high',
                'category': 'internal',
                'description': 'CEO with strong technology background and vision for digital transformation.',
                'ai_generated_insights': 'Highly influential decision-maker who values data-driven insights and innovative solutions. Key to securing executive buy-in for strategic initiatives.'
            },
            {
                'name': 'Michael Rodriguez',
                'title': 'Chief Technology Officer',
                'organization': 'TechCorp Inc.',
                'department': 'Technology',
                'email': 'michael.rodriguez@techcorp.com',
                'phone': '+1-555-0102',
                'influence': 'very_high',
                'interest': 'very_high',
                'category': 'internal',
                'description': 'Technical leader responsible for platform architecture and engineering teams.',
                'ai_generated_insights': 'Strong advocate for technical excellence and scalable solutions. Critical stakeholder for any technology-related decisions and implementations.'
            },
            # Management Level
            {
                'name': 'Jennifer Walsh',
                'title': 'VP Product Management',
                'organization': 'TechCorp Inc.',
                'department': 'Product',
                'email': 'jennifer.walsh@techcorp.com',
                'phone': '+1-555-0103',
                'influence': 'high',
                'interest': 'very_high',
                'category': 'internal',
                'description': 'Product strategy leader with strong market insights and user focus.',
                'ai_generated_insights': 'Customer-centric leader who prioritizes user experience and market fit. Essential for product roadmap alignment and feature prioritization.'
            },
            {
                'name': 'David Kim',
                'title': 'Engineering Manager',
                'organization': 'TechCorp Inc.',
                'department': 'Engineering',
                'email': 'david.kim@techcorp.com',
                'phone': '+1-555-0104',
                'influence': 'high',
                'interest': 'high',
                'category': 'internal',
                'description': 'Leads the core platform engineering team.',
                'ai_generated_insights': 'Practical engineering leader focused on delivery and team productivity. Key implementer of technical solutions and process improvements.'
            },
            # External Stakeholders
            {
                'name': 'Lisa Thompson',
                'title': 'Enterprise Customer Success Manager',
                'organization': 'GlobalCorp Ltd.',
                'department': 'Customer Success',
                'email': 'lisa.thompson@globalcorp.com',
                'phone': '+1-555-0201',
                'influence': 'medium',
                'interest': 'very_high',
                'category': 'customer',
                'description': 'Represents our largest enterprise customer with significant revenue impact.',
                'ai_generated_insights': 'High-value customer advocate who provides valuable feedback on enterprise features. Critical for retention and expansion opportunities.'
            },
            {
                'name': 'Robert Jackson',
                'title': 'Lead Developer',
                'organization': 'Integration Partners LLC',
                'department': 'Development',
                'email': 'robert.jackson@integrationpartners.com',
                'phone': '+1-555-0301',
                'influence': 'medium',
                'interest': 'high',
                'category': 'external',
                'description': 'Technical contact for key integration partner.',
                'ai_generated_insights': 'Technical integration expert who can accelerate or block partnership implementations. Important for ecosystem growth and technical partnerships.'
            },
            # Additional diverse stakeholders
            {
                'name': 'Amanda Foster',
                'title': 'Legal Counsel',
                'organization': 'TechCorp Inc.',
                'department': 'Legal',
                'email': 'amanda.foster@techcorp.com',
                'phone': '+1-555-0105',
                'influence': 'high',
                'interest': 'medium',
                'category': 'internal',
                'description': 'Corporate legal counsel specializing in technology and data privacy.',
                'ai_generated_insights': 'Risk-aware legal expert who ensures compliance and mitigates legal exposure. Critical for privacy, security, and regulatory initiatives.'
            },
            {
                'name': 'Carlos Mendoza',
                'title': 'Security Architect',
                'organization': 'TechCorp Inc.',
                'department': 'Security',
                'email': 'carlos.mendoza@techcorp.com',
                'phone': '+1-555-0106',
                'influence': 'high',
                'interest': 'high',
                'category': 'internal',
                'description': 'Enterprise security architect ensuring platform security and compliance.',
                'ai_generated_insights': 'Security-first mindset with deep expertise in enterprise security frameworks. Essential for security architecture and compliance validation.'
            },
            {
                'name': 'Rachel Green',
                'title': 'UX Research Lead',
                'organization': 'TechCorp Inc.',
                'department': 'Design',
                'email': 'rachel.green@techcorp.com',
                'phone': '+1-555-0107',
                'influence': 'medium',
                'interest': 'very_high',
                'category': 'internal',
                'description': 'User experience researcher focused on customer insights and usability.',
                'ai_generated_insights': 'User-centric researcher who provides valuable insights into customer behavior and needs. Key to ensuring solutions meet real user requirements.'
            },
            {
                'name': 'Kevin O\'Brien',
                'title': 'Sales Director',
                'organization': 'TechCorp Inc.',
                'department': 'Sales',
                'email': 'kevin.obrien@techcorp.com',
                'phone': '+1-555-0108',
                'influence': 'high',
                'interest': 'medium',
                'category': 'internal',
                'description': 'Enterprise sales leader with strong customer relationships.',
                'ai_generated_insights': 'Revenue-focused leader with deep customer relationships. Important for understanding market needs and ensuring solutions support sales objectives.'
            }
        ]

        stakeholders = []
        for data in stakeholders_data:
            stakeholder = Stakeholder.objects.create(created_by=user, **data)
            stakeholders.append(stakeholder)

        # Create diverse engagements
        self.create_sample_engagements(user, stakeholders)
        self.create_sample_relationships(user, stakeholders)

    def load_tech_startup_data(self, user):
        """Load tech startup specific demo data"""
        # Implementation for tech startup scenario
        self.load_standard_data(user)  # For now, use standard data
        # Could customize for startup-specific stakeholders

    def load_enterprise_data(self, user):
        """Load enterprise project specific demo data"""
        # Implementation for enterprise scenario
        self.load_standard_data(user)  # For now, use standard data
        # Could customize for enterprise-specific stakeholders

    def load_product_launch_data(self, user):
        """Load product launch specific demo data"""
        # Implementation for product launch scenario
        self.load_standard_data(user)  # For now, use standard data
        # Could customize for product launch-specific stakeholders

    def create_sample_engagements(self, user, stakeholders):
        """Create realistic sample engagements"""
        engagement_templates = [
            {
                'title': 'Q4 Strategic Planning Session',
                'type': 'meeting',
                'status': 'completed',
                'description': 'Quarterly strategic planning and goal setting for the product roadmap.',
                'objectives': 'Define Q4 priorities, align on resource allocation, and establish success metrics.',
                'outcomes': 'Agreed on 3 key initiatives for Q4 with clear ownership and timelines.',
                'action_items': '1. Draft detailed project plans by end of week\n2. Schedule weekly check-ins\n3. Prepare resource allocation proposal',
                'sentiment': 'positive',
                'effectiveness_rating': 4,
                'ai_summary': 'Productive strategic session with clear outcomes and strong stakeholder alignment.',
                'ai_action_items': 'Follow up on resource allocation proposal and establish weekly tracking cadence.',
                'ai_sentiment_analysis': 'Positive engagement with high stakeholder satisfaction and clear next steps.',
                'duration_minutes': 120,
                'days_ago': 15
            },
            {
                'title': 'Technical Architecture Review',
                'type': 'presentation',
                'status': 'completed',
                'description': 'Presentation of proposed technical architecture for the new platform.',
                'objectives': 'Get architectural approval and address technical concerns.',
                'outcomes': 'Architecture approved with minor modifications requested.',
                'action_items': '1. Update architecture docs with feedback\n2. Schedule implementation kickoff\n3. Prepare detailed timeline',
                'sentiment': 'positive',
                'effectiveness_rating': 5,
                'ai_summary': 'Successful architecture review with stakeholder buy-in and clear implementation path.',
                'ai_action_items': 'Incorporate feedback into final architecture documentation and begin implementation planning.',
                'ai_sentiment_analysis': 'Highly positive response with strong technical confidence and clear approval.',
                'duration_minutes': 90,
                'days_ago': 8
            },
            {
                'title': 'Customer Feedback Analysis',
                'type': 'workshop',
                'status': 'completed',
                'description': 'Collaborative session to analyze recent customer feedback and identify improvement opportunities.',
                'objectives': 'Understand customer pain points and prioritize UX improvements.',
                'outcomes': 'Identified top 5 UX issues and created improvement roadmap.',
                'action_items': '1. Create user stories for top issues\n2. Estimate effort for each improvement\n3. Present findings to product team',
                'sentiment': 'neutral',
                'effectiveness_rating': 3,
                'ai_summary': 'Informative session that highlighted important customer concerns requiring attention.',
                'ai_action_items': 'Develop detailed improvement plan and prioritize based on customer impact.',
                'ai_sentiment_analysis': 'Neutral sentiment with some concerns about implementation complexity.',
                'duration_minutes': 180,
                'days_ago': 12
            },
            {
                'title': 'Security Compliance Review',
                'type': 'meeting',
                'status': 'completed',
                'description': 'Review of security measures and compliance requirements for enterprise deployment.',
                'objectives': 'Ensure platform meets enterprise security standards.',
                'outcomes': 'Identified 3 security enhancements needed for enterprise readiness.',
                'action_items': '1. Implement additional encryption\n2. Add audit logging\n3. Complete penetration testing',
                'sentiment': 'negative',
                'effectiveness_rating': 2,
                'ai_summary': 'Challenging session revealing significant security gaps requiring immediate attention.',
                'ai_action_items': 'Prioritize security enhancements and establish timeline for enterprise compliance.',
                'ai_sentiment_analysis': 'Concerned sentiment due to security gaps, but constructive path forward identified.',
                'duration_minutes': 75,
                'days_ago': 5
            },
            # Future engagements
            {
                'title': 'Product Demo for Enterprise Customer',
                'type': 'presentation',
                'status': 'planned',
                'description': 'Demonstration of new features for key enterprise customer.',
                'objectives': 'Showcase recent improvements and gather feedback for future development.',
                'outcomes': '',
                'action_items': '',
                'sentiment': '',
                'effectiveness_rating': None,
                'ai_summary': '',
                'ai_action_items': '',
                'ai_sentiment_analysis': '',
                'duration_minutes': 60,
                'days_ahead': 3
            },
            {
                'title': 'Monthly Team Sync',
                'type': 'meeting',
                'status': 'planned',
                'description': 'Regular monthly sync with engineering team on progress and blockers.',
                'objectives': 'Review sprint progress, address blockers, and plan next iteration.',
                'outcomes': '',
                'action_items': '',
                'sentiment': '',
                'effectiveness_rating': None,
                'ai_summary': '',
                'ai_action_items': '',
                'ai_sentiment_analysis': '',
                'duration_minutes': 45,
                'days_ahead': 7
            },
            {
                'title': 'Executive Quarterly Review',
                'type': 'meeting',
                'status': 'planned',
                'description': 'Quarterly business review with executive team.',
                'objectives': 'Present Q3 results and Q4 planning.',
                'outcomes': '',
                'action_items': '',
                'sentiment': '',
                'effectiveness_rating': None,
                'ai_summary': '',
                'ai_action_items': '',
                'ai_sentiment_analysis': '',
                'duration_minutes': 90,
                'days_ahead': 14
            }
        ]

        for template in engagement_templates:
            # Assign to random stakeholder
            stakeholder = random.choice(stakeholders)
            
            # Calculate date
            if 'days_ago' in template:
                scheduled_date = timezone.now() - timedelta(days=template['days_ago'])
            else:
                scheduled_date = timezone.now() + timedelta(days=template['days_ahead'])
            
            engagement_data = template.copy()
            engagement_data.pop('days_ago', None)
            engagement_data.pop('days_ahead', None)
            
            Engagement.objects.create(
                stakeholder=stakeholder,
                created_by=user,
                scheduled_date=scheduled_date,
                **engagement_data
            )

    def create_sample_relationships(self, user, stakeholders):
        """Create sample stakeholder relationships"""
        if len(stakeholders) < 4:
            return

        # Create some realistic relationships
        relationships = [
            (0, 1, 'collaborates'),  # CEO collaborates with CTO
            (1, 3, 'manages'),       # CTO manages Engineering Manager
            (2, 8, 'collaborates'),  # VP Product collaborates with UX Research
            (0, 2, 'collaborates'),  # CEO collaborates with VP Product
            (4, 2, 'influences'),    # Customer influences VP Product
        ]

        for from_idx, to_idx, rel_type in relationships:
            if from_idx < len(stakeholders) and to_idx < len(stakeholders):
                StakeholderRelationship.objects.create(
                    from_stakeholder=stakeholders[from_idx],
                    to_stakeholder=stakeholders[to_idx],
                    relationship_type=rel_type,
                    strength='strong',
                    created_by=user
                )
