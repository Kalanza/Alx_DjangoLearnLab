# Django REST API Deployment Guide

## 1. Prepare for Production
- Set `DEBUG = False` in `settings.py` (now controlled by `DJANGO_DEBUG` env var)
- Set `ALLOWED_HOSTS` to your domain or server IP (via `DJANGO_ALLOWED_HOSTS`)
- Set a strong `SECRET_KEY` in your environment variables
- Enable security settings: SSL redirect, secure cookies, XSS filter, etc.
- Use a production database (e.g., PostgreSQL)

## 2. Static and Media Files
- Run `python manage.py collectstatic` before deployment
- Serve static files from `/staticfiles` (Heroku does this automatically with WhiteNoise or via Nginx)
- For media files, use a cloud storage solution (e.g., AWS S3) in production

## 3. Deployment to Heroku (Example)
1. Install Heroku CLI and log in
2. Create a new Heroku app: `heroku create your-app-name`
3. Set environment variables:
   ```sh
   heroku config:set DJANGO_DEBUG=False DJANGO_ALLOWED_HOSTS=yourdomain.com DJANGO_SECRET_KEY=your-secret-key
   ```
4. Add a PostgreSQL database: `heroku addons:create heroku-postgresql:hobby-dev`
5. Push your code:
   ```sh
   git add .
   git commit -m "Prepare for production deployment"
   git push heroku main
   ```
6. Run migrations and collectstatic:
   ```sh
   heroku run python manage.py migrate
   heroku run python manage.py collectstatic --noinput
   ```
7. Open your app: `heroku open`

## 4. Gunicorn and Web Server
- The `Procfile` uses Gunicorn to serve your app: `web: gunicorn social_media_api.wsgi --log-file -`
- For custom servers (AWS, DigitalOcean), use Nginx as a reverse proxy to Gunicorn or uWSGI

## 5. Environment Variables
- Use `.env` or Heroku config vars for all secrets and production settings
- Example: see `.env.example`

## 6. Monitoring and Maintenance
- Use Heroku dashboard or a tool like Sentry for error monitoring
- Regularly update dependencies and apply security patches
- Back up your database and media files

## 7. Final Testing
- Test all endpoints in production
- Check static/media file serving
- Ensure HTTPS is enforced
- Validate user registration, login, posts, comments, likes, follows, and notifications

---

**For AWS, DigitalOcean, or other platforms, adapt the above steps to your provider’s documentation.**

---

## Example Live URL
- (Replace with your deployed app URL)
- https://your-app-name.herokuapp.com/
