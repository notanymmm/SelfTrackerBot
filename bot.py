import telebot
import gspread
import os
import json
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime

# --- Telegram Bot Token từ biến môi trường ---
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# --- Kết nối Google Sheets từ GOOGLE_CREDS ---
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

google_creds_json = os.getenv("GOOGLE_CREDS")
creds_dict = json.loads(google_creds_json)
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)

client = gspread.authorize(creds)
sheet = client.open("Ghi chép hằng ngày").sheet1

# --- Lệnh /start ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Chào bạn! Gửi theo cú pháp: nội dung | phân loại (Sức khỏe / Học tập / Trao dồi thêm kỹ năng)")

# --- Nhận dữ liệu ---
@bot.message_handler(func=lambda message: True)
def save_to_sheet(message):
    try:
        parts = message.text.split("|")
        if len(parts) != 2:
            bot.reply_to(message, "Sai cú pháp! Gửi: nội dung | phân loại")
            return
        
        noi_dung = parts[0].strip()
        phan_loai = parts[1].strip()

        if phan_loai not in ["Sức khỏe", "Học tập", "Trao dồi thêm kỹ năng"]:
            bot.reply_to(message, "Phân loại không hợp lệ!")
            return

        thoi_gian = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sheet.append_row([thoi_gian, noi_dung, phan_loai])
        bot.reply_to(message, "✅ Đã lưu thành công!")
    except Exception as e:
        bot.reply_to(message, f"Lỗi: {e}")

# --- Chạy bot ---
bot.polling()

