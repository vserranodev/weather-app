import reflex as rx


def info_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.icon_button(
                rx.icon("info", size=18),
                size="2",
                variant="ghost",
                color="white",
                cursor="pointer",
                _hover={"background": "rgba(255,255,255,0.1)"},
            ),
        ),
        rx.dialog.content(
            rx.dialog.title(
                rx.hstack(
                    rx.icon("rocket", size=24, color="var(--blue-9)"),
                    rx.text("About PM Accelerator"),
                    gap="2",
                    align="center",
                ),
            ),
            rx.dialog.description(
                rx.vstack(
                    rx.text(
                        "The Product Manager Accelerator Program is designed to support PM professionals through every stage of their careers. From students looking for entry-level jobs to Directors looking to take on a leadership role, the program has helped over hundreds of students fulfill their career aspirations.",
                        color="var(--gray-11)",
                        line_height="1.6",
                    ),
                    rx.text(
                        "The Product Manager Accelerator community members are ambitious and committed. Through the program they have learnt, honed and developed new PM and leadership skills, giving them a strong foundation for their future endeavors.",
                        color="var(--gray-11)",
                        line_height="1.6",
                        margin_top="8px",
                    ),
                    rx.text(
                        "Services offered:",
                        font_weight="600",
                        margin_top="16px",
                    ),
                    rx.vstack(
                        rx.text("🚀 PMA Pro - End-to-end product manager job hunting program", font_size="13px"),
                        rx.text("🚀 AI PM Bootcamp - Hands-on AI Product Management skills", font_size="13px"),
                        rx.text("🚀 PMA Power Skills - Sharpen PM and leadership skills", font_size="13px"),
                        rx.text("🚀 PMA Leader - Accelerate career to Director level", font_size="13px"),
                        rx.text("🚀 1:1 Resume Review - Stand out with a killer PM resume", font_size="13px"),
                        gap="1",
                        align="start",
                        color="var(--gray-11)",
                    ),
                    rx.text(
                        "PM Accelerator has also published over 500+ free training courses on YouTube and Instagram.",
                        color="var(--gray-11)",
                        font_size="13px",
                        margin_top="12px",
                    ),
                    rx.hstack(
                        rx.link(
                            rx.button(
                                rx.hstack(
                                    rx.icon("linkedin", size=14),
                                    rx.text("LinkedIn", font_size="13px"),
                                    gap="1",
                                    align="center",
                                ),
                                size="1",
                            ),
                            href="https://www.linkedin.com/school/pmaccelerator/",
                            is_external=True,
                        ),
                        rx.link(
                            rx.button(
                                rx.hstack(
                                    rx.icon("youtube", size=14),
                                    rx.text("YouTube", font_size="13px"),
                                    gap="1",
                                    align="center",
                                ),
                                size="1",
                                variant="outline",
                            ),
                            href="https://www.youtube.com/c/drnancyli",
                            is_external=True,
                        ),
                        gap="2",
                        margin_top="16px",
                    ),
                    gap="2",
                    width="100%",
                ),
            ),
            rx.dialog.close(
                rx.button(
                    "Close",
                    variant="ghost",
                    margin_top="16px",
                ),
            ),
            max_width="520px",
            style={"max-height": "80vh", "overflow-y": "auto"},
        ),
    )


def navbar() -> rx.Component:
    return rx.hstack(
        rx.hstack(
            rx.icon("cloud", size=24, color="white"),
            rx.text(
                "WeatherApp",
                font_size="20px",
                font_weight="700",
                color="white",
                letter_spacing="-0.01em",
            ),
            gap="2",
            align="center",
        ),
        rx.spacer(),
        rx.hstack(
            rx.text(
                "by Víctor Serrano",
                font_size="14px",
                color="rgba(255,255,255,0.7)",
            ),
            info_modal(),
            gap="3",
            align="center",
        ),
        position="sticky",
        top="0",
        background="rgba(30, 58, 95, 0.9)",
        backdrop_filter="blur(10px)",
        padding="16px 24px",
        z_index="999",
        width="100%",
    )

