import reflex as rx
from .navbar import navbar_icons
# from .default_content import about_me # REMOVED: No longer needed here

# base_page now MUST accept the combined content as an argument
def base_page(child: rx.Component, *args, **kwargs) -> rx.Component:
    
    return rx.fragment(
        # 1. The Navbar is rendered first. The 'sticky' position will make it float.
        navbar_icons(),
        
        # 2. The single, long, scrollable content goes here.
        # Removed the outer padding, letting the content itself manage its spacing.
        rx.box(
            child, # This is the single_page_content() from app.py
            width="100%",
            padding="1em", # Removed this to give the content full width/control
            margin_top="200px",
            margin_bottom="200px",
        ),
    )