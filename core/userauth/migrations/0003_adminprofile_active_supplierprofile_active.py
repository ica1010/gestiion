# Generated by Django 5.0.4 on 2024-06-08 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauth', '0002_alter_user_phone'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminprofile',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='supplierprofile',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
