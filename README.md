# Prism: A Multi-faceted Stakeholder Management Tool

A comprehensive Django-based web application that refracts complex stakeholder relationships into clear, actionable insights through multiple analytical perspectives, enhanced with AI-powered intelligence using Google's Gemini API.

## 🎬 Quick Demo

**Try it instantly**: Visit the deployed application and use these credentials:
- **Username**: `demo`
- **Password**: `password`

**Features showcased in demo**:
- ✅ AI Integration with Google Gemini
- ✅ Interactive Data Visualizations  
- ✅ Responsive Design with Modern UI
- ✅ One-click demo data loading/clearing
- ✅ Power-Interest stakeholder mapping
- ✅ Comprehensive engagement tracking

## � Why "Prism"? - Multi-Faceted Analysis

Like a prism refracts light into its component colors, **Prism** breaks down complex stakeholder relationships into clear, actionable insights through multiple analytical perspectives:

### 📊 Multiple Analytical Facets
- **Power/Interest Matrix**: Strategic stakeholder positioning
- **AI-Powered Insights**: Intelligent analysis and recommendations  
- **Relationship Mapping**: Network visualization and connections
- **Engagement Analytics**: Temporal interaction tracking
- **Sentiment Analysis**: Emotional intelligence in communications
- **Data Visualization**: Multi-dimensional chart representations

### 🎭 Scenario Versatility
- **Tech Startup**: Investor and team stakeholder management
- **Enterprise Projects**: Large-scale initiative coordination
- **Product Launches**: Campaign and market stakeholder tracking
- **General Business**: Universal stakeholder relationship management

### 🎯 Dimensional Analysis
- **Influence Spectrum**: Low → Medium → High → Very High
- **Interest Levels**: Stakeholder engagement measurement
- **Priority Scoring**: Comprehensive 16-point ranking system
- **Category Classification**: Organized stakeholder grouping
- **Engagement Types**: Meetings, calls, emails, presentations

## �🚀 Features

### 🎯 Demo Mode (New!)
- **One-Click Demo Data**: Instantly populate the database with realistic sample data
- **Multiple Scenarios**: Choose from Standard, Tech Startup, Enterprise Project, or Product Launch scenarios
- **Easy Cleanup**: Clear all data with a single click
- **Demo Report Export**: Generate downloadable reports showcasing application capabilities
- **Visual Demo Indicators**: Clear banners and badges showing demo mode status

### Core Features
- **User Authentication**: Secure login and user profile management
- **Stakeholder Management**: Add, edit, view, and delete stakeholders with detailed profiling
- **Engagement Tracking**: Record and monitor interactions with stakeholders
- **Interactive Dashboard**: Visualize stakeholder data with charts and analytics
- **Power/Interest Grid**: Interactive stakeholder mapping with hover effects and tooltips
- **Responsive Design**: Built with Bootstrap 5 for seamless experience across devices

### 🤖 AI-Powered Features (Gemini Integration)
- **Smart Content Generation**: AI-generated stakeholder profiles and insights
- **AI-Powered Profile Completion**: Enhance stakeholder profiles with AI suggestions
- **Smart Communication Drafting**: Generate personalized emails and messages
- **Automated Meeting Summary Generation**: Extract key points and action items
- **Contextual Recommendations**: AI-driven engagement strategies and next steps
- **Sentiment Analysis**: Analyze stakeholder communications for sentiment

## 🛠️ Technology Stack

- **Backend**: Django 5.2.3, Python 3.12+
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (development), PostgreSQL (production ready)
- **AI Integration**: Google Gemini API (gemini-1.5-flash)
- **Charts**: Chart.js for data visualization
- **Icons**: Bootstrap Icons

## 📋 Prerequisites

- Python 3.12 or higher
- Google Gemini API key
- Git (for version control)

## 🔧 Installation & Setup

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd "Stakeholder Management"
```

### 2. Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate  # On Windows
source venv/bin/activate  # On macOS/Linux
```

### 3. Install Dependencies
```bash
pip install django python-dotenv google-generativeai requests
```

### 4. Environment Configuration
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
GEMINI_API_KEY=your-gemini-api-key-here
```

### 5. Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### 6. Run the Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

## 🎯 Usage Guide

### Demo Mode Management

**For End Users:**
- Visit the dashboard to see demo mode banner when active
- Use "Load Demo Data" button to populate with sample stakeholders and engagements
- Choose from different scenarios (Standard, Tech Startup, Enterprise, Product Launch)
- Export demo reports to showcase application capabilities
- Clear all data with one click when done testing

**For Developers:**

```bash
# Load demo data (creates demo user if needed)
python manage.py load_demo_data --scenario=standard

# Load for specific user
python manage.py load_demo_data --user=yourusername --scenario=tech_startup

# Clear demo data
python manage.py clear_demo_data --user=demo --confirm

# Toggle demo mode
python manage.py toggle_demo_mode --user=demo --scenario=enterprise_project
```

**Available Scenarios:**
- `standard`: General stakeholder management demonstration
- `tech_startup`: Technology company stakeholder scenario
- `enterprise_project`: Large enterprise project stakeholders
- `product_launch`: Product launch campaign stakeholders

### Getting Started
1. **Login**: Use the credentials you created during setup
2. **Add Stakeholders**: Navigate to Stakeholders > Add New
3. **Enable AI Insights**: Check the "Generate AI Insights" option when creating stakeholders
4. **Schedule Engagements**: Create meetings and interactions
5. **View Dashboard**: Analyze stakeholder data and relationships

### Interactive Power/Interest Grid
- **Hover Effects**: Move your mouse over stakeholder points to see detailed tooltips
- **Visual Mapping**: Stakeholders are positioned based on their influence and interest levels
- **Quadrant Analysis**: 
  - **Manage Closely**: High Power, High Interest
  - **Keep Satisfied**: High Power, Low Interest  
  - **Keep Informed**: Low Power, High Interest
  - **Monitor**: Low Power, Low Interest

### AI Features
- **Smart Profiling**: AI analyzes basic stakeholder info to generate comprehensive profiles
- **Communication Drafting**: Generate personalized emails based on stakeholder characteristics
- **Meeting Summaries**: Upload meeting notes to get structured summaries and action items
- **Engagement Strategies**: Get AI recommendations for optimal stakeholder engagement

## 📊 Dashboard Features

### Metrics Overview
- Total stakeholders count
- Total engagements tracked
- High-priority stakeholders
- Upcoming meetings

### Visualizations
- **Interactive Stakeholder Grid**: Power/Interest mapping with hover tooltips
- **Category Distribution**: Pie chart of stakeholder categories
- **Engagement Types**: Bar chart of engagement frequency
- **Recent Activity**: Latest stakeholder additions and upcoming meetings

## 🔐 Security Features

- Django's built-in authentication system
- CSRF protection
- Secure password handling
- Environment variable configuration
- User-specific data isolation

## 🎨 User Experience Enhancements

### Interactive Elements
- **Hover Effects**: Stakeholder cards and grid points respond to mouse interaction
- **Tooltips**: Detailed information on hover without navigation
- **Smooth Animations**: CSS transitions for better visual feedback
- **Responsive Grids**: Mobile-friendly layouts

### AI Integration UX
- **Loading States**: Visual feedback during AI processing
- **Progressive Enhancement**: Works with or without AI features
- **Error Handling**: Graceful degradation when AI services are unavailable
- **Copy to Clipboard**: Easy sharing of AI-generated content

## 🚀 Deployment

### Environment Variables for Production
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com
GEMINI_API_KEY=your-gemini-api-key
DATABASE_URL=postgresql://user:pass@localhost/dbname
```

### Static Files
```bash
python manage.py collectstatic
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 API Documentation

### AI Service Methods
- `generate_stakeholder_profile(basic_info)`: Generate comprehensive stakeholder analysis
- `draft_communication(stakeholder_info, type, purpose)`: Create personalized communications
- `summarize_meeting(notes, stakeholder_info)`: Extract insights from meeting notes
- `analyze_stakeholder_sentiment(text)`: Determine sentiment from communications
- `suggest_engagement_strategy(stakeholder_data)`: Recommend engagement approaches

## 🐛 Troubleshooting

### Common Issues
1. **AI Features Not Working**: Check your `GEMINI_API_KEY` in `.env`
2. **Static Files Missing**: Run `python manage.py collectstatic`
3. **Database Errors**: Ensure migrations are applied with `python manage.py migrate`
4. **Login Issues**: Create a superuser with `python manage.py createsuperuser`

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Django framework for robust web development
- Google Gemini API for AI capabilities
- Bootstrap for responsive UI components
- Chart.js for data visualization
- Bootstrap Icons for consistent iconography

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check the troubleshooting section
- Review the Django documentation for framework-specific questions

---

**Built with ❤️ using Django and enhanced with AI capabilities - Prism refracts stakeholder complexity into clear, actionable insights**
