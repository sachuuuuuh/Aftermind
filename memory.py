from pathlib import Path
from datetime import datetime

# =========================
# MEMORY DIRECTORY
# =========================

MEMORY_DIR = Path("memories")
MEMORY_DIR.mkdir(exist_ok=True)

# =========================
# SAVE MEMORY
# =========================

def save_memory(username, memory_text):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H-%M-%S"
    )

    filename = MEMORY_DIR / f"{timestamp}.txt"

    content = f"""User: {username}
Date: {timestamp}

{memory_text}
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

# =========================
# LOAD ALL MEMORIES
# =========================

def load_all_memories():

    memories = []

    for file in sorted(MEMORY_DIR.glob("*.txt")):

        try:
            with open(file, "r", encoding="utf-8") as f:
                memories.append(f.read())

        except Exception as e:
            print(f"Error reading {file}: {e}")

    return memories

# =========================
# MEMORY COUNT
# =========================

def memory_count():
    return len(list(MEMORY_DIR.glob("*.txt")))

# =========================
# LIST MEMORIES
# =========================

def list_memories():
    return [file.name for file in MEMORY_DIR.glob("*.txt")]

# =========================
# DELETE MEMORY
# =========================

def delete_memory(filename):

    file_path = MEMORY_DIR / filename

    if file_path.exists():
        file_path.unlink()
        return True

    return False

# =========================
# CLEAR MEMORIES
# =========================

def clear_memories():

    count = 0

    for file in MEMORY_DIR.glob("*.txt"):

        try:
            file.unlink()
            count += 1

        except Exception as e:
            print(f"Failed to delete {file}: {e}")

    return count