import reflex as rx
import json
import os
# Removed 'import urllib.parse' as it's no longer needed with space-free filenames

from .base_page import base_page

# --- COLOR MAPPING FOR COMPANIES ---
# Using standard Radix color names for light, professional variation.
COMPANY_COLOR_MAP = {
    "Microsoft Corporation": "orange",
    "Hewlett Packard Enterprise Company": "grass",
    "INDO-GERMAN INSTITUTE OF ADVANCED TECHNOLOGY": "blue",
}

# --- DATA LOADING FUNCTION (Simplified file-reading logic) ---

def load_work_data():
    """
    Reads the work experience data from the JSON file using the confirmed relative path.
    
    We attempt to load directly from 'assets/work_experience.json'.
    """
    file_path = os.path.join("assets", "work_experience.json")
    
    try:
        # CRITICAL: Read the data from the external file
        with open(file_path, 'r') as f:
            loaded_data = json.load(f)
            return loaded_data
    except FileNotFoundError:
        # Handle the case where the file is missing at the confirmed path.
        print(f"Error: work_experience.json not found at the expected path: {file_path}. Returning empty list.")
        return []
    except json.JSONDecodeError:
        # Handle the case where the file exists but the content is not valid JSON.
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
    )


def project_details(project: dict) -> rx.Component:
    """Renders project title, description bullets, and tech stack. This is the deepest level (Level 3)."""
    
    # We use rx.box with margin_left to achieve indentation relative to the Role title.
    return rx.box(
        rx.vstack(
            # 1. Project Title (placed above the description for better hierarchy)
            rx.text(
                project["title"], 
                size="5", 
                weight="bold", 
                margin_bottom="2"
            ),
            
            # 2. Description Bullet Points (CRITICAL: Loop through the array)
            *[
                rx.text(
                    f"• {desc}", # Add the bullet point symbol
                    size="4",
                    text_align="left",
                    margin_bottom="1",
                    # Indentation for the bullet point text itself to align text after the bullet
                    padding_left="2", 
                )
                for desc in project['description'] # Iterate over the description array
            ],
            
            # 3. Technology Stack
            tech_stack_row(project["technology_stack"]),
            
            align_items="flex-start",
            width="100%",
        ),
        # Level 3 Indentation: Pushed 20px right from the Role's start point
        margin_left="20px", 
        width="100%", 
        padding_bottom="4",
    )

def role_section(role: dict) -> rx.Component:
    """Renders the Role title and date range, followed by project details. This is Level 2."""
    
    # We use rx.box with margin_left to achieve indentation relative to the Company name.
    return rx.box(
        rx.vstack(
            # Role Title and Date (HStack to put date on the right)
            rx.hstack(
                rx.text(
                    role["title"], 
                    size="6", 
                    weight="bold",
                    color_scheme="gray", 
                ),
                rx.spacer(),
                rx.text(
                    role["date_range"], 
                    size="4", 
                    weight="medium",
                    color="gray"
                ),
                width="100%",
                margin_bottom="2", # Space between role title/date and first project
            ),
            
            # All Projects under this Role
            *[project_details(proj) for proj in role["projects"]],
            
            align_items="flex-start",
            width="100%",
        ),
        # Level 2 Indentation: Pushed 10px right from the Company's start point
        margin_left="10px", 
        width="100%",
    )

def company_section(company_data: dict) -> rx.Component:
    """Renders the Company name and logo, followed by all roles. This is Level 1."""
    company_name = company_data["company"]
    logo_filename = company_data.get("logo") 
    company_href = company_data.get("href", "#") 
    color_scheme = COMPANY_COLOR_MAP.get(company_name, "blue")
    
    # Image path uses the root-relative path (leading slash) as confirmed.
    full_logo_path = f"/{logo_filename}" if logo_filename else None

    # Define the linked logo component
    linked_logo = rx.cond(
        full_logo_path,
        rx.link( # The logo is now wrapped in an rx.link
            rx.image(
                src=full_logo_path, # Uses the corrected path format: /filename.png
                alt=f"{company_name} logo",
                width="40px",
                height="40px",
                object_fit="contain",
                margin_right="3",
                border_radius="10px", 
            ),
            href=company_href, # Use the href from JSON
            is_external=(company_href != "#" and company_href.startswith("http")), # Set to True if it looks like an external URL
        ),
        rx.box(), # Empty box if no logo path
    )
    
    # Define the linked heading component
    linked_heading = rx.link(
        rx.heading(
            company_name, 
            size="8", 
            weight="bold",
            color_scheme=color_scheme, 
        ),
        href=company_href, # Use the href from JSON
        is_external=(company_href != "#" and company_href.startswith("http")), # Set to True if it looks like an external URL
        style={"textDecoration": "none"} # Removes underline from heading link
    )
    
    return rx.card(
        rx.vstack(
            # Company Logo and Name in a horizontal stack
            rx.hstack(
                # 1. Linked Logo
                linked_logo,
                
                # 2. Linked Company Name Heading
                linked_heading,

                align_items="center",
                margin_bottom="4",
            ),
            
            # All Roles within this company
            *[role_section(role) for role in company_data["roles"]],
            
            align_items="flex-start",
            width="100%",
        ),
        # Card settings
        width="100%", 
        margin_y="4",
    )

# The main component that stitches everything together
def work(*args, **kwargs) -> rx.Component:
    return rx.box(
        rx.vstack(
            # CRITICAL: Loop through the loaded data
            *[company_section(data) for data in WORK_EXPERIENCE_DATA],
            
            spacing="5",
            align="center",
            width="100%", 
            min_height="85vh",
        ),
        max_width="100%", 
        width="100%",
    )


def work_page() -> rx.Component: 
     # Assuming base_page takes care of the overall layout, including header and footer.
     return base_page(work())