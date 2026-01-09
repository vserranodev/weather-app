import reflex as rx
from weather_app.frontend.state import WeatherState


def location_suggestion_item(location: dict) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.icon("map-pin", size=16, color="var(--blue-9)"),
            rx.text(location["display_name"], font_size="14px"),
            gap="2",
            align="center",
        ),
        padding="12px 16px",
        cursor="pointer",
        _hover={"background": "var(--blue-3)"},
        on_click=lambda: WeatherState.select_location(location),
        width="100%",
        transition="background 0.15s ease",
    )


def location_input() -> rx.Component:
    return rx.box(
        rx.vstack(
            rx.hstack(
                rx.icon("search", size=20, color="var(--gray-9)"),
                rx.input(
                    placeholder="Search for a city...",
                    value=WeatherState.search_query,
                    on_change=WeatherState.on_search_change,
                    width="100%",
                    size="3",
                    variant="soft",
                    style={
                        "background": "transparent",
                        "border": "none",
                        "outline": "none",
                        "box-shadow": "none",
                    },
                ),
                background="rgba(255,255,255,0.95)",
                border_radius="12px",
                padding="4px 16px",
                width="100%",
                align="center",
                box_shadow="0 4px 20px rgba(0,0,0,0.15)",
            ),
            rx.cond(
                WeatherState.location_suggestions.length() > 0,
                rx.box(
                    rx.foreach(
                        WeatherState.location_suggestions,
                        location_suggestion_item,
                    ),
                    position="absolute",
                    top="100%",
                    left="0",
                    right="0",
                    margin_top="8px",
                    background="white",
                    border_radius="12px",
                    box_shadow="0 8px 30px rgba(0,0,0,0.2)",
                    z_index="100",
                    max_height="250px",
                    overflow_y="auto",
                    overflow_x="hidden",
                ),
            ),
            width="100%",
            position="relative",
            gap="0",
        ),
        width="100%",
        max_width="500px",
    )
