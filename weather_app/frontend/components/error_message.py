import reflex as rx
from weather_app.frontend.state import WeatherState


def error_message() -> rx.Component:
    return rx.cond(
        WeatherState.has_error,
        rx.box(
            rx.hstack(
                rx.icon("alert-circle", size=18, color="#ff6b6b"),
                rx.text(
                    WeatherState.error_message,
                    color="white",
                    font_size="14px",
                    flex="1",
                ),
                rx.icon_button(
                    rx.icon("x", size=14),
                    size="1",
                    variant="ghost",
                    color="white",
                    on_click=WeatherState.clear_error,
                    cursor="pointer",
                ),
                gap="3",
                align="center",
                width="100%",
            ),
            background="rgba(255, 107, 107, 0.25)",
            border="1px solid rgba(255, 107, 107, 0.4)",
            border_radius="10px",
            padding="10px 14px",
            width="100%",
        ),
    )


def success_message() -> rx.Component:
    return rx.cond(
        WeatherState.has_success,
        rx.box(
            rx.hstack(
                rx.icon("check-circle", size=18, color="#4ade80"),
                rx.text(
                    WeatherState.success_message,
                    color="white",
                    font_size="14px",
                    flex="1",
                ),
                rx.icon_button(
                    rx.icon("x", size=14),
                    size="1",
                    variant="ghost",
                    color="white",
                    on_click=WeatherState.clear_success,
                    cursor="pointer",
                ),
                gap="3",
                align="center",
                width="100%",
            ),
            background="rgba(74, 222, 128, 0.25)",
            border="1px solid rgba(74, 222, 128, 0.4)",
            border_radius="10px",
            padding="10px 14px",
            width="100%",
        ),
    )


def loading_spinner() -> rx.Component:
    return rx.cond(
        WeatherState.is_loading,
        rx.hstack(
            rx.spinner(size="3", color="white"),
            rx.text("Loading...", color="rgba(255,255,255,0.8)", font_size="14px"),
            gap="3",
            align="center",
        ),
    )
