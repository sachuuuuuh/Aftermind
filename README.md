# 🧠 Aftermind

An auxiliary AI memory assistant that stores, retrieves, and manages contextual information.

Most AI systems cant remember everything after a conversation ends. Aftermind solves this problem of normal chatbots by introducing a memory layer which allows ai models to store and remember information.

This enables more natural, consistant and context-aware interactions over time.


---

# 🌟 Highlights

- 🧠 Persistent memory layer for AI assistants  
- 💾 Stores and retrieves contextual information  
- 🔍 Enables long-term memory across interactions  
- ⚙️ Lightweight and easy to extend  
- 🤖 Works with local LLMs 
- 🧩 Simple architecture, focused on clarity over complexity  

---


# ⚙️ How it works

Aftermind processes each message through a simple memory-driven pipeline inside the Discord `on_message` event.

> [!WARNING]  
> This project is still in early development. The code may contain bugs, and unexpected behavior can occur.
## 📥 1. Message filtering  
  
Every incoming message is first filtered:  
  
- ✔️Bots are ignored  
- ✔️ Only Discord DMs are allowed  
- ✔️ Only the owner can interact with the system  

## 🧠 2. Action detection  
  
The message is then analyzed to decide what to do:  
  
- **STORE** → Save new information  
- **RECALL** → Retrieve past memory  
- **CHAT** → Normal conversation  
  
This decision is made using:  
- fast keyword rules (first check)  
- LLM-based classification (fallback)
  
> 💾 **STORE**
> 
> If the action is STORE:  
>  
>- The message is converted into a clean memory statement using the LLM  
>- The structured memory is saved to persistent storage (as .txt files for now) 
>- The bot confirms with: *"Got it, I’ll remember that."*
	
> **🔎RECALL**
>  
>If the action is RECALL:  
>  
>- Stored memories are loaded  
>- Relevant memories are filtered using the LLM  
>- A strict prompt ensures no hallucination  
>- The bot responds using only real stored data

>**💬CHAT**
>
>If no memory action is needed:  
>  
>- The message is sent to the LLM with a system prompt  
>- A natural conversational response is generated

___
# 📦 Installation

See full setup instructions in:

👉 [`INSTALL.md`](install.md)
---

# 📁 Project Structure

| File               | Description           |
| ------------------ | --------------------- |
| `bot.py`           | Main bot logic        |
| `memory.py`        | Memory logic          |
| `system_prompt.py` | AI behavior rules     |
| `config.py`        | Configuration         |
| `INSTALL.md`       | Setup guide           |
| `README.md`        | Project documentation |
