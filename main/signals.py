from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import People, Admin, Oylik
import requests

@receiver(post_delete, sender=People)  # User modelidan foydalanuvchi o'chirilganda signal ishga tushadi
def kick_user_from_telegram(sender, instance, **kwargs):
    admi_settings = Admin.objects.first()
    print(instance)
    if admi_settings and admi_settings.bot_token:        
        BOT_TOKEN = admi_settings.bot_token
        CHAT_ID = instance.gruppa   
        telegram_user_id = instance.user_id   
        
        if telegram_user_id:
            url = f"https://api.telegram.org/bot{BOT_TOKEN}/kickChatMember?chat_id={CHAT_ID}&user_id={telegram_user_id}"          
            response = requests.get(url)
            
            if response.status_code == 200:
                print(f"Foydalanuvchi {instance.username} {CHAT_ID} telegram guruhidan chiqarildi.")
            else:
                print(f"Xatolik yuz berdi: {response.status_code}")
        else:
            print("O'chirilgan foydalanuvchining telegram_id topilmadi.")
    else:
        print("Admin sozlamalari yoki bot tokeni topilmadi.")
    
    user_orders = Oylik.objects.filter(user_id=instance.user_id, gruppa=instance.gruppa)  # Foydalanuvchining barcha buyurtmalarini olish
    if user_orders.exists():
        user_orders.delete()  # Buyurtmalarni o'chirish
        print(f"Foydalanuvchi {instance.username} oylikdan o'chirildi.")
    else:
        print(f"Foydalanuvchi {instance.username} oylikdan topilmadi.")    
