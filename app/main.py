from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import logging
from dotenv import load_dotenv
from app.gemini import get_weather_recommendations

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Weather data model
class WeatherData(BaseModel):
    city: str
    country: str
    temperature: float
    feels_like: float
    humidity: int
    wind_speed: float
    weather: str
    icon: str
    coordinates: dict
    timestamp: int

# Recommendation endpoint
@app.post("/recommendations")
async def get_recommendations(weather_data: WeatherData):
    try:
        recommendations = await get_weather_recommendations(weather_data)
        return {"recommendations": recommendations}
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating recommendations: {str(e)}")

# Health check endpoint
@app.get("/health")
async def health_check():
    logger.info("Health check route hit")
    return {"status": "Ok", "message": "Weather API is running smoothly!"}
