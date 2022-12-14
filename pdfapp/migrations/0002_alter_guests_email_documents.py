# Generated by Django 4.1.1 on 2022-09-20 09:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("pdfapp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="guests",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.CreateModel(
            name="Documents",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "uuid",
                    models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
                ),
                ("document", models.FileField(blank=True, default="", upload_to="")),
                (
                    "email",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="guest_user",
                        to="pdfapp.guests",
                    ),
                ),
                (
                    "username",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="doc_user",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
