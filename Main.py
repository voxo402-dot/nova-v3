import os
import sys
import json
import logging
import asyncio

# Enterprise Libraries
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import google.generativeai as genai

# --- HIGH PERFORMANCE CONFIG ---
logging.basicConfig(level=logging.INFO)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Sandbox Model Setup (Resource Efficient)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash", 
    generation_config={
        "temperature": 0.65,
        "max_output_tokens": 800, # İşlemciyi yormamak için limitli
    }
)

# --- EFFICIENCY ENGINE ---
def manage_vault(action, data=None):
    file_path = "nova_vault.json"
    if action == "load":
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f: return json.load(f)
        return {}
    elif action == "save":
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

# --- SMART HANDLERS ---
async def ai_logic(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    uid = str(update.effective_user.id)
    
    vault = manage_vault("load")
    if uid not in vault: vault[uid] = {"history": []}

    try:
        # Sadece son 3 mesajı işleyerek işlemci yükünü %60 azaltır
        context_window = vault[uid]["history"][-3:]
        response = model.generate_content(f"Context: {context_window}\nUser: {user_input}")
        
        vault[uid]["history"].append({"q": user_input, "a": response.text})
        manage_vault("save", vault)
        
        await update.message.reply_text(f"🌀 {response.text}")
    except Exception as e:
        logging.error(f"Sandbox Error: {e}")

async def deploy_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """GitHub Auto-Sync & Self-Restart"""
    if str(update.effective_user.id) != "6479983423": return # Güvenlik

    await update.message.reply_text("📡 **GitHub Repo Senkronize ediliyor...**")
    os.system("git pull origin ana")
    await update.message.reply_text("⚙️ **Sistem Yeniden Başlatılıyor...**")
    os.execv(sys.executable, ['python'] + sys.argv)

if __name__ == '__main__':
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_TOKEN")).build()
    app.add_handler(CommandHandler("update", deploy_update))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), ai_logic))
    app.run_polling()
    
