import json
import os
import google.generativeai as genai

class NovaCore:
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        self.db_path = "nova_vault.json"

    def get_ai_response(self, prompt, user_id):
        try:
            # Profesyonel Sistem Talimatı (System Instruction)
            full_prompt = f"System: Sen Nova V3'sün. Kullanıcı ID: {user_id}. Yanıtların kısa ve öz olsun.\nUser: {prompt}"
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"⚠️ AI Error: {str(e)}"

    def load_db(self):
        if os.path.exists(self.db_path):
            with open(self.db_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def save_db(self, data):
        with open(self.db_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
