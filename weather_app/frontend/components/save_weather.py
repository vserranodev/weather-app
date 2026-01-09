import reflex as rx
from weather_app.frontend.state import WeatherState


def save_weather_form() -> rx.Component:
    return rx.cond(
        WeatherState.has_weather_data,
        rx.hstack(
            rx.hstack(
                rx.input(
                    type="date",
                    value=WeatherState.date_from,
                    on_change=WeatherState.set_date_from,
                    size="1",
                    width="130px",
                ),
                rx.text("→", color="rgba(255,255,255,0.5)"),
                rx.input(
                    type="date",
                    value=WeatherState.date_to,
                    on_change=WeatherState.set_date_to,
                    size="1",
                    width="130px",
                ),
                gap="2",
                align="center",
            ),
            rx.button(
                rx.hstack(
                    rx.icon("bookmark-plus", size=14),
                    rx.text("Save"),
                    gap="1",
                    align="center",
                ),
                on_click=WeatherState.save_weather_record,
                disabled=~WeatherState.can_save,
                size="2",
                cursor="pointer",
            ),
            gap="3",
            align="center",
            justify="center",
            background="rgba(255, 255, 255, 0.08)",
            border="1px solid rgba(255, 255, 255, 0.1)",
            border_radius="12px",
            padding="10px 14px",
            width="100%",
            max_width="500px",
        ),
    )
