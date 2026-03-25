import pickle

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

with open("sentiment_model_v1.0_pkl", "rb") as file:
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
