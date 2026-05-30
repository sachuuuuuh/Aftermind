import discord
from discord.ext import commands
from config import TOKEN, OWNER_ID, NAME
from system_prompt import SYSTEM_PROMPT_VARIABLE

import requests

from memory import (
    save_memory,
    load_all_memories
)

# =========================
# CONFIG
# =========================

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = ""

# =========================
# SYSTEM PROMPT
# =========================

SYSTEM_PROMPT = SYSTEM_PROMPT_VARIABLE

# =========================
# DISCORD SETUP
# =========================

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)

# =========================
# OLLAMA
# =========================

def ask_ollama(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL,
                "prompt": prompt,
                "stream": False
            },
            timeout=120
        )

        response.raise_for_status()

        return response.json()["response"].strip()

    except Exception as e:
        print(f"Ollama Error: {e}")
        return "Something went wrong."

# =========================
# MEMORY CREATION
# =========================

def create_memory(user_text):

    prompt = f"""
Convert the user's message into ONE clean factual sentence to remember.

Rules:
- Always return a memory, no matter what
- Keep it short and clear
- Start with "User" if referring to the person

Examples:

Message: I have an apple in my bag
Memory: User has an apple in their bag.

Message: remember that my dog's name is Max
Memory: User's dog's name is Max.

Message: jhon fell today
Memory: Jhon fell.

Message:
{user_text}

Memory:
"""

    result = ask_ollama(prompt).strip()
    result = result.replace("Memory:", "").strip()

    return result if result else user_text  # fallback: store raw text

# =========================
# NORMAL CHAT
# =========================

def chat(user_text):

    prompt = f"""
{SYSTEM_PROMPT}

User:
{user_text}

Answer naturally.
"""

    return ask_ollama(prompt)

# =========================
# MEMORY DECISION
# =========================

def determine_action(message):
    text = message.lower()

    # ------------------------
    # HARD RULES (VERY IMPORTANT)
    # ------------------------

    # FORCE RECALL triggers
    recall_keywords = [
        "do you remember",
        "remember when",
        "what happened",
        "tell me about",
        "when did",
        "when was"
    ]

    # FORCE STORE triggers
    store_keywords = [
        "remember",
        "note this",
        "save this",
        "keep this",
        "don't forget"
    ]

    for w in recall_keywords:
        if w in text:
            return "RECALL"

    for w in store_keywords:
        if w in text:
            return "STORE"

    # ------------------------
    # AI fallback ONLY
    # ------------------------

    prompt = f"""
Classify message:
STORE = factual information to remember
RECALL = asking about past memory
CHAT = normal talk

Message:
{text}

Answer ONLY one word:
STORE, RECALL, CHAT
"""

    result = ask_ollama(prompt).strip().upper()

    if "STORE" in result:
        return "STORE"
    if "RECALL" in result:
        return "RECALL"
    return "CHAT"

# =========================
# MEMORY SEARCH
# =========================

def search_memories(query):

    memories = load_all_memories()

    if not memories:
        return "NONE"

    prompt = f"""
Find memories relevant to the user's question.

Question:
{query}

Stored Memories:

{chr(10).join(memories)}

Return only relevant memories.

If none are relevant return:
NONE
"""

    return ask_ollama(prompt)

# =========================
# EVENTS
# =========================

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game(name="Remembering things 🧠")
    )

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    # Ignore servers completely
    if not isinstance(message.channel, discord.DMChannel):
        return

    # Non-owner DM
    if message.author.id != OWNER_ID:
        await message.reply(
            f"Sorry, you are not a verified user"
        )
        return

    if message.content.startswith("!"):
        await bot.process_commands(message)
        return

    user_text = message.content

    print(f"{message.author}: {user_text}")

    action = determine_action(user_text)

    print(f"Action: {action}")

    # =====================
    # STORE
    # =====================

    if action == "STORE":

        memory = create_memory(user_text)

        memory = memory.replace("Memory:", "").strip()

        save_memory(
            str(message.author),
            memory
        )

        print(f"Memory saved: {memory}")

        await message.reply("Got it, I'll remember that.")
        return
    
    # =====================
    # RECALL
    # =====================

    if action == "RECALL":

        relevant_memories = search_memories(user_text)

        prompt = f"""
You are a STRICT memory retrieval system.

You are ONLY allowed to use the memories below.

RULES:
- Do NOT guess anything
- Do NOT add explanations
- Do NOT infer missing details
- Do NOT correct or "improve" memory
- If the answer is not explicitly in memory, say EXACTLY:
"I don't know."

MEMORIES:
{relevant_memories}

USER QUESTION:
{user_text}

ANSWER:
"""

        answer = ask_ollama(prompt).strip()

        await message.reply(answer[:1900])
        return

    # =====================
    # NORMAL CHAT
    # =====================

    answer = chat(user_text)

    await message.reply(answer[:1900])

# =========================
# RUN
# =========================

bot.run(TOKEN)