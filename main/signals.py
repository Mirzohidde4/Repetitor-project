from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
import requests

@receiver(post_delete, sender=User)
def kick_user_from_telegram(sender, instance, **kwargs):
    # Telegram bot va chat ma'lumotlarini oling
    BOT_TOKEN = 'YOUR_BOT_TOKEN'
    CHAT_ID = 'YOUR_CHAT_ID'
    
    # Telegram foydalanuvchi ID (user_id) ni qanday olish sizning loyihangizga bog'liq
    # Bu yerda biz User modeliga 'telegram_user_id' maydoni qo'shilgan deb taxmin qilamiz
    telegram_user_id = instance.telegram_user_id
    
    # URLni tuzing
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/kickChatMember?chat_id={CHAT_ID}&user_id={telegram_user_id}"
    
    # So'rovni yuboring
    response = requests.get(url)
    
    if response.status_code == 200:
        print(f"Foydalanuvchi {telegram_user_id} Telegram guruhidan chiqarildi.")
    else:
        print(f"Xatolik yuz berdi: {response.text}")
