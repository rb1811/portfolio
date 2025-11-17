import reflex as rx

from .base_page import base_page


def projects_page() -> rx.Component: 
    return base_page(projects()) 


def projects(*args, **kwargs) -> rx.Component:
    return rx.vstack(
        rx.heading("My projects", size="9"),
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