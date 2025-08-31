# Social Media API - Project Structure Documentation

## Complete Project Structure

```
social_media_api/
├── README.md                          # Comprehensive project documentation
├── requirements.txt                   # Python dependencies
├── test_api.py                       # API testing script
├── manage.py                         # Django management script
├── db.sqlite3                        # SQLite database (created after migrations)
├── media/                            # Directory for user uploads (profile pictures)
│   └── profile_pics/                 # Profile pictures subdirectory
├── social_media_api/                 # Main Django project directory
│   ├── __init__.py                   # Python package marker
│   ├── settings.py                   # Django settings configuration
│   ├── urls.py                       # Main URL routing configuration
│   ├── wsgi.py                       # WSGI configuration for deployment
│   └── asgi.py                       # ASGI configuration (created by Django)
└── accounts/                         # Django app for user management
    ├── __init__.py                   # Python package marker
    ├── admin.py                      # Django admin configuration
    ├── apps.py                       # App configuration
    ├── models.py                     # Database models (CustomUser, Follow)
    ├── serializers.py                # DRF serializers for API
    ├── views.py                      # API views and endpoints
    ├── urls.py                       # URL routing for accounts app
    ├── tests.py                      # Unit tests (default Django file)
    ├── management/                   # Custom Django management commands
    │   ├── __init__.py               # Python package marker
    │   └── commands/                 # Management commands directory
    │       ├── __init__.py           # Python package marker
    │       └── create_sample_data.py # Command to create test users
    └── migrations/                   # Database migration files
        ├── __init__.py               # Python package marker
        └── 0001_initial.py           # Initial migration (CustomUser, Follow)
```

## Key Components Description

### 1. **Main Project Configuration** (`social_media_api/`)
- **settings.py**: Contains all Django configuration including:
  - Installed apps (Django, DRF, accounts)
  - Database configuration (SQLite)
  - Authentication settings (Token-based)
  - Media files configuration
  - Custom user model specification

- **urls.py**: Main URL routing that includes:
  - Admin interface routes
  - API routes (delegated to accounts app)
  - Media file serving for development

### 2. **Accounts App** (`accounts/`)
This app handles all user-related functionality:

#### Models (`models.py`)
- **CustomUser**: Extends AbstractUser with:
  - `bio`: Text field for user biography
  - `profile_picture`: Image field for profile photos
  - `followers`: ManyToMany relationship for social connections

- **Follow**: Intermediate model for follower relationships:
  - `follower`: User who follows
  - `following`: User being followed
  - `created_at`: Timestamp of follow action

#### Serializers (`serializers.py`)
- **UserRegistrationSerializer**: Handles user signup with password confirmation
- **UserLoginSerializer**: Validates login credentials
- **UserProfileSerializer**: Manages profile data with follower/following counts

#### Views (`views.py`)
- **RegisterView**: CreateAPIView for user registration
- **login_view**: Function-based view for user authentication
- **ProfileView**: RetrieveUpdateAPIView for profile management

#### URL Configuration (`urls.py`)
- `/register/`: User registration endpoint
- `/login/`: User authentication endpoint
- `/profile/`: Profile retrieval and update endpoint

#### Admin Configuration (`admin.py`)
- Custom admin interface for user management
- Follow relationship administration

### 3. **Database Models Relationship**

```
CustomUser (1) ←→ (Many) Follow (Many) ←→ (1) CustomUser
    ↑                                           ↑
follower                                  following
```

Each Follow instance connects:
- One user as a follower
- One user as the person being followed

### 4. **Authentication Flow**

1. **Registration**:
   - User submits registration data
   - Password validation and confirmation
   - User account creation
   - Token generation and return

2. **Login**:
   - User submits credentials
   - Authentication validation
   - Token retrieval/creation
   - User data and token return

3. **Profile Access**:
   - Token-based authentication required
   - User can view/update their profile
   - Follower/following counts calculated dynamically

### 5. **API Security Features**

- **Token Authentication**: Each user gets a unique token
- **Password Validation**: Minimum length and confirmation required
- **Permission Classes**: Authentication required for protected endpoints
- **User Model Validation**: Email and username uniqueness enforced

### 6. **Development Tools**

- **test_api.py**: Automated testing script for all endpoints
- **create_sample_data.py**: Management command for creating test users
- **README.md**: Comprehensive documentation with examples
- **requirements.txt**: Dependency management

## Database Schema

### CustomUser Table
```sql
- id (Primary Key)
- username (Unique)
- email (Unique)
- first_name
- last_name
- bio
- profile_picture
- date_joined
- last_login
- is_active
- is_staff
- is_superuser
- password (hashed)
```

### Follow Table
```sql
- id (Primary Key)
- follower_id (Foreign Key → CustomUser)
- following_id (Foreign Key → CustomUser)
- created_at
- UNIQUE(follower_id, following_id)
```

### Token Table (Django REST Framework)
```sql
- key (Primary Key)
- user_id (Foreign Key → CustomUser)
- created
```

## Configuration Details

### Django Settings Highlights
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'accounts',
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

AUTH_USER_MODEL = 'accounts.CustomUser'
```

This structure provides a solid foundation for a social media API with proper separation of concerns, security implementation, and extensibility for future features.
