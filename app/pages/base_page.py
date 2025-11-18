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
        rx.box( 
            rx.hstack( # This stack puts them next to each other
                rx.color_mode.button(), 
                rx.icon("languages"),
                spacing="2",
                align_items="center",
            ),
            position="fixed",
            bottom="20px", # Increased margin from the bottom
            right="20px",  # Increased margin from the right
            z_index="100",
        )
        
    )