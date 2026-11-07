import requests
from getpass import getpass

token = getpass("9187891942:AAFjyTtpzicU1pIM3RJw737zqXlcXTAbHJQ ")

url = f"@KAKNUS_order_bot"
response = requests.get(url, timeout=20)
data = response.json()

if data.get("ok") and data.get("result"):
    message = data["result"][-1].get("message", {})
    chat = message.get("chat", {})
    print("Sizning Chat ID:", chat.get("9187891942:AAFjyTtpzicU1pIM3RJw737zqXlcXTAbHJQ"))
else:
    print("Chat ID topilmadi. Botga /start yuboring va qayta urinib ko‘ring.")