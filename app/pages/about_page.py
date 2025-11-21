import reflex as rx
import json
import os
import typing
from .base_page import base_page

# --- DATA LOADING ---
# Define a type hint for the loaded data structure
LoadedAboutMeData = typing.Dict[str, typing.Any]

def load_about_me_data() -> LoadedAboutMeData:
    """Loads the bio and personal insight data from the JSON file."""
    # Assuming the JSON file is placed in an 'assets' folder for Reflex
    # If the file is placed directly in the project root, adjust the path
    file_path = os.path.join("assets", "about_me_data.json")
    
    # Fallback path if 'assets' isn't the correct directory structure
    if not os.path.exists(file_path):
        file_path = "about_me_data.json"
        
    try:
        # NOTE: In a real Reflex app, you might use rx.get_asset() or similar.
        # Here we simulate local file reading for demonstration.
        with open(file_path, 'r') as f:
            data = json.load(f)
            # Ensure the structure matches the new object format
            if 'standard_bio' not in data or 'personal_insights' not in data or 'my_selfie' not in data:
                print("Warning: JSON structure mismatch. Using empty defaults.")
                # Ensure footnote key exists in default for safety
                return {"standard_bio": "", "personal_insights": [], "my_selfie": False, "footnote": {}}
            
            # Ensure footnote key exists even if it was missing in the loaded data for safety
            if 'footnote' not in data:
                data['footnote'] = {}
                
            return data
            
    except FileNotFoundError:
        print(f"Error: Data file not found at {file_path}. Using empty data.")
        return {"standard_bio": "", "personal_insights": [], "my_selfie": False, "footnote": {}}
    except Exception as e:
        print(f"Error loading about me data: {e}")
        return {"standard_bio": "", "personal_insights": [], "my_selfie": False, "footnote": {}}

ABOUT_ME_DATA = load_about_me_data()

# --- CONSTANTS ---
PROFILE_PIC_PATH = "/my_profile_pic.jpg"
# Define the custom font family string
TITLE_FONT = "'Mountains of Christmas', serif"
CONTENT_FONT = "'Iceland', serif"


# --- COMPONENTS ---

def section_header(text: str, custom_font: typing.Optional[str] = None) -> rx.Component:
    """A styled header for a major section, with optional custom font."""
    style_props = {
        "size": "9",
        "weight": "bold",
        "margin_top": "10px",
        "margin_bottom": "5px",
        "color": rx.color_mode_cond("black", "white"),
        "border_bottom": "2px solid var(--accent-8)",
        "padding_bottom": "2",
        "font_family": TITLE_FONT,
        "white_space": "normal", # Ensure header text wraps
        "width": "100%", # Ensure it takes up available width
    }
    
    if custom_font:
        style_props["font_family"] = custom_font
        # Increase text size slightly for decorative fonts
        style_props["size"] = "8" 
        
    return rx.heading(
        text,
        **style_props
    )

def bio_paragraph(text: str) -> rx.Component:
    """A standard, readable text paragraph."""
    return rx.text(
        text,
        size="8",
        margin_bottom="4",
        line_height="1.2", 
        color=rx.color_mode_cond("gray.700", "gray.300"),
        font_family=CONTENT_FONT,
        white_space="normal" 
    )

def personal_insight_card(data: dict) -> rx.Component:
    """A card for the more opinionated, insightful points."""
    return rx.card(
        rx.vstack(
            rx.heading(
                data["title"],
                size="5",
                weight="bold",
                color="indigo.500",
            ),
            # Content now uses the decorative font
            rx.text(
                data["content"],
                size="8",
                line_height="1.2", 
                color=rx.color_mode_cond("gray.700", "gray.400"),
                font_family=CONTENT_FONT,
                white_space="normal", 
            ),
            align_items="flex-start",
            spacing="3",
            width="100%"
        ),
        width="100%",
        padding="5",
        border_left="4px solid var(--indigo-8)",
        background=rx.color_mode_cond("white", "rgba(255, 255, 255, 0.05)"),
    )

def profile_picture_component() -> rx.Component:
    """
    The large profile picture component for desktop view.
    """
    return rx.center( 
        rx.vstack(
            rx.avatar(
                src=PROFILE_PIC_PATH,
                size="9", # Large size for desktop
                fallback="PR",
                radius="full",
                border="4px solid var(--accent-9)",
                box_shadow="lg",
                color_scheme="blue",
                color="blue.500",
                background="rgba(66, 153, 225, 0.1)", 
            ),
            align_items="center",
            width="100%",
        ),
        width="300px", # Fixed desktop width
        align_self="flex-start",
        margin_bottom="0",
    )

def top_bio_content() -> rx.Component:
    """The title and main biography text."""
    return rx.vstack(
        # 1. Professional Bio Header
        section_header("The Engineer"),
        
        # 2. Bio Paragraph
        bio_paragraph(ABOUT_ME_DATA["standard_bio"]),
        align_items="flex-start",
        width="100%",
    )

def top_bio_section() -> rx.Component:
    """
    Combines the main bio text and the profile picture (desktop only).
    """
    if not ABOUT_ME_DATA["standard_bio"]:
        return rx.box()

    # --- FIX APPLIED HERE ---
    # The LARGE profile picture is only visible on desktop and only if my_selfie is true.
    desktop_large_pic = rx.cond(
        # Condition 1: Check the flag (honor the flag)
        ABOUT_ME_DATA.get("my_selfie", False),
        
        # Condition 2: Check the screen size (hide on mobile)
        rx.desktop_only(
            rx.box(
                profile_picture_component(),
                align_self="flex-start", 
            )
        ),
        # If my_selfie is False, render an empty box (no change for mobile/desktop)
        rx.box()
    )
    # --- END FIX ---
    
    # The inner flex holds the content and has the width constraint
    inner_flex = rx.flex(
        top_bio_content(), # Text/Header (always the main column)
        desktop_large_pic, # Large Profile Pic (only visible on desktop AND if my_selfie=True)
        
        # Layout control: Column on mobile (text spans full width), Row on desktop
        direction={"base": "column", "lg": "row"},
        spacing="8",
        width="90%", 
        align_items="flex-start",
        padding_x={"base": "0", "md": "0"}, 
    )
    
    # The outer center component ensures the inner flex is centered horizontally
    return rx.center( 
        inner_flex,
        width="100%", 
        padding_y="8",
    )

def bottom_insights_section() -> rx.Component:
    """
    The section for personal insights, which spans the full width.
    """
    if not ABOUT_ME_DATA["personal_insights"]:
        return rx.box()

    return rx.center( # Center the content within the full width
        rx.vstack(
            # 1. "A Bit More About Me" Header
            section_header("A Bit More About Me"),
            # 2. Insights List
            rx.vstack(
                rx.foreach(
                    ABOUT_ME_DATA["personal_insights"],
                    personal_insight_card
                ),
                spacing="5",
                width="100%"
            ),
            align_items="flex-start",
            width="90%", # Match the top section width
            padding_x={"base": "0", "md": "0"},
            padding_bottom="8",
        ),
        width="100%",
    )

def footnote_section() -> rx.Component:
    """
    Displays the final footnote with a centered, larger image and text as a subscript.
    """
    footnote_data = ABOUT_ME_DATA.get("footnote", {})
    if not footnote_data or not footnote_data.get("content"):
        return rx.box()

    return rx.center(
        rx.vstack( # Use vstack to stack image and text vertically
            # AI Meme Image (Conditional, larger and centered)
            rx.cond(
                footnote_data.get("ai_meme"),
                rx.image(
                    src=f'/{footnote_data["ai_meme"]}',
                    alt="AI Meme",
                    width={"base": "200px", "md": "300px"}, # Larger on desktop
                    height={"base": "200px", "md": "300px"},
                    object_fit="contain",
                    border_radius="md",
                    margin_bottom="4", # Space between image and text
                ),
            ),
            
            # Footnote text as subscript
            rx.text(
                footnote_data["content"],
                size="4", # Smaller text for subscript/caption
                weight="medium",
                color="var(--gray-9)",
                font_style="italic",
                text_align="center", # Center the text below the image
                max_width="600px", # Limit text width for readability
            ),
            
            spacing="2", # Space between elements in the vstack
            align_items="center", # Center items within the vstack
            width="90%", # Match the content width
            max_width="1000px", # Keep overall max-width for the section
            margin_top="10px",
            padding="6",
            border_top="1px solid var(--gray-6)",
        ),
        width="100%",
    )


def about_me_section() -> rx.Component:
    """The main container combining all parts."""
    return rx.vstack(
        top_bio_section(),
        rx.box(height="10px"), # Visual spacer
        bottom_insights_section(),
        footnote_section(),
        
        width="100%",
        spacing="0" # Control spacing between the main sections manually
    )

def about_page() -> rx.Component:
     # No need for an extra center here, as the sections handle their own centering
     return base_page(
        about_me_section(),
        title="About Me"
     )