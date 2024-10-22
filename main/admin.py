from django.contrib import admin, messages
from .models import Admin, Card, Oylik, People, Gruppa, BotButtonInlyne, BotButtonReply, BotMessage
from django.contrib.auth.models import User, Group
from unfold.admin import ModelAdmin
from django.utils.html import format_html

# Register your models here.
admin.site.unregister(User)
admin.site.unregister(Group)


@admin.register(Admin)
class AdminAdmin(ModelAdmin):
    list_display = ('admin_id', 'link', 'bot_token', 'price')

    def has_add_permission(self, request):
        if Card.objects.count() >= 1:
            return False
        else:
            return True


@admin.register(Card)
class AdminCard(ModelAdmin):
    list_display = ('photo', 'number', 'username')

    def has_add_permission(self, request):
        if Card.objects.count() >= 1:
            return False
        else:
            return True


@admin.register(Gruppa)
class AdminGruppa(ModelAdmin):
    list_display = ('name', 'group_id')
    search_fields = ['name']


# @admin.register(Oylik)
# class AdminOylik(ModelAdmin):
#     list_display = ('user', 'user_id', 'gruppa', 'status', 'narx', 'date', 'info', 'month')
#     search_fields = ['user', 'user_id']


@admin.register(People)
class AdminPeople(ModelAdmin):
    list_display = ('fullname', 'phone', 'gruppa','region', 'goal', 'status_monthly')
    search_fields = ['fullname', 'username', 'phone', 'user_id']
    list_filter = ['gruppa', 'monthly']

    def status_monthly(self, obj):
        if obj.monthly == "to'lagan ✅":
            return format_html('<span style="color: green;">{}</span>', obj.monthly)
        elif obj.monthly == "to'lamagan ❌":
            return format_html('<span style="color: red;">{}</span>', obj.monthly)
        else:
            return obj.monthly

    status_monthly.short_description = 'Oylik'


@admin.register(BotMessage)
class AdminMessage(ModelAdmin):
    list_display = ('command', 'text')
    search_fields = ['command']


@admin.register(BotButtonInlyne)
class AdminInline(ModelAdmin):
    list_display = ('message', 'text')
    search_fields = ['message']


@admin.register(BotButtonReply)
class AdminReply(ModelAdmin):
    list_display = ('message', 'text')
    search_fields = ['message']