# Generated by Django 5.1 on 2024-10-09 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_card_options_alter_oylik_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='people',
            name='start',
            field=models.CharField(max_length=10, verbose_name='start bot'),
        ),
    ]
