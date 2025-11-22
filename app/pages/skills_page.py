import reflex as rx
import json
import os
from .base_page import base_page
from reflex.components.radix.themes.base import LiteralAccentColor

# --- Data Loading ---

def load_skills_data():
    """Reads the skills data from the JSON file."""
    # Assuming assets/skills_data.json exists relative to the project root
    file_path = os.path.join("assets", "skills_data.json")
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading skills data: {e}")
        # Return an empty list on failure
        return []

SKILLS_DATA = load_skills_data()

# --- Helper Components (Adapted from previous template) ---

def skill_item(
    name: str, 
    progress: int, 
    color: LiteralAccentColor, 
    icon: str
) -> rx.Component:
    """Creates a single skill bar item."""
    
    # 1. Skill Name and Icon (Left Side)
    skill_info = rx.hstack(
        rx.icon(icon, size=24, color=f"{color}.9"),
        rx.text(
            name,
            size="4",
            weight="medium",
            # Ensure skill name is visible on all screen sizes
            min_width="100px", 
        ),
        width=["40%", "30%", "25%"],
        align="center",
        spacing="3",
    )

    # 2. Progress Bar and Percentage (Right Side)
    progress_bar = rx.flex(
        # Percentage text over the bar
        rx.text(
            f"{progress}%",
            position="absolute",
            top="50%",
            # Adjust left position to keep text clearly inside or near the bar end
            left=f"{progress-5}%", 
            transform="translateY(-50%)",
            size="2",
            weight="bold",
            color=rx.color_mode_cond("white", "black"),
            z_index="10"
        ),
        rx.progress(
            value=progress,
            height="25px",
            color_scheme=color,
            width="100%",
            # Ensure the progress bar background is visible
            background=rx.color_mode_cond("gray.200", "gray.700"),
            border_radius="lg"
        ),
        position="relative",
        width=["60%", "70%", "75%"],
        align_items="center",
        padding_left="2"
    )

    return rx.hstack(
        skill_info,
        progress_bar,
        width="100%",
        align="center",
        justify="between",
        padding_y="3",
        padding_x="4",
        border_radius="lg",
        cursor="pointer",
        # --- HOVER EFFECT ADDED HERE ---
        transition="all 0.2s ease-in-out",
        _hover={
            "background_color": rx.color_mode_cond("gray.50", "gray.800"),
            "transform": "scale(1.01)",
            "box_shadow": rx.color_mode_cond(
                "0 4px 6px rgba(0, 0, 0, 0.1)", 
                "0 4px 6px rgba(255, 255, 255, 0.05)"
            ),
        }
    )

def skill_category(category: dict) -> rx.Component:
    """Renders a category title and all skill items within it."""
    
    # 1. Category Title Header
    header = rx.hstack(
        rx.icon(category["category_icon"], size=30, color="indigo"),
        rx.heading(
            category["category_title"],
            size="7",
            weight="bold",
            color=rx.color_mode_cond("gray.900", "gray.100"),
            padding_bottom="3"
        ),
        width="100%",
        spacing="3",
        align="center",
    )
    
    # 2. List of Skills
    skill_list = rx.vstack(
        *[
            skill_item(
                name=skill["name"], 
                progress=skill["progress"], 
                color=skill["color"], 
                icon=skill["icon"]
            ) 
            for skill in category["skills"]
        ],
        width="100%",
        spacing="2",
        padding_left=["0", "0", "4"], # Indent skills slightly on desktop
    )
    
    # 3. Combine Header and List
    return rx.vstack(
        header,
        skill_list,
        width="100%",
        spacing="6",
        padding_top="6",
    )


# --- Main Page ---

def acquisition() -> rx.Component:
    """Renders all skill categories defined in SKILLS_DATA."""
    return rx.vstack(
        *[skill_category(category) for category in SKILLS_DATA],
        width="100%",
        spacing="8",
    )


def skills_page() -> rx.Component: 
    # Use base_page to wrap the content
        return rx.center(
            rx.vstack(
                rx.divider(width="100%", size="4"),
                acquisition(),
                width="90%",
                max_width="4xl",
                padding_y="12",
                spacing="8"
            ),
            width="100%",
            padding_x="6",
            id="skills"
        )
    
    # return base_page(
    #     rx.center(
    #         rx.vstack(
    #             rx.divider(width="100%", size="4"),
    #             acquisition(),
    #             width="90%",
    #             max_width="4xl",
    #             padding_y="12",
    #             spacing="8"
    #         ),
    #         width="100%",
    #         padding_x="6"
    #     )
    # )