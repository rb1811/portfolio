import reflex as rx
import typing
import json
import os
import time
from pydantic import BaseModel, Field
from .base_page import base_page 
from reflex.components.radix.themes.base import LiteralAccentColor


# --- Structured Data Class Definition ---

class ContactLink(BaseModel):
    """Defines the structure for a single contact link."""
    name: str 
    icon: str
    href: str
    color: LiteralAccentColor 

class ContactData(BaseModel):
    """Defines the overall structure of the contact data."""
    profile_pic: str
    resume: str
    qrcode: str 
    links: typing.List[ContactLink]
    name: str = "Prabhat Racherla"


# --- DATA LOADING AND STATE ---

def load_contact_data() -> ContactData:
    """Loads contact data from 'assets/contact_me.json'."""
    # Assuming 'assets' folder is at the project root level
    file_path = os.path.join(os.getcwd(), "assets", "contact_me.json")
    
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
                return ContactData(**data)
        else:
            print(f"Error: Contact data file not found at: {file_path}")
            
    except Exception as e:
        print(f"Error loading contact data: {e}") 
        pass
        
    return ContactData(
        profile_pic="", 
        resume="",
        qrcode="",
        links=[]
    )
        
CONTACT_DATA: ContactData = load_contact_data()


class ContactState(rx.State):
    """State to hold contact data."""
    contact_info: ContactData = CONTACT_DATA
    
    @rx.var
    def profile_image_path(self) -> str:
        """Computes the full path to the profile image/GIF."""
        if self.contact_info.profile_pic:
            return f"/{self.contact_info.profile_pic}"
        return ""

    @rx.var
    def qrcode_image_path(self) -> str:
        """Computes the full path to the QR code image."""
        if self.contact_info.qrcode:
            return f"/{self.contact_info.qrcode}"
        return ""


# --- COMPONENTS ---

# Define the font family for reuse
ICEBERG_FONT = "'Iceberg', sans-serif" 


def contact_link_item(link: rx.Var[ContactLink]) -> rx.Component:
    """
    Creates a single hyperlinked contact item.
    """
    return rx.link(
        rx.hstack(
            # Icon 
            rx.icon(
                tag=link.icon,
                width="40px",  
                height="40px", 
                color_scheme=link.color,
                margin_right="6",
                min_width="2.5em", 
            ),
            
            # Text is the URL/Handle
            rx.vstack(
                rx.text(
                    link.href,
                    size='7', 
                    weight="medium",
                    color_scheme=link.color, 
                    text_decoration="underline",
                    _hover={"color": link.color + ".8"},
                    font_family=ICEBERG_FONT 
                ),
                align_items="flex-start",
                spacing="1",
            ),
            align="center",
            width="100%",
        ),
        href=link.href,
        is_external=True,
        width="100%", 
        padding="6", 
        border_radius="xl", 
        # Interactive block style
        _hover={
            "background": rx.color_mode_cond("var(--gray-3)", "var(--gray-a3)"), 
            "cursor": "pointer",
            "transform": "scale(1.01)", 
            "box_shadow": rx.color_mode_cond(
                "0 4px 6px rgba(0, 0, 0, 0.1)", 
                "0 4px 6px rgba(255, 255, 255, 0.05)"
            ),
        },
        transition="all 0.2s ease-in-out",
        margin_y="4",
    )

def qrcode_section() -> rx.Component:
    """
    Component to display the QR code, placed immediately below the links.
    """
    return rx.cond(
        ContactState.qrcode_image_path,
        rx.center(
            rx.vstack(
                # Updated text
                rx.text(
                    "Download me", 
                    size="7", 
                    weight="bold", 
                    color=rx.color_mode_cond("black", "white"),
                    text_align="center",
                    margin_bottom="2",
                    font_family=ICEBERG_FONT
                ),
                rx.image(
                    src=ContactState.qrcode_image_path,
                    alt="Resume QR Code (Dummy)",
                    # Increased size
                    width="100%",
                    max_width="250px",
                    max_height="250px", 
                    border_radius="lg",
                    box_shadow="lg",
                    margin_bottom="4",
                    margin_left="50px"
                ),
                width="100%",
                max_width="250px",
                align_items="center",
                padding="6",
                padding_top="10", # Added padding above the QR code for separation
            ),
            width="100%",
            justify_content="flex-start", # Align left to match links
            padding_x="6",
        )
    )


def contact_details_section() -> rx.Component:
    """
    The left-hand side section displaying all contact links, followed by the QR code.
    No need for flex-grow spacer anymore.
    """
    return rx.vstack(
        # All Links
        rx.foreach(
            ContactState.contact_info.links,
            contact_link_item
        ),
        
        # QR Code Section (Immediately below the links)
        qrcode_section(),
        
        # Removed the rx.box(flex_grow=1) spacer
        
        align_items="flex-start",
        width="100%",
        # Critical: Remove height 100% since we don't need the column to stretch 
        # to the image height for forced alignment.
        height="auto", 
        padding_y="5",
        padding_x={"base": "0", "md": "5"},
        justify_content="flex-start", 
    )


def profile_image_section() -> rx.Component:
    """
    The right-hand side section displaying the profile image/GIF (7fr).
    """
    return rx.center(
        rx.box(
            rx.image(
                src=ContactState.profile_image_path,
                alt="Profile Image/GIF",
                width="100%", 
                max_width="100%", 
                border_radius="3xl",
                box_shadow=rx.color_mode_cond("0 15px 30px -10px rgba(0, 0, 0, 0.3)", "0 15px 30px -10px rgba(255, 255, 255, 0.15)"),
                object_fit="cover",
                aspect_ratio="1 / 1"
            ),
            height="100%", 
            width="100%",
        ),
        width="100%",
        height="100%", 
        padding_y="5",
        padding_x={"base": "0", "md": "5"},
        justify_content="center",
    )


def contact_me(*args, **kwargs) -> rx.Component:
    """
    Main component for the contact me page.
    """
    return rx.center(
        rx.grid(
            # Column 1: Contact Details (3fr)
            contact_details_section(),
            
            # Column 2: Profile Image/GIF (7fr)
            profile_image_section(),
            
            # Grid Configuration
            columns={"base": "1", "lg": "3fr 7fr"}, 
            spacing="9", 
            width="90%",
            max_width="1200px", 
            
            # Now the grid height depends only on the content
            height="auto", 
            
            # Use align_items="flex-start" to align the top of the columns
            align_items="flex-start", 
            margin_y="10",
        ),
        width="100%",
        padding_x="20px",
        padding_y="10px", 
        justify="center",
        
        # Ensure content starts from the top of the page (below header)
        align_items="flex-start", 
        padding_top="50px", 
    )


def contact_me_page() -> rx.Component: 
    return base_page(contact_me())