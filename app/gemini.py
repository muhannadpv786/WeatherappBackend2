import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel('gemini-1.5-flash')

async def get_weather_recommendations(weather_data):
    prompt = f"""
    Based on the following weather conditions in {weather_data.city}, {weather_data.country}, provide practical recommendations on what to do and what to avoid:

    Current Weather: {weather_data.weather}
    Temperature: {weather_data.temperature}°C (Feels like {weather_data.feels_like}°C)
    Humidity: {weather_data.humidity}%
    Wind Speed: {weather_data.wind_speed} m/s

    Provide the recommendations in the following format:
    - Do's: (3-5 bullet points)
    - Don'ts: (3-5 bullet points)

    Make the recommendations practical, health-conscious, and suitable for the general public.
    """

    response = model.generate_content(prompt)
    return response.text