import reflex as rx
from datetime import date, datetime
from typing import Optional, TypedDict

from weather_app.backend.services.api import (
    weather_service,
    WeatherAPIError,
)
from weather_app.backend.services.database import (
    init_db,
    create_weather_record,
    get_all_weather_records,
    update_weather_record,
    delete_weather_record,
    validate_date_range,
    export_records_to_csv,
)


#we create a forecast day typed dict because reflex was giving errors when accessing the forecast temp
class ForecastDay(TypedDict):
    date: str
    date_short: str
    temp_min_c: float
    temp_max_c: float
    temp_min_f: float
    temp_max_f: float
    condition: str
    description: str
    icon: str
    icon_url: str
    humidity_avg: int
    precipitation_prob: float


init_db()


class WeatherState(rx.State):
    
    search_query: str = ""
    location_suggestions: list[dict] = []  
    is_searching: bool = False
    
    selected_location_name: str = ""
    selected_latitude: float = 0.0
    selected_longitude: float = 0.0
    
    has_weather_data: bool = False
    location_display: str = ""
    temperature: float = 0.0
    temperature_kelvin: float = 0.0
    feels_like: float = 0.0
    feels_like_kelvin: float = 0.0
    humidity: int = 0
    wind_speed: float = 0.0
    description: str = ""
    icon_code: str = ""
    
    forecast_days: list[ForecastDay] = []
    
    use_celsius: bool = True
    
    is_loading: bool = False
    error_message: str = ""
    success_message: str = ""
    
    date_from: str = ""
    date_to: str = ""
    
    weather_records: list[dict] = []
    show_history: bool = False
    
    editing_record_id: Optional[int] = None
    edit_location_name: str = ""
    edit_date_from: str = ""
    edit_date_to: str = ""
    edit_description: str = ""
    show_edit_modal: bool = False

    @rx.var
    def temperature_display(self) -> str:
        if not self.has_weather_data:
            return ""
        temp = self.temperature if self.use_celsius else self._to_fahrenheit(self.temperature)
        unit = "°C" if self.use_celsius else "°F"
        return f"{temp:.1f}{unit}"
    
    @rx.var
    def feels_like_display(self) -> str:
        if not self.has_weather_data:
            return ""
        temp = self.feels_like if self.use_celsius else self._to_fahrenheit(self.feels_like)
        unit = "°C" if self.use_celsius else "°F"
        return f"{temp:.1f}{unit}"
    
    @rx.var
    def has_error(self) -> bool:
        return bool(self.error_message)
    
    @rx.var
    def has_success(self) -> bool:
        return bool(self.success_message)
    
    @rx.var
    def has_forecast(self) -> bool:
        return len(self.forecast_days) > 0
    
    @rx.var
    def has_records(self) -> bool:
        return len(self.weather_records) > 0
    
    @rx.var
    def can_save(self) -> bool:
        return self.has_weather_data and bool(self.date_from) and bool(self.date_to)

    def _to_fahrenheit(self, celsius: float) -> float:
        return celsius * 9/5 + 32
    
    def _clear_messages(self):
        self.error_message = ""
        self.success_message = ""
    
    @rx.event
    def clear_error(self):
        self.error_message = ""
    
    @rx.event
    def clear_success(self):
        self.success_message = ""

    @rx.event
    def on_search_change(self, value: str):
        self.search_query = value
        self._clear_messages()
        
        if len(value) < 2:
            self.location_suggestions = []
            return
        
        self.is_searching = True
        
        try:
            locations = weather_service.search_locations(value, limit=5)
            self.location_suggestions = [
                {
                    "name": loc.name,
                    "country": loc.country,
                    "state": loc.state or "",
                    "display_name": loc.display_name,
                    "latitude": loc.latitude,
                    "longitude": loc.longitude,
                }
                for loc in locations
            ]
        except Exception:
            self.location_suggestions = []
        finally:
            self.is_searching = False
    
    @rx.event
    def select_location(self, location: dict):
        self.selected_location_name = location["display_name"]
        self.selected_latitude = location["latitude"]
        self.selected_longitude = location["longitude"]
        self.search_query = location["display_name"]
        self.location_suggestions = []  
        return WeatherState.fetch_weather
    
    @rx.event
    def fetch_weather(self):
        if not self.selected_latitude and not self.selected_longitude:
            self.error_message = "Please select a location first"
            return
        
        self.is_loading = True
        self._clear_messages()
        
        try:
            weather = weather_service.get_current_weather_by_coords(
                self.selected_latitude,
                self.selected_longitude
            )
            
            self.location_display = f"{weather.location_name}, {weather.country}"
            self.temperature = weather.temperature_celsius
            self.temperature_kelvin = weather.temperature_kelvin
            self.feels_like = weather.feels_like_celsius
            self.feels_like_kelvin = weather.feels_like_kelvin
            self.humidity = weather.humidity
            self.wind_speed = weather.wind_speed
            self.description = weather.condition.description.capitalize()
            self.icon_code = weather.condition.icon
            self.has_weather_data = True
            
            today = date.today().isoformat()
            self.date_from = today
            self.date_to = today
            
            forecast = weather_service.get_forecast_by_coords(
                self.selected_latitude,
                self.selected_longitude
            )
            self.forecast_days = forecast.get_daily_summary()
            
        except WeatherAPIError as e:
            self.error_message = str(e)
            self.has_weather_data = False
        except Exception as e:
            self.error_message = f"Error: {str(e)}"
            self.has_weather_data = False
        finally:
            self.is_loading = False
    
    @rx.event
    def toggle_temperature_unit(self):
        self.use_celsius = not self.use_celsius
    
    @rx.event
    def use_current_location(self, coords: dict):
        self.selected_latitude = coords.get("latitude", 0.0)
        self.selected_longitude = coords.get("longitude", 0.0)
        self.selected_location_name = "Current loc"
        self.search_query = "Current location"
        self.location_suggestions = []
        return WeatherState.fetch_weather
    
    @rx.event
    def clear_search(self):
        self.search_query = ""
        self.location_suggestions = []
        self.has_weather_data = False
        self.forecast_days = []
        self._clear_messages()

    @rx.event
    def set_date_from(self, value: str):
        self.date_from = value
    
    @rx.event
    def set_date_to(self, value: str):
        self.date_to = value
    
    @rx.event
    def save_weather_record(self):
        if not self.has_weather_data:
            self.error_message = "No weather data to save"
            return
        
        if not self.date_from or not self.date_to:
            self.error_message = "Please select a date range"
            return
        
        try:
            date_from_obj = date.fromisoformat(self.date_from)
            date_to_obj = date.fromisoformat(self.date_to)
            
            is_valid, error_msg = validate_date_range(date_from_obj, date_to_obj)
            if not is_valid:
                self.error_message = error_msg
                return
            
            create_weather_record(
                location_name=self.location_display,
                latitude=self.selected_latitude,
                longitude=self.selected_longitude,
                date_from=date_from_obj,
                date_to=date_to_obj,
                temperature_kelvin=self.temperature_kelvin,
                temperature_feels_like=self.feels_like_kelvin,
                humidity=self.humidity,
                description=self.description,
                icon_code=self.icon_code,
                wind_speed=self.wind_speed,
            )
            
            self.success_message = "Weather record saved successfully!"
            return WeatherState.load_weather_records
            
        except Exception as e:
            self.error_message = f"Error saving record: {str(e)}"
    
    @rx.event
    def load_weather_records(self):
        try:
            records = get_all_weather_records()
            self.weather_records = [
                {
                    "id": r.id,
                    "location_name": r.location_name,
                    "latitude": r.latitude,
                    "longitude": r.longitude,
                    "date_from": r.date_from.isoformat() if r.date_from else "",
                    "date_to": r.date_to.isoformat() if r.date_to else "",
                    "temperature": round(r.temperature_kelvin - 273.15, 1),
                    "humidity": r.humidity,
                    "description": r.description,
                    "icon_code": r.icon_code,
                    "wind_speed": r.wind_speed,
                    "created_at": r.created_at.strftime("%Y-%m-%d %H:%M") if r.created_at else "",
                }
                for r in records
            ]
        except Exception as e:
            self.error_message = f"Error loading records: {str(e)}"
    
    @rx.event
    def toggle_history(self):
        self.show_history = not self.show_history
        if self.show_history:
            return WeatherState.load_weather_records
    
    @rx.event
    def open_edit_modal(self, record: dict):
        self.editing_record_id = record["id"]
        self.edit_location_name = record["location_name"]
        self.edit_date_from = record["date_from"]
        self.edit_date_to = record["date_to"]
        self.edit_description = record["description"]
        self.show_edit_modal = True
    
    @rx.event
    def close_edit_modal(self):
        self.show_edit_modal = False
        self.editing_record_id = None
    
    @rx.event
    def set_edit_location_name(self, value: str):
        self.edit_location_name = value
    
    @rx.event
    def set_edit_date_from(self, value: str):
        self.edit_date_from = value
    
    @rx.event
    def set_edit_date_to(self, value: str):
        self.edit_date_to = value
    
    @rx.event
    def set_edit_description(self, value: str):
        self.edit_description = value
    
    @rx.event
    def update_record(self):
        if not self.editing_record_id:
            return
        
        try:
            date_from_obj = date.fromisoformat(self.edit_date_from) if self.edit_date_from else None
            date_to_obj = date.fromisoformat(self.edit_date_to) if self.edit_date_to else None
            
            if date_from_obj and date_to_obj:
                is_valid, error_msg = validate_date_range(date_from_obj, date_to_obj)
                if not is_valid:
                    self.error_message = error_msg
                    return
            
            update_weather_record(
                record_id=self.editing_record_id,
                location_name=self.edit_location_name or None,
                date_from=date_from_obj,
                date_to=date_to_obj,
                description=self.edit_description or None,
            )
            
            self.success_message = "Record updated successfully!"
            self.show_edit_modal = False
            return WeatherState.load_weather_records
            
        except Exception as e:
            self.error_message = f"Error updating record: {str(e)}"
    
    @rx.event
    def delete_record(self, record_id: int):
        try:
            success = delete_weather_record(record_id)
            if success:
                self.success_message = "Record deleted successfully!"
                return WeatherState.load_weather_records
            else:
                self.error_message = "Record not found"
        except Exception as e:
            self.error_message = f"Error deleting record: {str(e)}"
    
    @rx.event
    def export_csv(self):
        try:
            csv_content = export_records_to_csv()
            filename = f"weather_history_{date.today().isoformat()}.csv"
            return rx.download(data=csv_content, filename=filename)
        except Exception as e:
            self.error_message = f"Error exporting CSV: {str(e)}"
