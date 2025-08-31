# Social Media API

A Django REST Framework-based social media API that provides user authentication, profile management, and social features.

## Project Overview

This Social Media API is built with Django and Django REST Framework, featuring:
- Custom user authentication with token-based authentication
- User registration and login
- User profile management with bio and profile pictures
- Following/followers system
- RESTful API endpoints

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip (Python package manager)

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd social_media_api
   ```

2. **Install dependencies:**
   ```bash
   pip install django djangorestframework Pillow
   ```

3. **Run migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Create a superuser (optional):**
   ```bash
   python manage.py createsuperuser
   ```

5. **Start the development server:**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://127.0.0.1:8000/`

## API Endpoints

### Authentication Endpoints

#### User Registration
- **URL:** `POST /api/register/`
- **Description:** Register a new user account
- **Request Body:**
  ```json
  {
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "first_name": "John",
    "last_name": "Doe",
    "bio": "Hello, I'm John!"
  }
  ```
- **Response:**
  ```json
  {
    "user": {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "bio": "Hello, I'm John!",
      "profile_picture": null,
      "followers_count": 0,
      "following_count": 0,
      "date_joined": "2025-08-31T10:30:00Z"
    },
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "message": "User registered successfully"
  }
  ```

#### User Login
- **URL:** `POST /api/login/`
- **Description:** Login with existing credentials
- **Request Body:**
  ```json
  {
    "username": "johndoe",
    "password": "securepassword123"
  }
  ```
- **Response:**
  ```json
  {
    "user": {
      "id": 1,
      "username": "johndoe",
      "email": "john@example.com",
      "first_name": "John",
      "last_name": "Doe",
      "bio": "Hello, I'm John!",
      "profile_picture": null,
      "followers_count": 0,
      "following_count": 0,
      "date_joined": "2025-08-31T10:30:00Z"
    },
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "message": "Login successful"
  }
  ```

#### User Profile
- **URL:** `GET /api/profile/`
- **Description:** Get current user's profile information
- **Headers:** `Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`
- **Response:**
  ```json
  {
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "bio": "Hello, I'm John!",
    "profile_picture": null,
    "followers_count": 0,
    "following_count": 0,
    "date_joined": "2025-08-31T10:30:00Z"
  }
  ```

- **URL:** `PUT /api/profile/`
- **Description:** Update current user's profile
- **Headers:** `Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b`
- **Request Body:**
  ```json
  {
    "first_name": "John",
    "last_name": "Smith",
    "bio": "Updated bio information",
    "email": "johnsmith@example.com"
  }
  ```

## User Model

The `CustomUser` model extends Django's `AbstractUser` with additional fields:

- **bio:** Text field for user biography (max 500 characters)
- **profile_picture:** Image field for user's profile picture
- **followers:** Many-to-many relationship for user following system

### Follow Model

The `Follow` model manages the following relationships between users:
- **follower:** User who follows another user
- **following:** User being followed
- **created_at:** Timestamp of when the follow relationship was created

## Authentication

This API uses Token-based authentication. After successful registration or login, you'll receive a token that must be included in the `Authorization` header for protected endpoints:

```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

## Testing with Postman

1. **Register a new user:**
   - Method: POST
   - URL: `http://127.0.0.1:8000/api/register/`
   - Body: JSON with user details
   - Save the returned token

2. **Login:**
   - Method: POST
   - URL: `http://127.0.0.1:8000/api/login/`
   - Body: JSON with username and password

3. **Access profile:**
   - Method: GET
   - URL: `http://127.0.0.1:8000/api/profile/`
   - Headers: `Authorization: Token <your-token>`

## Project Structure

```
social_media_api/
├── manage.py
├── social_media_api/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── accounts/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    └── migrations/
```

## Development Notes

- The project uses SQLite database by default (suitable for development)
- Media files (profile pictures) are stored in the `media/` directory
- Debug mode is enabled in development settings
- Custom user model is configured as the default user model

## Future Enhancements

This foundational setup can be extended with:
- Posts and content creation
- Comments and likes system
- Real-time notifications
- Advanced search functionality
- Content moderation features
- API rate limiting and throttling

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License.
