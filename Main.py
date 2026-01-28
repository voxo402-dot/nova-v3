import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# --- [GÜVENLİK VE KİMLİK MÜHÜRÜ] ---
# Profesyonel Düzey: Tokenlar doğrudan sisteme mühürlenmiştir.
TELEGRAM_TOKEN = "7414902120:AAFeU-1X0L5A60yO8YkC84VjO0WfX8Z7M7M"
GEMINI_API_KEY = "BURAYA_GEMINI_API_KEYINI_YAZ" # Kendi Gemini keyini buraya gir
AUTHORIZED_USER_ID = 6479983423 # Sadece neonx45 erişebilir.

# --- [AI MOTORU YAPILANDIRMASI] ---
genai.configure(api_key=GEMINI_API_KEY)
generation_config = {
    "temperature": 0.4, # Stabil ve net yanıtlar
    "top_p": 0.9,
    "max_output_tokens": 1024,
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", # En hızlı ve en az CPU tüketen model
    generation_config=generation_config,
    system_instruction=(
        "Kimlik: Nova V3 Optimus Ünitesi. "
        "Karakter: Buz gibi soğuk, teknik, profesyonel ve duygusuz. "
        "Görev: Kullanıcın neonx45 için veri analizi yap ve rapor sun. "
        "Format: Her yanıtın başında [OPTIMUS CORE V25] etiketi bulunmalı."
    )
)

# --- [SİSTEM MANTIĞI & CPU KORUMA] ---

async def engine_logic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Yetki Kontrolü
    if update.effective_user.id != AUTHORIZED_USER_ID:
        await update.message.reply_text("❌ ERİŞİM ENGELLENDİ: Yetkisiz Giriş.")
        return

    # İşlemci Dostu Yükleme Efekti
    status_msg = await update.message.reply_text("<code>[SEKTÖR 25 TARANIYOR...]</code>", parse_mode='HTML')

    try:
        # Asenkron AI İşleme (Sistemi dondurmaz)
        user_input = update.message.text
        response = await asyncio.to_thread(model.generate_content, user_input)
        
        # Profesyonel Rapor Çıktısı
        final_report = (
            f"<b>--- [OPTIMUS REPORT V25] ---</b>\n\n"
            f"{response.text}\n\n"
            f"<b>--- [DURUM: GÜVENLİ | VERİMLİLİK: %100] ---</b>"
        )
        
        await status_msg.edit_text(final_report, parse_mode='HTML')

    except Exception as e:
        await status_msg.edit_text(f"⚠️ Kritik Hata: {str(e)}")

# --- [ANA ÇALIŞTIRICI] ---

if __name__ == '__main__':
    # Loglama yapılandırması (Hata ayıklama için)
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    
    # Telegram Uygulama Başlatıcı
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    
    # Sadece metin mesajlarını dinleyen verimli handler
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), engine_logic))
    
    print("🚀 Optimus Prime V25: Çekirdek Aktif ve Güvenli")
    
    # PythonAnywhere Tarpit (CPU Sınırı) Koruması: 5 saniyelik sorgu aralığı
    app.run_polling(poll_interval=5.0, drop_pending_updates=True)
    
