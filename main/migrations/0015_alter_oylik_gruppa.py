# Generated by Django 5.1.2 on 2024-10-16 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_people_gruppa_id_alter_oylik_gruppa_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='oylik',
            name='gruppa',
            field=models.CharField(max_length=100, verbose_name='gruppa'),
        ),
    ]
