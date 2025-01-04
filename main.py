from pyrogram import Client
import json
import os
from fastapi import FastAPI, HTTPException

app = FastAPI()

API_ID = "16904713"  # Хардкодим API ID
API_HASH = "6c3aedb0f03d6ff6c9f5cfcba089a494"  # Хардкодим API HASH
SESSION_STRING = "AgEB8gkAS39ms4PxZzrLDcOPppObOADF1wB3x9dJTSS7e6XzyW5vgwy6qwdGZd64Zn-GQqRJ3liW4Kmcc01ysC1mpfXjD4zkM2-vhx-4GZDuH-UciOh9YJz695UDd_JMKiAE6i7S91icFeNL8B_lzj35pJGdt5MntKNnsPDpzo0uNGQ3ztdyTvFj7WUMJfBf0pIUCf1J5KaQQlsyIWUXU3Bn1JKSu-zd3g1aTo3-0p4RmlgqiTfyPeLpACafjz-6x6SAyAbV3Rvk6YEvmsRR_MRvvgDWQRXw969nNwGLRWz5AqGiRg9C9hDUZnG0oxNCJNyHc22OT_L5NHczXwG3MGGCvWA5LgAAAAAWY7jyAA"  # Хардкодим сессию

# Создаем глобальный клиент
client = Client(
    name="my_account",
    api_id=int(API_ID),
    api_hash=API_HASH,
    session_string=SESSION_STRING,
    in_memory=True
)

@app.on_event("startup")
async def startup():
    await client.start()

@app.on_event("shutdown")
async def shutdown():
    await client.stop()

@app.get("/api/messages")
async def get_messages(chat_id: int):
    try:
        print("🚀 Starting...")
        messages = []
        
        print(f"📥 Getting messages for chat {chat_id}...")
        async for message in client.get_chat_history(chat_id=chat_id, limit=10):
            message_info = {
                "message_id": message.id,
                "date": message.date.isoformat(),
                "text": message.text if message.text else None,
                "from_user": {
                    "id": message.from_user.id if message.from_user else None,
                    "username": message.from_user.username if message.from_user else None,
                    "first_name": message.from_user.first_name if message.from_user else None
                } if message.from_user else None
            }
            messages.append(message_info)

        print(f"✅ Got {len(messages)} messages")
        return {
            "success": True,
            "messages_count": len(messages),
            "messages": messages
        }

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080) 