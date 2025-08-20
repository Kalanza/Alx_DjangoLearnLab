# 🚀 Django LibraryProject - Production HTTPS Deployment Guide

## 📋 Pre-Deployment Checklist

Before deploying your Django LibraryProject with HTTPS security, ensure you have:

- [ ] A registered domain name pointing to your server
- [ ] A VPS or dedicated server with root/sudo access
- [ ] Python 3.8+ installed
- [ ] Nginx or Apache web server
- [ ] A valid email address for SSL certificate registration

## 🛠️ Step-by-Step Deployment Instructions

### Step 1: Server Preparation

```bash
# Update your server
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3 python3-pip python3-venv nginx certbot python3-certbot-nginx git

# Create application directory
sudo mkdir -p /var/www/libraryproject
cd /var/www/libraryproject

# Clone your project (replace with your repository)
sudo git clone https://github.com/yourusername/libraryproject.git .
sudo chown -R www-data:www-data /var/www/libraryproject
```

### Step 2: Virtual Environment Setup

```bash
# Create virtual environment
sudo -u www-data python3 -m venv venv

# Activate virtual environment
sudo -u www-data /var/www/libraryproject/venv/bin/pip install --upgrade pip

# Install dependencies
sudo -u www-data /var/www/libraryproject/venv/bin/pip install -r requirements.txt
```

### Step 3: Environment Configuration

```bash
# Copy production environment file
sudo cp deployment/.env.production /var/www/libraryproject/.env

# Edit environment variables
sudo nano /var/www/libraryproject/.env
```

**Update the following in your `.env` file:**
```bash
DEBUG=False
USE_HTTPS=True
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SECRET_KEY=your-super-secure-secret-key-here
DATABASE_URL=sqlite:///var/www/libraryproject/db.sqlite3

# Add your domain
DOMAIN_NAME=yourdomain.com
```

### Step 4: Django Application Setup

```bash
# Navigate to project directory
cd /var/www/libraryproject

# Run Django commands as www-data user
sudo -u www-data /var/www/libraryproject/venv/bin/python manage.py collectstatic --noinput
sudo -u www-data /var/www/libraryproject/venv/bin/python manage.py migrate
sudo -u www-data /var/www/libraryproject/venv/bin/python manage.py check --deploy
```

### Step 5: SSL Certificate Installation

```bash
# Make SSL setup script executable
chmod +x deployment/setup_ssl.sh

# Run SSL setup (replace with your domain and email)
sudo ./deployment/setup_ssl.sh yourdomain.com your-email@yourdomain.com
```

### Step 6: Web Server Configuration

#### For Nginx:

```bash
# Copy Nginx configuration
sudo cp deployment/nginx_https.conf /etc/nginx/sites-available/libraryproject

# Update domain in configuration
sudo sed -i 's/yourdomain.com/your-actual-domain.com/g' /etc/nginx/sites-available/libraryproject

# Enable the site
sudo ln -s /etc/nginx/sites-available/libraryproject /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# Test configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx
```

#### For Apache:

```bash
# Enable required modules
sudo a2enmod ssl rewrite headers

# Copy Apache configuration
sudo cp deployment/apache_https.conf /etc/apache2/sites-available/libraryproject.conf

# Update domain in configuration
sudo sed -i 's/yourdomain.com/your-actual-domain.com/g' /etc/apache2/sites-available/libraryproject.conf

# Enable the site
sudo a2ensite libraryproject.conf
sudo a2dissite 000-default.conf

# Test configuration
sudo apache2ctl configtest

# Restart Apache
sudo systemctl restart apache2
```

### Step 7: Gunicorn Setup

```bash
# Create Gunicorn service file
sudo tee /etc/systemd/system/libraryproject.service > /dev/null << EOF
[Unit]
Description=LibraryProject Django Application
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/libraryproject
Environment="PATH=/var/www/libraryproject/venv/bin"
ExecStart=/var/www/libraryproject/venv/bin/gunicorn --workers 3 --bind unix:/var/www/libraryproject/libraryproject.sock LibraryProject.wsgi:application
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the service
sudo systemctl daemon-reload
sudo systemctl enable libraryproject
sudo systemctl start libraryproject
sudo systemctl status libraryproject
```

### Step 8: Firewall Configuration

```bash
# Configure UFW firewall
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw --force enable
sudo ufw status
```

### Step 9: Security Testing

```bash
# Run security tests
cd /var/www/libraryproject
python3 deployment/test_https_security.py https://yourdomain.com
```

## 🔧 Configuration Files Explained

### Nginx Configuration (`nginx_https.conf`)

The Nginx configuration includes:
- **SSL/TLS Settings:** Modern cipher suites and protocols
- **Security Headers:** Comprehensive security header implementation
- **Static Files:** Efficient serving of CSS, JS, and media files
- **Proxy Settings:** Proper forwarding to Gunicorn application

Key features:
```nginx
# SSL Configuration
ssl_protocols TLSv1.2 TLSv1.3;
ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384;

# Security Headers
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Content-Type-Options nosniff;
add_header X-Frame-Options DENY;
```

### Apache Configuration (`apache_https.conf`)

The Apache configuration provides:
- **Virtual Host Setup:** Separate HTTP and HTTPS configurations
- **SSL Module Configuration:** Secure SSL/TLS settings
- **Security Headers:** Implemented via mod_headers
- **WSGI Integration:** Django application serving

Key features:
```apache
# SSL Configuration
SSLEngine on
SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
SSLCipherSuite ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256

# Security Headers
Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
Header always set X-Content-Type-Options nosniff
```

## 📊 Monitoring and Maintenance

### Daily Checks

```bash
# Check service status
sudo systemctl status libraryproject nginx

# Check SSL certificate expiry
sudo certbot certificates

# Review logs
sudo tail -f /var/log/nginx/error.log
sudo journalctl -u libraryproject -f
```

### Weekly Maintenance

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Check for security updates
sudo unattended-upgrades --dry-run

# Review security logs
sudo grep "Failed\|Error" /var/log/nginx/access.log
```

### Monthly Tasks

```bash
# Renew SSL certificates (automatic with certbot)
sudo certbot renew --dry-run

# Update Django dependencies
cd /var/www/libraryproject
sudo -u www-data /var/www/libraryproject/venv/bin/pip list --outdated

# Run security audit
python3 deployment/test_https_security.py https://yourdomain.com
```

## 🚨 Troubleshooting Guide

### Common Issues and Solutions

#### SSL Certificate Issues

**Problem:** Certificate not working
```bash
# Check certificate status
sudo certbot certificates

# Manually renew if needed
sudo certbot renew --force-renewal
```

#### Nginx/Apache Not Starting

**Problem:** Web server fails to start
```bash
# Check configuration syntax
sudo nginx -t  # For Nginx
sudo apache2ctl configtest  # For Apache

# Check error logs
sudo tail -f /var/log/nginx/error.log
sudo tail -f /var/log/apache2/error.log
```

#### Django Application Errors

**Problem:** 500 Internal Server Error
```bash
# Check Gunicorn service
sudo systemctl status libraryproject

# Check Django logs
sudo journalctl -u libraryproject -n 50

# Check Django settings
cd /var/www/libraryproject
sudo -u www-data /var/www/libraryproject/venv/bin/python manage.py check --deploy
```

#### Security Headers Not Working

**Problem:** Security tests fail
```bash
# Verify middleware in settings.py
grep -n "SecurityHeadersMiddleware" /var/www/libraryproject/LibraryProject/settings.py

# Check web server configuration
curl -I https://yourdomain.com
```

## 📱 Testing Your Deployment

### Quick Verification

```bash
# Test HTTPS redirect
curl -I http://yourdomain.com

# Test SSL certificate
curl -I https://yourdomain.com

# Test security headers
curl -I https://yourdomain.com | grep -E "(Strict-Transport|X-Content|X-Frame)"
```

### Comprehensive Testing

```bash
# Run full security test suite
cd /var/www/libraryproject
python3 deployment/test_https_security.py https://yourdomain.com

# Test Django admin
curl -I https://yourdomain.com/admin/

# Test application endpoints
curl -I https://yourdomain.com/bookshelf/
```

## 🔄 Backup and Recovery

### Create Backup Script

```bash
# Create backup directory
sudo mkdir -p /var/backups/libraryproject

# Create backup script
sudo tee /var/backups/backup_libraryproject.sh > /dev/null << 'EOF'
#!/bin/bash
BACKUP_DIR="/var/backups/libraryproject"
DATE=$(date +%Y%m%d_%H%M%S)

# Backup database
cp /var/www/libraryproject/db.sqlite3 $BACKUP_DIR/db_$DATE.sqlite3

# Backup media files
tar -czf $BACKUP_DIR/media_$DATE.tar.gz /var/www/libraryproject/media/

# Backup configuration
cp /var/www/libraryproject/.env $BACKUP_DIR/env_$DATE.backup

# Clean old backups (keep 30 days)
find $BACKUP_DIR -name "*.sqlite3" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
find $BACKUP_DIR -name "*.backup" -mtime +30 -delete

echo "Backup completed: $DATE"
EOF

# Make executable
sudo chmod +x /var/backups/backup_libraryproject.sh

# Add to crontab for daily backups
echo "0 2 * * * /var/backups/backup_libraryproject.sh" | sudo crontab -
```

## 🎉 Deployment Complete!

Your Django LibraryProject is now securely deployed with HTTPS! 

### Next Steps:

1. **Monitor Performance:** Set up monitoring tools like New Relic or DataDog
2. **Regular Updates:** Keep Django and dependencies updated
3. **Security Audits:** Perform regular security assessments
4. **Backup Testing:** Regularly test your backup and recovery procedures

### Useful Commands for Management:

```bash
# Restart all services
sudo systemctl restart libraryproject nginx

# View real-time logs
sudo journalctl -u libraryproject -f

# Check disk usage
df -h

# Monitor system resources
htop
```

---

**Remember:** Security is an ongoing process. Regularly review and update your security measures to protect against new threats.

For additional support, refer to the [Django deployment documentation](https://docs.djangoproject.com/en/stable/howto/deployment/) and the [Security Implementation Guide](SECURITY_IMPLEMENTATION_GUIDE.md).
