"""
Security tests for the LibraryProject Django application.
Tests various security measures implemented to protect against common vulnerabilities.
"""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test.utils import override_settings
from django.middleware.csrf import get_token
from bookshelf.models import Book, UserProfile
import json

User = get_user_model()


class SecurityTestCase(TestCase):
    """
    Test suite for security measures including CSRF, XSS, SQL injection prevention,
    and access control.
    """
    
    def setUp(self):
        """Set up test data and users with different permissions."""
        self.client = Client()
        
        # Create test users
        self.admin_user = User.objects.create_user(
            username='admin_test',
            email='admin@test.com',
            password='secure_password_123'
        )
        self.admin_user.is_staff = True
        self.admin_user.save()
        
        self.regular_user = User.objects.create_user(
            username='regular_test',
            email='regular@test.com',
            password='secure_password_123'
        )
        
        # Create test book
        self.test_book = Book.objects.create(
            title='Test Book',
            author='Test Author',
            publication_year=2023
        )
    
    def test_csrf_protection(self):
        """Test that CSRF protection is working correctly."""
        # Try to create a book without CSRF token
        self.client.login(username='admin_test', password='secure_password_123')
        
        response = self.client.post(reverse('book_create'), {
            'title': 'CSRF Test Book',
            'author': 'CSRF Test Author',
            'publication_year': 2023
        })
        
        # Should fail due to missing CSRF token
        self.assertEqual(response.status_code, 403)
    
    def test_csrf_protection_with_token(self):
        """Test that requests with valid CSRF tokens work."""
        self.client.login(username='admin_test', password='secure_password_123')
        
        # Get CSRF token
        response = self.client.get(reverse('book_create'))
        csrf_token = get_token(response.wsgi_request)
        
        # Make request with CSRF token
        response = self.client.post(reverse('book_create'), {
            'title': 'Valid CSRF Book',
            'author': 'Valid Author',
            'publication_year': 2023,
            'csrfmiddlewaretoken': csrf_token
        })
        
        # Should redirect on success
        self.assertIn(response.status_code, [200, 302])
    
    def test_xss_prevention_in_forms(self):
        """Test that XSS attempts in forms are prevented."""
        self.client.login(username='admin_test', password='secure_password_123')
        
        # Try to inject script tag
        xss_payload = '<script>alert("XSS")</script>'
        
        response = self.client.get(reverse('book_create'))
        csrf_token = get_token(response.wsgi_request)
        
        response = self.client.post(reverse('book_create'), {
            'title': xss_payload,
            'author': 'Test Author',
            'publication_year': 2023,
            'csrfmiddlewaretoken': csrf_token
        })
        
        # Form should reject the input
        self.assertContains(response, 'invalid characters', status_code=200)
    
    def test_sql_injection_prevention(self):
        """Test that SQL injection attempts are prevented."""
        self.client.login(username='admin_test', password='secure_password_123')
        
        # Try SQL injection in search
        sql_injection_payload = "'; DROP TABLE bookshelf_book; --"
        
        response = self.client.get(reverse('book_list'), {
            'search_query': sql_injection_payload,
            'search_type': 'title'
        })
        
        # Should not cause any database errors
        self.assertEqual(response.status_code, 200)
        
        # Books table should still exist
        self.assertTrue(Book.objects.exists())
    
    def test_permission_based_access_control(self):
        """Test that views require proper permissions."""
        # Test without login
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
        
        # Test with user without permissions
        self.client.login(username='regular_test', password='secure_password_123')
        response = self.client.get(reverse('book_list'))
        self.assertEqual(response.status_code, 403)  # Permission denied
    
    def test_secure_headers_present(self):
        """Test that security headers are present in responses."""
        self.client.login(username='admin_test', password='secure_password_123')
        response = self.client.get(reverse('book_list'))
        
        # Check for security headers
        self.assertIn('Content-Security-Policy', response)
        self.assertIn('X-Content-Type-Options', response)
        self.assertIn('X-Frame-Options', response)
        self.assertEqual(response['X-Frame-Options'], 'DENY')
        self.assertEqual(response['X-Content-Type-Options'], 'nosniff')
    
    def test_input_validation(self):
        """Test that form inputs are properly validated."""
        self.client.login(username='admin_test', password='secure_password_123')
        
        response = self.client.get(reverse('book_create'))
        csrf_token = get_token(response.wsgi_request)
        
        # Test with invalid publication year
        response = self.client.post(reverse('book_create'), {
            'title': 'Test Book',
            'author': 'Test Author',
            'publication_year': 3000,  # Future year
            'csrfmiddlewaretoken': csrf_token
        })
        
        # Should show validation error
        self.assertContains(response, 'cannot be in the future')
    
    def test_secure_book_deletion(self):
        """Test that book deletion requires proper permissions and CSRF."""
        # Try to delete without permission
        self.client.login(username='regular_test', password='secure_password_123')
        response = self.client.post(reverse('book_delete', kwargs={'pk': self.test_book.pk}))
        self.assertEqual(response.status_code, 403)  # Permission denied
        
        # Book should still exist
        self.assertTrue(Book.objects.filter(pk=self.test_book.pk).exists())
    
    def test_safe_url_parameters(self):
        """Test that URL parameters are safely handled."""
        self.client.login(username='admin_test', password='secure_password_123')
        
        # Try with invalid book ID
        response = self.client.get(reverse('book_detail', kwargs={'pk': 'invalid'}))
        # Should handle gracefully and redirect
        self.assertIn(response.status_code, [302, 404])
        
        # Try with non-existent book ID
        response = self.client.get(reverse('book_detail', kwargs={'pk': 99999}))
        self.assertEqual(response.status_code, 404)
    
    def test_search_security(self):
        """Test that search functionality is secure."""
        self.client.login(username='admin_test', password='secure_password_123')
        
        # Test with various potentially dangerous inputs
        dangerous_inputs = [
            '<script>alert("xss")</script>',
            'javascript:alert("xss")',
            'data:text/html,<script>alert("xss")</script>',
            '../../etc/passwd',
            'UNION SELECT * FROM users',
        ]
        
        for dangerous_input in dangerous_inputs:
            response = self.client.get(reverse('book_list'), {
                'search_query': dangerous_input,
                'search_type': 'all'
            })
            
            # Should not cause errors and should handle safely
            self.assertEqual(response.status_code, 200)
    
    @override_settings(DEBUG=True)
    def test_debug_mode_warning(self):
        """Test that debug mode warnings are displayed appropriately."""
        self.client.login(username='admin_test', password='secure_password_123')
        response = self.client.get(reverse('book_list'))
        
        # Should show debug warning when DEBUG=True
        self.assertContains(response, 'Development Mode')
    
    def test_csp_report_endpoint(self):
        """Test that CSP reporting endpoint exists and works."""
        # CSP report should accept POST requests
        response = self.client.post(reverse('csp_report'), 
                                  data=json.dumps({'csp-report': {'violated-directive': 'script-src'}}),
                                  content_type='application/json')
        
        # Should return 204 No Content
        self.assertEqual(response.status_code, 204)


class FormSecurityTestCase(TestCase):
    """Test security aspects of Django forms."""
    
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username='admin_form_test',
            email='admin@test.com',
            password='secure_password_123'
        )
        self.admin_user.is_staff = True
        self.admin_user.save()
        
        self.client = Client()
        self.client.login(username='admin_form_test', password='secure_password_123')
    
    def test_form_field_validation(self):
        """Test that form fields properly validate input."""
        from bookshelf.forms import BookForm
        
        # Test with valid data
        valid_data = {
            'title': 'Valid Book Title',
            'author': 'Valid Author',
            'publication_year': 2023
        }
        form = BookForm(data=valid_data)
        self.assertTrue(form.is_valid())
        
        # Test with invalid data
        invalid_data = {
            'title': '<script>alert("xss")</script>',
            'author': 'Valid Author',
            'publication_year': 2023
        }
        form = BookForm(data=invalid_data)
        self.assertFalse(form.is_valid())
        self.assertIn('invalid characters', str(form.errors))
    
    def test_search_form_security(self):
        """Test that search form validates input properly."""
        from bookshelf.forms import BookSearchForm
        
        # Test with potentially dangerous search query
        dangerous_data = {
            'search_query': '<script>alert("xss")</script>',
            'search_type': 'all'
        }
        form = BookSearchForm(data=dangerous_data)
        self.assertFalse(form.is_valid())
        self.assertIn('invalid characters', str(form.errors))


class MiddlewareSecurityTestCase(TestCase):
    """Test security middleware functionality."""
    
    def setUp(self):
        self.client = Client()
        self.admin_user = User.objects.create_user(
            username='middleware_test',
            email='middleware@test.com',
            password='secure_password_123'
        )
        self.admin_user.is_staff = True
        self.admin_user.save()
    
    def test_security_headers_middleware(self):
        """Test that security headers middleware adds proper headers."""
        self.client.login(username='middleware_test', password='secure_password_123')
        response = self.client.get(reverse('book_list'))
        
        # Check for required security headers
        expected_headers = [
            'Content-Security-Policy',
            'X-Content-Type-Options',
            'X-Frame-Options',
            'X-XSS-Protection',
            'Referrer-Policy'
        ]
        
        for header in expected_headers:
            self.assertIn(header, response)
    
    def test_request_logging_middleware(self):
        """Test that suspicious requests are logged."""
        # This test would need to check log files in a real implementation
        # For now, just verify the request is handled properly
        response = self.client.get(reverse('book_list') + '?test=<script>alert("xss")</script>')
        self.assertEqual(response.status_code, 302)  # Redirect to login
