import reflex as rx
from weather_app.frontend.components.navbar import navbar
from weather_app.frontend.components.location_input import location_input
from weather_app.frontend.components.weather_card import weather_card
from weather_app.frontend.components.forecast import forecast
from weather_app.frontend.components.error_message import error_message, success_message, loading_spinner
from weather_app.frontend.components.save_weather import save_weather_form
from weather_app.frontend.components.history import edit_modal
from weather_app.frontend.components.geolocation import geolocation_button
from weather_app.frontend.state import WeatherState



def main_content() -> rx.Component:
    return rx.vstack(
        rx.vstack(
            rx.icon("cloud-sun", size=40, color="white"),
            rx.heading(
                "Weather app",
                size="8",
                color="white",
                font_weight="800",
            ),
            rx.text(
                "Discover the weather anywhere",
                color="rgba(255,255,255,0.8)",
                font_size="16px",
            ),
            align="center",
            gap="1",
            margin_bottom="20px",
        ),
        rx.vstack(
            location_input(),
            geolocation_button(),
            gap="2",
            align="center",
            width="100%",
            max_width="500px",
        ),
        error_message(),
        success_message(),
        loading_spinner(),
        weather_card(),
        forecast(),
        save_weather_form(),
        align="center",
        gap="4",
        width="100%",
        flex="1",
    )


def sidebar_history() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.hstack(
                    rx.icon("history", size=20, color="white"),
                    rx.text(
                        "Search history",
                        font_weight="700",
                        font_size="17px",
                        color="white",
                        text_shadow="0 1px 2px rgba(0,0,0,0.3)",
                    ),
                    gap="2",
                    align="center",
                ),
                rx.spacer(),
                rx.tooltip(
                    rx.icon_button(
                        rx.icon("download", size=16, color="white"),
                        size="1",
                        variant="outline",
                        color="white",
                        on_click=WeatherState.export_csv,
                        cursor="pointer",
                        background="rgba(255,255,255,0.15)",
                        border="1px solid rgba(255,255,255,0.4)",
                        _hover={"background": "rgba(255,255,255,0.25)"},
                    ),
                    content="Export to CSV",
                ),
                width="100%",
                align="center",
            ),
            rx.cond(
                WeatherState.has_records,
                rx.vstack(
                    rx.foreach(
                        WeatherState.weather_records,
                        history_record_item,
                    ),
                    gap="2",
                    width="100%",
                    max_height="500px",
                    overflow_y="auto",
                    padding_right="4px",
                ),
                rx.vstack(
                    rx.icon("inbox", size=32, color="rgba(255,255,255,0.3)"),
                    rx.text(
                        "No saved searches yet",
                        color="rgba(255,255,255,0.5)",
                        font_size="14px",
                    ),
                    align="center",
                    gap="2",
                    padding="24px",
                ),
            ),
            gap="4",
            width="100%",
            align="start",
        ),
        background="rgba(255, 255, 255, 0.1)",
        backdrop_filter="blur(20px)",
        border="1px solid rgba(255, 255, 255, 0.15)",
        border_radius="20px",
        padding="20px",
        width="100%",
        min_width="280px",
        max_width="320px",
    )


def history_record_item(record: dict) -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.text(
                    record["location_name"],
                    font_weight="600",
                    font_size="13px",
                    color="white",
                    no_of_lines=1,
                ),
                rx.spacer(),
                rx.hstack(
                    rx.icon_button(
                        rx.icon("pencil", size=12),
                        size="1",
                        variant="ghost",
                        on_click=lambda: WeatherState.open_edit_modal(record),
                        cursor="pointer",
                    ),
                    rx.icon_button(
                        rx.icon("trash-2", size=12),
                        size="1",
                        variant="ghost",
                        color_scheme="red",
                        on_click=lambda: WeatherState.delete_record(record["id"]),
                        cursor="pointer",
                    ),
                    gap="0",
                ),
                width="100%",
                align="center",
            ),
            rx.hstack(
                rx.text(
                    f"{record['temperature']}°C",
                    font_weight="500",
                    font_size="12px",
                    color="rgba(255,255,255,0.9)",
                ),
                rx.text("•", color="rgba(255,255,255,0.4)"),
                rx.text(
                    record["description"],
                    font_size="11px",
                    color="rgba(255,255,255,0.7)",
                    no_of_lines=1,
                ),
                gap="1",
            ),
            rx.text(
                f"{record['date_from']} → {record['date_to']}",
                font_size="10px",
                color="rgba(255,255,255,0.5)",
            ),
            gap="1",
            align="start",
            width="100%",
        ),
        background="rgba(255, 255, 255, 0.08)",
        border_radius="10px",
        padding="10px 12px",
        width="100%",
        _hover={"background": "rgba(255, 255, 255, 0.12)"},
        transition="background 0.15s ease",
    )


@rx.page(route="/", on_load=WeatherState.load_weather_records)
def index() -> rx.Component:
    return rx.box(
        navbar(),
        rx.box(
            rx.hstack(
                main_content(),
                sidebar_history(),
                gap="6",
                align="start",
                width="100%",
                max_width="1100px",
                flex_wrap=["wrap", "wrap", "nowrap"],
            ),
            padding="40px 24px",
            width="100%",
            display="flex",
            justify_content="center",
        ),
        edit_modal(),
        min_height="100vh",
        background="linear-gradient(135deg, #1e3a5f 0%, #2d5a87 30%, #3d7ab5 60%, #6ba3d6 100%)",
    )
