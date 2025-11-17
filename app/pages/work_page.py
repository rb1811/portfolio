import reflex as rx
import json
import os
from .base_page import base_page

# --- COLOR MAPPING FOR COMPANIES ---
COMPANY_COLOR_MAP = {
    "Microsoft Corporation": "orange",
    "Hewlett Packard Enterprise Company": "grass",
    "INDO-GERMAN INSTITUTE OF ADVANCED TECHNOLOGY": "blue",
}

# --- DATA LOADING FUNCTION ---

def load_work_data():
    """Reads the work experience data from the JSON file."""
    # Define potential file paths, with the most likely one first:
    file_paths_to_check = [
        os.path.join("assets", "work_experience.json"),
        "work_experience.json" 
    ]
    
    loaded_data = []
    found = False
    
    for file_path in file_paths_to_check:
        try:
            with open(file_path, 'r') as f:
                loaded_data = json.load(f)
                found = True
                break
        except FileNotFoundError:
            continue
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {file_path}.")
            return []
    
    if not found:
        print(f"Error: work_experience.json not found in any checked path (e.g., assets/work_experience.json). Returning empty list.")
        return []
        
    return loaded_data

# Load the data once when the script is initialized
WORK_EXPERIENCE_DATA = load_work_data()

# --- HELPER COMPONENTS ---

def tech_stack_row(tech_list: list) -> rx.Component:
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
    return rx.vstack(
        rx.text(
            f"• {project['description']}",
            size="4",
            padding_left="4",
            text_align="left",
            margin_bottom="1",
        ),
        tech_stack_row(project["technology_stack"]),
        align_items="flex-start",
        width="100%",
    )

def role_section(role: dict) -> rx.Component:
    return rx.vstack(
        # Role Title (Steel Grey) and Date (Right Aligned)
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
            margin_bottom="1",
        ),
        
        # Projects/Bullet Points
        *[project_details(proj) for proj in role["projects"]],
        
        align_items="flex-start",
        width="100%",
        padding_bottom="4",
    )

def company_section(company_data: dict) -> rx.Component:
    company_name = company_data["company"]
    color_scheme = COMPANY_COLOR_MAP.get(company_name, "blue")
    
    return rx.card(
        rx.vstack(
            # Company Name with Dynamic Color
            rx.heading(
                company_name, 
                size="8", 
                weight="bold",
                color_scheme=color_scheme, 
                margin_bottom="4",
            ),
            
            # All Roles within this company
            *[role_section(role) for role in company_data["roles"]],
            
            align_items="flex-start",
            width="100%",
        ),
        width="100%", 
        margin_y="4",
    )

# The main work component that stitches everything together
def work(*args, **kwargs) -> rx.Component:
    # Use rx.container for automatic centering and layout.
    return rx.box(
            rx.vstack(
                # CRITICAL: Loop through the loaded data
                *[company_section(data) for data in WORK_EXPERIENCE_DATA],
                
                spacing="5",
                align="center",
                width="100%",
                min_height="100%",
            ),
            max_width="100%", 
            width="100%",
            # padding_y="6", 
            # # Keep padding_x="6" for horizontal spacing inside the container
            # padding_x="6",
            # padding="1em"
    )


def work_page() -> rx.Component: 
     return base_page(work())