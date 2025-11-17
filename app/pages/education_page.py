import reflex as rx
import json
import os

from .base_page import base_page

# --- DATA LOADING FUNCTION ---

def load_education_data():
    """Reads the education data from the JSON file."""
    file_path = os.path.join("assets", "education_data.json")
    
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading education data: {e}")
        return []

# Load the data once
EDUCATION_DATA = load_education_data()

# --- HELPER COMPONENTS ---

def education_card(edu: dict) -> rx.Component:
    """
    Creates a responsive, visually striking card for an education entry. 
    It uses the logo as a background or overlay element for visual interest.
    """
    
    logo_path = f"/{edu.get('logo')}" if edu.get('logo') else None
    card_href = edu.get("href", "#") # Get the href for linking the entire card
    
    # The VSTACK holds all the text content
    text_content = rx.vstack(
        # 1. Degree Title (e.g., Masters in Computer Science)
        rx.text(
            edu["degree"],
            size="6",
            weight="bold",
            color="white", 
        ),
        
        # 2. Institution Name (Now a clickable link)
        rx.link(
            rx.text(
                edu["institution"],
                size="5",
                weight="medium",
                color="white",
                text_decoration="underline", # Add visual cue for link
                _hover={"color": f"var(--{edu['color']}-3)"} # Highlight on hover
            ),
            href=card_href,
            is_external=True,
            style={"textDecoration": "none"}, # Prevent double underline from inner text
            # FIXED: Use rx.stop_propagation() instead of a lambda to stop the event bubble
            on_click=rx.stop_propagation() 
        ),
        
        # 3. Location and GPA Details
        rx.text(
            f"{edu['location']} | {edu['details']}",
            size="4",
            weight="light",
            color="gray.300",
        ),
        
        # 4. Date Range 
        rx.text(
            edu["date_range"],
            size="3",
            weight="medium",
            color="gray.200",
            margin_top="3"
        ),

        align_items="flex-start",
        width="100%",
        z_index="2" # Keep text on top
    )

    # The background box containing the text content, overlay, and image
    background_box = rx.box(
        text_content,
        # Semi-transparent overlay 
        background="rgba(0, 0, 0, 0.4)", 
        position="absolute",
        top="0",
        left="0",
        width="100%",
        height="100%",
        padding="6",
        border_radius="lg",
        # Gradient based on the color from JSON
        style={
            "background": f"linear-gradient(135deg, var(--{edu['color']}-9) 0%, rgba(0,0,0,0.5) 100%)"
        },
        z_index="1"
    )
    
    # Background Image (Logo)
    logo_image = rx.cond(
        logo_path,
        rx.image(
            src=logo_path,
            alt=f"{edu['institution']} logo",
            object_fit="cover", 
            opacity="0.2", 
            position="absolute",
            top="0",
            left="0",
            width="100%",
            height="100%",
            z_index="0"
        ),
        rx.box(background=f"var(--{edu['color']}-9)", position="absolute", top="0", left="0", width="100%", height="100%", z_index="0")
    )
    
    # Outer box wrapped in a link
    return rx.link(
        rx.box(
            background_box,
            logo_image,

            # Outer box styling (sets size and positioning context)
            width="100%",
            min_height="250px",
            position="relative", 
            border_radius="lg",
            overflow="hidden", 
            box_shadow="lg",
            # The link itself is the interactive element, but we use the box style for visual feedback
            transition="all 0.3s ease",
            _hover={
                "box_shadow": "var(--shadow-xl)",
                "transform": "translateY(-5px)"
            }
        ),
        href=card_href,
        is_external=True, # Links to external university sites
        width="100%", # Ensures the link takes full grid cell width
        style={"textDecoration": "none"} # Remove default link style
    )


# --- MAIN PAGE COMPONENT ---

def education(*args, **kwargs) -> rx.Component:
    """The main education component."""
    return rx.box(
        rx.vstack(
            rx.heading("My Education", size="9", margin_y="6"),
            
            # Use rx.grid for responsive 2-column layout (stacks on smaller screens)
            rx.grid(
                *[education_card(edu) for edu in EDUCATION_DATA],
                
                # Grid settings
                columns={"base": "1", "md": "2"}, # 1 column on mobile, 2 columns on medium screens and up
                spacing="5",
                width="100%",
                max_width="1000px", # Control overall width
                padding="5",
            ),
            
            spacing="5",
            align="center",
            width="100%", 
            min_height="85vh",
        ),
        max_width="100%", 
        width="100%",
    )


def education_page() -> rx.Component: 
     return base_page(education())