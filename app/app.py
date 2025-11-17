"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
from .pages.base_page import base_page


from . import pages

class State(rx.State):
    pass


def index() -> rx.Component:  
    return base_page()  

app = rx.App()
app.add_page(index)
app.add_page(pages.about_page, route="/about")
app.add_page(pages.work_page, route="/work")
app.add_page(pages.contact_me_page, route="/contact")
app.add_page(pages.skills_page, route="/skills")
app.add_page(pages.projects_page, route="/projects")
app.add_page(pages.education_page, route="/education")

