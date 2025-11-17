"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
from .base_page import base_page


class State(rx.State):
    pass




def index() -> rx.Component:  
    return base_page()  
    # return rx.container(
    #     rx.vstack(
    #         rx.color_mode.button(position="bottom-right"),
    #         rx.heading("Welcome to Reflex!", size="9"),
    #         rx.text(
    #             "Get started by editing ",
    #             rx.code(f"{config.app_name}/{config.app_name}.py"),
    #             size="5",
    #         ),
    #         rx.button("Pick Prabhat"),
    #         rx.link(
    #             rx.button("Check out our docs!"),
    #             href="https://reflex.dev/docs/getting-started/introduction/",
    #             is_external=True,
    #         ),
    #         spacing="5",
    #         justify="center",
    #         min_height="85vh",
    #     ),
    # )


app = rx.App()
app.add_page(index)
