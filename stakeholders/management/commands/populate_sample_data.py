import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from stakeholders.models import Stakeholder, Engagement, StakeholderRelationship


class Command(BaseCommand):
    help = 'Populate the database with sample stakeholder data for testing'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before populating',
        )
        parser.add_argument(
            '--user',
            type=str,
            default='admin',
            help='Username to assign data to (default: admin)',
        )

    def handle(self, *args, **options):
        username = options['user']
        
        # Get or create user
        try:
            user = User.objects.get(username=username)
            self.stdout.write(f"Using existing user: {username}")
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=username,
                email=f'{username}@example.com',
                password='password123'
            )
            self.stdout.write(f"Created new user: {username}")

        if options['clear']:
            self.stdout.write("Clearing existing data...")
            Stakeholder.objects.filter(created_by=user).delete()
            self.stdout.write("Existing data cleared.")

        self.stdout.write("Creating sample stakeholders...")
        stakeholders = self.create_stakeholders(user)
        
        self.stdout.write("Creating sample engagements...")
        self.create_engagements(user, stakeholders)
        
        self.stdout.write("Creating stakeholder relationships...")
        self.create_relationships(user, stakeholders)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully populated database with sample data for user: {username}'
            )
        )

    def create_stakeholders(self, user):
        """Create sample stakeholders across different categories"""
        stakeholder_data = [
            # Executive Leadership
            {
                'name': 'Sarah Chen',
                'title': 'Chief Executive Officer',
                'organization': 'TechCorp Solutions',
                'department': 'Executive',
                'email': 'sarah.chen@techcorp.com',
                'phone': '+1-555-0101',
                'influence': 'very_high',
                'interest': 'high',
                'category': 'internal',
                'description': 'CEO with strong technology background and strategic vision for digital transformation.',
                'notes': 'Key decision maker for all major initiatives. Prefers data-driven presentations.'
            },
            {
                'name': 'Michael Rodriguez',
                'title': 'Chief Technology Officer',
                'organization': 'TechCorp Solutions',
                'department': 'Technology',
                'email': 'michael.rodriguez@techcorp.com',
                'phone': '+1-555-0102',
                'influence': 'very_high',
                'interest': 'very_high',
                'category': 'internal',
                'description': 'Experienced CTO leading digital transformation and cloud migration initiatives.',
                'notes': 'Strong advocate for innovation and automation. Technical expert with business acumen.'
            },
            {
                'name': 'Jennifer Thompson',
                'title': 'Chief Financial Officer',
                'organization': 'TechCorp Solutions',
                'department': 'Finance',
                'email': 'jennifer.thompson@techcorp.com',
                'phone': '+1-555-0103',
                'influence': 'very_high',
                'interest': 'medium',
                'category': 'internal',
                'description': 'CFO focused on cost optimization and ROI measurement for technology investments.',
                'notes': 'Requires detailed financial justification for all projects. Budget-conscious but supportive.'
            },
            
            # Department Heads
            {
                'name': 'David Park',
                'title': 'VP of Engineering',
                'organization': 'TechCorp Solutions',
                'department': 'Engineering',
                'email': 'david.park@techcorp.com',
                'phone': '+1-555-0201',
                'influence': 'high',
                'interest': 'very_high',
                'category': 'internal',
                'description': 'Engineering leader with 15+ years experience in software development and team management.',
                'notes': 'Passionate about developer experience and code quality. Advocates for technical excellence.'
            },
            {
                'name': 'Lisa Wang',
                'title': 'VP of Marketing',
                'organization': 'TechCorp Solutions',
                'department': 'Marketing',
                'email': 'lisa.wang@techcorp.com',
                'phone': '+1-555-0202',
                'influence': 'high',
                'interest': 'medium',
                'category': 'internal',
                'description': 'Marketing executive focused on brand development and customer acquisition strategies.',
                'notes': 'Interested in customer-facing technology improvements and analytics capabilities.'
            },
            {
                'name': 'Robert Johnson',
                'title': 'VP of Sales',
                'organization': 'TechCorp Solutions',
                'department': 'Sales',
                'email': 'robert.johnson@techcorp.com',
                'phone': '+1-555-0203',
                'influence': 'high',
                'interest': 'high',
                'category': 'internal',
                'description': 'Sales leader with strong customer relationships and market insights.',
                'notes': 'Focuses on solutions that improve customer satisfaction and sales efficiency.'
            },
            
            # Team Leads
            {
                'name': 'Amanda Foster',
                'title': 'Senior Product Manager',
                'organization': 'TechCorp Solutions',
                'department': 'Product',
                'email': 'amanda.foster@techcorp.com',
                'phone': '+1-555-0301',
                'influence': 'medium',
                'interest': 'very_high',
                'category': 'internal',
                'description': 'Product manager with expertise in user experience and agile methodologies.',
                'notes': 'Champion of user-centered design and data-driven product decisions.'
            },
            {
                'name': 'James Mitchell',
                'title': 'DevOps Lead',
                'organization': 'TechCorp Solutions',
                'department': 'Engineering',
                'email': 'james.mitchell@techcorp.com',
                'phone': '+1-555-0302',
                'influence': 'medium',
                'interest': 'very_high',
                'category': 'internal',
                'description': 'DevOps expert responsible for infrastructure automation and deployment pipelines.',
                'notes': 'Focused on reliability, scalability, and security of systems.'
            },
            
            # External Stakeholders - Customers
            {
                'name': 'Patricia Williams',
                'title': 'IT Director',
                'organization': 'Global Manufacturing Inc',
                'department': 'Information Technology',
                'email': 'patricia.williams@globalmanuf.com',
                'phone': '+1-555-1001',
                'influence': 'high',
                'interest': 'high',
                'category': 'customer',
                'description': 'IT Director at major manufacturing client, focused on operational efficiency.',
                'notes': 'Key customer stakeholder for manufacturing solutions. Values reliability and integration.'
            },
            {
                'name': 'Thomas Brown',
                'title': 'CTO',
                'organization': 'FinanceFirst Bank',
                'department': 'Technology',
                'email': 'thomas.brown@financefirst.com',
                'phone': '+1-555-1002',
                'influence': 'very_high',
                'interest': 'high',
                'category': 'customer',
                'description': 'CTO at major financial client, concerned with security and compliance.',
                'notes': 'Extremely security-conscious. Requires extensive compliance documentation.'
            },
            
            # External Stakeholders - Partners
            {
                'name': 'Maria Garcia',
                'title': 'Partnership Manager',
                'organization': 'CloudTech Partners',
                'department': 'Business Development',
                'email': 'maria.garcia@cloudtech.com',
                'phone': '+1-555-2001',
                'influence': 'medium',
                'interest': 'medium',
                'category': 'supplier',
                'description': 'Partnership manager for key cloud infrastructure provider.',
                'notes': 'Facilitates integration with cloud services. Helpful with technical support.'
            },
            {
                'name': 'Andrew Davis',
                'title': 'Account Executive',
                'organization': 'Security Solutions Pro',
                'department': 'Sales',
                'email': 'andrew.davis@securitypro.com',
                'phone': '+1-555-2002',
                'influence': 'medium',
                'interest': 'medium',
                'category': 'supplier',
                'description': 'Account executive for cybersecurity solutions and consulting services.',
                'notes': 'Provides security expertise and compliance guidance. Responsive to technical needs.'
            },
            
            # Investors
            {
                'name': 'Victoria Zhang',
                'title': 'Managing Partner',
                'organization': 'Growth Capital Ventures',
                'department': 'Investment',
                'email': 'victoria.zhang@growthcapital.com',
                'phone': '+1-555-3001',
                'influence': 'very_high',
                'interest': 'medium',
                'category': 'investor',
                'description': 'Managing partner at venture capital firm, board member.',
                'notes': 'Focused on growth metrics and market expansion. Strategic advisor.'
            },
            
            # Regulators
            {
                'name': 'Charles Wilson',
                'title': 'Senior Compliance Officer',
                'organization': 'Industry Regulatory Board',
                'department': 'Compliance',
                'email': 'charles.wilson@industryboard.gov',
                'phone': '+1-555-4001',
                'influence': 'high',
                'interest': 'low',
                'category': 'regulator',
                'description': 'Senior compliance officer overseeing industry data protection regulations.',
                'notes': 'Ensures compliance with data protection and privacy regulations.'
            },
            
            # Community
            {
                'name': 'Rebecca Martinez',
                'title': 'Community Relations Director',
                'organization': 'Local Business Association',
                'department': 'Community Outreach',
                'email': 'rebecca.martinez@localbusiness.org',
                'phone': '+1-555-5001',
                'influence': 'low',
                'interest': 'medium',
                'category': 'community',
                'description': 'Community relations director focused on local business development.',
                'notes': 'Interested in community impact and local job creation initiatives.'
            }
        ]
        
        stakeholders = []
        for data in stakeholder_data:
            stakeholder = Stakeholder.objects.create(
                created_by=user,
                **data
            )
            stakeholders.append(stakeholder)
            self.stdout.write(f"Created stakeholder: {stakeholder.name}")
        
        return stakeholders

    def create_engagements(self, user, stakeholders):
        """Create sample engagements for stakeholders"""
        engagement_templates = [
            {
                'title': 'Quarterly Business Review',
                'type': 'meeting',
                'duration_minutes': 90,
                'objectives': 'Review quarterly performance metrics and discuss strategic initiatives for next quarter.',
                'description': 'Comprehensive review of business performance including financial metrics, operational efficiency, and strategic goal progress.',
            },
            {
                'title': 'Technical Architecture Discussion',
                'type': 'meeting',
                'duration_minutes': 60,
                'objectives': 'Discuss technical architecture decisions and implementation roadmap.',
                'description': 'Deep dive into technical architecture choices, scalability considerations, and implementation timeline.',
            },
            {
                'title': 'Budget Planning Session',
                'type': 'meeting',
                'duration_minutes': 120,
                'objectives': 'Plan budget allocation for upcoming fiscal year technology investments.',
                'description': 'Detailed budget planning session covering technology investments, resource allocation, and ROI projections.',
            },
            {
                'title': 'Customer Feedback Review',
                'type': 'presentation',
                'duration_minutes': 45,
                'objectives': 'Present customer feedback analysis and proposed improvement actions.',
                'description': 'Presentation of customer satisfaction metrics, feedback themes, and proposed action items.',
            },
            {
                'title': 'Security Compliance Check',
                'type': 'interview',
                'duration_minutes': 30,
                'objectives': 'Review current security posture and compliance requirements.',
                'description': 'Security assessment interview covering current policies, procedures, and compliance status.',
            },
            {
                'title': 'Product Roadmap Discussion',
                'type': 'workshop',
                'duration_minutes': 180,
                'objectives': 'Collaborate on product roadmap priorities and feature planning.',
                'description': 'Interactive workshop session for product roadmap planning and feature prioritization.',
            },
            {
                'title': 'Partnership Strategy Meeting',
                'type': 'meeting',
                'duration_minutes': 60,
                'objectives': 'Discuss partnership opportunities and strategic alliances.',
                'description': 'Strategic discussion about potential partnerships and collaboration opportunities.',
            },
            {
                'title': 'Weekly Status Update',
                'type': 'email',
                'duration_minutes': 15,
                'objectives': 'Provide weekly progress update on key initiatives.',
                'description': 'Regular weekly communication covering project status, milestones, and upcoming deliverables.',
            }
        ]
        
        # Create engagements for each stakeholder
        for stakeholder in stakeholders:
            # Create 2-5 engagements per stakeholder
            num_engagements = random.randint(2, 5)
            
            for _ in range(num_engagements):
                template = random.choice(engagement_templates)
                
                # Random date within last 90 days or next 30 days
                days_offset = random.randint(-90, 30)
                scheduled_date = timezone.now() + timedelta(days=days_offset)
                
                # Determine status based on date
                if days_offset < -7:
                    status = 'completed'
                    sentiment = random.choice(['positive', 'neutral', 'negative'])
                    effectiveness_rating = random.randint(2, 5)
                    outcomes = self.generate_outcomes(sentiment)
                    action_items = self.generate_action_items()
                elif days_offset < 0:
                    status = random.choice(['completed', 'completed', 'completed', 'cancelled'])
                    sentiment = random.choice(['positive', 'neutral', 'negative']) if status == 'completed' else ''
                    effectiveness_rating = random.randint(2, 5) if status == 'completed' else None
                    outcomes = self.generate_outcomes(sentiment) if status == 'completed' else ''
                    action_items = self.generate_action_items() if status == 'completed' else ''
                else:
                    status = 'planned'
                    sentiment = ''
                    effectiveness_rating = None
                    outcomes = ''
                    action_items = ''
                
                engagement = Engagement.objects.create(
                    stakeholder=stakeholder,
                    title=template['title'],
                    type=template['type'],
                    status=status,
                    scheduled_date=scheduled_date,
                    duration_minutes=template['duration_minutes'],
                    description=template['description'],
                    objectives=template['objectives'],
                    outcomes=outcomes,
                    action_items=action_items,
                    sentiment=sentiment,
                    effectiveness_rating=effectiveness_rating,
                    created_by=user
                )
                
                self.stdout.write(f"Created engagement: {engagement.title} for {stakeholder.name}")

    def create_relationships(self, user, stakeholders):
        """Create sample relationships between stakeholders"""
        # Create some realistic organizational relationships
        relationships_data = [
            # CEO relationships
            ('Sarah Chen', 'Michael Rodriguez', 'manages'),
            ('Sarah Chen', 'Jennifer Thompson', 'manages'),
            ('Sarah Chen', 'Victoria Zhang', 'reports_to'),
            
            # Department head relationships
            ('Michael Rodriguez', 'David Park', 'manages'),
            ('Michael Rodriguez', 'James Mitchell', 'collaborates'),
            ('Jennifer Thompson', 'Lisa Wang', 'collaborates'),
            ('Jennifer Thompson', 'Robert Johnson', 'collaborates'),
            
            # Team relationships
            ('David Park', 'Amanda Foster', 'collaborates'),
            ('David Park', 'James Mitchell', 'manages'),
            ('Amanda Foster', 'Lisa Wang', 'collaborates'),
            ('Robert Johnson', 'Patricia Williams', 'supports'),
            ('Robert Johnson', 'Thomas Brown', 'supports'),
            
            # External relationships
            ('Michael Rodriguez', 'Maria Garcia', 'collaborates'),
            ('James Mitchell', 'Andrew Davis', 'depends_on'),
            ('Charles Wilson', 'Michael Rodriguez', 'influences'),
            
            # Customer relationships
            ('Patricia Williams', 'David Park', 'depends_on'),
            ('Thomas Brown', 'Michael Rodriguez', 'depends_on'),
        ]
        
        # Convert names to stakeholder objects and create relationships
        stakeholder_dict = {s.name: s for s in stakeholders}
        
        for from_name, to_name, rel_type in relationships_data:
            if from_name in stakeholder_dict and to_name in stakeholder_dict:
                from_stakeholder = stakeholder_dict[from_name]
                to_stakeholder = stakeholder_dict[to_name]
                
                # Avoid duplicate relationships
                existing = StakeholderRelationship.objects.filter(
                    from_stakeholder=from_stakeholder,
                    to_stakeholder=to_stakeholder,
                    relationship_type=rel_type
                ).exists()
                
                if not existing:
                    strength = random.choice(['moderate', 'strong', 'strong'])  # Bias toward stronger relationships
                    
                    StakeholderRelationship.objects.create(
                        from_stakeholder=from_stakeholder,
                        to_stakeholder=to_stakeholder,
                        relationship_type=rel_type,
                        strength=strength,
                        description=f"{rel_type.replace('_', ' ').title()} relationship in organizational context.",
                        created_by=user
                    )
                    
                    self.stdout.write(f"Created relationship: {from_name} {rel_type} {to_name}")

    def generate_outcomes(self, sentiment):
        """Generate realistic outcomes based on sentiment"""
        positive_outcomes = [
            "Strong alignment achieved on project objectives and timeline.",
            "Stakeholder expressed high satisfaction with current progress.",
            "Received approval for next phase implementation.",
            "Positive feedback on team performance and deliverables.",
            "Stakeholder committed additional resources to support initiative."
        ]
        
        neutral_outcomes = [
            "Discussion covered key topics, follow-up actions identified.",
            "Information shared, stakeholder will review and provide feedback.",
            "Status update provided, no major concerns raised.",
            "Routine check-in completed, project on track.",
            "Questions answered, stakeholder satisfied with responses."
        ]
        
        negative_outcomes = [
            "Stakeholder expressed concerns about project timeline.",
            "Budget constraints may impact project scope.",
            "Technical challenges identified, additional analysis needed.",
            "Stakeholder requested changes to current approach.",
            "Delays in decision-making process, follow-up required."
        ]
        
        if sentiment == 'positive':
            return random.choice(positive_outcomes)
        elif sentiment == 'negative':
            return random.choice(negative_outcomes)
        else:
            return random.choice(neutral_outcomes)

    def generate_action_items(self):
        """Generate realistic action items"""
        action_items = [
            "Follow up with technical team on implementation details",
            "Prepare detailed cost analysis for next review meeting",
            "Schedule follow-up session with key stakeholders",
            "Update project documentation and share with team",
            "Coordinate with external vendors on timeline",
            "Prepare presentation for executive review",
            "Review and update risk assessment document",
            "Organize training session for end users",
            "Conduct impact analysis on proposed changes",
            "Schedule technical review with architecture team"
        ]
        
        # Return 1-3 random action items
        num_items = random.randint(1, 3)
        selected_items = random.sample(action_items, num_items)
        return "\n".join([f"• {item}" for item in selected_items])
