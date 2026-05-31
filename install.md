# ⚙️ Installation Guide – Aftermind

This guide will help you set up and run Aftermind.

---

> [!WARNING]
> This project is in early development. Bugs, unexpected behavior, or incomplete features may occur.

---

# 📌 Requirements

Before starting, make sure you have:

- Python 3.10+
- A Discord bot created (with token)
- Ollama installed and running locally

---

# 📥 1. Clone the repository

Open your terminal and run these commands

```bash
git clone https://github.com/yourusername/aftermind.git
cd Aftermind 
```

# 📦 2. Install dependencies

Install required Python libraries:

```
pip install discord.py requests
```

# ⚙️ 3. Configure the bot

Open `config.py` and fill in your details:

```
TOKEN = "your_discord_bot_token"
OWNER_ID = your_discord_user_id
NAME = "Aftermind"
```
*You can change the bot name if you want here

# 🧠 4. Setup Ollama (AI model)

Install Ollama:  
👉 [https://ollama.com](https://ollama.com)

Then pull a model:

```
ollama run qwen2.5:3b
```

Make sure Ollama is running locally at:

```
http://localhost:11434
```


# 🚀 5. Run the bot

Start Aftermind:

```
python bot.py
```

Now, the DM the bot and have fun!