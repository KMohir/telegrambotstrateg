import os
from supabase import create_client, Client

url: str = os.environ.get("VITE_SUPABASE_URL")
key: str = os.environ.get("VITE_SUPABASE_PUBLISHABLE_KEY")

supabase: Client = create_client(url, key)

async def save_user_answers(user_id: int, answers: dict):
    try:
        data = {
            "user_id": user_id,
            "topic": answers.get("topic"),
            "audience": answers.get("audience"),
            "goal": answers.get("goal"),
            "tone": answers.get("tone"),
            "format": answers.get("format"),
            "additional": answers.get("additional"),
            # "created_at": "now()" # Supabase usually handles this if default is set
        }
        
        # Assuming table name is 'user_answers'
        response = supabase.table("user_answers").insert(data).execute()
        return response
    except Exception as e:
        print(f"Error saving to Supabase: {e}")
        return None
