import reflex as rx
from weather_app.frontend.state import WeatherState


def edit_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title("Edit Record"),
            rx.vstack(
                rx.vstack(
                    rx.text("Location", font_size="12px", color="var(--gray-11)"),
                    rx.input(
                        value=WeatherState.edit_location_name,
                        on_change=WeatherState.set_edit_location_name,
                        width="100%",
                    ),
                    align="start",
                    width="100%",
                ),
                rx.hstack(
                    rx.vstack(
                        rx.text("From", font_size="12px", color="var(--gray-11)"),
                        rx.input(
                            type="date",
                            value=WeatherState.edit_date_from,
                            on_change=WeatherState.set_edit_date_from,
                        ),
                        align="start",
                    ),
                    rx.vstack(
                        rx.text("To", font_size="12px", color="var(--gray-11)"),
                        rx.input(
                            type="date",
                            value=WeatherState.edit_date_to,
                            on_change=WeatherState.set_edit_date_to,
                        ),
                        align="start",
                    ),
                    width="100%",
                ),
                rx.vstack(
                    rx.text("Description", font_size="12px", color="var(--gray-11)"),
                    rx.input(
                        value=WeatherState.edit_description,
                        on_change=WeatherState.set_edit_description,
                        width="100%",
                    ),
                    align="start",
                    width="100%",
                ),
                rx.hstack(
                    rx.dialog.close(
                        rx.button(
                            "Cancel",
                            variant="ghost",
                            on_click=WeatherState.close_edit_modal,
                        ),
                    ),
                    rx.button(
                        "Save changes",
                        on_click=WeatherState.update_record,
                    ),
                    justify="end",
                    width="100%",
                    margin_top="16px",
                ),
                gap="4",
                width="100%",
            ),
            max_width="400px",
        ),
        open=WeatherState.show_edit_modal,
    )
