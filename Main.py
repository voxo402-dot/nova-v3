import os
import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# --- [PROFESYONEL YAPILANDIRMA & GÜVENLİK] ---
TELEGRAM_TOKEN = "7414902120:AAFeU-1X0L5A60yO8YkC84VjO0WfX8Z7M7M"
GEMINI_API_KEY = "BURAYA_GEMINI_KEYINI_YAZ"
AUTHORIZED_USER_ID = 6479983423  # neonx45 Güvenlik Kilidi

# AI Çekirdek Ayarları
genai.configure(api_key=GEMINI_API_KEY)
generation_config = {
    "temperature": 0.3,      
    "top_p": 0.85,
    "max_output_tokens": 1500, 
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", 
    generation_config=generation_config,
    system_instruction=(
        "Sen Nova V3 Optimus ünitesisin. Kimliğin: Buz gibi soğuk, ruhsuz ve %100 teknik profesyonel. "
        "Kullanıcın neonx45 için interneti tarar ve en saf bilgiyi sunarsın. "
        "Yanıtlarını her zaman teknik bir rapor formatında [SEKTÖR 25] başlığıyla ver."
    )
)

# --- [OPTİMİZE EDİLMİŞ MOTOR MANTIĞI] ---

async def engine_logic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ ERİŞİM REDDEDİLDİ: Yetkisiz Terminal.")
        return

    # ECO-MOD: İşlemciyi yormayan düşük seviyeli görsel efekt
    loading = await update.message.reply_text("<code>[ANALİZ EDİLİYOR...]</code>", parse_mode='HTML')

    try:
        # Yapay Zeka İşleme
        user_query = update.message.text
        response = await asyncio.to_thread(model.generate_content, user_query)
        
        report = (
            f"--- <b>[OPTIMUS CORE V25 REPORT]</b> ---\n\n"
            f"{response.text}\n\n"
            f"--- <b>[STATUS: SECURE | CPU: ECO]</b> ---"
        )
        
        await loading.edit_text(report, parse_mode='HTML')

    except Exception as e:
        await loading.edit_text(f"⚠️ Kritik Sistem Hatası: {str(e)}")

# --- [ANA ÇALIŞTIRICI] ---

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), engine_logic))
    
    print("🚀 Optimus Prime V25: Sistem Çevrimiçi")

    app.run_polling(poll_interval=5.0, drop_pending_updates=True)
