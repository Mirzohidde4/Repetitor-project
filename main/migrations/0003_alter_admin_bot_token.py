# Generated by Django 5.1 on 2024-10-08 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_admin_options_alter_admin_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin',
            name='bot_token',
            field=models.CharField(max_length=200, verbose_name='bot token'),
        ),
    ]
