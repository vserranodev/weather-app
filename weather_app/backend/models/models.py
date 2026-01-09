from datetime import datetime, date
from typing import Optional
from sqlmodel import SQLModel, Field

class WeatherRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)                 
    location_name: str                    
    latitude: float
    longitude: float
    date_from: date
    date_to: date
    temperature_kelvin: float
    temperature_feels_like: float
    humidity: int
    description: str
    icon_code: str
    wind_speed: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None