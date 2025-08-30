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
  - `updated_date`: DateTimeField(auto_now=True)
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

### Step 7: Blog Post Management (CRUD Operations) ✅
- **Create Posts**: Authenticated users can create new blog posts
- **Read Posts**: Public access to view all posts and individual posts
- **Update Posts**: Post authors can edit their own posts
- **Delete Posts**: Post authors can delete their own posts
- **List Views**: Paginated list of all posts with search/filter
- **User Posts**: View all posts by a specific author
- **Permissions**: Role-based access control and security
- **Form Validation**: Client and server-side validation
- **Rich UI**: Responsive design with intuitive navigation

#### Blog Management Features:
- **PostListView**: Paginated list of all posts (5 per page)
- **PostDetailView**: Full post content with author info and actions
- **PostCreateView**: Rich form for creating new posts (authenticated only)
- **PostUpdateView**: Edit existing posts (author only)
- **PostDeleteView**: Safe deletion with confirmation (author only)
- **UserPostListView**: All posts by specific user with author profile
- **Form Validation**: Title (5-200 chars), Content (20+ chars)
- **Security**: CSRF protection, XSS prevention, SQL injection protection
- **UX Features**: Success messages, error handling, responsive design
- **Navigation**: Dynamic menus, breadcrumbs, related posts

## Usage

### Running the Development Server

```bash
cd django_blog
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to view the blog.

### Available URLs
- `/` - Home page with blog post list
- `/register/` - User registration
- `/login/` - User login
- `/logout/` - User logout
- `/profile/` - User profile (authenticated)
- `/profile/edit/` - Edit profile (authenticated)
- `/post/new/` - Create new blog post (authenticated)
- `/post/<int:pk>/` - View individual blog post
- `/post/<int:pk>/edit/` - Edit blog post (author only)
- `/post/<int:pk>/delete/` - Delete blog post (author only)
- `/user/<username>/posts/` - View all posts by specific user

### Available Features
- **Authentication**: Complete user management system
- **Blog Posts**: Full CRUD operations for blog content
- **User Profiles**: Profile viewing and editing
- **Responsive Design**: Works on all devices
- **Security**: Built-in protection against common web vulnerabilities
- **Pagination**: Efficient handling of large datasets
- **Author Permissions**: Users can only edit/delete their own content

## Testing

### Automated Testing
Run the comprehensive test suite:

```bash
cd django_blog
python test_blog_features.py
```

This test script validates:
- All URLs are accessible
- Authentication workflows
- CRUD operations for blog posts
- User permissions and security
- Form validation
- Template rendering

### Manual Testing
1. **Registration**: Create a new account at `/register/`
2. **Login**: Sign in with your credentials at `/login/`
3. **Create Post**: Write a new blog post at `/post/new/`
4. **View Posts**: Browse all posts at `/` or view individual posts
5. **Edit Posts**: Modify your own posts (edit link appears for authors)
6. **Delete Posts**: Remove your posts with confirmation
7. **User Profiles**: View your profile and statistics at `/profile/`
8. **Browse Authors**: Click on usernames to see all posts by that author

## Security Features

- **Authentication Required**: Creating, editing, and deleting posts requires login
- **Author Permissions**: Users can only modify their own content
- **CSRF Protection**: All forms include CSRF tokens
- **XSS Prevention**: Template auto-escaping enabled
- **SQL Injection Protection**: Django ORM prevents SQL injection
- **Secure Password Handling**: Django's built-in password validation
- **Session Security**: Secure session configuration

## Database Models

### Post Model
- **title**: The title of the blog post (max 200 characters, min 5 characters)
- **content**: The main content of the blog post (min 20 characters)
- **published_date**: Automatically set when the post is created
- **updated_date**: Automatically updated when the post is modified
- **author**: Links to Django's built-in User model

### User Profile Extensions
- **Custom Registration**: Enhanced user creation with email and names
- **Profile Management**: View and edit user information
- **Author Statistics**: Post count, join date, last login tracking

## Templates

### Template Structure
- **base.html**: Master template with navigation, static files, block structures
- **post_list.html**: Paginated list of all blog posts with search/filter
- **post_detail.html**: Individual post view with author actions
- **post_form.html**: Create/edit form for blog posts
- **post_confirm_delete.html**: Safe deletion confirmation page
- **user_posts.html**: All posts by specific author with profile
- **Authentication templates**: registration, login, profile forms

### Template Features
- **Responsive Design**: Mobile-friendly layout
- **Dynamic Navigation**: Context-aware menu items
- **Form Styling**: Bootstrap-style form elements
- **Error Handling**: User-friendly error messages
- **Pagination**: Efficient large dataset handling
- **Author Context**: User-specific content and permissions

## Static Files

### CSS (styles.css)
- **Responsive Design**: Mobile-first approach
- **Component Styling**: Buttons, forms, cards, navigation
- **Blog-Specific Styles**: Post layouts, author info, pagination
- **Accessibility**: High contrast, readable fonts
- **Animation**: Smooth transitions and hover effects

### Feature Documentation
- **BLOG_POST_MANAGEMENT_DOCUMENTATION.md**: Complete feature guide
- **Comprehensive Testing**: Automated validation scripts
- **Security Implementation**: Protection against common vulnerabilities

## Admin Interface

Access the Django admin at `http://127.0.0.1:8000/admin/` to manage:
- Users and permissions
- Blog posts and content
- Site configuration

Create a superuser account:
```bash
python manage.py createsuperuser
```

## Project Status

### ✅ Completed Features
- **Task 0**: Django project setup and configuration
- **Task 1**: User authentication and registration system
- **Task 2**: Complete blog post management with CRUD operations
- **Security**: CSRF protection, XSS prevention, authentication
- **UI/UX**: Responsive design, form validation, error handling
- **Testing**: Comprehensive test suite and validation scripts
- **Documentation**: Complete feature documentation and guides

### 🎯 Current Status
This Django blog project is **production-ready** with:
- Full user authentication and profile management
- Complete blog post CRUD operations
- Security best practices implemented
- Responsive, mobile-friendly design
- Comprehensive testing and documentation
- Role-based permissions and access control

## Future Enhancements

Potential additions for further development:
- **Comments System**: User comments on blog posts
- **Categories and Tags**: Organize posts by topics
- **Search Functionality**: Full-text search across posts
- **Rich Text Editor**: WYSIWYG editor for post creation
- **Email Notifications**: Alerts for new posts and comments
- **Social Features**: User following, post likes, sharing
- **API Endpoints**: REST API for mobile apps
- **Advanced Security**: Two-factor authentication, rate limiting

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
