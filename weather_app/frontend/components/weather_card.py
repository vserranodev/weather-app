import reflex as rx
from weather_app.frontend.state import WeatherState


def weather_card() -> rx.Component:
    return rx.cond(
        WeatherState.has_weather_data,
        rx.box(
            rx.vstack(
                rx.hstack(
                    rx.icon("map-pin", size=16, color="rgba(255,255,255,0.7)"),
                    rx.text(
                        WeatherState.location_display,
                        font_size="16px",
                        font_weight="600",
                        color="white",
                    ),
                    gap="2",
                    align="center",
                ),
                rx.hstack(
                    rx.text(
                        WeatherState.temperature_display,
                        font_size="52px",
                        font_weight="700",
                        color="white",
                        line_height="1",
                    ),
                    rx.vstack(
                        rx.text(
                            WeatherState.description,
                            font_size="15px",
                            color="rgba(255,255,255,0.85)",
                            text_transform="capitalize",
                        ),
                        rx.button(
                            rx.hstack(
                                rx.icon("repeat", size=12),
                                rx.cond(
                                    WeatherState.use_celsius,
                                    rx.text("°F", font_size="12px"),
                                    rx.text("°C", font_size="12px"),
                                ),
                                gap="1",
                                align="center",
                            ),
                            on_click=WeatherState.toggle_temperature_unit,
                            variant="ghost",
                            color="white",
                            size="1",
                            cursor="pointer",
                            padding="4px 8px",
                            _hover={"background": "rgba(255,255,255,0.1)"},
                        ),
                        align="start",
                        gap="2",
                    ),
                    align="center",
                    gap="4",
                ),
                rx.hstack(
                    rx.hstack(
                        rx.icon("thermometer", size=16, color="rgba(255,255,255,0.6)"),
                        rx.vstack(
                            rx.text("Feels", font_size="10px", color="rgba(255,255,255,0.5)"),
                            rx.text(WeatherState.feels_like_display, font_weight="600", font_size="13px", color="white"),
                            gap="0",
                            align="center",
                        ),
                        gap="1",
                        align="center",
                    ),
                    rx.hstack(
                        rx.icon("droplets", size=16, color="rgba(255,255,255,0.6)"),
                        rx.vstack(
                            rx.text("Humidity", font_size="10px", color="rgba(255,255,255,0.5)"),
                            rx.text(f"{WeatherState.humidity}%", font_weight="600", font_size="13px", color="white"),
                            gap="0",
                            align="center",
                        ),
                        gap="1",
                        align="center",
                    ),
                    rx.hstack(
                        rx.icon("wind", size=16, color="rgba(255,255,255,0.6)"),
                        rx.vstack(
                            rx.text("Wind", font_size="10px", color="rgba(255,255,255,0.5)"),
                            rx.text(f"{WeatherState.wind_speed} m/s", font_weight="600", font_size="13px", color="white"),
                            gap="0",
                            align="center",
                        ),
                        gap="1",
                        align="center",
                    ),
                    justify="between",
                    width="100%",
                    padding_top="8px",
                    border_top="1px solid rgba(255,255,255,0.1)",
                ),
                align="center",
                gap="3",
                width="100%",
            ),
            background="rgba(255, 255, 255, 0.12)",
            backdrop_filter="blur(20px)",
            border="1px solid rgba(255, 255, 255, 0.15)",
            border_radius="20px",
            padding="20px 24px",
            width="100%",
            max_width="500px",
        ),
    )
