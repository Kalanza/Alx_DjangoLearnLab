# Django Blog Project

A comprehensive Django blog application with a complete setup including models, templates, static files, and admin interface.

## Project Structure

```
django_blog/
├── blog/                          # Main blog application
│   ├── migrations/               # Database migrations
│   ├── static/                   # Static files
│   │   ├── css/                 # CSS stylesheets
│   │   │   └── styles.css
│   │   └── js/                  # JavaScript files
│   │       └── scripts.js
│   ├── templates/               # HTML templates
│   │   └── blog/
│   │       ├── base.html        # Base template
│   │       └── home.html        # Home page template
│   ├── admin.py                 # Admin configuration
│   ├── models.py                # Database models
│   ├── urls.py                  # URL routing
│   └── views.py                 # View functions
├── django_blog/                 # Project configuration
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Main URL configuration
│   └── wsgi.py                  # WSGI configuration
├── static/                      # Global static files directory
├── db.sqlite3                   # SQLite database
├── manage.py                    # Django management script
└── requirements.txt             # Python dependencies
```

## Features

- **Post Model**: Complete blog post model with title, content, published_date, and author
- **Admin Interface**: Configured admin panel for managing blog posts
- **Static Files**: CSS and JavaScript files properly configured
- **Templates**: Base template with navigation and home page
- **Database**: SQLite database with completed migrations
- **User Management**: Django's built-in User model integration

## Getting Started

### Prerequisites

- Python 3.12+
- Django 5.2.5+

### Installation

1. Navigate to the project directory:
   ```bash
   cd django_blog
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run migrations (already completed):
   ```bash
   python manage.py migrate
   ```

4. Create a superuser (already created - username: admin):
   ```bash
   python manage.py createsuperuser
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

6. Open your browser and visit:
   - Home page: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Models

### Post Model
- `title`: CharField (max_length=200)
- `content`: TextField
- `published_date`: DateTimeField (auto_now_add=True)
- `author`: ForeignKey to User model

## URL Patterns

- `/` - Home page
- `/posts/` - Blog posts (placeholder)
- `/login/` - Login page (placeholder)
- `/register/` - Register page (placeholder)
- `/admin/` - Admin interface

## Admin Interface

The admin interface is configured with:
- Post management with list display
- Search functionality
- Date and author filtering
- User-friendly post creation

## Static Files Configuration

- CSS files: `blog/static/css/`
- JavaScript files: `blog/static/js/`
- Global static directory: `static/`

## Templates

- Base template with navigation and footer
- Responsive design with basic CSS styling
- Template inheritance setup

## Next Steps

1. Implement user authentication and registration
2. Create detailed post views and templates
3. Add comment functionality
4. Implement search and pagination
5. Add user profiles and permissions
6. Enhance the UI/UX design

## Development Notes

- Using Django 5.2.5
- SQLite database (can be changed to PostgreSQL in production)
- Debug mode enabled (disable in production)
- Static files served by Django development server
