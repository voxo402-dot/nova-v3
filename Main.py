import asyncio
import logging
import sys
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# --- [PROFESYONEL YAPILANDIRMA] ---
# Tokenlar doğrudan çekirdeğe mühürlenmiştir
TELEGRAM_TOKEN = "7414902120:AAFeU-1X0L5A60yO8YkC84VjO0WfX8Z7M7M"
GEMINI_API_KEY = "BURAYA_KENDI_API_KEYINI_YAZ" # Gemini Key'ini buraya yapıştır
AUTHORIZED_USER_ID = 6479983423 # Sadece neonx45 erişebilir

# --- [AI MOTORU: ULTRA-HIZ MODU] ---
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", # En düşük CPU tüketimi, en yüksek hız
    system_instruction=(
        "Kimlik: Nova V3 Optimus. Buz gibi soğuk, ruhsuz ve profesyonel. "
        "Format: Yanıtlar teknik rapor şeklinde [SEKTÖR 25] başlığıyla verilir."
    )
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # GÜVENLİK DUVARI: Yetkisiz girişleri anında bloklar
    if update.effective_user.id != AUTHORIZED_USER_ID:
        return

    # ECO-MOD: İşlemciyi yormayan görsel geri bildirim
    status_msg = await update.message.reply_text("<code>[SEKTÖR 25 ANALİZ EDİLİYOR...]</code>", parse_mode='HTML')

    try:
        user_input = update.message.text
        # Asenkron İşleme: Sistemin donmasını ve çökmesini engeller
        response = await asyncio.to_thread(model.generate_content, user_input)
        
        report = f"<b>--- [OPTIMUS REPORT V25] ---</b>\n\n{response.text}\n\n<b>--- [DURUM: GÜVENLİ] ---</b>"
        await status_msg.edit_text(report, parse_mode='HTML')
        
    except Exception as e:
        await status_msg.edit_text(f"⚠️ Kritik Sistem Hatası: {str(e)}")

# --- [ANA MOTOR BAŞLATICI] ---
if __name__ == '__main__':
    # Hata ayıklama loglarını terminale basar
    logging.basicConfig(level=logging.INFO)
    
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("🚀 Optimus Prime V25: Sistem Çevrimiçi")
    
    # poll_interval=5.0: PythonAnywhere Tarpit koruması için kritik bekleme süresi
    app.run_polling(poll_interval=5.0, drop_pending_updates=True)
        
