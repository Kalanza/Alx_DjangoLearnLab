from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Post

class Command(BaseCommand):
    help = 'Create sample data for the blog'

    def handle(self, *args, **options):
        # Create a test user if it doesn't exist
        if not User.objects.filter(username='testuser').exists():
            user = User.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='testpass123',
                first_name='Test',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS(f'Created user: {user.username}'))
        else:
            user = User.objects.get(username='testuser')
            self.stdout.write(self.style.WARNING(f'User {user.username} already exists'))

        # Create sample posts
        sample_posts = [
            {
                'title': 'Welcome to Django Blog',
                'content': '''Welcome to our amazing Django blog! This is our first post and we're excited to share our journey with you. 
                
                In this blog, you'll find tutorials, tips, and insights about web development, Django framework, and much more. 
                
                Stay tuned for more exciting content!'''
            },
            {
                'title': 'Getting Started with Django',
                'content': '''Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. 
                
                Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel.
                
                Here are some key features of Django:
                - Fast development
                - Security focused
                - Scalable
                - Versatile'''
            },
            {
                'title': 'Authentication in Django',
                'content': '''Django comes with a robust authentication system that handles user accounts, groups, permissions, and cookie-based user sessions.
                
                The authentication system includes:
                - User authentication
                - Permission system
                - User groups
                - Password hashing
                - Form validation
                
                This makes it easy to build secure web applications with user management functionality.'''
            }
        ]

        for post_data in sample_posts:
            if not Post.objects.filter(title=post_data['title']).exists():
                post = Post.objects.create(
                    title=post_data['title'],
                    content=post_data['content'],
                    author=user
                )
                self.stdout.write(self.style.SUCCESS(f'Created post: {post.title}'))
            else:
                self.stdout.write(self.style.WARNING(f'Post "{post_data["title"]}" already exists'))

        self.stdout.write(self.style.SUCCESS('Sample data creation completed!'))
