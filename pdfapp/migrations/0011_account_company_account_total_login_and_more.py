# Generated by Django 4.1.1 on 2022-09-23 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pdfapp", "0010_remove_account_updated_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="account",
            name="company",
            field=models.CharField(default="", max_length=255),
        ),
        migrations.AddField(
            model_name="account",
            name="total_login",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="account",
            name="total_visit",
            field=models.IntegerField(default=0),
        ),
    ]