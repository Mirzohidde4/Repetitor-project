# Generated by Django 5.1.2 on 2024-10-16 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_oylik_gruppa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oylik',
            name='gruppa',
            field=models.BigIntegerField(verbose_name='gruppa'),
        ),
    ]
