"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
from .pages.base_page import base_page

# Import all pages from the 'pages' directory
from . import pages

class State(rx.State):
    pass

# --- 1. Define the custom font links using rx.el.link ---
ICEBERG_FONT_LINKS = [
    # Preconnect for faster loading
    rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
    rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", crossorigin="anonymous"),
    rx.el.link(
        rel="stylesheet",
        href="https://fonts.googleapis.com/css2?family=Iceberg&display=swap",
    ),
]
# -----------------------------------------------------------


def index() -> rx.Component:  
    return base_page()  

# --- 2. Initialize the App with head_components ---
app = rx.App(
    head_components=ICEBERG_FONT_LINKS,
)
# --------------------------------------------------

# --- ALL ORIGINAL ROUTES PRESERVED ---
app.add_page(index)
app.add_page(pages.about_page, route="/about")
app.add_page(pages.work_page, route="/work")
app.add_page(pages.contact_me_page, route="/contact")
app.add_page(pages.skills_page, route="/skills")
app.add_page(pages.projects_page, route="/projects")
app.add_page(pages.education_page, route="/education")