import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# --- [KRİTİK MÜHÜR] ---
TELEGRAM_TOKEN = "7414902120:AAFeU-1X0L5A60yO8YkC84VjO0WfX8Z7M7M"
GEMINI_API_KEY = "BURAYA_GEMINI_KEYINI_YAZ" # Kendi Key'ini buraya yapıştır
AUTHORIZED_USER_ID = 6479983423

# --- [AI MOTORU: ULTRA HIZ] ---
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", # Hız ve düşük CPU için en iyisi
    system_instruction="Sen Nova V3 Optimus ünitesisin. Ruhsuz, buz gibi soğuk ve %100 profesyonel bir teknik analistsin."
)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Güvenlik Kilidi
    if update.effective_user.id != AUTHORIZED_USER_ID:
        return

    # İşlemci Dostu Yükleme
    status = await update.message.reply_text("<code>[SEKTÖR 25 ANALİZ EDİLİYOR...]</code>", parse_mode='HTML')

    try:
        user_text = update.message.text
        # Asenkron İşleme (Donmayı Engeller)
        response = await asyncio.to_thread(model.generate_content, user_text)
        
        report = f"<b>[OPTIMUS CORE V25]</b>\n\n{response.text}"
        await status.edit_text(report, parse_mode='HTML')
    except Exception as e:
        await status.edit_text(f"⚠️ Sistem Hatası: {str(e)}")

if __name__ == '__main__':
    # İşlemciyi Koruyan Yapılandırma
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("🚀 Optimus Prime V25: Sistem Çevrimiçi")
    # poll_interval=5.0: PythonAnywhere CPU koruması (Tarpit önleyici)
    app.run_polling(poll_interval=5.0, drop_pending_updates=True)
    
