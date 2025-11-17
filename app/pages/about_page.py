import reflex as rx

from .base_page import base_page
from .default_content import about_me

def about_page() -> rx.Component: 
     return base_page(about_me()) 