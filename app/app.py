"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx

from rxconfig import config
from .work import work
from .base_page import base_page
from .about_page import about_me
from .projects import projects
from .education import education
from .skills import skills
from .work import work
from .contact_me import contact_me

class State(rx.State):
    pass


def index() -> rx.Component:  
    return base_page()  

def about_page() -> rx.Component: 
     return base_page(about_me()) 

def work_page() -> rx.Component: 
     return base_page(work()) 
 
def contact_me_page() -> rx.Component: 
    return base_page(contact_me()) 

def skills_page() -> rx.Component: 
    return base_page(skills()) 

def projects_page() -> rx.Component: 
    return base_page(projects()) 
 
def education_page() -> rx.Component: 
    return base_page(education()) 


app = rx.App()
app.add_page(index)
app.add_page(about_page, route="/about")
app.add_page(work_page, route="/work")
app.add_page(contact_me_page, route="/contact")
app.add_page(skills_page, route="/skills")
app.add_page(projects_page, route="/projects")
app.add_page(education_page, route="/education")

