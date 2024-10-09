from django.contrib import admin
from .models import Admin, Card, Oylik, People, Group

# Register your models here.
@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('admin_id', 'link', 'bot_token', 'group1', 'group2', 'group3', 'price')


@admin.register(Card)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('photo', 'number', 'username')


@admin.register(Group)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('name', 'group_id')


@admin.register(Oylik)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_id', 'gruppa', 'status', 'narx', 'date', 'info', 'month')


@admin.register(People)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'fullname', 'phone', 'start', 'toifa', 'birthday', 'region', 'secodn_phone', 'age', 'goal', 'monthly')
