from django.db import models

# Create your models here.
class Admin(models.Model):
    admin_id = models.BigIntegerField(verbose_name='admin id')
    link = models.CharField(verbose_name='link', max_length=150)
    bot_token = models.CharField(verbose_name='bot token', max_length=200, blank=True, null=True)
    price = models.IntegerField(verbose_name='kurs narxi')
    
    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Adminlar'


class Card(models.Model):
    photo = models.ImageField(verbose_name='qr code', upload_to='images')
    number = models.DecimalField(verbose_name='karta raqami', max_digits=16, decimal_places=0)
    username = models.CharField(verbose_name='ism-familiya', max_length=150)

    def __str__(self) -> str:
        return self.username
    
    class Meta:
        verbose_name = 'Karta'
        verbose_name_plural = 'Karta'


class Oylik(models.Model):
    user = models.CharField(verbose_name='foydalanuvchi', max_length=200)
    user_id = models.BigIntegerField(verbose_name='telegram id')
    gruppa = models.IntegerField(verbose_name='gruppa')
    status = models.DecimalField(max_digits=1, decimal_places=0, verbose_name='status')
    narx = models.IntegerField(verbose_name='narx')
    date = models.IntegerField(verbose_name='sana')
    info = models.DecimalField(max_digits=1, decimal_places=0, verbose_name='malumot')
    month = models.IntegerField(verbose_name='oy')

    def __str__(self) -> str:
        return self.user
    
    class Meta:
        verbose_name = "Oylik"
        verbose_name_plural = "Oyliklar"


class Gruppa(models.Model):
    name = models.CharField(verbose_name='gruppa nomi', max_length=100)
    group_id = models.BigIntegerField(verbose_name='gruppa id')

    def __str__(self) -> str:
        return self.name
    
    class Meta:
        verbose_name = 'Gruppa'
        verbose_name_plural = 'Gruppalar'


class People(models.Model):
    user_id = models.BigIntegerField(verbose_name='telegram id')
    username = models.CharField(verbose_name='username', max_length=100)
    fullname = models.CharField(verbose_name='ism-familiya', max_length=100)
    phone = models.DecimalField(verbose_name='tel raqam', max_digits=13, decimal_places=0)
    gruppa = models.CharField(max_length=100, verbose_name='gruppa')
    start = models.CharField(verbose_name='start bot', max_length=10)
    toifa = models.TextField(verbose_name='toifa')
    birthday = models.CharField(max_length=10, verbose_name="tug'ilgan sana")
    region = models.CharField(verbose_name='yashash hududi', max_length=20)
    second_phone = models.DecimalField(verbose_name="qo'shimcha tel", max_digits=13, decimal_places=0, null=True, blank=True)
    age = models.IntegerField(verbose_name='yosh')
    goal = models.TextField(verbose_name='maqsad')
    monthly = models.CharField(verbose_name='oylik', max_length=20)

    def __str__(self) -> str:
        return self.username
    
    class Meta:
        verbose_name = "O'quvchi"
        verbose_name_plural = "O'quvchilar"


#! tgdan user ochirish
from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'your_app'

    def ready(self):
        import main.signals  # Bu yerda signalni yuklaymiz

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    telegram_user_id = models.CharField(max_length=255, blank=True, null=True)
