import telebot
from telebot import types

# === SOZLAMALAR ===
TOKEN = '9019130393:AAEyN2Cv2_BAjS1jonC5eQ1hiZBIMFZCD60'  # BotFather dan olgan yangi token
SITE_URL = 'https://frolicking-sawine-4e5c6f.netlify.app/'  # Sizning saytingiz

bot = telebot.TeleBot(TOKEN)

# === /START BUYRUG'I ===
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Tugmalar yaratish
    markup = types.InlineKeyboardMarkup(row_width=1)
    
    # Saytga o'tish tugmasi (url parametri bilan)
    btn_site = types.InlineKeyboardButton("🌐 Ilovani ochish (Sayt)", url=SITE_URL)
    
    # Boshqa tugmalar (ixtiyoriy)
    btn_help = types.InlineKeyboardButton("💬 Yordam", callback_data="help")
    
    markup.add(btn_site, btn_help)
    
    bot.send_message(
        message.chat.id,
        "Assalomu alaykum! 👋\n\n"
        "KAKNUS Zakaz xizmatiga xush kelibsiz!\n"
        "Buyurtma berish va barcha xizmatlarimizdan foydalanish uchun pastdagi tugmani bosing:",
        reply_markup=markup
    )

# === YORDAM TUGMASI BOSILGANDA ===
@bot.callback_query_handler(func=lambda call: call.data == "help")
def help_handler(call):
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "Savollaringiz bo'lsa, @Abuuciservic ga yozing!")

# === BOTNI ISHGA TUSHIRISH ===
print("✅ Bot ishga tushdi! Sayt tugmasi tayyor.")
bot.infinity_polling()