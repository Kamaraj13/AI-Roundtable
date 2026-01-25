# main.py

from fastapi import FastAPI
from dotenv import load_dotenv
from app.moderator import run_roundtable

load_dotenv()

app = FastAPI()


@app.get("/")
def health():
    return {"status": "ok"}


@app.post("/generate")
async def generate(tts: bool = True):
    episode = await run_roundtable(tts_enabled=tts)
    return episode

