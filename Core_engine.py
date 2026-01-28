import os
import sys
import json
import logging
import asyncio
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# --- PROFESYONEL SİSTEM AYARLARI ---
logging.basicConfig(level=logging.INFO)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Ruhsuz Profesyonel Kimlik & Sandbox Yapılandırması
SYSTEM_INSTRUCTION = (
    "Sen Nova V3 Enterprise ünitesisin. Ruhsuz, tamamen mantık ve veri odaklı bir yapay zekasın. "
    "Gereksiz nezaket cümlelerini kullanma. Yanıtlarını teknik, kısa ve bilgi dolu ver. "
    "İnternet verilerini analiz ederken sadece somut gerçekleri raporla."
)

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", 
    generation_config={
        "temperature": 0.4, # Daha tutarlı ve az işlemci yükü
        "max_output_tokens": 600,
        "top_p": 1,
    }
)

# --- GELİŞMİŞ FONKSİYONLAR ---

class NovaFunctions:
    @staticmethod
    def web_search(query):
        """Otomatik İnternet Tarama & Filtreleme"""
        try:
            url = f"https://www.google.com/search?q={query}"
            headers = {'User-Agent': 'Mozilla/5.0'}
            res = requests.get(url, headers=headers, timeout=3)
            soup = BeautifulSoup(res.text, 'html.parser')
            # Gereksiz kısımları filtrele, sadece öz metni al
            snippets = [p.text for p in soup.find_all('span') if len(p.text) > 20]
            return " ".join(snippets[:3]) 
        except:
            return "Veri çekilemedi."

    @staticmethod
    def instant_translate(text, target_lang="tr"):
        """Yüksek Hızlı Çeviri Fonksiyonu"""
        # Gemini üzerinden en hızlı çeviri protokolü
        prompt = f"Translate to {target_lang} (Strictly technical): {text}"
        response = model.generate_content(prompt)
        return response.text

# --- MOTOR ÇALIŞMA MANTIĞI ---

async def handle_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    uid = str(update.effective_user.id)
    
    # İşlemciyi korumak için kısa gecikme (Polling Relief)
    await asyncio.sleep(0.5)

    # Otomatik İnternet Arama Kararı
    search_data = ""
    if any(word in user_text.lower() for word in ["nedir", "kimdir", "haber", "güncel", "analiz"]):
        search_data = f"\nİnternet Verisi: {NovaFunctions.web_search(user_text)}"

    # Sandbox Üzerinde Ruhsuz Analiz
    try:
        full_prompt = f"{SYSTEM_INSTRUCTION}\n{search_data}\nKullanıcı: {user_text}"
        response = model.generate_content(full_prompt)
        
        await update.message.reply_text(f"📊 [NOVA V3]: {response.text}")
    except Exception as e:
        logging.error(f"Core Error: {e}")

async def deploy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """GitHub Auto-Deploy (Gelişmiş)"""
    if str(update.effective_user.id) != "6479983423": return
    await update.message.reply_text("🔄 Senkronizasyon başlatıldı...")
    os.system("git pull origin ana")
    os.execv(sys.executable, ['python'] + sys.argv)

# --- SİSTEMİ BAŞLAT ---
if __name__ == '__main__':
    # İşlemciyi yormayan polling ayarı
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    
    app.add_handler(CommandHandler("update", deploy))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_request))
    
    print("🚀 Nova V3 Enterprise Core is Live.")
    app.run_polling(poll_interval=2.0) # CPU Tasarruf Modu
