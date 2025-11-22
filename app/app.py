"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
# from .pages.about_page import about_page # REMOVED: No longer imported individually

# Import all pages from the 'pages' directory
from . import pages
from .pages.base_page import base_page # NEW: Import the modified base_page

class State(rx.State):
    pass

# --- 1. Define the custom font links using rx.el.link ---
ALL_FONT_LINKS = [
    # Preconnect for faster loading (needed only once)
    rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
    rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin="anonymous"),
    
    # Combined link for all custom fonts: Iceberg and Mountains of Christmas
    rx.el.link(
        rel="stylesheet",
        href="https://fonts.googleapis.com/css2?family=Iceberg&family=Mountains+of+Christmas:wght@400;700&family=Iceland&display=swap",
    ),
]
# -----------------------------------------------------------

# --- NEW: Consolidate all page components into one vertical stack ---
def single_page_content() -> rx.Component:
    """Combines all logical 'pages' into a single scrollable view."""
    return rx.vstack(
        # IMPORTANT: These page functions must be updated to wrap their content
        # in rx.box(..., id="section_name") for scrolling to work.
        pages.about_page(),     # Links to /#about
        pages.work_page(),      # Links to /#work
        pages.education_page(), # Links to /#education
        pages.skills_page(),    # Links to /#skills
        pages.projects_page(),  # Links to /#projects
        pages.contact_me_page(),# Links to /#contact
        
        spacing="9", 
        width="100%",
        align="center",
    )

def index() -> rx.Component:  
    # Now calls the new base_page with the combined content
    return base_page(single_page_content())  

# --- 2. Initialize the App with head_components ---
app = rx.App(
    enable_state=False,
    head_components=ALL_FONT_LINKS,
    style={
        "body": {
            # Define the CSS Variable for Navbar Height
            "--navbar-height": "75px", 
            # We keep this for smooth scrolling, but it's not the primary fix.
            "scroll-behavior": "smooth", 
        }
    }
)
# --------------------------------------------------

# --- UPDATED ROUTES: Only keep the root route ---
app.add_page(index)
# app.add_page(pages.about_page, route="/about") # REMOVED
# app.add_page(pages.work_page, route="/work") # REMOVED
# app.add_page(pages.contact_me_page, route="/contact") # REMOVED
# app.add_page(pages.skills_page, route="/skills") # REMOVED
# app.add_page(pages.projects_page, route="/projects") # REMOVED
# app.add_page(pages.education_page, route="/education") # REMOVED