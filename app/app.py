"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
from .pages.base_page import base_page

# Import all pages from the 'pages' directory
from . import pages

class State(rx.State):
    pass

# --- 1. Define the custom font links using rx.el.link ---
# We use rx.el.link (the raw HTML element component) for head_components 
# to ensure it generates a self-closing <link> tag without validation errors.
HOMEMADE_APPLE_FONT_LINKS = [
    # Preconnect for faster loading
    rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
    rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin="anonymous"),
    # The main font stylesheet link
    rx.el.link(
        rel="stylesheet",
        href="https://fonts.googleapis.com/css2?family=Homemade+Apple&display=swap",
    ),
]
# -----------------------------------------------------------


def index() -> rx.Component:  
    return base_page()  

# --- 2. Initialize the App with head_components ---
# We add the font links here so they are globally available in the HTML <head>
app = rx.App(
    head_components=HOMEMADE_APPLE_FONT_LINKS,
)
# --------------------------------------------------

app.add_page(index)
app.add_page(pages.about_page, route="/about")
app.add_page(pages.work_page, route="/work")
app.add_page(pages.contact_me_page, route="/contact")
app.add_page(pages.skills_page, route="/skills")
app.add_page(pages.projects_page, route="/projects")
app.add_page(pages.education_page, route="/education")