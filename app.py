from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
import requests
import os

load_dotenv()

app = Flask(__name__)

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


@app.get("/")
def home():
    return send_from_directory(".", "index.html")


@app.get("/<path:filename>")
def files(filename):
    allowed = {"style.css", "script.js"}
    if filename not in allowed:
        return "Topilmadi", 404
    return send_from_directory(".", filename)


@app.post("/api/order")
def new_order():
    if not BOT_TOKEN or not CHAT_ID:
        return jsonify({"error": "Telegram sozlamalari topilmadi"}), 500

    data = request.get_json(silent=True) or {}

    name = str(data.get("name", "")).strip()
    phone = str(data.get("phone", "")).strip()
    address = str(data.get("address", "")).strip()
    items = data.get("items", [])
    total = data.get("total", 0)

    if not name or not phone or not address or not items:
        return jsonify({"error": "Barcha maydonlarni to‘ldiring"}), 400

    if not isinstance(items, list) or len(items) > 50:
        return jsonify({"error": "Mahsulotlar ro‘yxati noto‘g‘ri"}), 400

    message = (
        "🛍 KAKNUS — YANGI BUYURTMA!\n\n"
        f"👤 Ism: {name}\n"
        f"📞 Telefon: {phone}\n"
        f"📍 Manzil: {address}\n\n"
        "🛒 Mahsulotlar:\n"
    )

    for item in items:
        product = str(item.get("name", "Mahsulot"))[:100]
        quantity = item.get("quantity", 1)
        price = item.get("price", 0)

        message += f"• {product} — {quantity} dona — {price} so‘m\n"

    message += f"\n💰 Jami: {total} so‘m"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:
        response = requests.post(
            url,
            json={"chat_id": CHAT_ID, "text": message},
            timeout=20
        )
        result = response.json()

        if not result.get("ok"):
            return jsonify({"error": "Telegram xabarni yubora olmadi"}), 502

        return jsonify({"success": True, "message": "Buyurtma yuborildi!"})

    except requests.RequestException:
        return jsonify({"error": "Telegram bilan aloqa uzildi"}), 502

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def start(message):
    markup = InlineKeyboardMarkup(row_width=3)
    btn_menu = InlineKeyboardButton("📋 Menu", callback_data="menu")
    btn_order = InlineKeyboardButton("🗓 Order", callback_data="order")
    btn_support = InlineKeyboardButton("📍 Support", callback_data="support")
    
    markup.add(btn_menu, btn_order, btn_support)
    
    bot.send_message(message.chat.id, "Welcome to KAKNUS Zakaz!\nPlease select an option:", reply_markup=markup)
if __name__ == "__main__":
    app.run(debug=False)