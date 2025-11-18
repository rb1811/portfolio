import reflex as rx
import json
import os

from .base_page import base_page

# --- DATA LOADING FUNCTION ---

def load_education_data():
    """Reads the education data from the JSON file."""
    # NOTE: The logo image files must be present in the assets directory 
    # (e.g., assets/arizona_state_university.png)
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
    Creates an education card that is a structural replica of the work card style,
    and displays the GPA in a badge format.
    """
    
    logo_filename = edu.get('logo')
    full_logo_path = f"/{logo_filename}" if logo_filename else None
    
    card_href = edu.get("href", "#") 
    
    # --- GPA and Location Parsing (FIXED) ---
    # Data source structure: location is in 'location', GPA is in 'details' (e.g., "GPA: 3.73/4.0")
    
    location = edu.get('location', '')
    gpa_detail_string = edu.get('details', '')

    # 1. Parse the GPA detail string to separate the label (GPA:) from the score (X.XX/Y.Y)
    gpa_detail_parts = gpa_detail_string.split(':', 1)
    
    # Determine the display label (e.g., "GPA:") and the score (e.g., "3.73/4.0")
    if len(gpa_detail_parts) > 1:
        # e.g., parts[0]="GPA", parts[1]=" 3.73/4.0"
        gpa_label = gpa_detail_parts[0].strip() + ":"
        gpa_score = gpa_detail_parts[1].strip()
    else:
        # Fallback if 'details' is not in the expected format
        gpa_label = "GPA : "
        gpa_score = gpa_detail_string.strip() # May just be the score or the full string

    # 2. Define the GPA badge component
    gpa_badge = rx.badge(
        gpa_score,
        variant="soft", 
        color_scheme="indigo", 
        size="3",
        margin_left="1", # Small margin to separate it from the 'GPA:' label
        margin_y="0",
    )
    
    # 3. Create the Location and GPA text component
    location_and_gpa = rx.hstack(
        rx.text(
            f"{location} | {gpa_label}", # Combines location, separator, and the 'GPA:' label
            size="4",
            weight="medium",
            color=rx.color_mode_cond("gray.500", "gray.400"),
            margin_bottom="2",
            margin_left="4",
            white_space="nowrap",
        ),
        gpa_badge, # The new GPA badge with the score
        spacing="0",
        align_items="center"
    )
    # --- End GPA and Location Parsing ---

    # 1. Define the linked logo component
    linked_logo = rx.cond(
        full_logo_path,
        rx.link(
            rx.image(
                src=full_logo_path,
                alt=f"{edu['degree']} logo",
                width="48px",
                height="48px",
                border_radius="8px",
                object_fit="contain",
                on_click=rx.stop_propagation
            ),
            href=card_href,
            is_external=True,
            on_click=rx.stop_propagation
        ),
        rx.box(width="48px", height="48px", border_radius="8px", background="gray.700")
    )
    
    # 2. Main Title and Logo Section (HStack)
    title_section = rx.hstack(
        linked_logo,
        
        rx.link(
            rx.text(
                edu["degree"],
                size="6",
                weight="bold",
                color=f"{edu['color']}.400",
                _hover={"color": f"{edu['color']}.300"},
            ),
            href=card_href,
            is_external=True,
            style={"textDecoration": "none"},
            on_click=rx.stop_propagation
        ),
        spacing="4",
        align="center",
        width="100%",
        padding_top="4", 
        padding_x="6"
    )

    # 3. Details and Date Section (HStack)
    details_and_date = rx.hstack(
        rx.vstack(
            # Degree Name (e.g., Masters in Computer Science)
            rx.text(
                edu["institution"],
                size="5",
                weight="bold", 
                color=rx.color_mode_cond("gray.900", "gray.100"), 
                margin_left="4",
            ),
            
            # Location and GPA details (Now using the new component)
            location_and_gpa,
            
            align_items="flex-start",
            spacing="0",
            width="100%" 
        ),
        
        # Date Range (Time on the right)
        rx.text(
            edu["date_range"],
            size="3",
            weight="medium",
            color=rx.color_mode_cond("gray.500", "gray.400"),
            min_width="max-content",
            text_align="right",
            margin_right="10px"
        ),
        width="100%",
        spacing="4",
        padding_x="6"
    )
    
    # 4. Description (List of accomplishments, simplified for education)
    description_list = rx.vstack(
        spacing="1",
        align_items="flex-start",
        width="100%",
        padding_bottom="4",
        padding_x="6"
    )

    # 5. The final education card structure (VStack)
    return rx.vstack(
        title_section,
        details_and_date,
        description_list,
        
        spacing="1",
        width="100%",
        align_items="flex-start",
        border_radius="xl",
        padding="0",
        
        # --- RESPONSIVE STYLING FOR LIGHT/DARK MODE ---
        background=rx.color_mode_cond("white", "rgba(255, 255, 255, 0.05)"),
        box_shadow=rx.color_mode_cond("lg", "lg"),
        border=rx.color_mode_cond("1px solid var(--gray-4)", "1px solid rgba(255, 255, 255, 0.1)"),
        # --- END RESPONSIVE STYLING ---
        
        transition="all 0.2s ease-in-out",
        _hover={
            "box_shadow": rx.color_mode_cond("xl", "xl"),
            "transform": "translateY(-2px)",
            "border": f"1px solid var(--link{edu['color']}-6)" 
        }
    )

# --- MAIN PAGE COMPONENT ---

def education(*args, **kwargs) -> rx.Component:
    """The main education component, structured like the Work Experience page."""
    
    return rx.center( 
        rx.vstack(
            # List of education cards
            *[education_card(edu) for edu in EDUCATION_DATA],
            spacing="6",
            align="center",
            width="90%",
            max_width="7xl"
        ),
        width="100%",
        padding_y="12",
        padding_x="6"
    )


def education_page() -> rx.Component: 
     return base_page(education())