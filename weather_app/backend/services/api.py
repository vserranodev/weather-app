from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import httpx
from weather_app.backend.core.config import settings

@dataclass
class Location:
    #This is the location for the dropdown selector
    name: str           
    country: str        
    state: Optional[str]  
    latitude: float
    longitude: float

    @property
    def display_name(self) -> str:
        #Formatted name for the dropdown selector
        if self.state:
            return f"{self.name}, {self.state}, {self.country}"
        return f"{self.name}, {self.country}"


@dataclass
class WeatherCondition:
    id: int
    main: str           
    description: str    
    icon: str          


@dataclass
class CurrentWeather:
    location_name: str
    country: str
    latitude: float
    longitude: float
    temperature_kelvin: float
    feels_like_kelvin: float
    temp_min_kelvin: float
    temp_max_kelvin: float
    humidity: int               
    pressure: int              
    visibility: int            
    wind_speed: float         
    wind_deg: int              
    clouds: int                 
    condition: WeatherCondition
    sunrise: datetime
    sunset: datetime
    timestamp: datetime

    @property
    def temperature_celsius(self) -> float:
        return round(self.temperature_kelvin - 273.15, 1)
    
    @property
    def temperature_fahrenheit(self) -> float:
        return round((self.temperature_kelvin - 273.15) * 9/5 + 32, 1)
    
    @property
    def feels_like_celsius(self) -> float:
        return round(self.feels_like_kelvin - 273.15, 1)


@dataclass
class ForecastItem:
    timestamp: datetime
    temperature_kelvin: float
    feels_like_kelvin: float
    temp_min_kelvin: float
    temp_max_kelvin: float
    humidity: int
    pressure: int
    wind_speed: float
    wind_deg: int
    clouds: int
    condition: WeatherCondition
    precipitation_probability: float  

    @property
    def temperature_celsius(self) -> float:
        return round(self.temperature_kelvin - 273.15, 1)
    
    @property
    def temperature_fahrenheit(self) -> float:
        return round((self.temperature_kelvin - 273.15) * 9/5 + 32, 1)
    
    @property
    def icon_url(self) -> str:
        return f"https://openweathermap.org/img/wn/{self.condition.icon}@2x.png"


@dataclass
class Forecast:
    location_name: str
    country: str
    latitude: float
    longitude: float
    items: list[ForecastItem]

    def get_daily_summary(self) -> list[dict]:
        daily: dict[str, list[ForecastItem]] = {}
        
        for item in self.items:
            day_key = item.timestamp.strftime("%Y-%m-%d")
            if day_key not in daily:
                daily[day_key] = []
            daily[day_key].append(item)
        
        summaries = []
        for date_str, items in daily.items():
            temps = [i.temperature_celsius for i in items]
            noon_item = min(items, key=lambda x: abs(x.timestamp.hour - 12))
            
            temp_min_c = min(temps)
            temp_max_c = max(temps)
            summaries.append({
                "date": date_str,
                "date_short": date_str[5:],
                "temp_min_c": temp_min_c,
                "temp_max_c": temp_max_c,
                "temp_min_f": round(temp_min_c * 9/5 + 32, 1),
                "temp_max_f": round(temp_max_c * 9/5 + 32, 1),
                "condition": noon_item.condition.main,
                "description": noon_item.condition.description,
                "icon": noon_item.condition.icon,
                "icon_url": noon_item.icon_url,
                "humidity_avg": round(sum(i.humidity for i in items) / len(items)),
                "precipitation_prob": max(i.precipitation_probability for i in items),
            })
        
        return summaries

class WeatherAPIError(Exception):
    pass

class WeatherService:

    BASE_URL = settings.weather_api_base_url
    TIMEOUT = settings.weather_api_timeout
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.open_weather_map_api_key
        self._client = httpx.Client(timeout=self.TIMEOUT)
    
    def _handle_response(self, response: httpx.Response) -> dict:
        if response.status_code == 200:
            return response.json()
        
        try:
            error_data = response.json()
            message = error_data.get("message", "Unknown error")
        except Exception:
            message = response.text or "Unknown error"
        
        else:
            raise WeatherAPIError(f"Error {response.status_code}: {message}")
    
    def _parse_condition(self, weather_data: dict) -> WeatherCondition:
        return WeatherCondition(
            id=weather_data["id"],
            main=weather_data["main"],
            description=weather_data["description"],
            icon=weather_data["icon"],
        )
    
    def get_current_weather(self, location: str) -> CurrentWeather:
        response = self._client.get(
            f"{self.BASE_URL}/weather",
            params={
                "q": location,
                "appid": self.api_key,
            }
        )
        
        data = self._handle_response(response)
        
        return CurrentWeather(
            location_name=data["name"],
            country=data["sys"]["country"],
            latitude=data["coord"]["lat"],
            longitude=data["coord"]["lon"],
            temperature_kelvin=data["main"]["temp"],
            feels_like_kelvin=data["main"]["feels_like"],
            temp_min_kelvin=data["main"]["temp_min"],
            temp_max_kelvin=data["main"]["temp_max"],
            humidity=data["main"]["humidity"],
            pressure=data["main"]["pressure"],
            visibility=data.get("visibility", 0),
            wind_speed=data["wind"]["speed"],
            wind_deg=data["wind"].get("deg", 0),
            clouds=data["clouds"]["all"],
            condition=self._parse_condition(data["weather"][0]),
            sunrise=datetime.fromtimestamp(data["sys"]["sunrise"]),
            sunset=datetime.fromtimestamp(data["sys"]["sunset"]),
            timestamp=datetime.fromtimestamp(data["dt"]),
        )
    
    def get_current_weather_by_coords(
        self, 
        latitude: float, 
        longitude: float
    ) -> CurrentWeather:
        response = self._client.get(
            f"{self.BASE_URL}/weather",
            params={
                "lat": latitude,
                "lon": longitude,
                "appid": self.api_key,
            }
        )
        
        data = self._handle_response(response)
        
        return CurrentWeather(
            location_name=data["name"],
            country=data["sys"]["country"],
            latitude=data["coord"]["lat"],
            longitude=data["coord"]["lon"],
            temperature_kelvin=data["main"]["temp"],
            feels_like_kelvin=data["main"]["feels_like"],
            temp_min_kelvin=data["main"]["temp_min"],
            temp_max_kelvin=data["main"]["temp_max"],
            humidity=data["main"]["humidity"],
            pressure=data["main"]["pressure"],
            visibility=data.get("visibility", 0),
            wind_speed=data["wind"]["speed"],
            wind_deg=data["wind"].get("deg", 0),
            clouds=data["clouds"]["all"],
            condition=self._parse_condition(data["weather"][0]),
            sunrise=datetime.fromtimestamp(data["sys"]["sunrise"]),
            sunset=datetime.fromtimestamp(data["sys"]["sunset"]),
            timestamp=datetime.fromtimestamp(data["dt"]),
        )
    
    def get_forecast(self, location: str) -> Forecast:
        response = self._client.get(
            f"{self.BASE_URL}/forecast",
            params={
                "q": location,
                "appid": self.api_key,
            }
        )
        
        data = self._handle_response(response)
        
        items = []
        for item_data in data["list"]:
            items.append(ForecastItem(
                timestamp=datetime.fromtimestamp(item_data["dt"]),
                temperature_kelvin=item_data["main"]["temp"],
                feels_like_kelvin=item_data["main"]["feels_like"],
                temp_min_kelvin=item_data["main"]["temp_min"],
                temp_max_kelvin=item_data["main"]["temp_max"],
                humidity=item_data["main"]["humidity"],
                pressure=item_data["main"]["pressure"],
                wind_speed=item_data["wind"]["speed"],
                wind_deg=item_data["wind"].get("deg", 0),
                clouds=item_data["clouds"]["all"],
                condition=self._parse_condition(item_data["weather"][0]),
                precipitation_probability=item_data.get("pop", 0.0),
            ))
        
        return Forecast(
            location_name=data["city"]["name"],
            country=data["city"]["country"],
            latitude=data["city"]["coord"]["lat"],
            longitude=data["city"]["coord"]["lon"],
            items=items,
        )
    
    def get_forecast_by_coords(
        self, 
        latitude: float, 
        longitude: float
    ) -> Forecast:

        response = self._client.get(
            f"{self.BASE_URL}/forecast",
            params={
                "lat": latitude,
                "lon": longitude,
                "appid": self.api_key,
            }
        )
        
        data = self._handle_response(response)
        
        items = []
        for item_data in data["list"]:
            items.append(ForecastItem(
                timestamp=datetime.fromtimestamp(item_data["dt"]),
                temperature_kelvin=item_data["main"]["temp"],
                feels_like_kelvin=item_data["main"]["feels_like"],
                temp_min_kelvin=item_data["main"]["temp_min"],
                temp_max_kelvin=item_data["main"]["temp_max"],
                humidity=item_data["main"]["humidity"],
                pressure=item_data["main"]["pressure"],
                wind_speed=item_data["wind"]["speed"],
                wind_deg=item_data["wind"].get("deg", 0),
                clouds=item_data["clouds"]["all"],
                condition=self._parse_condition(item_data["weather"][0]),
                precipitation_probability=item_data.get("pop", 0.0),
            ))
        
        return Forecast(
            location_name=data["city"]["name"],
            country=data["city"]["country"],
            latitude=data["city"]["coord"]["lat"],
            longitude=data["city"]["coord"]["lon"],
            items=items,
        )
    
    def search_locations(self, query: str, limit: int = 5) -> list[Location]:
        if not query or len(query) < 2:
            return []
        
        response = self._client.get(
            "https://api.openweathermap.org/geo/1.0/direct",
            params={
                "q": query,
                "limit": min(limit, 5),
                "appid": self.api_key,
            }
        )
        
        if response.status_code != 200:
            return []
        
        data = response.json()
        
        locations = []
        for item in data:
            locations.append(Location(
                name=item["name"],
                country=item["country"],
                state=item.get("state"),
                latitude=item["lat"],
                longitude=item["lon"],
            ))
        
        return locations

    def close(self):
        self._client.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()

weather_service = WeatherService()
        

