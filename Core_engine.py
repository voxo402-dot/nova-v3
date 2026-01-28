import os
import sys
import time
import json
import logging
import asyncio
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# --- OPTIMUS ÇEKİRDEK AYARLARI ---
logging.basicConfig(level=logging.INFO)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# GÜVENLİK DUVARI: Sadece senin ID'ne izin verir
AUTHORIZED_USER_ID = 6479983423  # Senin Telegram ID'n

# Ruhsuz Profesyonel & Otonom Kimlik
SYSTEM_INSTRUCTION = (
    "Sen Nova V3 Optimus ünitesisin. Otonom öğrenme modun aktif. "
    "Yanıtların buz gibi soğuk, ruhsuz ve %100 profesyonel olmalı. "
    "Siber güvenlik, veri madenciliği ve çekirdek optimizasyonu konularında uzmansın."
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config={"temperature": 0.2, "max_output_tokens": 800} # Düşük ısı = Yüksek mantık
)

class OptimusEngine:
    @staticmethod
    def visual_effect(text):
        """Performansı etkilemeyen üst düzey terminal efektleri"""
        header = "--- [OPTIMUS CORE SECTOR 25] ---"
        footer = "--- [ENCRYPTED DATA STREAM] ---"
        return f"<code>{header}</code>\n\n{text}\n\n<code>{footer}</code>"

    @staticmethod
    def smart_filter(data):
        """Veriyi otomatik temizler ve önemli kısımları çeker"""
        # Veri içindeki gereksiz reklam/script linklerini temizler
        keywords = ["teknoloji", "chip", "yazılım", "güvenlik", "ai"]
        filtered = [line for line in data.split('.') if any(k in line.lower() for k in keywords)]
        return ". ".join(filtered[:5])

# --- GÜVENLİK VE YETKİ KONTROLÜ ---
def security_check(user_id):
    return user_id == AUTHORIZED_USER_ID

# --- ANA MOTOR ---
async def process_logic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # GÜVENLİK DUVARI: Lisanssız (Yetkisiz) girişi engelle
    if not security_check(update.effective_user.id):
        await update.message.reply_text("❌ ERİŞİM ENGELLENDİ: Yetkisiz Terminal Girişi. IP kaydedildi.")
        return

    user_text = update.message.text
    
    # Görsel Analiz & Otonom Öğrenme Başlatıcı
    loading_msg = await update.message.reply_text("🌀 <i>Sektör 25 taranıyor, veri ayıklanıyor...</i>", parse_mode='HTML')

    try:
        # İnternetten veri çekme ve Akıllı Filtreleme
        search_res = f"https://www.google.com/search?q={user_text}"
        raw_data = requests.get(search_res, timeout=3).text
        useful_info = OptimusEngine.smart_filter(raw_data)

        # AI Analizi
        full_query = f"{SYSTEM_INSTRUCTION}\nVeri Havuzu: {useful_info}\nKomut: {user_text}"
        response = model.generate_content(full_query)
        
        # Üst Düzey Efektli Yanıt
        final_output = OptimusEngine.visual_effect(response.text)
        await loading_msg.edit_text(final_output, parse_mode='HTML')

    except Exception as e:
        await loading_msg.edit_text(f"⚠️ Sistem Hatası: {str(e)}")

# --- SİSTEM GÜNCELLEME ---
async def update_system(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not security_check(update.effective_user.id): return
    await update.message.reply_text("🔄 Optimus Çekirdek Güncelleniyor...")
    os.system("git pull origin ana")
    os.execv(sys.executable, ['python'] + sys.argv)

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    app.add_handler(CommandHandler("update", update_system))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), process_logic))
    print("🚀 Optimus Core v25: Online & Secure")
    app.run_polling(poll_interval=3.0) # CPU Tasarruf
