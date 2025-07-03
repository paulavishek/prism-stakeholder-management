# Google Cloud Deployment Guide

This guide will help you deploy the Stakeholder Management System to Google Cloud Platform.

## Prerequisites

- Google Cloud Platform account
- Google Cloud CLI installed
- Docker installed (for containerized deployment)
- Domain name (optional, for custom domain)

## Deployment Options

### Option 1: Google App Engine (Recommended)

App Engine is perfect for Django applications and handles scaling automatically.

#### 1. Prepare app.yaml

```yaml
runtime: python312

env_variables:
  DJANGO_SETTINGS_MODULE: stakeholder_management.settings
  SECRET_KEY: "your-secret-key-here"
  GEMINI_API_KEY: "your-gemini-api-key"
  DEBUG: "False"
  ALLOWED_HOSTS: "your-app-id.appspot.com,your-custom-domain.com"

automatic_scaling:
  min_instances: 1
  max_instances: 10
```

#### 2. Update settings.py for production

```python
# Add to settings.py
import os

if os.getenv('GAE_APPLICATION', None):
    # Running on production App Engine
    DEBUG = False
    ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')
    
    # Use Cloud SQL for production
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('DB_NAME'),
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': f'/cloudsql/{os.getenv("CLOUD_SQL_CONNECTION_NAME")}',
            'PORT': '5432',
        }
    }
    
    # Static files on Google Cloud Storage
    DEFAULT_FILE_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    STATICFILES_STORAGE = 'storages.backends.gcloud.GoogleCloudStorage'
    GS_BUCKET_NAME = os.getenv('GS_BUCKET_NAME')
```

#### 3. Add requirements.txt entries

```
# Add to requirements.txt
psycopg2-binary==2.9.7
django-storages[google]==1.13.2
```

#### 4. Deploy to App Engine

```bash
# Initialize gcloud
gcloud init

# Set project
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable appengine.googleapis.com
gcloud services enable cloudsql.googleapis.com
gcloud services enable storage.googleapis.com

# Create App Engine app
gcloud app create --region=us-central

# Deploy
gcloud app deploy
```

### Option 2: Google Cloud Run (Containerized)

#### 1. Create Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run migrations (you might want to do this separately)
RUN python manage.py migrate

EXPOSE 8080

CMD exec gunicorn --bind :8080 --workers 1 --threads 8 stakeholder_management.wsgi:application
```

#### 2. Add gunicorn to requirements.txt

```
gunicorn==21.2.0
```

#### 3. Deploy to Cloud Run

```bash
# Build and deploy
gcloud run deploy stakeholder-management \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --set-env-vars DJANGO_SETTINGS_MODULE=stakeholder_management.settings \
    --set-env-vars SECRET_KEY=your-secret-key \
    --set-env-vars GEMINI_API_KEY=your-gemini-api-key \
    --set-env-vars DEBUG=False
```

## Database Setup

### Cloud SQL (PostgreSQL)

```bash
# Create Cloud SQL instance
gcloud sql instances create stakeholder-db \
    --database-version=POSTGRES_14 \
    --tier=db-f1-micro \
    --region=us-central1

# Create database
gcloud sql databases create stakeholder_management --instance=stakeholder-db

# Create user
gcloud sql users create app-user --instance=stakeholder-db --password=secure-password
```

## Static Files & Media

### Google Cloud Storage

```bash
# Create storage bucket
gsutil mb gs://your-app-static-files

# Set bucket permissions
gsutil iam ch allUsers:objectViewer gs://your-app-static-files
```

## Environment Variables Management

### Using Google Secret Manager

```bash
# Store secrets
gcloud secrets create django-secret-key --data-file=-
gcloud secrets create gemini-api-key --data-file=-

# Grant access to App Engine
gcloud secrets add-iam-policy-binding django-secret-key \
    --member=serviceAccount:your-project@appspot.gserviceaccount.com \
    --role=roles/secretmanager.secretAccessor
```

## Post-Deployment Steps

### 1. Load Demo Data

```bash
# SSH into your deployed instance or use Cloud Shell
gcloud app ssh

# Load demo data
python manage.py load_demo_data --scenario=standard
```

### 2. Create Superuser

```bash
python manage.py createsuperuser
```

### 3. Test Demo Functionality

1. Visit your deployed URL
2. Use demo credentials: `demo` / `password`
3. Test demo data loading/clearing
4. Verify AI features work with your Gemini API key

## Custom Domain Setup

```bash
# Map custom domain
gcloud app domain-mappings create your-domain.com

# Add SSL certificate (automatic with managed certificates)
```

## Monitoring & Logging

### Enable logging

```python
# Add to settings.py
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
```

### View logs

```bash
# View application logs
gcloud app logs tail -s default

# Or use Cloud Console
```

## Cost Optimization

1. **App Engine**: F1 instances are free tier eligible
2. **Cloud SQL**: f1-micro is free tier eligible
3. **Cloud Storage**: 5GB free per month
4. **Gemini API**: Check current pricing and set quotas

## Security Checklist

- [ ] Set strong SECRET_KEY
- [ ] Disable DEBUG in production
- [ ] Set proper ALLOWED_HOSTS
- [ ] Use HTTPS (automatic with App Engine)
- [ ] Secure Gemini API key in Secret Manager
- [ ] Set up proper IAM roles
- [ ] Enable Cloud Security Command Center

## Demo URL Example

After deployment, your app will be available at:
- App Engine: `https://your-project-id.appspot.com`
- Cloud Run: `https://stakeholder-management-hash-uc.a.run.app`

Share this URL with recruiters along with demo credentials:
- Username: `demo`
- Password: `password`

## Troubleshooting

### Common Issues

1. **Static files not loading**: Check Cloud Storage bucket permissions
2. **Database connection errors**: Verify Cloud SQL proxy settings
3. **AI features not working**: Check Gemini API key and quotas
4. **Demo data not loading**: Check database migrations

### Useful Commands

```bash
# Check app status
gcloud app browse

# View instance logs
gcloud app logs tail

# Update environment variables
gcloud app deploy --set-env-vars KEY=VALUE
```
