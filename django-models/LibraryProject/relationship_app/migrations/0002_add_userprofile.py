# Generated migration for UserProfile
# This is a replacement for the auto-generated migration

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("relationship_app", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name="author",
            name="author",
        ),
        migrations.AddField(
            model_name="author",
            name="name",
            field=models.CharField(default="Unknown Author", max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="book",
            name="author",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="relationship_app.author",
            ),
        ),
        migrations.AlterField(
            model_name="book",
            name="title",
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name="librarian",
            name="name",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="library",
            name="name",
            field=models.CharField(max_length=200),
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "role",
                    models.CharField(
                        choices=[
                            ("Admin", "Admin"),
                            ("Librarian", "Librarian"),
                            ("Member", "Member"),
                        ],
                        default="Member",
                        max_length=20,
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
