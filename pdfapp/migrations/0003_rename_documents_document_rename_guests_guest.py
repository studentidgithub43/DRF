# Generated by Django 4.1.1 on 2022-09-20 09:32

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("pdfapp", "0002_alter_guests_email_documents"),
    ]

    operations = [
        migrations.RenameModel(old_name="Documents", new_name="Document",),
        migrations.RenameModel(old_name="Guests", new_name="Guest",),
    ]
