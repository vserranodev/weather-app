import reflex as rx
from weather_app.frontend.state import WeatherState


##### button to see the current geolocation (geoloc)


def geolocation_button() -> rx.Component:
    return rx.button(
        rx.hstack(
            rx.icon("locate", size=16),
            rx.text("Use my location"),
            gap="2",
            align="center",
        ),
        on_click=rx.call_script(
            """
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(
                    (pos) => {
                        window.__reflex_state.use_current_location({
                            latitude: pos.coords.latitude,
                            longitude: pos.coords.longitude
                        });
                    },
                    () => alert('Could not get loc data')
                );
            } else {
                alert('Geolocation not supported');
            }
            """
        ),
        variant="ghost",
        color="white",
        size="2",
        cursor="pointer",
        _hover={"background": "rgba(255,255,255,0.1)"},
    )

