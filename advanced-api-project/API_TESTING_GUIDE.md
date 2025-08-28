# API Testing Guide - Django REST Framework Views

This guide provides practical examples for testing all API endpoints using curl commands and describes expected responses.

## Prerequisites

1. Django development server running: `python manage.py runserver`
2. Create a superuser: `python manage.py createsuperuser`
3. API available at: `http://127.0.0.1:8000/api/`

## Testing Read-Only Endpoints (No Authentication Required)

### 1. List All Authors

```bash
curl -X GET "http://127.0.0.1:8000/api/authors/"
```

**Expected Response:**
```json
{
    "message": "Authors retrieved successfully",
    "count": 3,
    "authors": [
        {
            "id": 1,
            "name": "J.K. Rowling",
            "books": [
                {
                    "id": 1,
                    "title": "Harry Potter and the Philosopher's Stone",
                    "publication_year": 1997,
                    "author": 1
                }
            ]
        }
    ]
}
```

### 2. Get Specific Author

```bash
curl -X GET "http://127.0.0.1:8000/api/authors/1/"
```

### 3. List All Books

```bash
curl -X GET "http://127.0.0.1:8000/api/books/"
```

**Expected Response:**
```json
{
    "message": "Books retrieved successfully",
    "total_count": 5,
    "filters_applied": {
        "search": null,
        "author": null,
        "year_after": null,
        "year_before": null
    },
    "books": [
        {
            "id": 1,
            "title": "1984",
            "publication_year": 1949,
            "author": 2
        }
    ]
}
```

### 4. Get Specific Book with Related Books

```bash
curl -X GET "http://127.0.0.1:8000/api/books/1/"
```

**Expected Response:**
```json
{
    "message": "Book retrieved successfully",
    "book": {
        "id": 1,
        "title": "1984",
        "publication_year": 1949,
        "author": 2
    },
    "related_books_by_author": [
        {
            "id": 2,
            "title": "Animal Farm",
            "publication_year": 1945,
            "author": 2
        }
    ]
}
```

### 5. Get Books by Specific Author

```bash
curl -X GET "http://127.0.0.1:8000/api/books/by-author/1/"
```

### 6. Get Book Statistics

```bash
curl -X GET "http://127.0.0.1:8000/api/books/statistics/"
```

**Expected Response:**
```json
{
    "message": "Book statistics retrieved successfully",
    "statistics": {
        "total_books": 5,
        "total_authors": 3,
        "books_per_decade": {
            "1940s": 2,
            "1990s": 2,
            "1950s": 1
        },
        "most_prolific_authors": [
            {
                "name": "J.K. Rowling",
                "book_count": 2
            },
            {
                "name": "George Orwell",
                "book_count": 2
            }
        ]
    }
}
```

## Testing Search and Filtering

### 1. Search Books by Title or Author

```bash
# Search for "Harry" in title or author name
curl -X GET "http://127.0.0.1:8000/api/books/?search=Harry"

# Search for "Orwell" in author name
curl -X GET "http://127.0.0.1:8000/api/books/?search=Orwell"
```

### 2. Filter by Author

```bash
# Get all books by author with ID 1
curl -X GET "http://127.0.0.1:8000/api/books/?author=1"
```

### 3. Filter by Publication Year

```bash
# Get books published in 1949
curl -X GET "http://127.0.0.1:8000/api/books/?publication_year=1949"

# Get books published after 1990
curl -X GET "http://127.0.0.1:8000/api/books/?year_after=1990"

# Get books published before 1950
curl -X GET "http://127.0.0.1:8000/api/books/?year_before=1950"
```

### 4. Ordering Results

```bash
# Order by title (ascending)
curl -X GET "http://127.0.0.1:8000/api/books/?ordering=title"

# Order by publication year (descending)
curl -X GET "http://127.0.0.1:8000/api/books/?ordering=-publication_year"

# Order by author name
curl -X GET "http://127.0.0.1:8000/api/books/?ordering=author__name"
```

### 5. Complex Filtering

```bash
# Search for "Harry" AND filter by author 1 AND order by year
curl -X GET "http://127.0.0.1:8000/api/books/?search=Harry&author=1&ordering=publication_year"

# Books published between 1990 and 2000
curl -X GET "http://127.0.0.1:8000/api/books/?year_after=1990&year_before=2000"
```

## Testing Write Operations (Authentication Required)

### 1. Get Authentication Token/Session

First, you need to authenticate. For basic testing, use Django admin login or create a session:

```bash
# Create a session using Django admin login
curl -c cookies.txt -X GET "http://127.0.0.1:8000/admin/login/"
```

Or use basic authentication (replace username:password):

```bash
# Example using basic auth (replace admin:password123 with your credentials)
AUTH="admin:password123"
```

### 2. Create Author (Authentication Required)

```bash
# Using basic authentication
curl -X POST "http://127.0.0.1:8000/api/authors/" \
     -H "Content-Type: application/json" \
     -u admin:password123 \
     -d '{
         "name": "New Test Author"
     }'
```

**Expected Response:**
```json
{
    "id": 4,
    "name": "New Test Author",
    "books": []
}
```

**Without Authentication (Should Fail):**
```bash
curl -X POST "http://127.0.0.1:8000/api/authors/" \
     -H "Content-Type: application/json" \
     -d '{
         "name": "Unauthorized Author"
     }'
```

**Expected Response:** HTTP 401 or 403

### 3. Create Book (Authentication Required)

```bash
# Using basic authentication
curl -X POST "http://127.0.0.1:8000/api/books/create/" \
     -H "Content-Type: application/json" \
     -u admin:password123 \
     -d '{
         "title": "New Test Book",
         "publication_year": 2023,
         "author": 1
     }'
```

**Expected Response:**
```json
{
    "message": "Book 'New Test Book' created successfully",
    "book": {
        "id": 6,
        "title": "New Test Book",
        "publication_year": 2023,
        "author": 1
    }
}
```

### 4. Test Custom Validation (Future Year)

```bash
# This should fail validation
curl -X POST "http://127.0.0.1:8000/api/books/create/" \
     -H "Content-Type: application/json" \
     -u admin:password123 \
     -d '{
         "title": "Future Book",
         "publication_year": 2026,
         "author": 1
     }'
```

**Expected Response:** HTTP 400
```json
{
    "publication_year": [
        "Publication year cannot be in the future. Current year is 2025."
    ]
}
```

### 5. Update Book (Authentication Required)

```bash
# Update book title (replace 1 with actual book ID)
curl -X PATCH "http://127.0.0.1:8000/api/books/1/update/" \
     -H "Content-Type: application/json" \
     -u admin:password123 \
     -d '{
         "title": "Updated Book Title"
     }'
```

**Expected Response:**
```json
{
    "message": "Book 'Updated Book Title' updated successfully",
    "book": {
        "id": 1,
        "title": "Updated Book Title",
        "publication_year": 1949,
        "author": 2
    }
}
```

### 6. Update Author (Authentication Required)

```bash
# Update author name
curl -X PATCH "http://127.0.0.1:8000/api/authors/1/" \
     -H "Content-Type: application/json" \
     -u admin:password123 \
     -d '{
         "name": "Updated Author Name"
     }'
```

### 7. Delete Book (Authentication Required)

```bash
# Delete a book (replace 6 with actual book ID)
curl -X DELETE "http://127.0.0.1:8000/api/books/6/delete/" \
     -u admin:password123
```

**Expected Response:** HTTP 204
```json
{
    "message": "Book 'New Test Book' deleted successfully"
}
```

### 8. Delete Author (Authentication Required)

```bash
# Delete an author (this will cascade delete all their books)
curl -X DELETE "http://127.0.0.1:8000/api/authors/4/" \
     -u admin:password123
```

## Testing Error Scenarios

### 1. Non-existent Resources

```bash
# Try to get non-existent book
curl -X GET "http://127.0.0.1:8000/api/books/999/"

# Try to get books by non-existent author
curl -X GET "http://127.0.0.1:8000/api/books/by-author/999/"
```

### 2. Invalid Data

```bash
# Invalid publication year (string instead of integer)
curl -X POST "http://127.0.0.1:8000/api/books/create/" \
     -H "Content-Type: application/json" \
     -u admin:password123 \
     -d '{
         "title": "Invalid Year Book",
         "publication_year": "not-a-year",
         "author": 1
     }'

# Missing required fields
curl -X POST "http://127.0.0.1:8000/api/books/create/" \
     -H "Content-Type: application/json" \
     -u admin:password123 \
     -d '{
         "title": "Incomplete Book"
     }'
```

### 3. Unauthorized Operations

```bash
# Try to create without authentication
curl -X POST "http://127.0.0.1:8000/api/authors/" \
     -H "Content-Type: application/json" \
     -d '{
         "name": "Unauthorized Author"
     }'

# Try to update without authentication
curl -X PATCH "http://127.0.0.1:8000/api/books/1/update/" \
     -H "Content-Type: application/json" \
     -d '{
         "title": "Unauthorized Update"
     }'
```

## Testing with Postman

### Setting Up Postman

1. **Import Collection**: Create a Postman collection with the above endpoints
2. **Environment Variables**: 
   - `base_url`: `http://127.0.0.1:8000/api`
   - `username`: your admin username
   - `password`: your admin password

3. **Authorization**: Use Basic Auth with your Django admin credentials

### Postman Test Examples

```javascript
// Test for successful author creation
pm.test("Author created successfully", function () {
    pm.response.to.have.status(201);
    pm.expect(pm.response.json()).to.have.property('name');
});

// Test for validation error
pm.test("Future year validation works", function () {
    pm.response.to.have.status(400);
    pm.expect(pm.response.json()).to.have.property('publication_year');
});
```

## Performance Testing

### Load Testing with curl

```bash
# Test multiple concurrent requests
for i in {1..10}; do
    curl -X GET "http://127.0.0.1:8000/api/books/" &
done
wait

# Test search performance
time curl -X GET "http://127.0.0.1:8000/api/books/?search=test"
```

## Monitoring and Logging

### Check Logs

The API logs all operations. Check the logs:

```bash
# View recent API logs
tail -f api.log

# Filter for specific operations
grep "created" api.log
grep "deleted" api.log
```

### Server Console Output

Monitor the Django development server console for:
- Request logs
- Query counts
- Error messages
- Performance warnings

## Summary of Endpoints

| Method | Endpoint | Auth Required | Purpose |
|--------|----------|---------------|---------|
| GET | `/authors/` | No | List authors |
| POST | `/authors/` | Yes | Create author |
| GET | `/authors/<id>/` | No | Get author |
| PUT/PATCH | `/authors/<id>/` | Yes | Update author |
| DELETE | `/authors/<id>/` | Yes | Delete author |
| GET | `/books/` | No | List books (with filtering) |
| POST | `/books/create/` | Yes | Create book |
| GET | `/books/<id>/` | No | Get book details |
| PUT/PATCH | `/books/<id>/update/` | Yes | Update book |
| DELETE | `/books/<id>/delete/` | Yes | Delete book |
| GET | `/books/by-author/<id>/` | No | Books by author |
| GET | `/books/statistics/` | No | Book statistics |

This testing guide covers all major functionality and edge cases for the Django REST Framework views implementation.
