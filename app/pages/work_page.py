import reflex as rx
import json
import os
from .base_page import base_page

# --- DATA LOADING FUNCTION ---

def load_work_data():
    """Reads the work experience data from the JSON file."""
    # Define potential file paths, with the most likely one first:
    # 1. assets/work_experience.json (Relative to project root, standard Reflex location)
    # 2. work_experience.json (If the script is somehow executing inside assets/)
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
                break  # Exit loop if file is successfully loaded
        except FileNotFoundError:
            continue
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON format in {file_path}.")
            return [] # Fail immediately on JSON error
    
    if not found:
        # This will only execute if none of the paths worked
        print(f"Error: work_experience.json not found in any checked path (e.g., assets/work_experience.json). Returning empty list.")
        return []
        
    return loaded_data

# Load the data once when the script is initialized
WORK_EXPERIENCE_DATA = load_work_data()

# --- HELPER COMPONENTS ---

# Helper to render the tech stack as tags/badges
def tech_stack_row(tech_list: list) -> rx.Component:
    return rx.flex(
        *[
            rx.badge(
                tech, 
                variant="soft", 
                # FIX: Changed 'accent' to 'indigo' to use a supported color_scheme for rx.badge
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


# Helper to render a single project/bullet point
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

# Helper to render a single role (e.g., Software Engineer 2)
def role_section(role: dict) -> rx.Component:
    return rx.vstack(
        # Role Title and Date
        rx.hstack(
            rx.text(
                role["title"], 
                size="6", 
                weight="bold",
                color_scheme="blue",
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
        padding_bottom="4", # Spacing between roles
    )

# Helper to render a single company section
def company_section(company_data: dict) -> rx.Component:
    return rx.card(
        rx.vstack(
            # Company Name
            rx.heading(
                company_data["company"], 
                size="8", 
                weight="bold",
                color_scheme="blue",
                margin_bottom="4",
            ),
            
            # All Roles within this company
            *[role_section(role) for role in company_data["roles"]],
            
            align_items="flex-start",
            width="100%",
        ),
        width="100%",
        max_width="800px", # Keeps the content readable and centered
        margin_y="4",
    )

# The main work component that stitches everything together
def work(*args, **kwargs) -> rx.Component:
    return rx.vstack(
        # CRITICAL: Loop through the loaded data
        *[company_section(data) for data in WORK_EXPERIENCE_DATA],
        
        spacing="5",
        align="center",
        width="100%",
        min_height="85vh",
        padding="6",
    )


def work_page() -> rx.Component: 
     return base_page(work())