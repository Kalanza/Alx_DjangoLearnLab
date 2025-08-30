# Django Blog Project

This is a comprehensive Django blog application created as part of the ALX Django learning curriculum.

## Project Structure

```
django_blog/
├── blog/                          # Main blog application
│   ├── migrations/               # Database migrations
│   ├── static/                   # Static files (CSS, JS)
│   │   ├── css/
│   │   │   └── styles.css
│   │   └── js/
│   │       └── scripts.js
│   ├── templates/               # HTML templates
│   │   └── blog/
│   │       ├── base.html        # Base template with auth nav
│   │       ├── home.html        # Home page
│   │       ├── login.html       # Login form
│   │       ├── register.html    # Registration form
│   │       ├── logout.html      # Logout confirmation
│   │       ├── profile.html     # User profile management
│   │       └── posts_list.html  # Blog posts listing
│   ├── admin.py                 # Django admin configuration
│   ├── forms.py                 # Custom authentication forms
│   ├── models.py                # Database models
│   ├── urls.py                  # URL routing
│   └── views.py                 # View functions
├── django_blog/                 # Project configuration
│   ├── settings.py              # Project settings (with auth config)
│   ├── urls.py                  # Main URL configuration
│   └── wsgi.py                  # WSGI configuration
├── static/                      # Project-level static files
├── create_sample_posts.py       # Sample data creation script
├── test_authentication.py       # Authentication system tests
├── db.sqlite3                   # SQLite database
├── manage.py                    # Django management script
├── README.md                    # This file
└── AUTHENTICATION_SYSTEM_DOCUMENTATION.md  # Detailed auth documentation
```

## Features Implemented

### Step 1: Project Setup ✅
- Created Django project `django_blog`
- Created Django app `blog`
- Registered the blog app in `INSTALLED_APPS`

### Step 2: Database Configuration ✅
- Using SQLite database with USER and PORT fields configured
- Database configuration completed in `settings.py`

### Step 3: Blog Models ✅
- Created `Post` model with required fields:
  - `title`: CharField(max_length=200)
  - `content`: TextField()
  - `published_date`: DateTimeField(auto_now_add=True)
  - `author`: ForeignKey to User model
- Applied migrations to create database tables

### Step 4: Static Files and Templates ✅
- Created template directories: `blog/templates/blog/`
- Created static file directories: `blog/static/css/` and `blog/static/js/`
- Implemented base template with navigation
- Created CSS styles for responsive design
- Added JavaScript for dynamic behavior
- Configured Django settings for static files and templates

### Step 5: Development Server ✅
- Successfully launched Django development server
- Application accessible at http://127.0.0.1:8000/
- Created sample blog posts for testing

### Step 6: User Authentication System ✅
- **User Registration**: Extended form with email, first/last name
- **User Login**: Django's built-in secure authentication
- **User Logout**: Secure session termination with confirmation
- **Profile Management**: View and edit user profile information
- **Navigation Integration**: Dynamic menu based on auth status
- **CSRF Protection**: All forms secured against CSRF attacks
- **Password Security**: Django's built-in password hashing
- **Form Validation**: Client and server-side validation
- **Responsive Design**: Mobile-friendly authentication pages
- **Error Handling**: User-friendly error messages
- **Automatic Redirects**: Smart redirection after auth events

#### Authentication Features:
- Registration with username, email, first name, last name
- Secure login/logout with session management
- Profile viewing and editing
- User statistics (join date, last login, post count)
- Recent posts display in profile
- Responsive forms with Bootstrap-style CSS
- Complete CSRF protection
- Django's secure password validation

## Usage

### Running the Development Server

```bash
cd django_blog
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to view the blog.

### Authentication System

#### For Users:
- **Register**: Visit `/register/` to create a new account
- **Login**: Visit `/login/` to access your account
- **Profile**: Visit `/profile/` to view and edit your profile
- **Logout**: Click logout in navigation to end session

#### Testing Authentication:
```bash
cd django_blog
python test_authentication.py
```

### Admin Interface

Access the Django admin at `http://127.0.0.1:8000/admin/`
- Username: admin
- Password: admin123

### Creating Sample Data

Run the sample data script:

```bash
python create_sample_posts.py
```

## Database Models

### Post Model
- **title**: The title of the blog post (max 200 characters)
- **content**: The main content of the blog post
- **published_date**: Automatically set when the post is created
- **author**: Links to Django's built-in User model

## Templates

### base.html
Base template that includes:
- Navigation menu
- Static file loading
- Block structures for extending
- Footer

### home.html
Home page template that:
- Extends base.html
- Displays recent blog posts
- Shows post metadata (author, date)

## Static Files

### CSS (styles.css)
- Responsive design
- Navigation styling
- Content layout
- Footer styling

### JavaScript (scripts.js)
- DOM ready event handling
- Console logging for debugging

## Next Steps

This foundation allows for further development of:
- User authentication and registration
- Post creation and editing forms
- Comments system
- Search functionality
- Category and tag systems
- User profiles
- Rich text editing

## Requirements

- Python 3.8+
- Django 5.2.5
- SQLite (included with Python)

## Installation

1. Clone the repository
2. Navigate to the project directory
3. Install Django: `pip install django`
4. Run migrations: `python manage.py migrate`
5. Create superuser: `python manage.py createsuperuser`
6. Start the server: `python manage.py runserver`
