"""
Custom security middleware for the LibraryProject.
Implements additional security headers and Content Security Policy (CSP).
"""
import logging

logger = logging.getLogger('security')


class SecurityHeadersMiddleware:
    """
    Middleware to add security headers to all responses.
    Implements multiple layers of security protection.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Add security headers
        self.add_security_headers(response)
        
        return response
    
    def add_security_headers(self, response):
        """
        Add comprehensive security headers to the response.
        Implements HTTPS-aware security headers for maximum protection.
        """
        from django.conf import settings
        
        # Content Security Policy - Prevent XSS attacks
        csp_directives = [
            "default-src 'self'",
            "script-src 'self'",
            "style-src 'self' 'unsafe-inline'",  # Allow inline styles for basic styling
            "img-src 'self' data:",
            "font-src 'self'",
            "connect-src 'self'",
            "frame-src 'none'",
            "object-src 'none'",
            "base-uri 'self'",
            "form-action 'self'"
        ]
        
        # Add upgrade-insecure-requests only if HTTPS is enabled
        if getattr(settings, 'SECURE_SSL_REDIRECT', False):
            csp_directives.append("upgrade-insecure-requests")
        
        response['Content-Security-Policy'] = "; ".join(csp_directives)
        
        # Core Security Headers
        response['X-Content-Type-Options'] = 'nosniff'  # Prevent MIME type sniffing
        response['X-Frame-Options'] = 'DENY'  # Prevent clickjacking
        response['X-XSS-Protection'] = '1; mode=block'  # Enable XSS filtering
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'  # Control referrer info
        
        # Feature Policy / Permissions Policy - Disable unnecessary browser features
        permissions_policy = [
            'geolocation=()',
            'camera=()',
            'microphone=()',
            'payment=()',
            'usb=()',
            'magnetometer=()',
            'accelerometer=()',
            'gyroscope=()'
        ]
        response['Permissions-Policy'] = ', '.join(permissions_policy)
        
        # HTTPS-specific headers
        if getattr(settings, 'SECURE_SSL_REDIRECT', False):
            # Strict Transport Security (HSTS) - Force HTTPS
            hsts_max_age = getattr(settings, 'SECURE_HSTS_SECONDS', 31536000)
            hsts_header = f'max-age={hsts_max_age}'
            
            if getattr(settings, 'SECURE_HSTS_INCLUDE_SUBDOMAINS', False):
                hsts_header += '; includeSubDomains'
            
            if getattr(settings, 'SECURE_HSTS_PRELOAD', False):
                hsts_header += '; preload'
            
            response['Strict-Transport-Security'] = hsts_header
            
            # Expect-CT header for certificate transparency
            response['Expect-CT'] = 'max-age=86400, enforce'
        
        # Cache control for sensitive pages
        request_path = getattr(response, 'url', '')
        if any(path in str(request_path) for path in ['/admin/', '/book/', '/accounts/']):
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, private'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        else:
            # For static content, allow caching but require revalidation
            response['Cache-Control'] = 'public, max-age=3600, must-revalidate'
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'


class CSPReportingMiddleware:
    """
    Middleware to handle Content Security Policy violation reports.
    Helps monitor and improve application security.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Add CSP reporting directive in development/testing
        if hasattr(request, 'user') and request.user.is_staff:
            existing_csp = response.get('Content-Security-Policy', '')
            if existing_csp and 'report-uri' not in existing_csp:
                response['Content-Security-Policy'] = existing_csp + "; report-uri /csp-report/"
        
        return response


class RequestLoggingMiddleware:
    """
    Security-focused request logging middleware.
    Logs potentially suspicious activities for security monitoring.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Log suspicious patterns
        self.log_suspicious_requests(request)
        
        response = self.get_response(request)
        
        # Log failed authentication attempts
        if response.status_code in [401, 403]:
            logger.warning(f'Access denied: {request.method} {request.path} from {self.get_client_ip(request)}')
        
        return response
    
    def log_suspicious_requests(self, request):
        """
        Log requests that might be security threats.
        """
        suspicious_patterns = [
            'script', 'javascript:', 'data:', 'vbscript:',
            '<script', '</script>', 'eval(', 'alert(',
            'onload=', 'onerror=', 'onclick=',
            'union select', 'drop table', 'insert into'
        ]
        
        # Check for suspicious patterns in request data
        request_data = str(request.GET) + str(request.POST if hasattr(request, 'POST') else '')
        for pattern in suspicious_patterns:
            if pattern.lower() in request_data.lower():
                logger.warning(f'Suspicious request pattern "{pattern}" detected: {request.method} {request.path} from {self.get_client_ip(request)}')
                break
    
    def get_client_ip(self, request):
        """
        Get the client's IP address, considering proxy headers.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
