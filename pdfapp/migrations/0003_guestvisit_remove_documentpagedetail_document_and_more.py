# Generated by Django 4.1.1 on 2022-09-22 13:43

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("pdfapp", "0002_documentpagedetail_document_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="GuestVisit",
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
                ("viewed_time", models.IntegerField(default=0)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.RemoveField(model_name="documentpagedetail", name="document",),
        migrations.RemoveField(model_name="documentpagedetail", name="email",),
        migrations.RemoveField(model_name="documentpagedetail", name="username",),
        migrations.RemoveField(model_name="document", name="email",),
        migrations.RemoveField(model_name="document", name="total_time",),
        migrations.DeleteModel(name="DocumentDetail",),
        migrations.DeleteModel(name="DocumentPageDetail",),
        migrations.AddField(
            model_name="guestvisit",
            name="document",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="document_viewed",
                to="pdfapp.document",
            ),
        ),
        migrations.AddField(
            model_name="guestvisit",
            name="email",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="guest_view",
                to="pdfapp.guest",
            ),
        ),
    ]
