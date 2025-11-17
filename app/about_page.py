import reflex as rx

def about_me(*args, **kwargs) -> rx.Component:
    return rx.vstack(
        rx.heading("A bit about me", size="9"),
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