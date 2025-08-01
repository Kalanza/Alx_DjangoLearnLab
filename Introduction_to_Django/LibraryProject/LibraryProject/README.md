# LibraryProject - Django Learning Lab

A Django web application developed as part of the ALX Django Learning Lab curriculum. This project demonstrates fundamental Django concepts including project structure, settings configuration, and basic web application setup.

## Project Overview

LibraryProject is a Django-based web application designed to manage library resources. This project serves as an introduction to Django framework and follows best practices for Django development.

## Features

- Django project structure with proper configuration
- Modular application design
- WSGI and ASGI support for deployment
- Development and production settings management

## Project Structure

```
LibraryProject/
├── manage.py                 # Django management script
├── LibraryProject/          # Main project directory
│   ├── __init__.py         # Python package marker
│   ├── settings.py         # Django settings configuration
│   ├── urls.py             # URL routing configuration
│   ├── wsgi.py             # WSGI application entry point
│   └── asgi.py             # ASGI application entry point
└── README.md               # Project documentation
```

## Prerequisites

- Python 3.8 or higher
- Django 4.0 or higher
- pip (Python package installer)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Kalanza/Alx_DjangoLearnLab.git
   cd Alx_DjangoLearnLab/Introduction_to_Django/LibraryProject
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install Django:**
   ```bash
   pip install django
   ```

5. **Apply migrations:**
   ```bash
   python manage.py migrate
   ```

## Usage

### Running the Development Server

To start the Django development server:

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

### Common Django Commands

- **Create a new app:**
  ```bash
  python manage.py startapp app_name
  ```

- **Create migrations:**
  ```bash
  python manage.py makemigrations
  ```

- **Apply migrations:**
  ```bash
  python manage.py migrate
  ```

- **Create a superuser:**
  ```bash
  python manage.py createsuperuser
  ```

- **Collect static files:**
  ```bash
  python manage.py collectstatic
  ```

## Configuration

The project uses Django's default settings with standard configurations for:

- Database: SQLite (default for development)
- Debug mode: Enabled for development
- Static files: Configured for development
- Template engine: Django Template Language (DTL)

## Development

This project is part of the ALX Django Learning Lab curriculum and demonstrates:

- Django project initialization
- Basic project structure understanding
- Configuration management
- Development server setup

## Contributing

This is a learning project. If you're also learning Django, feel free to:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Learning Objectives

By working with this project, you will learn:

- How to create a Django project
- Understanding Django project structure
- Basic Django configuration
- Running Django development server
- Django app architecture fundamentals

## Resources

- [Django Official Documentation](https://docs.djangoproject.com/)
- [Django Tutorial](https://docs.djangoproject.com/en/stable/intro/tutorial01/)
- [ALX Learning Platform](https://www.alxafrica.com/)

## License

This project is created for educational purposes as part of the ALX Django Learning Lab curriculum.

## Contact

For questions related to this learning project, please refer to the ALX Django Learning Lab materials or reach out through the ALX platform.

---

**Note:** This is a learning project developed as part of the ALX Software Engineering Program's Django curriculum.
