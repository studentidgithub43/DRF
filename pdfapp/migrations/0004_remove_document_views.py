# Generated by Django 4.1.1 on 2022-09-22 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pdfapp", "0003_guestvisit_remove_documentpagedetail_document_and_more"),
    ]

    operations = [
        migrations.RemoveField(model_name="document", name="views",),
    ]