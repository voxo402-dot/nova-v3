# Nova V3: High-Performance Cloud AI

Nova V3 is an enterprise-grade Telegram AI assistant integrated with **Google Gemini 1.5 Flash** and **Google Drive API**. Designed for resilience in stateless environments.

## 🛠 Core Technologies
- **Engine:** Python 3.10+ (Asynchronous)
- **AI Logic:** Google Gemini Pro Engine
- **Persistence:** Dual-Layer Cloud Sync (Local + G-Drive)
- **Deployment:** GitHub Actions Ready

## 📂 Project Structure
- `core/`: Main bot logic and AI processing.
- `utils/`: Cloud synchronization and error handling modules.
- `.gitignore`: Security layer for credential protection.

## ⚙️ Deployment
1. Clone the repository: `git clone https://github.com/neonx45/NovaV3.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Place `credentials.json` in the root directory.
4. Run: `python nova_v3.py`

## 🛡 License
This project is licensed under the MIT License.
