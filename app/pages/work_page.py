import reflex as rx
import json
import os
import typing

from .base_page import base_page

# --- DATA LOADING FUNCTION (Simplified file-reading logic) ---

def load_work_data():
    """
    Reads the work experience data from the JSON file using the confirmed relative path.
    """
    file_path = os.path.join("assets", "work_experience.json")
    
    try:
        # Read the data from the external file
        with open(file_path, 'r') as f:
            loaded_data = json.load(f)
            return loaded_data
    except FileNotFoundError:
        print(f"Error: work_experience.json not found at the expected path: {file_path}. Returning empty list.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}. Returning empty list.")
        return []

# Load the data once when the script is initialized
WORK_EXPERIENCE_DATA = load_work_data()

# --- HELPER COMPONENTS ---

def tech_stack_row(tech_list: list) -> rx.Component:
    """Renders the technology stack badges."""
    return rx.flex(
        *[
            rx.badge(
                tech, 
                variant="soft", 
                color_scheme="indigo", 
                size="1",
                margin_right="2",
                margin_y="1",
            )
            for tech in tech_list
        ],
        spacing="1",
        padding_top="2",
        flex_wrap="wrap",
        width="100%", 
        min_width="0", 
    )


def project_details(project: dict) -> rx.Component:
    """Renders project title, description bullets, and tech stack. This is the deepest level (Level 3)."""
    
    return rx.box(
        rx.vstack(
            # 1. Project Title 
            rx.text(
                project["title"], 
                size="5", 
                weight="bold", 
                margin_bottom="2",
                word_break="break-word", 
                width="100%", 
                min_width="0",
                white_space="normal", # Ensure text is allowed to wrap normally
            ),
            
            # 2. Description Bullet Points 
            *[
                rx.text(
                    f"• {desc}", 
                    size="4",
                    text_align="left",
                    margin_bottom="1",
                    # FIX 2: Responsive padding_left: 0 on mobile, 2 for desktop/larger
                    padding_left={"base": "0", "md": "2"}, 
                    word_break="break-word", # Ensures long, unbroken text wraps
                    width="100%",
                    min_width="0",
                    white_space="normal", # CRITICAL FIX: Explicitly allow normal wrapping behavior
                    style={"hyphens": "auto"}, 
                )
                for desc in project['description'] 
            ],
            
            # 3. Technology Stack
            tech_stack_row(project["technology_stack"]),
            
            align_items="flex-start",
            width="100%",
        ),
        # Level 3 Indentation: Use base: 0 for mobile, 20px for desktop
        margin_left={"base": "0px", "md": "20px"}, 
        width="100%", 
        padding_bottom="4",
        min_width="0", 
    )

def role_section(role: dict) -> rx.Component:
    """Renders the Role title and date range, followed by project details. This is Level 2."""
    
    # 1. Title Component
    role_title = rx.text(
        role["title"], 
        size={"base": "6", "md": "6"}, 
        weight="bold",
        color_scheme="gray", 
        width={"base": "100%", "md": "auto"}, 
        word_break="break-word",
        min_width="0", 
        white_space="normal", # Ensure title wraps
    )
    
    # 2. Date Component
    role_date = rx.text(
        role["date_range"], 
        size="4", 
        weight="medium",
        color="gray",
        text_align={"base": "left", "md": "right"}, 
        margin_right={"base": "0", "md": "10px"},
        min_width={"base": "100%", "md": "max-content"},
    )
    
    # Responsive container for Title and Date: VStack on mobile, HStack on desktop
    responsive_header = rx.box(
        rx.fragment(
            # Desktop/Large Tablet: Title on left, Date on right (HStack)
            rx.desktop_only(
                rx.hstack(
                    role_title,
                    rx.spacer(),
                    role_date,
                    width="100%",
                    min_width="0",
                )
            ),
            # Mobile/Small Tablet: Title and Date stacked vertically (VStack)
            rx.mobile_and_tablet(
                rx.vstack(
                    role_title,
                    role_date,
                    width="100%",
                    align_items="flex-start",
                    spacing="0",
                )
            )
        ),
        margin_bottom="2", 
        width="100%",
        min_width="0",
    )
    
    return rx.box(
        rx.vstack(
            responsive_header,
            
            # All Projects under this Role
            *[project_details(proj) for proj in role["projects"]],
            
            align_items="flex-start",
            width="100%",
        ),
        # Level 2 Indentation: Use base: 0 for mobile, 10px for desktop
        margin_left={"base": "0px", "md": "10px"}, 
        width="100%",
        min_width="0",
    )

def company_section(company_data: typing.Dict[str, typing.Any]) -> rx.Component:
    """Renders the Company name and logo, followed by all roles. This is Level 1."""
    
    full_company_name = company_data["company"]
    display_name_to_use = company_data.get("display_name", full_company_name)
    
    logo_filename = company_data.get("logo") 
    company_href = company_data.get("href", "#") 
    color_scheme = company_data.get("color", "blue")
    
    full_logo_path = f"/{logo_filename}" if logo_filename else None

    # Define the linked logo component
    linked_logo = rx.cond(
        full_logo_path,
        rx.link( 
            rx.image(
                src=full_logo_path, 
                alt=f"{full_company_name} logo", 
                width="80px",
                height="80px",
                object_fit="contain",
                margin_right="3",
                border_radius="10px", 
            ),
            href=company_href, 
            is_external=(company_href != "#" and company_href.startswith("http")), 
        ),
        rx.box(), # Empty box if no logo path
    )
    
    # Define the linked heading component
    linked_heading = rx.link(
        rx.heading(
            display_name_to_use, 
            size="8", 
            weight="bold",
            color_scheme=color_scheme, 
            word_break="break-word", 
            min_width="0",
            white_space="normal", # Ensure heading wraps
        ),
        href=company_href, 
        is_external=(company_href != "#" and company_href.startswith("http")), 
        style={"textDecoration": "none", "minWidth": "0px"} 
    )
    
    return rx.card(
        rx.vstack(
            # Company Logo and Name in a horizontal stack. 
            rx.hstack(
                # 1. Linked Logo
                linked_logo,
                
                # 2. Linked Company Name Heading
                linked_heading,

                align_items="center",
                margin_bottom="4",
                flex_wrap="wrap", # Allows wrapping if space is tight
                width="100%",
                min_width="0",
            ),
            
            # All Roles within this company
            *[role_section(role) for role in company_data["roles"]],
            
            align_items="flex-start",
            width="100%",
        ),
        # Card settings
        width="100%", 
        margin_y="4",
        padding="6",
        
        # ADDED HOVER LOGIC FOR CONSISTENCY
        transition="all 0.2s ease-in-out",
        _hover={
            "box_shadow": rx.color_mode_cond("xl", "xl"),
            "transform": "translateY(-2px)",
            "border": f"1px solid var(--link-{color_scheme}-6)" 
        }
        # END HOVER LOGIC
    )

# The main component that stitches everything together
def work(*args, **kwargs) -> rx.Component:
    return rx.center(
        rx.vstack(
            # Loop through the loaded data
            *[company_section(data) for data in WORK_EXPERIENCE_DATA],
            
            spacing="5",
            align="center",
            # User's desired 90% width (relative to container size)
            width="90%", 
            min_height="85vh",
        ),
        # Removed top padding, keeping it clean
        width="100%",
    )


def work_page() -> rx.Component: 
     return base_page(work())