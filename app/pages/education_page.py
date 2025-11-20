import reflex as rx
import json
import os
import typing

from .base_page import base_page

# --- DATA LOADING ---

def load_education_data():
    file_path = os.path.join("assets", "education_data.json")
    
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading education data: {e}")
        return []

EDUCATION_DATA = load_education_data()

# --- HELPER COMPONENTS ---

def education_card(edu: typing.Dict[str, rx.Var]) -> rx.Component:
    
    logo_filename = edu.get('logo')
    campus_pic_filename = edu.get('campus_pic')
    card_href = edu.get("href", "#") 
    location = edu.get('location', '')
    gpa_detail_string = edu.get('details', '') 
    color_scheme=edu.get('color', 'blue')

    # Prepare paths for logo and campus image
    full_logo_path = rx.cond(
        logo_filename, 
        "/" + logo_filename, 
        "",                           
    )
    
    full_campus_pic_path = rx.cond(
        campus_pic_filename,
        "/" + campus_pic_filename,
        "",
    )
    
    # GPA badge component
    gpa_badge = rx.badge(
        rx.text(gpa_detail_string, size="4"),
        variant="soft", 
        color_scheme="indigo", 
        size="3",
        margin_left="1px", 
        margin_y="0",
    )
    
    # Location and GPA text component
    location_and_gpa = rx.hstack(
        rx.text(
            location, 
            size="4",
            weight="medium",
            color=rx.color_mode_cond("gray.500", "gray.400"),
            margin_bottom="2px",
            margin_left="10px",
            white_space="nowrap",
        ),
        rx.text(
            " GPA: ", 
            size="4",
            weight="medium",
            color=rx.color_mode_cond("gray.500", "gray.400"),
            margin_bottom="2px",
            margin_left="10px",
            white_space="nowrap",
        ),
        gpa_badge, 
        spacing="2", 
        align_items="center"
    )

    # Linked logo component
    linked_logo = rx.cond(
        full_logo_path != "",
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
    
    # Main Title and Logo Section (HStack)
    title_section = rx.hstack(
        linked_logo,
        
        rx.link(
            rx.text(
                edu["institution"],
                size="6",
                weight="bold",
                color=color_scheme,
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

    # Details and Date Section (HStack)
    details_and_date = rx.hstack(
        rx.vstack(
            rx.text(
                edu["degree"],
                size="5",
                weight="bold", 
                color=rx.color_mode_cond("gray.900", "gray.100"), 
                margin_left="10px",
            ),
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
    
    # Campus Image Component (New)
    campus_image = rx.cond(
        full_campus_pic_path != "",
        # FIX: Wrap the image display in rx.link to make it clickable
        rx.link(
            rx.box(
                rx.image(
                    src=full_campus_pic_path,
                    alt=f"Campus image of {edu['institution']}",
                    width="100%",
                    height="auto",
                    object_fit="cover",
                    style={
                        "aspectRatio": "21/9", # Set a fixed aspect ratio for visual consistency
                        "filter": "grayscale(10%) contrast(90%)", # Subtle filter for integration with dark mode
                    },
                ),
                # Padding removed to make the image span the full width of the card's interior
                width="100%",
                border_bottom_radius="xl", 
                overflow="hidden",
            ),
            href=card_href,            # <-- The key to making it a link
            is_external=True,
            width="100%",
            on_click=rx.stop_propagation # Use stop_propagation if the parent container is also clickable
        ),
        rx.box() # Empty box if no image is available
    )
    
    # Description list (maintained structure)
    description_list = rx.vstack(
        spacing="1",
        align_items="flex-start",
        width="100%",
        padding_bottom="4",
        padding_x="6"
    )

    # The final education card structure (VStack)
    return rx.vstack(
        title_section,
        details_and_date,
        
        # Place the image here
        campus_image, 
        
        description_list,
        
        spacing="1",
        width="100%",
        align_items="flex-start",
        border_radius="xl",
        padding="0",
        
        # Responsive styling
        background=rx.color_mode_cond("white", "rgba(255, 255, 255, 0.05)"),
        box_shadow=rx.color_mode_cond("lg", "lg"),
        border=rx.color_mode_cond("1px solid var(--gray-4)", "1px solid rgba(255, 255, 255, 0.1)"),
        
        transition="all 0.2s ease-in-out",
        _hover={
            "box_shadow": rx.color_mode_cond("xl", "xl"),
            "transform": "translateY(-2px)",
            "border": f"1px solid var(--link{edu['color']}-6)" 
        }
    )

# --- MAIN PAGE COMPONENT ---

def education(*args, **kwargs) -> rx.Component:
    """
    Displays education cards in a responsive two-column grid layout, centered
    on larger screens and stacked on mobile.
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
            # FIX: Changed list of strings to a dictionary for responsive props
            # 'base' and 'md' breakpoints get 1 column, 'lg' breakpoint gets 2 columns.
            columns={"base": "1", "md": "1", "lg": "2"}, 
            spacing="5",
            width="90%", 
            align_items="stretch" 
        ),
        width="100%",
        margin_left="20px" 
    )


def education_page() -> rx.Component: 
     return base_page(education())