#!/usr/bin/env python3
"""
HTTPS Security Testing and Validation Script
============================================
This script tests the HTTPS security implementation of the Django LibraryProject.
"""

import os
import sys
import requests
import ssl
import socket
from urllib.parse import urlparse
import json
from datetime import datetime
import subprocess

class HTTPSSecurityTester:
    def __init__(self, base_url):
        self.base_url = base_url.rstrip('/')
        self.domain = urlparse(base_url).netloc
        self.results = {}
        
    def print_header(self, text):
        print(f"\n{'='*60}")
        print(f"🔐 {text}")
        print(f"{'='*60}")
    
    def print_status(self, status, message):
        symbols = {"✅": "PASS", "❌": "FAIL", "⚠️": "WARNING", "ℹ️": "INFO"}
        print(f"{status} {message}")
    
    def test_https_redirect(self):
        """Test that HTTP requests are redirected to HTTPS"""
        self.print_header("Testing HTTPS Redirect")
        
        try:
            http_url = self.base_url.replace('https://', 'http://')
            response = requests.get(http_url, allow_redirects=False, timeout=10)
            
            if response.status_code in [301, 302, 307, 308]:
                location = response.headers.get('Location', '')
                if location.startswith('https://'):
                    self.print_status("✅", f"HTTP redirects to HTTPS ({response.status_code})")
                    self.results['https_redirect'] = True
                else:
                    self.print_status("❌", f"HTTP redirects but not to HTTPS: {location}")
                    self.results['https_redirect'] = False
            else:
                self.print_status("❌", f"HTTP request not redirected (status: {response.status_code})")
                self.results['https_redirect'] = False
                
        except Exception as e:
            self.print_status("❌", f"Error testing HTTP redirect: {e}")
            self.results['https_redirect'] = False
    
    def test_ssl_certificate(self):
        """Test SSL certificate validity and configuration"""
        self.print_header("Testing SSL Certificate")
        
        try:
            context = ssl.create_default_context()
            with socket.create_connection((self.domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=self.domain) as ssock:
                    cert = ssock.getpeercert()
                    
                    # Check certificate validity
                    not_after = datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    days_until_expiry = (not_after - datetime.now()).days
                    
                    if days_until_expiry > 30:
                        self.print_status("✅", f"Certificate valid for {days_until_expiry} days")
                        self.results['cert_validity'] = True
                    elif days_until_expiry > 0:
                        self.print_status("⚠️", f"Certificate expires in {days_until_expiry} days")
                        self.results['cert_validity'] = True
                    else:
                        self.print_status("❌", "Certificate has expired")
                        self.results['cert_validity'] = False
                    
                    # Check certificate subject
                    subject = dict(x[0] for x in cert['subject'])
                    self.print_status("ℹ️", f"Certificate issued to: {subject.get('commonName', 'Unknown')}")
                    
                    # Check TLS version
                    tls_version = ssock.version()
                    if tls_version in ['TLSv1.2', 'TLSv1.3']:
                        self.print_status("✅", f"Using secure TLS version: {tls_version}")
                        self.results['tls_version'] = True
                    else:
                        self.print_status("❌", f"Using insecure TLS version: {tls_version}")
                        self.results['tls_version'] = False
                        
        except Exception as e:
            self.print_status("❌", f"Error testing SSL certificate: {e}")
            self.results['cert_validity'] = False
            self.results['tls_version'] = False
    
    def test_security_headers(self):
        """Test presence and configuration of security headers"""
        self.print_header("Testing Security Headers")
        
        try:
            response = requests.get(self.base_url, timeout=10)
            headers = response.headers
            
            # Required security headers
            security_headers = {
                'Strict-Transport-Security': 'HSTS header',
                'X-Content-Type-Options': 'Content type protection',
                'X-Frame-Options': 'Clickjacking protection',
                'X-XSS-Protection': 'XSS protection',
                'Content-Security-Policy': 'CSP header',
                'Referrer-Policy': 'Referrer policy'
            }
            
            header_results = {}
            
            for header, description in security_headers.items():
                if header in headers:
                    self.print_status("✅", f"{description}: {headers[header]}")
                    header_results[header] = True
                else:
                    self.print_status("❌", f"Missing {description}")
                    header_results[header] = False
            
            self.results['security_headers'] = header_results
            
            # Check HSTS configuration
            hsts = headers.get('Strict-Transport-Security', '')
            if 'max-age=' in hsts and 'includeSubDomains' in hsts:
                self.print_status("✅", "HSTS properly configured with subdomains")
            elif 'max-age=' in hsts:
                self.print_status("⚠️", "HSTS configured but without subdomains")
            
        except Exception as e:
            self.print_status("❌", f"Error testing security headers: {e}")
            self.results['security_headers'] = {}
    
    def test_cookie_security(self):
        """Test cookie security configuration"""
        self.print_header("Testing Cookie Security")
        
        try:
            # Make a request that might set cookies
            session = requests.Session()
            response = session.get(f"{self.base_url}/admin/login/", timeout=10)
            
            secure_cookies = 0
            httponly_cookies = 0
            total_cookies = 0
            
            for cookie in session.cookies:
                total_cookies += 1
                if cookie.secure:
                    secure_cookies += 1
                if hasattr(cookie, 'has_nonstandard_attr') and cookie.has_nonstandard_attr('HttpOnly'):
                    httponly_cookies += 1
            
            if total_cookies > 0:
                if secure_cookies == total_cookies:
                    self.print_status("✅", f"All {total_cookies} cookies are secure")
                    self.results['secure_cookies'] = True
                else:
                    self.print_status("❌", f"Only {secure_cookies}/{total_cookies} cookies are secure")
                    self.results['secure_cookies'] = False
                
                if httponly_cookies == total_cookies:
                    self.print_status("✅", f"All {total_cookies} cookies are HttpOnly")
                    self.results['httponly_cookies'] = True
                else:
                    self.print_status("⚠️", f"Only {httponly_cookies}/{total_cookies} cookies are HttpOnly")
                    self.results['httponly_cookies'] = False
            else:
                self.print_status("ℹ️", "No cookies found to test")
                self.results['secure_cookies'] = True
                self.results['httponly_cookies'] = True
                
        except Exception as e:
            self.print_status("❌", f"Error testing cookie security: {e}")
            self.results['secure_cookies'] = False
            self.results['httponly_cookies'] = False
    
    def test_form_csrf_protection(self):
        """Test CSRF protection on forms"""
        self.print_header("Testing CSRF Protection")
        
        try:
            # Test a form endpoint
            response = requests.get(f"{self.base_url}/bookshelf/books/create/", timeout=10)
            
            if 'csrfmiddlewaretoken' in response.text:
                self.print_status("✅", "CSRF tokens found in forms")
                self.results['csrf_protection'] = True
            else:
                self.print_status("❌", "No CSRF tokens found in forms")
                self.results['csrf_protection'] = False
                
        except Exception as e:
            self.print_status("⚠️", f"Could not test CSRF protection: {e}")
            self.results['csrf_protection'] = None
    
    def test_mixed_content(self):
        """Test for mixed content issues"""
        self.print_header("Testing for Mixed Content")
        
        try:
            response = requests.get(self.base_url, timeout=10)
            content = response.text.lower()
            
            # Look for HTTP resources in HTTPS page
            http_resources = []
            for resource_type in ['src="http://', 'href="http://', 'action="http://']:
                if resource_type in content:
                    http_resources.append(resource_type)
            
            if http_resources:
                self.print_status("❌", f"Mixed content found: {', '.join(http_resources)}")
                self.results['mixed_content'] = False
            else:
                self.print_status("✅", "No mixed content detected")
                self.results['mixed_content'] = True
                
        except Exception as e:
            self.print_status("❌", f"Error testing mixed content: {e}")
            self.results['mixed_content'] = False
    
    def generate_report(self):
        """Generate a summary report"""
        self.print_header("Security Test Summary")
        
        total_tests = len([v for v in self.results.values() if v is not None])
        passed_tests = len([v for v in self.results.values() if v is True])
        
        print(f"\n📊 Overall Score: {passed_tests}/{total_tests} tests passed")
        
        if passed_tests == total_tests:
            print("🎉 Excellent! All security tests passed.")
        elif passed_tests >= total_tests * 0.8:
            print("👍 Good security implementation with minor issues.")
        elif passed_tests >= total_tests * 0.6:
            print("⚠️ Moderate security - improvements needed.")
        else:
            print("🚨 Poor security - immediate action required!")
        
        # Detailed results
        print(f"\n📋 Detailed Results:")
        for test, result in self.results.items():
            status = "✅ PASS" if result else "❌ FAIL" if result is False else "⚠️ SKIP"
            print(f"  {status} {test.replace('_', ' ').title()}")
        
        # Save results to file
        report_file = f"https_security_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'target_url': self.base_url,
                'results': self.results,
                'score': f"{passed_tests}/{total_tests}"
            }, f, indent=2)
        
        print(f"\n💾 Report saved to: {report_file}")
    
    def run_all_tests(self):
        """Run all security tests"""
        print(f"🔐 Starting HTTPS Security Tests for: {self.base_url}")
        print(f"🕒 Test started at: {datetime.now()}")
        
        self.test_https_redirect()
        self.test_ssl_certificate()
        self.test_security_headers()
        self.test_cookie_security()
        self.test_form_csrf_protection()
        self.test_mixed_content()
        
        self.generate_report()

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 test_https_security.py <https://yourdomain.com>")
        sys.exit(1)
    
    url = sys.argv[1]
    if not url.startswith('https://'):
        print("❌ URL must start with https://")
        sys.exit(1)
    
    tester = HTTPSSecurityTester(url)
    tester.run_all_tests()

if __name__ == "__main__":
    main()
