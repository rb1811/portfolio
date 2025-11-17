import reflex as rx
from .navbar import navbar_icons
# from .navbar import navbar_buttons

def base_page(*args, **kwargs) -> rx.Component:
    return rx.fragment(
        rx.box(
            # navbar_buttons(),
            navbar_icons(),
            padding="1em",
            width="100%",
        ),
        rx.color_mode.button(position="bottom-right"),
        
    )