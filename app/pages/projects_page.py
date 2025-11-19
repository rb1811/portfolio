import reflex as rx

from .base_page import base_page


def projects_page() -> rx.Component: 
    return base_page(projects()) 


def projects(*args, **kwargs) -> rx.Component:
    return (
        rx.center(
            rx.grid(
                rx.foreach(
                    rx.Var.range(2),
                    lambda i: rx.card(f"Card {i + 1}", height="70vh"),
                ),
            columns="2",
            spacing="4",
            width="90%",
        ),
        margin_left="10px"  
        )
    )