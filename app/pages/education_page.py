import reflex as rx
import json
import os
import typing

from .base_page import base_page

# --- DATA LOADING ---

def load_education_data():
    file_path = os.path.join("assets", "education_data.json")
    
    try:
        if not os.path.exists(file_path):
            file_path = os.path.join(os.getcwd(), "assets", "education_data.json")
            
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading education data: {e}")
        return []

EDUCATION_DATA = load_education_data()

# --- SHARED HELPER COMPONENTS ---

def gpa_badge(gpa_detail_string: str) -> rx.Component:
    """Renders the GPA badge."""
    return rx.badge(
        rx.text(gpa_detail_string, size="4"),
        variant="soft", 
        color_scheme="indigo", 
        size="3",
        margin_left="1px", 
        margin_y="0",
    )

def linked_logo(full_logo_path: str, card_href: str, institution: str) -> rx.Component:
    """Renders the linked institution logo."""
    return rx.cond(
        full_logo_path != "",
        rx.link(
            rx.image(
                src=full_logo_path,
                alt=f"{institution} logo",
                width="48px",
                height="48px",
                border_radius="8px",
                object_fit="contain",
                margin_top="5px", 
                margin_left="5px", 
                on_click=rx.stop_propagation
            ),
            href=card_href,
            is_external=True,
            on_click=rx.stop_propagation
        ),
        rx.box(width="48px", height="48px", border_radius="8px", background="gray.700")
    )

def title_section(edu: typing.Dict[str, typing.Any], linked_logo_comp: rx.Component) -> rx.Component:
    """Renders the institution title and logo."""
    color_scheme = edu.get('color', 'blue')
    card_href = edu.get("href", "#") 
    
    return rx.hstack(
        linked_logo_comp,
        
        rx.link(
            rx.text(
                edu["institution"],
                size="6",
                weight="bold",
                color=color_scheme,
                _hover={"color": f"{color_scheme}.300"},
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

# --- DESKTOP LAYOUT (UNCHANGED) ---

def desktop_education_details(edu: typing.Dict[str, typing.Any], gpa_badge_comp: rx.Component) -> rx.Component:
    """
    Desktop layout:
    Line 1: Degree Title
    Line 2: Location | GPA | Date Range
    """
    # 48px (Logo) + 16px (Spacing) = 64px indent
    indent_offset = "64px" 
    
    # 1. Degree Title (Line 1)
    degree_line = rx.text(
        edu["degree"],
        size="5", 
        weight="bold", 
        color=rx.color_mode_cond("gray.900", "gray.100"), 
        margin_left=indent_offset,
        width="100%", 
        padding_top="2",
        white_space="normal", 
    )
    
    # 2. Location | GPA | Date Range (Line 2)
    details_line = rx.hstack(
        # Location
        rx.text(
            edu["location"],
            size="4",
            weight="medium",
            color=rx.color_mode_cond("gray.700", "gray.300"), 
            white_space="nowrap",
        ),
        rx.text("|", size="4", color="gray.500"),
        
        # GPA Label and Badge
        rx.text(
            "GPA: ",
            size="4",
            weight="medium",
            color=rx.color_mode_cond("gray.700", "gray.300"),
            white_space="nowrap",
        ),
        gpa_badge_comp,
        rx.text("|", size="4", color="gray.500"),
        
        # Date Range
        rx.text(
            edu["date_range"],
            size="4",
            weight="medium",
            color=rx.color_mode_cond("gray.700", "gray.300"),
            white_space="nowrap",
        ),
        
        align_items="center",
        spacing="3",
        margin_left=indent_offset, 
        width="100%",
        padding_bottom="3",
    )
    
    # Final container for desktop details
    return rx.vstack(
        degree_line,
        details_line,
        align_items="flex-start",
        spacing="0",
        width="100%",
        padding_x="6",
    )

# --- MOBILE LAYOUT (UPDATED FOR WRAPPING) ---

def mobile_education_details(edu: typing.Dict[str, typing.Any], gpa_badge_comp: rx.Component) -> rx.Component:
    """
    Mobile layout: All details stacked vertically, with degree wrapping enabled.
    Location, GPA, and Date are on separate lines.
    """
    # 48px (Logo) + 10px (Spacing) = 58px indent
    mobile_indent_offset = "58px" 
    
    return rx.vstack(
        # 1. Degree (Wrapped in a Box to control its width)
        rx.box(
            rx.text(
                edu["degree"],
                size="5",
                weight="bold", 
                color=rx.color_mode_cond("gray.900", "gray.100"), 
                white_space="normal", # Allows wrapping
            ),
            # CRITICAL FIX: Set padding-left on the Box/VStack and remove width/margin from inner text
            # The padding-left here ensures the content starts at the right place.
            padding_left=mobile_indent_offset, 
            width="100%", # Ensures the box itself contains content within bounds
            padding_top="2",
        ),
        
        # 2. Location (Separate Line)
        rx.text(
            edu["location"], 
            size="4",
            weight="medium",
            color=rx.color_mode_cond("gray.500", "gray.400"),
            margin_left=mobile_indent_offset,
            padding_top="1",
            width="100%",
            white_space="normal",
        ),

        # 3. GPA (Separate Line)
        rx.hstack(
            rx.text(
                "GPA:", 
                size="4",
                weight="medium",
                color=rx.color_mode_cond("gray.500", "gray.400"),
                white_space="nowrap",
            ),
            gpa_badge_comp, 
            spacing="2",
            align_items="center",
            margin_left=mobile_indent_offset,
            padding_top="1",
            width="100%",
        ),
        
        # 4. Date range (Separate Line)
        rx.text(
            edu["date_range"],
            size="3",
            weight="medium",
            color=rx.color_mode_cond("gray.500", "gray.400"),
            text_align="left", 
            width="100%",
            margin_top="1",
            margin_left=mobile_indent_offset,
            padding_bottom="4"
        ),
        
        align_items="flex-start",
        spacing="0",
        width="100%",
        padding_x="0", 
        padding_y="0"
    )

# --- MAIN CARD COMPONENT ---

def education_card(edu: typing.Dict[str, typing.Any]) -> rx.Component:
    
    logo_filename = edu.get('logo', '')
    campus_pic_filename = edu.get('campus_pic', '')
    card_href = edu.get("href", "#") 
    location = edu.get('location', '')
    gpa_detail_string = edu.get('details', '') 
    color_scheme=edu.get('color', 'blue')

    # Prepare shared sub-components
    gpa_comp = gpa_badge(gpa_detail_string)
    
    full_logo_path = rx.cond(logo_filename, "/" + logo_filename, "")
    linked_logo_comp = linked_logo(full_logo_path, card_href, edu["institution"])
    
    title_sec = title_section(edu, linked_logo_comp)
    
    # Campus Image Component
    full_campus_pic_path = rx.cond(campus_pic_filename, "/" + campus_pic_filename, "")
    campus_image = rx.cond(
        full_campus_pic_path != "",
        rx.link(
            rx.box(
                rx.image(
                    src=full_campus_pic_path,
                    alt=f"Campus image of {edu['institution']}",
                    width="100%",
                    height="auto",
                    object_fit="cover",
                    style={"aspectRatio": "21/9", "filter": "grayscale(10%) contrast(90%)"},
                ),
                width="100%",
                border_bottom_radius="xl", 
                overflow="hidden",
            ),
            href=card_href,
            is_external=True,
            width="100%",
            on_click=rx.stop_propagation
        ),
        rx.box()
    )
    
    # Description list (maintained structure)
    description_list = rx.vstack(
        spacing="1",
        align_items="flex-start",
        width="100%",
        padding_bottom="4",
        padding_x="6" 
    )

    # Responsive Detail Section (Switching Logic)
    responsive_details = rx.fragment(
        rx.desktop_only(
            desktop_education_details(edu, gpa_comp)
        ),
        rx.mobile_and_tablet(
            mobile_education_details(edu, gpa_comp)
        )
    )
    
    # The final education card structure
    return rx.vstack(
        title_sec,
        responsive_details, 
        campus_image, 
        description_list,
        
        spacing="1",
        width="100%",
        align_items="flex-start",
        border_radius="xl",
        padding="0",
        
        background=rx.color_mode_cond("white", "rgba(255, 255, 255, 0.05)"),
        box_shadow=rx.color_mode_cond("lg", "lg"),
        border=rx.color_mode_cond("1px solid var(--gray-4)", "1px solid rgba(255, 255, 255, 0.1)"),
        
        transition="all 0.2s ease-in-out",
        _hover={
            "box_shadow": rx.color_mode_cond("xl", "xl"),
            "transform": "translateY(-2px)",
            "border": f"1px solid var(--link-{color_scheme}-6)" 
        }
    )

# --- MAIN PAGE COMPONENT ---

def education(*args, **kwargs) -> rx.Component:
    """
    Displays education cards in a truly responsive two-column grid layout, centered
    and controlled by viewport padding.
    """
    
    return rx.center(
        rx.grid(
            rx.foreach(
                EDUCATION_DATA,
                lambda edu: rx.card(
                    education_card(edu),
                    height="100%", 
                    width="100%",
                    padding="0" 
                ),
            ),
            columns={"base": "1", "md": "1", "lg": "2"}, 
            spacing="5",
            width="90%", 
            align_items="stretch" 
        ),
        width="100%",
        padding_x={"base": "20px", "md": "40px", "lg": "10vw", "xl": "15vw"}, 
        padding_top="10px",
        padding_bottom="40px",
        id="education",
    )


def education_page() -> rx.Component: 
     return education()