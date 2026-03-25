import pickle
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

MODEL_PATH = Path(__file__).resolve().with_name("sentiment_model_v1.0_pkl")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173", "http://127.0.0.1:4173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with MODEL_PATH.open("rb") as file:
    sentiment_model = pickle.load(file)


@app.get("/")
async def root():
    return {"message": "Sentiment API is running"}


class SentimentRequest(BaseModel):
    text: str


@app.post("/sentiment")
async def analyze_sentiment(payload: SentimentRequest):
    prediction = sentiment_model.predict([payload.text])[0]
    return {
        "text": payload.text,
        "sentiment": str(prediction),
    }
