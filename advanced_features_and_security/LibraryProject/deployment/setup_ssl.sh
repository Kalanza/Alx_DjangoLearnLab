#!/bin/bash
# SSL Certificate Setup Script for LibraryProject
# ===============================================

set -e  # Exit on any error

echo "🔐 Setting up SSL certificates for LibraryProject..."

# Configuration
DOMAIN="yourdomain.com"
EMAIL="admin@yourdomain.com"
WEBROOT="/var/www/libraryproject"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   print_error "This script must be run as root (use sudo)"
   exit 1
fi

# Update system packages
print_status "Updating system packages..."
apt-get update -y

# Install Certbot for Let's Encrypt
print_status "Installing Certbot..."
apt-get install -y certbot python3-certbot-nginx

# Stop web server temporarily
print_status "Stopping web server..."
systemctl stop nginx 2>/dev/null || systemctl stop apache2 2>/dev/null || true

# Obtain SSL certificate using Let's Encrypt
print_status "Obtaining SSL certificate for $DOMAIN..."
certbot certonly \
    --standalone \
    --email $EMAIL \
    --agree-tos \
    --no-eff-email \
    --domains $DOMAIN,www.$DOMAIN

# Create certificate directory structure
print_status "Setting up certificate directories..."
mkdir -p /etc/ssl/certs/
mkdir -p /etc/ssl/private/

# Copy certificates to standard locations
print_status "Copying certificates to standard locations..."
cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem /etc/ssl/certs/$DOMAIN.crt
cp /etc/letsencrypt/live/$DOMAIN/privkey.pem /etc/ssl/private/$DOMAIN.key

# Set proper permissions
print_status "Setting certificate permissions..."
chmod 644 /etc/ssl/certs/$DOMAIN.crt
chmod 600 /etc/ssl/private/$DOMAIN.key
chown root:root /etc/ssl/certs/$DOMAIN.crt
chown root:root /etc/ssl/private/$DOMAIN.key

# Create auto-renewal script
print_status "Setting up automatic certificate renewal..."
cat > /etc/cron.d/certbot-renew << EOF
# Automatically renew Let's Encrypt certificates
0 3 * * * root certbot renew --quiet --post-hook "systemctl reload nginx || systemctl reload apache2"
EOF

# Generate strong DH parameters (for enhanced security)
print_status "Generating DH parameters (this may take a while)..."
openssl dhparam -out /etc/ssl/certs/dhparam.pem 2048
chmod 644 /etc/ssl/certs/dhparam.pem

# Create backup script
print_status "Creating certificate backup script..."
cat > /usr/local/bin/backup-ssl-certs.sh << 'EOF'
#!/bin/bash
# SSL Certificate Backup Script
BACKUP_DIR="/backup/ssl-certificates"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR
tar -czf $BACKUP_DIR/ssl-certs-$DATE.tar.gz /etc/letsencrypt/ /etc/ssl/certs/ /etc/ssl/private/

# Keep only last 30 days of backups
find $BACKUP_DIR -name "ssl-certs-*.tar.gz" -mtime +30 -delete

echo "SSL certificates backed up to $BACKUP_DIR/ssl-certs-$DATE.tar.gz"
EOF

chmod +x /usr/local/bin/backup-ssl-certs.sh

# Add weekly backup to cron
echo "0 2 * * 0 root /usr/local/bin/backup-ssl-certs.sh" >> /etc/cron.d/ssl-backup

# Test certificate validity
print_status "Testing certificate validity..."
openssl x509 -in /etc/ssl/certs/$DOMAIN.crt -text -noout | grep -E "Subject:|Issuer:|Not After:"

# Start web server
print_status "Starting web server..."
systemctl start nginx 2>/dev/null || systemctl start apache2 2>/dev/null || true

print_status "✅ SSL certificate setup completed!"
print_warning "Remember to:"
print_warning "1. Update your Django settings: USE_HTTPS=True"
print_warning "2. Configure your web server with the provided config files"
print_warning "3. Test HTTPS access: https://$DOMAIN"
print_warning "4. Check SSL rating: https://www.ssllabs.com/ssltest/"

echo ""
print_status "Certificate locations:"
echo "  Certificate: /etc/ssl/certs/$DOMAIN.crt"
echo "  Private Key: /etc/ssl/private/$DOMAIN.key"
echo "  DH Params:   /etc/ssl/certs/dhparam.pem"
echo ""
print_status "Auto-renewal is configured to run daily at 3 AM"
print_status "Certificate backups will run weekly on Sunday at 2 AM"
