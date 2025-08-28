# Django REST Framework Filtering, Searching, and Ordering Documentation

## Task 2: Implementing Filtering, Searching, and Ordering

This document demonstrates the comprehensive implementation of Django REST Framework's filtering capabilities in our advanced API project.

## ✅ Requirements Fulfilled

### 1. Django Filter Integration
- **Required Import**: `from django_filters import rest_framework` ✅
- **Location**: `api/views.py` line 19
- **Purpose**: Provides advanced filtering capabilities through django-filter package

### 2. Filter Backends Configuration
- **DjangoFilterBackend**: ✅ Integrated in views and settings
- **SearchFilter**: ✅ Integrated for text-based searching
- **OrderingFilter**: ✅ Integrated for result ordering

### 3. Search Functionality on Book Model
- **Fields**: title, author name ✅
- **Implementation**: Multi-field search with priority levels
- **Example**: `/api/books/?search=Harry` searches both title and author fields

## 🔧 Implementation Details

### Book Model Filtering (`BookListView`)

#### Available Filter Options:
```python
# Basic filters
?publication_year=2020           # Exact year match
?author=1                        # Filter by author ID

# Advanced custom filters (via BookFilter class)
?title=Harry                     # Partial title match
?title_exact=1984               # Exact title match
?title_starts_with=The          # Title prefix match
?author_name=Rowling            # Author name partial match
?year_after=2000                # Books after year
?year_before=2010               # Books before year
?decade=1990s                   # Books from specific decade
?search=fantasy                 # Multi-field search
```

#### Search Configuration:
```python
search_fields = [
    'title',           # Search in book title
    'author__name',    # Search in author name
    '^title',          # Title starts with (higher priority)
    '=title',          # Exact title match (highest priority)
]
```

#### Ordering Options:
```python
?ordering=title                  # Order by title (A-Z)
?ordering=-publication_year      # Order by year (newest first)
?ordering=author__name           # Order by author name
```

### Author Model Filtering (`AuthorListCreateView`)

#### Available Filter Options:
```python
?name=J.K.                      # Partial name match
?name_starts_with=J             # Name prefix match
?has_books=true                 # Authors with books
?book_count_min=2               # Authors with at least 2 books
```

#### Search Configuration:
```python
search_fields = [
    'name',     # Search in author name
    '^name',    # Name starts with (higher priority)
    '=name',    # Exact name match (highest priority)
]
```

#### Ordering Options:
```python
?ordering=name                   # Order by name (A-Z)
?ordering=-book_count            # Order by book count (most prolific first)
```

## 🎯 Advanced Features

### Custom Filter Classes

#### BookFilter (`api/filters.py`)
```python
class BookFilter(FilterSet):
    # Text filters
    title = CharFilter(lookup_expr='icontains')
    title_exact = CharFilter(field_name='title', lookup_expr='exact')
    title_starts_with = CharFilter(field_name='title', lookup_expr='startswith')
    author_name = CharFilter(field_name='author__name', lookup_expr='icontains')
    
    # Date filters
    year_after = NumberFilter(field_name='publication_year', lookup_expr='gt')
    year_before = NumberFilter(field_name='publication_year', lookup_expr='lt')
    
    # Custom methods
    decade = CharFilter(method='filter_by_decade')
    search = CharFilter(method='filter_search')
    has_multiple_books_by_author = BooleanFilter(method='filter_prolific_authors')
```

#### AuthorFilter (`api/filters.py`)
```python
class AuthorFilter(FilterSet):
    name_starts_with = CharFilter(field_name='name', lookup_expr='startswith')
    has_books = BooleanFilter(method='filter_has_books')
    book_count_min = NumberFilter(method='filter_book_count_min')
```

### Settings Configuration

#### INSTALLED_APPS
```python
INSTALLED_APPS = [
    # ... other apps
    "rest_framework",
    "django_filters",  # ✅ Required for filtering
    "api",
]
```

#### REST_FRAMEWORK Settings
```python
REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',  # ✅ Required
        'rest_framework.filters.SearchFilter',               # ✅ Required
        'rest_framework.filters.OrderingFilter',             # ✅ Required
    ],
    # ... other settings
}
```

## 🧪 Example Usage

### 1. Basic Filtering
```bash
# Get books published in 1997
GET /api/books/?publication_year=1997

# Get books by a specific author
GET /api/books/?author=1
```

### 2. Search Functionality
```bash
# Search for books with "Harry" in title or author name
GET /api/books/?search=Harry

# Search for authors with "J.K." in name
GET /api/authors/?search=J.K.
```

### 3. Advanced Filtering
```bash
# Get books from the 1990s, ordered by publication year
GET /api/books/?decade=1990s&ordering=publication_year

# Get books by authors named Rowling, published after 1990
GET /api/books/?author_name=Rowling&year_after=1990

# Get books with titles starting with "The"
GET /api/books/?title_starts_with=The
```

### 4. Combined Operations
```bash
# Search for "fantasy" books, ordered by title, from prolific authors
GET /api/books/?search=fantasy&ordering=title&has_multiple_books_by_author=true

# Get authors with at least 2 books, ordered by book count
GET /api/authors/?book_count_min=2&ordering=-book_count
```

## 🔍 Response Format

### Book List Response
```json
{
    "message": "Books retrieved successfully",
    "total_count": 5,
    "current_page_count": 5,
    "filters_applied": {
        "search": "Harry",
        "ordering": "publication_year"
    },
    "ordering_applied": "publication_year",
    "search_query": "Harry",
    "available_filters": {
        "text_filters": {...},
        "date_filters": {...},
        "boolean_filters": {...}
    },
    "books": [...]
}
```

### Author List Response
```json
{
    "message": "Authors retrieved successfully",
    "total_count": 3,
    "current_page_count": 3,
    "filters_applied": {
        "name_starts_with": "J",
        "ordering": "name"
    },
    "ordering_applied": "name",
    "search_query": null,
    "available_filters": {...},
    "authors": [...]
}
```

## ✅ Validation Checklist

- [x] `from django_filters import rest_framework` import present
- [x] DjangoFilterBackend integration
- [x] SearchFilter integration  
- [x] OrderingFilter integration
- [x] Search functionality on Book title field
- [x] Search functionality on Book author field
- [x] Filter by publication_year
- [x] Filter by author
- [x] Advanced custom filtering
- [x] Proper settings configuration
- [x] Custom filter classes
- [x] Comprehensive documentation
- [x] Working test examples

## 🚀 Benefits

1. **User Experience**: Users can efficiently find specific books and authors
2. **Performance**: Optimized queries with select_related and proper indexing
3. **Flexibility**: Multiple filtering options for different use cases
4. **Extensibility**: Easy to add new filters and search capabilities
5. **API Standards**: Follows REST API best practices for filtering and pagination
