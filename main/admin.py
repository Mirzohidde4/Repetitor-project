from django.contrib import admin
from .models import Admin, Card, Oylik, People, Gruppa
from django.contrib.auth.models import User, Group

# Register your models here.
admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('admin_id', 'link', 'bot_token', 'price')


@admin.register(Card)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('photo', 'number', 'username')

    def has_add_permission(self, request):
        if Card.objects.count() >= 1:
            return False
        else:
            return True


@admin.register(Gruppa)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('name', 'group_id')


@admin.register(Oylik)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_id', 'gruppa', 'status', 'narx', 'date', 'info', 'month')


@admin.register(People)
class AdminAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'fullname', 'phone', 'gruppa', 'start', 'toifa', 'birthday', 'region', 'second_phone', 'age', 'goal', 'monthly')
