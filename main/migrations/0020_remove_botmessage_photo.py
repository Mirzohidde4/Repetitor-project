# Generated by Django 5.1.2 on 2024-10-24 13:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0019_remove_admin_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='botmessage',
            name='photo',
        ),
    ]