import reflex as rx
import typing
import json
import os
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


# --- DATA LOADING (Global Constant) ---

def load_contact_data() -> ContactData:
    """Loads contact data from 'assets/contact_me.json'."""
    # NOTE: os.getcwd() might be unreliable in some environments, but we keep it for robustness.
    file_path = os.path.join(os.getcwd(), "assets", "contact_me.json")
    
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
                return ContactData(**data)
        else:
            # Fallback for a static build environment where the path might be flatter
            file_path = os.path.join("assets", "contact_me.json")
            with open(file_path, 'r') as f:
                data = json.load(f)
                return ContactData(**data)
            
    except Exception as e:
        print(f"Error loading contact data: {e}") 
        
    return ContactData(
        profile_pic="", 
        resume="",
        qrcode="",
        links=[]
    )
        
CONTACT_DATA: ContactData = load_contact_data()


# --- STATIC PATH COMPUTATION FUNCTIONS ---

def get_profile_image_path() -> str:
    """Computes the full path to the profile image/GIF."""
    if CONTACT_DATA.profile_pic:
        return f"/{CONTACT_DATA.profile_pic}"
    return ""

def get_qrcode_image_path() -> str:
    """Computes the full path to the QR code image."""
    if CONTACT_DATA.qrcode:
        return f"/{CONTACT_DATA.qrcode}"
    return ""


# --- SHARED COMPONENTS ---

ICEBERG_FONT = "'Iceberg', sans-serif" 
MAX_CONTENT_WIDTH = "1200px"


def contact_link_item(link: ContactLink) -> rx.Component:
    """Creates a single hyperlinked contact item using static data."""
    return rx.link(
        rx.hstack(
            rx.icon(
                tag=link.icon,
                width="40px",  
                height="40px", 
                color_scheme=link.color,
                margin_right="6",
                min_width="2.5em", 
            ),
            rx.vstack(
                rx.text(
                    link.href,
                    size={'base': '6', 'md': '7'},
                    weight="medium",
                    color_scheme=link.color, 
                    text_decoration="underline",
                    _hover={"color": f"var(--{link.color}-9)"}, 
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
        margin_y="2",
    )
    
# --- STATIC LINK GENERATOR ---
# This list comprehension replaces rx.foreach to generate static components.
STATIC_CONTACT_LINKS = [
    contact_link_item(link) for link in CONTACT_DATA.links
]


def qrcode_section() -> rx.Component:
    """Component to display the QR code using static path."""
    qrcode_path = get_qrcode_image_path()
    
    if not qrcode_path:
        return rx.box()

    return rx.center(
        rx.vstack(
            rx.text(
                "Download Me",
                size={'base': '6', 'md': '7'}, 
                weight="bold", 
                color=rx.color_mode_cond("black", "white"),
                text_align="center",
                margin_bottom="2",
                font_family=ICEBERG_FONT
            ),
            rx.image(
                src=qrcode_path, # Static path here
                alt="Resume QR Code",
                width="100%",
                max_width="250px",
                max_height="250px", 
                border_radius="lg",
                box_shadow="lg",
                margin_bottom="4",
            ),
            width="100%",
            max_width="250px",
            align_items="center",
            padding_y="4",
            border_top="1px solid var(--gray-5)",
        ),
        width="100%",
        justify_content="center", 
        padding_x={"base": "0", "md": "6"},
    )

def profile_image_component() -> rx.Component:
    """The core image/GIF component using static path."""
    profile_path = get_profile_image_path()
    
    if not profile_path:
        return rx.box()
        
    return rx.image(
        src=profile_path, # Static path here
        alt="Profile Image/GIF",
        width="100%", 
        max_width="100%", 
        border_radius="3xl",
        box_shadow=rx.color_mode_cond("0 15px 30px -10px rgba(0, 0, 0, 0.3)", "0 15px 30px -10px rgba(255, 255, 255, 0.15)"),
        object_fit="cover",
        aspect_ratio="1 / 1"
    )

# --- LAYOUTS ---

def desktop_contact_me_layout() -> rx.Component:
    """
    Desktop (lg) and above layout: 3fr (Details) | 7fr (Image) Grid.
    """
    # Components passed directly from the STATIC_CONTACT_LINKS list.
    contact_details_section = rx.vstack(
        *STATIC_CONTACT_LINKS, # Unpack the generated components
        qrcode_section(),
        align_items="flex-start",
        width="100%",
        height="100%", 
        padding_y="5",
        padding_right="5",
        justify_content="flex-start", 
    )

    profile_image_section = rx.center(
        rx.box(
            profile_image_component(),
            width="100%",
            height="100%",
            max_width="500px",
        ),
        width="100%",
        height="100%", 
        padding_y="5",
        justify_content="center",
        align_items="center",
    )
    
    return rx.grid(
        contact_details_section,
        profile_image_section,
        columns="3fr 7fr", 
        spacing="9", 
        width="100%",
        height="auto", 
        align_items="flex-start", 
    )

def mobile_contact_me_layout() -> rx.Component:
    """
    Mobile and Tablet (base/md) layout: simple vertical stack in full-width cards.
    """
    
    # 1. Image Card (Top)
    image_card = rx.card(
        rx.center(
            profile_image_component(),
            width="100%",
        ),
        width="100%",
        padding="6",
    )
    
    # 2. Links/QR Card (Bottom)
    links_and_qr = rx.card(
        rx.vstack(
            
            # All Links
            *STATIC_CONTACT_LINKS, # Unpack the generated components
            
            # QR Code Section (Centered and full width)
            qrcode_section(),

            align_items="center",
            width="100%",
        ),
        width="100%",
        padding="6",
        margin_top="6",
    )

    return rx.vstack(
        image_card,
        links_and_qr,
        width="100%",
        spacing="0",
        align_items="center",
    )


def contact_me(*args, **kwargs) -> rx.Component:
    """
    Main component for the contact me page with responsive layout switch.
    """
    return rx.center(
        rx.vstack(
            rx.desktop_only(desktop_contact_me_layout()),
            rx.mobile_and_tablet(mobile_contact_me_layout()),
            
            # Use 95% width on mobile to give slight margin, and full width on desktop
            width={"base": "95%", "md": "90%", "lg": "100%"}, 
            max_width=MAX_CONTENT_WIDTH, 
            
            # Increased top padding for better gap below the navbar
            padding_top="50px", 
            padding_bottom="10",
            
            # Reduced horizontal padding on the wrapper for mobile 
            padding_x={"base": "0", "md": "5"}, 
            
            # This ensures the vstack content is centered horizontally
            align_items="center", 
        ),
        # Ensure the outer center component pushes the content to the true center
        width="100%",
        justify="center",
        align_items="flex-start",
        id="contactme"
    )


def contact_me_page() -> rx.Component: 
    # Use base_page to wrap the content
    return contact_me()
    # return base_page(contact_me())