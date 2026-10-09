import streamlit as st
import sqlite3
import json
import os

DATA_DIR = os.getenv("DATA_DIR", "./data")
os.makedirs(DATA_DIR, exist_ok = True)

CHAT_DB_PATH = os.path.join(DATA_DIR, "chats.db")
MEMORY_DB_PATH = os.path.join(DATA_DIR, "memory.db")
CHECKPOINT_DB_PATH = os.path.join(DATA_DIR, "checkpoints.db")



def connect_db():
    conn = sqlite3.connect(
        CHAT_DB_PATH,
        check_same_thread = False
    )

    return conn


def create_chat_table():

    conn = connect_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS CHATS (
            chat_id TEXT PRIMARY KEY,
            title TEXT,
            messages TEXT
        )
    """)

    conn.commit()
    conn.close()



def save_chat(chat_id, title, messages):
    conn = connect_db()

    conn.execute("""
        INSERT OR REPLACE INTO CHATS (chat_id, title, messages) VALUES (?,?,?)
    """,
                 (chat_id, title, json.dumps(messages)))

    conn.commit()
    conn.close()


def load_chats():
    conn = connect_db()
    try:

        rows = conn.execute("""
            SELECT chat_id, title, messages
            from CHATS
        """).fetchall()



        chats = {}

        for chat_id, title, messages in rows:
            chats[chat_id] = {
                "title" : title,
                "messages" : json.loads(messages)
            }

        return chats

    finally:
        conn.close()

























