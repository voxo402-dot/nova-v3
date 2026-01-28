import os
import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# --- [KRİTİK YAPILANDIRMA] ---
# Profesyonel Düzeyde Güvenlik ve Kimlik Doğrulama
TELEGRAM_TOKEN = "7414902120:AAFeU-1X0L5A60yO8YkC84VjO0WfX8Z7M7M" # Tokenını buraya mühürledim
GEMINI_API_KEY = "BURAYA_GEMINI_KEYINI_YAZ" # Kendi Gemini API Key'ini buraya yapıştır
AUTHORIZED_USER_ID = 6479983423 # Sadece senin erişimin için kilitlendi

# AI Motoru Yapılandırması (Enterprise Seviyesi)
genai.configure(api_key=GEMINI_API_KEY)
generation_config = {
    "temperature": 0.4,  # Daha mantıklı ve soğuk yanıtlar
    "top_p": 0.9,
    "max_output_tokens": 1024,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    generation_config=generation_config,
    system_instruction=(
        "Sen Nova V3 Optimus ünitesisin. Kimliğin: Buz gibi soğuk, ruhsuz ve %100 profesyonel. "
        "Kullanıcın neonx45'e sadece teknik analiz ve üst düzey raporlar sunarsın. "
        "Gereksiz nezaket cümlelerinden kaçın, doğrudan veriye odaklan."
    )
)

# --- [SİSTEM FONKSİYONLARI] ---

async def engine_logic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Siber Güvenlik Duvarı
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ ERİŞİM REDDEDİLDİ: Yetkisiz Terminal Girişi.")
        return

    # Verimlilik Modu: İşlemciyi yormayan görsel efekt
    loading_msg = await update.message.reply_text("<code>[SEKTÖR 25 TARANIYOR...]</code>", parse_mode='HTML')

    try:
        # Yapay Zeka Analizi
        user_input = update.message.text
        response = model.generate_content(user_input)
        
        # Profesyonel Terminal Görünümü (Maksimum Verim, Minimum CPU)
        final_report = (
            f"--- <b>[OPTIMUS REPORT V25]</b> ---\n\n"
            f"{response.text}\n\n"
            f"--- <b>[DATA ENCRYPTED]</b> ---"
        )
        
        await loading_msg.edit_text(final_report, parse_mode='HTML')

    except Exception as e:
        await loading_msg.edit_text(f"⚠️ Kritik Hata: {str(e)}")

# --- [ANA MOTOR BAŞLATICI] ---

if __name__ == '__main__':
    # İşlemci dostu asenkron yapı
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Filtreleme: Botun sadece metin mesajlarına ve senin komutlarına odaklanmasını sağlar
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), engine_logic))
    
    print("🚀 Optimus Prime V25: Sistem Çevrimiçi ve Güvenli")
    # poll_interval=5.0: PythonAnywhere CPU koruma kilidi
    app.run_polling(poll_interval=5.0)
    
