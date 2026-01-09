# Weather app for PM Accelerator

A modern weather application built with **Reflex** (Python) that provides real-time weather information and forecasts for any location worldwide using OpenWeatherMap API and SQLite.

**Author:** Víctor Serrano García

## Features

### Tech Assessment 1 - Core weather app

**Location searching**  : Search for any city with autocomplete suggestions using OpenWeatherMap Geocoding API 
`weather_app/frontend/components/location_input.py` 

**Current weather** :Display temperature, humidity, wind speed, and weather conditions 
`weather_app/frontend/components/weather_card.py` 

**5-Day Forecast** : Horizontal forecast cards showing daily min/max temperatures `weather_app/frontend/components/forecast.py`

**Geolocation** : Button to use browser's current location `weather_app/frontend/components/geolocation.py`

**Weather icons** :Dynamic icons from OpenWeatherMap based on conditions

**Temperature units** : Toggle between Celsius and Fahrenheit 
State toggle in `weather_card.py`

**Author info** : Name displayed in navbar with PM Accelerator info button `weather_app/frontend/components/navbar.py`

### Tech assessment 2 - CRUD db operations in SQLite

**CREATE** : Save weather searches with custom date ranges to SQLite database `weather_app/backend/services/database.py` → `create_weather_record()`

**READ** :View saved search history in sidebar panel

`weather_app/frontend/pages/index.py` → `sidebar_history()`

**UPDATE** : Edit saved records via modal dialog

`weather_app/frontend/components/history.py` → `edit_modal()`

**DELETE** : Remove records from history

State handler `delete_record()`

**Date validation** : Validates date ranges before saving

`Weather_app/backend/services/database.py` → `validate_date_range()`

**Location validation**  : Locations are validated via autocomplete dropdown (only real locations can be selected)

`weather_app/backend/services/api.py` → `search_locations()`

---

## Project structure

```

weather_app/

├── backend/

│   ├── core/

│   │   └── config.py           # Pydantic settings for environment variables

│   ├── models/

│   │   └── models.py           # SQLModel database

│   └── services/

│       ├── api.py              # OpenWeatherMap API client

│       └── database.py         # CRUD operations 

├── frontend/

│   ├── components/

│   │   ├── error_message.py    # Error/success notifications

│   │   ├── forecast.py         # 5-day forecast display

│   │   ├── geolocation.py      # Browser geolocation button

│   │   ├── history.py          # Edit modal for records

│   │   ├── location_input.py   # Search input with autocomplete

│   │   ├── navbar.py           # Navigation bar + PM Accelerator info

│   │   ├── save_weather.py     # Save to history form

│   │   └── weather_card.py     # Current weather display

│   ├── pages/

│   │   └── index.py            # Index page layout

│   └── state.py                # Reflex state management

└── weather_app.py              # App entry point

```

---

## How to use it

### Prerequisites

OpenWeatherMap API key
As in creating an environment variable like the following: OPEN_WEATHER_MAP_API_KEY="..."

### Installation

**1. Clone repo**

**2. Create virtual environment**

**3. Install dependencies of the requirements.txt file**

**4. Configure environment variables by creating .env file with the variables**

**Run the application with "reflex run"**

**6. Open in browser in localhost:3000/**

## Tech stack

-**Reflex** - Python web framework for reactive UIs

-**SQLModel** - Database ORM (SQLAlchemy + Pydantic)

-**SQLite** - Lightweight database

-**OpenWeatherMap API** - Weather data provider

-**Pydantic Settings** - Environment configuration

-**httpx** - HTTP client for API requests

## Screenshots

The application features:

- A clean UI
- Quality design for weather cards
- Responsive layout with search history sidebar
- Weather icons that reflect current conditions

---

**This project was created as part of the PM Accelerator Technical Assessment.**
