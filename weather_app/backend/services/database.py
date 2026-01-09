import csv
import io
from datetime import datetime, date
from typing import Optional
from sqlmodel import Session, create_engine, select, SQLModel

from weather_app.backend.models.models import WeatherRecord


DATABASE_URL = "sqlite:///weather_app.db"
engine = create_engine(DATABASE_URL, echo=False)


def init_db():
    SQLModel.metadata.create_all(engine)


def create_weather_record(
    location_name: str,
    latitude: float,
    longitude: float,
    date_from: date,
    date_to: date,
    temperature_kelvin: float,
    temperature_feels_like: float,
    humidity: int,
    description: str,
    icon_code: str,
    wind_speed: float,
) -> WeatherRecord:
    with Session(engine) as session:
        record = WeatherRecord(
            location_name=location_name,
            latitude=latitude,
            longitude=longitude,
            date_from=date_from,
            date_to=date_to,
            temperature_kelvin=temperature_kelvin,
            temperature_feels_like=temperature_feels_like,
            humidity=humidity,
            description=description,
            icon_code=icon_code,
            wind_speed=wind_speed,
        )
        session.add(record)
        session.commit()
        session.refresh(record)
        return record


def get_all_weather_records() -> list[WeatherRecord]:
    with Session(engine) as session:
        statement = select(WeatherRecord).order_by(WeatherRecord.created_at.desc())
        results = session.exec(statement)
        return results.all()


def get_weather_record_by_id(record_id: int) -> Optional[WeatherRecord]:
    with Session(engine) as session:
        return session.get(WeatherRecord, record_id)


def update_weather_record(
    record_id: int,
    location_name: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
    description: Optional[str] = None,
) -> Optional[WeatherRecord]:
    with Session(engine) as session:
        record = session.get(WeatherRecord, record_id)
        if not record:
            return None
        
        if location_name is not None:
            record.location_name = location_name
        if date_from is not None:
            record.date_from = date_from
        if date_to is not None:
            record.date_to = date_to
        if description is not None:
            record.description = description
        
        record.updated_at = datetime.utcnow()
        
        session.add(record)
        session.commit()
        session.refresh(record)
        return record


def delete_weather_record(record_id: int) -> bool:
    with Session(engine) as session:
        record = session.get(WeatherRecord, record_id)
        if not record:
            return False
        
        session.delete(record)
        session.commit()
        return True


def validate_date_range(date_from: date, date_to: date) -> tuple[bool, str]:
    today = date.today()
    
    if date_from > date_to:
        return False, "Start date must be before end date"
    
    if date_to < today:
        return False, "End date cannot be in the past"
    
    max_range = 5
    delta = (date_to - date_from).days
    if delta > max_range:
        return False, f"Date range cannot exceed {max_range} days"
    
    return True, ""


def export_records_to_csv() -> str:
    records = get_all_weather_records()
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow([
        "ID",
        "Location",
        "Latitude",
        "Longitude",
        "Date From",
        "Date To",
        "Temperature (°C)",
        "Feels Like (°C)",
        "Humidity (%)",
        "Description",
        "Wind Speed (m/s)",
        "Created At",
        "Updated At",
    ])
    
    for record in records:
        temp_celsius = round(record.temperature_kelvin - 273.15, 1)
        feels_like_celsius = round(record.temperature_feels_like - 273.15, 1)
        
        writer.writerow([
            record.id,
            record.location_name,
            record.latitude,
            record.longitude,
            record.date_from.isoformat() if record.date_from else "",
            record.date_to.isoformat() if record.date_to else "",
            temp_celsius,
            feels_like_celsius,
            record.humidity,
            record.description,
            record.wind_speed,
            record.created_at.strftime("%Y-%m-%d %H:%M:%S") if record.created_at else "",
            record.updated_at.strftime("%Y-%m-%d %H:%M:%S") if record.updated_at else "",
        ])
    
    return output.getvalue()

