import reflex as rx
import typing
import json
import os
import time
from pydantic import BaseModel
from .base_page import base_page 
from reflex.components.radix.themes.base import LiteralAccentColor


# --- Structured Data Class Definition ---

class ContactLink(BaseModel):
    """Defines the structure for a single contact link."""
    icon: str
    href: str
    color: LiteralAccentColor # Use the proper type hint for color schemes

class ContactData(BaseModel):
    """Defines the overall structure of the contact data."""
    profile_pic: str
    resume: str
    links: typing.List[ContactLink]


# --- DATA LOADING AND STATE ---

def load_contact_data() -> ContactData:
    """Loads contact data from 'assets/contact_me.json'."""
    file_path = os.path.join("assets", "contact_me.json")
    
    try:
        # Load logic remains the same
        if os.path.exists(file_path):
            if os.path.isdir("./assets"):
                full_path = os.path.join("./assets", "contact_me.json")
            else:
                full_path = file_path

            with open(full_path, 'r') as f:
                data = json.load(f)
                return ContactData(**data)
    except Exception as e:
        print(f"Error loading contact data: {e}") 
        # Return a safe default/empty structure
        return ContactData(
            profile_pic="", 
            name="Error Loading Data", 
            tagline="Please check contact_me.json and ensure files are present.", 
            links=[]
        )
        
CONTACT_DATA: ContactData = load_contact_data()


class ContactState(rx.State):
    """State to hold contact data."""
    contact_info: ContactData = CONTACT_DATA
    
    @rx.var
    def profile_image_path(self) -> str:
        """Computes the full path to the profile image/GIF."""
        try:
            if self.contact_info.profile_pic:
                return f"/{self.contact_info.profile_pic}"
            raise FileNotFoundError("Profile pic missing")
        except Exception as ex:
            return("Error: Profile pic not found")

# --- COMPONENTS ---

# Define the font family for reuse
ICEBERG_FONT = "'Iceberg', sans-serif" 


def contact_link_item(link: rx.Var[ContactLink]) -> rx.Component:
    """
    Creates a single hyperlinked contact item, showing only the icon and the handle/URL.
    """
    return rx.link(
        rx.hstack(
            # Icon (remains large and visually distinct)
            rx.icon(
                tag=link.icon,
                width="40px",  
                height="40px", 
                color_scheme=link.color,
                margin_right="6",
                min_width="2.5em", 
            ),
            
            # Text is simplified to just the URL/Handle
            rx.vstack(
                # Use a large text size (size="7") for the URL/Handle
                rx.text(
                    link.href,
                    size='7', 
                    weight="medium",
                    is_external=True,
                    color_scheme=link.color, 
                    text_decoration="underline",
                    _hover={"color": link.color + ".8"},
                    # Apply the custom font directly to the text element
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
        # Mimic the interactive block style
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


def contact_details_section() -> rx.Component:
    """
    The left-hand side section displaying all contact links (3fr).
    """
    return rx.vstack(
        # Applying the custom font to the title as well
        rx.foreach(
            ContactState.contact_info.links,
            contact_link_item
        ),
        align_items="flex-start",
        width="100%",
        height="100%", 
        padding_y="5",
        padding_x={"base": "0", "md": "5"},
        justify_content="center", 
    )


def profile_image_section() -> rx.Component:
    """
    The right-hand side section displaying the profile image/GIF (7fr).
    The increased column width will make the GIF much larger.
    """
    return rx.center(
        # The rx.box fills the 7fr column space
        rx.box(
            rx.image(
                src=ContactState.profile_image_path,
                alt="Profile Image/GIF",
                # The image will now expand to fill the available space of the larger 7fr column
                width="100%", 
                # Keeping max_width here ensures it doesn't get ridiculously large on ultra-wide screens, 
                # but the 7fr column is the primary constraint. 
                max_width="100%", 
                border_radius="3xl",
                box_shadow=rx.color_mode_cond("0 15px 30px -10px rgba(0, 0, 0, 0.3)", "0 15px 30px -10px rgba(255, 255, 255, 0.15)"),
                object_fit="cover",
                aspect_ratio="1 / 1"
            ),
            width="100%",
            # Removed fixed pixel max_width to allow the image to scale with the grid column.
        ),
        width="100%",
        height="100%", 
        padding_y="5",
        padding_x={"base": "0", "md": "5"},
        justify_content="center",
    )


def contact_me(*args, **kwargs) -> rx.Component:
    """
    Main component for the contact me page, using a Grid with a 3fr/7fr split.
    """
    return rx.center(
        # Use rx.grid for the new 2-column structure on large screens
        rx.grid(
            # Column 1: Contact Details (30% width)
            contact_details_section(),
            
            # Column 2: Profile Image/GIF (70% width) - MUCH BIGGER
            profile_image_section(),
            
            # Grid Configuration
            # Define the columns: Links (3 parts) / Image (7 parts)
            columns={"base": "1", "lg": "3fr 7fr"}, 
            
            # On mobile, use a single column
            # spacing={"base": "9", "lg": "0"}, 
            spacing="9", 
            
            # Set a wide max_width for the entire grid
            width="90%",
            max_width="1200px", 
            
            min_height="80vh", 
            margin_y="10",
            align_items="center", # Center items vertically
        ),
        width="100%",
        padding_x="20px",
        padding_y="10px", 
        justify="center",
    )


def contact_me_page() -> rx.Component: 
    return base_page(contact_me())