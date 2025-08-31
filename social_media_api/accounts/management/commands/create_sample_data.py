from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class Command(BaseCommand):
    help = 'Create sample users for testing the Social Media API'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=5,
            help='Number of sample users to create (default: 5)'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        self.stdout.write(
            self.style.SUCCESS(f'Creating {count} sample users...')
        )
        
        created_users = []
        
        for i in range(1, count + 1):
            username = f'user{i}'
            email = f'user{i}@example.com'
            
            # Check if user already exists
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'User {username} already exists, skipping...')
                )
                continue
            
            # Create user
            user = User.objects.create_user(
                username=username,
                email=email,
                password='testpassword123',
                first_name=f'User{i}',
                last_name='Test',
                bio=f'This is test user number {i} for the Social Media API.'
            )
            
            # Create token for the user
            token, created = Token.objects.get_or_create(user=user)
            
            created_users.append({
                'username': username,
                'email': email,
                'token': token.key
            })
            
            self.stdout.write(
                self.style.SUCCESS(f'Created user: {username}')
            )
        
        # Create some follow relationships
        if len(created_users) >= 2:
            self.stdout.write('\nCreating follow relationships...')
            
            users = User.objects.filter(username__in=[u['username'] for u in created_users])
            
            # Make user1 follow user2, user2 follow user3, etc.
            for i in range(len(users) - 1):
                follower = users[i]
                following = users[i + 1]
                
                # Add follow relationship through the intermediate model
                from accounts.models import Follow
                follow_relation, created = Follow.objects.get_or_create(
                    follower=follower,
                    following=following
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'{follower.username} now follows {following.username}')
                    )
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('Sample data creation completed!'))
        self.stdout.write('\nCreated users and their tokens:')
        self.stdout.write('-'*50)
        
        for user_data in created_users:
            self.stdout.write(f"Username: {user_data['username']}")
            self.stdout.write(f"Email: {user_data['email']}")
            self.stdout.write(f"Password: testpassword123")
            self.stdout.write(f"Token: {user_data['token']}")
            self.stdout.write('-'*30)
        
        self.stdout.write('\nYou can now test the API with these users!')
        self.stdout.write('Example API calls:')
        self.stdout.write('POST /api/login/ with username and password')
        self.stdout.write('GET /api/profile/ with Authorization: Token <token>')
