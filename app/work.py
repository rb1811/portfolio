import reflex as rx

def work(*args, **kwargs) -> rx.Component:
    return rx.vstack(
        rx.heading("My work experience", size="9"),
        rx.text(
            "Coming soon",
            size="5",
            align="center",
            text_align="center",
            justify="center",
        ),
        spacing="5",
        align="center",
        text_align="center",
        justify="center",
        min_height="85vh",
    )