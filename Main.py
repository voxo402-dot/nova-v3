import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# --- [SİSTEM YAPILANDIRMASI] ---
TELEGRAM_TOKEN = "7414902120:AAFeU-1X0L5A60yO8YkC84VjO0WfX8Z7M7M"
GEMINI_API_KEY = "BURAYA_KENDI_API_KEYINI_YAZ" # Gemini Key'ini buraya yapıştır
AUTHORIZED_USER_ID = 6479983423

# --- [AI MOTORU: HIZ & VERİMLİLİK] ---
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", # CPU dostu ve hızlı çekirdek
    system_instruction="Sen Nova V3 Optimus ünitesisin. Ruhsuz, buz gibi soğuk ve teknik bir analistsin."
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # GÜVENLİK: Yetkisiz giriş koruması
    if update.effective_user.id != AUTHORIZED_USER_ID:
        return

    # İŞLEMCİ DOSTU GERİ BİLDİRİM
    status = await update.message.reply_text("<code>[SEKTÖR 25 ANALİZ EDİLYOR...]</code>", parse_mode='HTML')

    try:
        user_text = update.message.text
        # ASENKRON İŞLEME: Sistemin donmasını engeller
        response = await asyncio.to_thread(model.generate_content, user_text)
        
        report = f"<b>--- [OPTIMUS REPORT V25] ---</b>\n\n{response.text}"
        await status.edit_text(report, parse_mode='HTML')
    except Exception as e:
        await status.edit_text(f"⚠️ Kritik Hata: {str(e)}")

if __name__ == '__main__':
    # Loglama: Terminalde sistem durumunu izle
    logging.basicConfig(level=logging.INFO)
    
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("🚀 Optimus Prime V25: Sistem Çevrimiçi")
    # poll_interval=5.0: PythonAnywhere Tarpit (yavaşlatma) koruması
    app.run_polling(poll_interval=5.0, drop_pending_updates=True)
    
