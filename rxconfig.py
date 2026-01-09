import reflex as rx

config = rx.Config(
    app_name="weather_app",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)