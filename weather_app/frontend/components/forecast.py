import reflex as rx
from weather_app.frontend.state import WeatherState, ForecastDay



#this is the forecast day card component

def forecast_day_card(day: ForecastDay) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.text(
                day["date_short"],
                font_size="10px",
                color="rgba(255,255,255,0.6)",
                font_weight="500",
            ),
            rx.image(
                src=day["icon_url"],
                width="32px",
                height="32px",
            ),
            rx.vstack(
                rx.cond(
                    WeatherState.use_celsius,
                    rx.hstack(
                        rx.text(day["temp_max_c"], font_weight="600", color="white", font_size="12px"),
                        rx.text("°", font_weight="600", color="white", font_size="12px"),
                        gap="0",
                    ),
                    rx.hstack(
                        rx.text(day["temp_max_f"], font_weight="600", color="white", font_size="12px"),
                        rx.text("°", font_weight="600", color="white", font_size="12px"),
                        gap="0",
                    ),
                ),
                rx.cond(
                    WeatherState.use_celsius,
                    rx.hstack(
                        rx.text(day["temp_min_c"], color="rgba(255,255,255,0.5)", font_size="11px"),
                        rx.text("°", color="rgba(255,255,255,0.5)", font_size="11px"),
                        gap="0",
                    ),
                    rx.hstack(
                        rx.text(day["temp_min_f"], color="rgba(255,255,255,0.5)", font_size="11px"),
                        rx.text("°", color="rgba(255,255,255,0.5)", font_size="11px"),
                        gap="0",
                    ),
                ),
                gap="0",
                align="center",
            ),
            align="center",
            gap="1",
            padding="8px 10px",
        ),
        background="rgba(255, 255, 255, 0.08)",
        border="1px solid rgba(255, 255, 255, 0.1)",
        border_radius="12px",
        min_width="58px",
        transition="background 0.15s ease",
        _hover={"background": "rgba(255, 255, 255, 0.15)"},
    )


def forecast() -> rx.Component:
    return rx.cond(
        WeatherState.has_forecast,
        rx.hstack(
            rx.foreach(
                WeatherState.forecast_days,
                forecast_day_card,
            ),
            gap="2",
            justify="center",
            align="center",
            padding="8px 12px",
            background="rgba(255, 255, 255, 0.06)",
            border_radius="16px",
            width="100%",
            max_width="500px",
        ),
    )
