# Django Blog Project

This is a comprehensive Django blog application developed as part of the ALX Django Learning Lab.

## Project Structure

```
django_blog/
├── blog/                          # Main blog application
│   ├── migrations/               # Database migrations
│   ├── static/                   # Static files (CSS, JS, Images)
│   │   └── blog/
│   │       ├── css/
│   │       │   └── style.css    # Custom CSS styles
│   │       └── js/
│   │           └── main.js      # Custom JavaScript
│   ├── templates/               # HTML templates
│   │   └── blog/
│   │       ├── base.html       # Base template
│   │       └── home.html       # Home page template
│   ├── management/              # Custom management commands
│   │   └── commands/
│   │       └── create_sample_posts.py
│   ├── admin.py                 # Admin configuration
│   ├── apps.py                  # App configuration
│   ├── models.py                # Database models
│   ├── urls.py                  # URL patterns
│   └── views.py                 # View functions
├── blog_project/                # Main project directory
│   ├── settings.py              # Project settings
│   ├── urls.py                  # Main URL configuration
│   └── wsgi.py                  # WSGI configuration
├── db.sqlite3                   # SQLite database
├── manage.py                    # Django management script
└── README.md                    # This file
```

## Features

- **Post Model**: Blog posts with title, content, publication date, and author
- **Responsive Design**: Mobile-friendly interface using Bootstrap
- **Admin Interface**: Easy content management through Django admin
- **Static Files**: Properly configured CSS and JavaScript
- **Template System**: Extensible template structure
- **User Authentication**: Built-in Django user system

## Models

### Post Model
- `title`: CharField(max_length=200) - The post title
- `content`: TextField - The main content of the post
- `published_date`: DateTimeField(auto_now_add=True) - Automatic timestamp
- `author`: ForeignKey(User) - Reference to Django's User model

## Setup Instructions

1. **Install Django**:
   ```bash
   pip install django
   ```

2. **Create the project** (Already done):
   ```bash
   django-admin startproject django_blog
   cd django_blog
   python manage.py startapp blog
   ```

3. **Configure the application**:
   - Add 'blog' to INSTALLED_APPS in settings.py
   - Configure static files and templates directories

4. **Run migrations**:
   ```bash
   python manage.py makemigrations blog
   python manage.py migrate
   ```

5. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Create sample posts** (optional):
   ```bash
   python manage.py create_sample_posts
   ```

7. **Start the development server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the application**:
   - Home page: http://127.0.0.1:8000/
   - Admin interface: http://127.0.0.1:8000/admin/

## Admin Interface

The admin interface is configured to manage blog posts with the following features:
- List display showing title, author, and publication date
- Filtering by publication date and author
- Search functionality for title and content
- Ordering by publication date (newest first)

## Static Files Configuration

Static files are organized as follows:
- CSS files: `blog/static/css/`
- JavaScript files: `blog/static/js/`
- Images (if any): `blog/static/images/`

The STATICFILES_DIRS setting in settings.py is configured to find these files.

Key static files:
- `styles.css`: Main stylesheet with clean, modern design
- `scripts.js`: JavaScript for interactive elements and animations

## Template Configuration

Templates are located in `blog/templates/blog/` and the TEMPLATES setting is configured to find them. The base template includes Bootstrap for responsive design.

## Database Configuration

By default, the project uses SQLite for simplicity. The database file is `db.sqlite3` in the project root. For production, you can configure PostgreSQL or another database in settings.py.

## Development Notes

- Debug mode is enabled in settings.py for development
- The project uses Django 5.2.5
- Bootstrap 5.1.3 is included via CDN for styling
- Custom CSS and JavaScript files are included for additional styling and functionality

## Next Steps

This foundational setup provides the base for extending the blog with additional features such as:
- User registration and login
- Comment system
- Post categories and tags
- Search functionality
- Pagination
- RSS feeds
- SEO optimization

## Security Notes

- The SECRET_KEY in settings.py should be changed for production
- Debug mode should be disabled in production
- Allowed hosts should be configured for production deployment
