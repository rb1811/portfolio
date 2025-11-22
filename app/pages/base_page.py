import reflex as rx
from ..navbar import navbar_icons
from .default_content import about_me

def base_page(child: rx.Component = about_me(), *args, **kwargs) -> rx.Component:
    
    return rx.fragment(
        rx.box(
            navbar_icons(),
            padding="1em",
            width="100%",
        ),
        rx.box(
            child,
            padding="1em",
            width="100%",
        ),
        rx.color_mode.button(position="bottom-right"),
        # rx.box( 
        #     rx.hstack(
        #         rx.color_mode.button(), 
        #         spacing="2",
        #         align_items="center",
        #     ),
        #     position="fixed",
        #     bottom="20px", 
        #     right="20px",
        #     z_index="100",
        # )  
    )