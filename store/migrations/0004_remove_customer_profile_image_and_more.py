# Generated by Django 5.0.3 on 2024-04-08 18:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_alter_customer_managers_customer_date_joined_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='profile_image',
        ),
        migrations.RemoveField(
            model_name='customer',
            name='profile_image_url',
        ),
    ]