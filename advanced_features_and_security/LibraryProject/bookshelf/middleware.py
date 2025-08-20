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
        """
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
            "form-action 'self'",
            "upgrade-insecure-requests"
        ]
        response['Content-Security-Policy'] = "; ".join(csp_directives)
        
        # Additional security headers
        response['X-Content-Type-Options'] = 'nosniff'  # Prevent MIME type sniffing
        response['X-Frame-Options'] = 'DENY'  # Prevent clickjacking
        response['X-XSS-Protection'] = '1; mode=block'  # Enable XSS filtering
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'  # Control referrer info
        response['Permissions-Policy'] = 'geolocation=(), camera=(), microphone=()'  # Disable unnecessary features
        
        # Cache control for sensitive pages
        if hasattr(response, 'url') and any(path in str(response.url) for path in ['/admin/', '/book/']):
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
