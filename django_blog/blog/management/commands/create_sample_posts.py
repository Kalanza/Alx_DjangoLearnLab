from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Post

class Command(BaseCommand):
    help = 'Create sample blog posts'

    def handle(self, *args, **options):
        # Get or create a superuser to be the author
        user, created = User.objects.get_or_create(
            username='author',
            defaults={
                'email': 'author@example.com',
                'first_name': 'Blog',
                'last_name': 'Author'
            }
        )
        if created:
            user.set_password('password123')
            user.save()
            self.stdout.write(self.style.SUCCESS('Created user: author'))

        # Sample posts data
        sample_posts = [
            {
                'title': 'Welcome to Django Blog',
                'content': '''Welcome to our amazing Django blog! This is the first post in our new blog platform. 
                
We've built this blog using Django, a powerful Python web framework that makes it easy to build robust web applications quickly.

In this blog, you'll find articles about web development, Django tutorials, Python tips and tricks, and much more. Stay tuned for exciting content!

Features of this blog:
- Clean and responsive design
- Easy-to-use admin interface
- SEO-friendly URLs
- Comment system (coming soon)
- User authentication
- And much more!

Thank you for visiting, and we hope you enjoy reading our posts!'''
            },
            {
                'title': 'Getting Started with Django',
                'content': '''Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers, it takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel.

Key Features of Django:
1. **Fast Development**: Django was designed to help developers take applications from concept to completion as quickly as possible.

2. **Security**: Django helps developers avoid many common security mistakes by providing a framework that has been engineered to "do the right things" to protect the website automatically.

3. **Scalable**: Some of the busiest sites on the web leverage Django's ability to quickly and flexibly scale.

Getting started with Django is easy. Simply install it using pip and create your first project!

Stay tuned for more Django tutorials and tips!'''
            },
            {
                'title': 'Understanding Django Models',
                'content': '''Models in Django are Python classes that define the structure of your database tables. They're the single, definitive source of information about your data.

A model is the single, definitive source of information about your data. It contains the essential fields and behaviors of the data you're storing. Generally, each model maps to a single database table.

Here's what makes Django models powerful:

**Database Independence**: Django's ORM (Object-Relational Mapping) allows you to work with your database using Python code instead of SQL.

**Automatic Database Schema**: Django can automatically generate database schemas from your models.

**Built-in Admin Interface**: Django can automatically generate a web-based administrative interface for your models.

**Data Validation**: Models include built-in validation to ensure data integrity.

**Relationships**: Django supports various types of relationships between models including one-to-one, one-to-many, and many-to-many.

In our blog, we use a simple Post model that includes fields for title, content, publication date, and author. This demonstrates the basic concepts that you can extend for more complex applications.'''
            }
        ]

        # Create sample posts
        for post_data in sample_posts:
            post, created = Post.objects.get_or_create(
                title=post_data['title'],
                defaults={
                    'content': post_data['content'],
                    'author': user
                }
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created post: {post.title}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Post already exists: {post.title}')
                )

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample posts!')
        )
