import reflex as rx
from weather_app.frontend.pages.index import index
from weather_app.frontend.state import WeatherState  

app = rx.App()
app.add_page(index)
