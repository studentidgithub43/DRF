# Generated by Django 4.1.1 on 2022-09-23 05:20

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("pdfapp", "0005_remove_guestvisit_document_guestvisit_doc_id"),
    ]

    operations = [
        migrations.CreateModel(
            name="DocumentPageVisit",
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
                ("page_num", models.IntegerField(default=0)),
                ("time_spent", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "doc_id",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="document_page_view",
                        to="pdfapp.document",
                    ),
                ),
                (
                    "email",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="guest_page_view",
                        to="pdfapp.guest",
                    ),
                ),
            ],
        ),
    ]