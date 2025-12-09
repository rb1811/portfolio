import reflex as rx
from typing import Optional

from .contact_me_page import CONTACT_DATA
from ..navbar import get_resume_path


def get_vcf_download_path() -> str:
    """Computes the correct path to the VCF file, matching the resume path logic."""
    if CONTACT_DATA.download_vcf:
        # This matches the working logic: prefix with / and ensure no double slash
        return f"/{CONTACT_DATA.download_vcf.lstrip('/')}"
    return ""

# --- Helper Component (remains the same) ---
def evcard_contact_item(icon_name: str, value: str, href: Optional[str] = None) -> rx.Component:
    # ... (content of this function remains the same)
    
    text_color = "white"
    
    if icon_name == "user":
        value_component = rx.heading(
            value, 
            size="6", 
            color=text_color, 
            weight="bold", 
            font_family="system-ui, sans-serif"
        )
    else:
        value_component = rx.text(
            value, 
            size="4", 
            color=text_color, 
            weight="medium", 
            font_family="system-ui, sans-serif"
        )

    content = rx.hstack(
        rx.icon(icon_name, size=24, color="var(--gray-6)"),
        value_component,
        spacing="3",
        align="center",
        padding_y="2",
    )

    if href:
        return rx.link(
            content, 
            href=href, 
            is_external=True, 
            text_decoration="none",
            _hover={"text_decoration": "underline", "color": "white"},
            width="100%", 
        )
    else:
        return content

def evcard_page(*args, **kwargs) -> rx.Component:
    """Creates the final e-vCard page with the VCF download button."""

    # Extract required data
    full_name = CONTACT_DATA.full_name
    phone_number = CONTACT_DATA.phone_number
    vcf_image_filename = CONTACT_DATA.vcf_image
    # NEW: VCF Download filename
    # vcf_download_filename = CONTACT_DATA.download_vcf 
    # vcf_download_path = f"/{CONTACT_DATA.download_vcf}"

    def find_link(name):
        return next((link for link in CONTACT_DATA.links if link.name == name), None)

    email_link = find_link("Email")
    website_link = find_link("Personal Website")

    # --- Layer 2: The Contact Details (Foreground) ---
    contact_content = rx.vstack(
        # 1. Full Name 
        evcard_contact_item("user", full_name),
        
        # Separator
        rx.divider(width="50%", margin_y="3", border_color="var(--gray-6)"),
        
        # 2. Phone Number
        evcard_contact_item("phone", phone_number, href=f"tel:{phone_number}"),
        
        # 3. Email
        *(
            [evcard_contact_item("mail", email_link.href, href=f"mailto:{email_link.href}")] 
            if email_link else []
        ),
        
        # 4. Personal Website
        *(
            [evcard_contact_item("globe", website_link.href, href=website_link.href)] 
            if website_link else []
        ),
        
        # --- VCF Download Button Section ---
        rx.box(
            # The rx.link handles the download attribute and points to the asset
            rx.link(
                rx.button(
                    "Add to Contacts",
                    size="1",
                    color_scheme="teal", # Use a vibrant color for the action
                    width="100%",
                ),
                # Href points to the static file in the assets folder
                href=get_vcf_download_path(),
                is_external=True,
                download=True, # Tells the browser to download the file instead of navigating
                width="100%",
            ),
            width="40%", # FIX 2: Reduced the width of the button container
            max_width="250px", # Added max width for control
            padding_top="50px", # FIX 1: Increased top padding to push button down
            padding_bottom="3", # Slight bottom padding for balance
        ),

        spacing="3",
        align_items="start", 
        width="100%",
    )
    
    # Layer 2 WRAPPER: This box provides the overlay styling.
    content_overlay_box = rx.box(
        contact_content,
        width="100%",
        height="100%",
        style={
            # Background opacity from previous fix (0.3)
            "backgroundColor": "rgba(0, 0, 0, 0.3)", 
            "padding": "20px", 
            "zIndex": 2, 
            "position": "absolute", 
            "top": "0", 
            "left": "0",
            "backdropFilter": "blur(1px)",
        },
    )

    # --- Layer 1: The Background Image (remains the same) ---
    background_image_box = rx.box(
        rx.image(
            src=f"/{vcf_image_filename}", 
            alt="Circuit Board Background",
            width="100%",
            height="100%",
            object_fit="cover",
        ),
        width="100%",
        height="100%",
        style={
            "position": "absolute",
            "top": "0",
            "left": "0",
            "zIndex": 1, 
        }
    )

    # --- The Main Card Container (remains the same) ---
    evcard = rx.box(
        background_image_box,     # Layer 1
        content_overlay_box,      # Layer 2
        
        width="100%", 
        max_width="450px", 
        min_height="550px",
        
        style={
            "position": "relative", 
            "borderRadius": "15px",
            "overflow": "hidden", 
            "boxShadow": "0 10px 30px rgba(0, 0, 0, 0.8)", 
        }
    )

    # The final container to center the card on the screen
    return rx.center(
        evcard,
        width="100%",
        min_height="100vh",
        padding_y="50px",
        background_color="#181818",
    )