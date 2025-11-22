import reflex as rx
import typing
import json
import os
from pydantic import Field, BaseModel
from .base_page import base_page


# Define a single, consistent color scheme.
DEFAULT_COLOR = "indigo"

# --- Structured Data Class Definition ---
class ProjectData(BaseModel):
    """
    Defines the structure of a single project item using (Pydantic).
    This ensures type-safe access to project attributes.
    """
    title: str
    short_description: str
    full_description: typing.List[str] 
    teamsize: int 
    href: str # This is now for the "Source Code" link
    languages_used: typing.List[str] # Data source from JSON
    extra_href: typing.Optional[str] = Field(None) # For research papers, etc.
    # NEW: The display name for the extra link (e.g., "Research Paper", "Course Link")
    extra_href_display_name: typing.Optional[str] = Field(None)
    # Optional image path for the project card
    image: typing.Optional[str] = Field(None) 
    
    color: str = DEFAULT_COLOR
    tech_stack: typing.List[str] = Field(default_factory=list)


# --- DATA LOADING AND PROCESSING ---

def load_projects_data() -> typing.List[ProjectData]:
    """
    Loads project data from 'assets/projects_data.json'. 
    Maps 'languages_used' to 'tech_stack' for display.
    """
    
    file_path = os.path.join(os.getcwd(), "assets", "projects_data.json")
    projects_dicts: typing.List[dict] = []
    
    # 1. Try to load JSON data
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                projects_dicts = json.load(f)
            print(f"Successfully loaded {len(projects_dicts)} raw project items.")
        else:
            # Fallback path check
            file_path = os.path.join("assets", "projects_data.json")
            with open(file_path, 'r') as f:
                projects_dicts = json.load(f)
            print(f"Successfully loaded {len(projects_dicts)} raw project items from fallback path.")
            
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Error loading project data: {e}")
        return []
    except Exception as e:
        print(f"General error loading project data: {e}") 
        return []

    # 2. Process and validate projects
    processed_projects: typing.List[ProjectData] = []
    for project_dict in projects_dicts:
        try:
            # Pydantic validation and object creation
            project = ProjectData(**project_dict)
            # Map languages_used to tech_stack for display consistency
            project.tech_stack = project.languages_used
            processed_projects.append(project)
        except Exception as e:
            print(f"Validation Error for item: {project_dict.get('title', 'Unknown Project')}. Error: {e}")

    print(f"Successfully processed {len(processed_projects)} valid project items.")
    return processed_projects


# Load data into a constant list
PROJECTS_DATA_LIST: typing.List[ProjectData] = load_projects_data()


# --- HELPER COMPONENTS: PROJECT DIALOG ---

# Since the ProjectData object is static, we must process it inside the function.
# The type hint is now a concrete Python object, not an rx.Var.
def project_dialog(project: ProjectData) -> rx.Component:
    """A dialog component to show full project details."""
    
    dialog_padding_x = "4"
    
    # Create a list of description items statically
    full_description_list_items = [
        rx.list.item(
            rx.text(
                item,
                size="3", 
                color=rx.color_mode_cond("gray.700", "gray.300"),
                word_break="break-word", 
            ),
            margin_bottom="10px",
        )
        for item in project.full_description
    ]
    
    # Render the static list comprehension results
    full_description_list = rx.unordered_list(
        *full_description_list_items,
        margin_top="20px",
        padding_x=dialog_padding_x,
        margin_bottom="10px",
    )
    
    # Conditional image display component (using static path/check)
    project_image = rx.cond(
        project.image, 
        rx.center(
            rx.image(
                src=f"/{project.image}",
                width="100%", 
                max_height="300px",
                object_fit="contain",
                border_radius="xl",
                box_shadow="lg",
                margin_y="6",
                alt=project.title,
            ),
            width="100%",
            padding_x=dialog_padding_x,
            padding_y="10px",
        ),
        rx.box()
    )
    
    # Research Paper Link Section (using static check)
    research_paper_link_section = rx.cond(
        project.extra_href, 
        rx.hstack(
            rx.text(
                # Use Python ternary operator logic here for static name
                f"{project.extra_href_display_name or 'Research Paper'}: ",
                weight="bold", 
                white_space="nowrap"
            ),
            rx.link(
                "Link", 
                href=project.extra_href, 
                is_external=True,
                color_scheme=project.color, 
                text_decoration="underline",
                _hover={"color": f"var(--{project.color}-8)"},
                on_click=rx.stop_propagation
            ),
            align_items="center",
            padding_x=dialog_padding_x,
            margin_y="3",
            margin_bottom="30px" 
        ),
        rx.box()
    )
    
    
    return rx.dialog.root(
        rx.dialog.trigger(
            rx.button(
                "Read Full Story", 
                size="3", 
                color_scheme=project.color,
                variant="soft",
                width="100%",
                box_shadow=rx.color_mode_cond("0 4px 6px -1px rgba(0, 0, 0, 0.1)", "0 4px 6px -1px rgba(255, 255, 255, 0.05)"),
                _hover={"opacity": 0.9, "cursor": "pointer"},
                margin_bottom="0",
                border_bottom_radius="xl",
                border_top_radius="0",
            )
        ),
        rx.dialog.content(
            rx.dialog.title(project.title, size="5"),
            
            rx.divider(margin_y="8"),
            
            rx.vstack(
                # Full Description 
                rx.box(
                    full_description_list,
                    width="100%",
                    text_align="left", 
                    padding="0", 
                    overflow_wrap="break-word", 
                ),
                
                # Source Code Link Section
                rx.hstack(
                    rx.text("Source Code: ", weight="bold", white_space="nowrap"),
                    rx.link(
                        project.href,
                        href=project.href, # Use static href directly
                        is_external=True,
                        color_scheme=project.color,
                        text_decoration="underline",
                        _hover={"color": f"var(--{project.color}-8)"},
                        on_click=rx.stop_propagation,
                        word_break="break-all"
                    ),
                    align_items="center",
                    padding_x=dialog_padding_x,
                    margin_bottom="10px",
                ),
                
                # Image display (conditionally rendered)
                project_image,
                
                # Extra Link Section (dynamically named)
                research_paper_link_section,
                
                align_items="flex-start",
                width="100%",
                padding_y="5",
            ),

            rx.divider(margin_y="5"),
            
            rx.flex(
                rx.dialog.close(
                    rx.button("Close", variant="soft", color_scheme="gray"),
                ),
                justify="start", 
                width="100%",
                margin_top="20px",
                padding_x=dialog_padding_x, 
            ),
            
            padding="24px", 
        ),
        max_width={"base": "95vw", "sm": "95vw", "md": "700px"} 
    )


# --- HELPER COMPONENTS: PROJECT CARD ---

# The type hint is now a concrete Python object, not an rx.Var.
def project_card(project: ProjectData) -> rx.Component:
    """
    A card displaying a single project.
    """
    
    teamsize_condition = project.teamsize == 1
    
    # Team size badge (Placed below the title)
    teamsize_badge = rx.badge(
        # Use simple Python conditional logic
        "Individual" if teamsize_condition else f"Team of {project.teamsize}",
        variant="soft", 
        color_scheme=project.color,
        size="2",
        font_weight="bold",
        align_self="flex-start",
        margin_top="3", 
        margin_bottom="4", 
    )

    # 1. Tech stack display (Label + Badges) 
    # Generate badges using a static list comprehension
    tech_badges = [
        rx.badge(
            tech,
            color_scheme=project.color,
            variant="outline",
            size="1",
        )
        for tech in project.tech_stack
    ]
    
    # Render the tech stack content conditionally based on the Python list size
    tech_stack_content = rx.cond(
        len(project.tech_stack) > 0,
        rx.vstack(
            rx.text("Tech Stack:", size="2", weight="bold", color=rx.color_mode_cond("gray.600", "gray.400"), margin_bottom="1"),
            rx.hstack(
                *tech_badges, # Unpack the static badges
                wrap="wrap",
                spacing="2",
                width="100%",
            ),
            align_items="flex-start",
            width="100%",
            margin_top="3", 
        )
    )

    # Title (now just text, no link)
    title_text = rx.text(
        project.title,
        size="6",
        weight="bold",
        color=rx.color_mode_cond("gray.900", "white"), 
        _hover={"color": f"var(--{project.color}-8)"},
        margin_left="-15px" 
    )
    
    # Short Description
    short_description_text = rx.text(
        project.short_description,
        size="3",
        color=rx.color_mode_cond("gray.600", "gray.400"), 
        margin_top="3", 
        text_align="left", 
        width="100%",
    )
    
    # Source Code link
    source_code_link = rx.hstack(
        rx.text("Source Code:", size="2", weight="bold", color=rx.color_mode_cond("gray.600", "gray.400")),
        rx.link(
            "Link", 
            href=project.href, # Static href
            is_external=True,
            color_scheme=project.color,
            text_decoration="underline",
            _hover={"color": f"var(--{project.color}-8)"},
            on_click=rx.stop_propagation
        ),
        align_items="center",
        align_self="flex-start", 
        margin_top="4",
    )
    
    # Calculate hover border color statically
    hover_border_color = f"1px solid var(--{project.color}-6)"
    
    card_content_padding_x = "30px" 
    card_content_padding_bottom = "20px"

    return rx.vstack(
        # --- Content Wrapper: Contains everything except the button/footer ---
        rx.box(
            rx.vstack(
                title_text,      
                rx.divider(margin_y="0"),
                teamsize_badge,  
                
                # --- Main Content Block (gets flex_grow) ---
                rx.vstack(
                    short_description_text,
                    rx.box(flex_grow=1), 
                    tech_stack_content, 
                    source_code_link,
                    align_items="flex-start",
                    width="100%",
                ),
                
                align_items="flex-start", 
                width="100%",
                padding="0",
            ),
            
            width="100%",
            padding_x=card_content_padding_x,
            padding_top="20px", 
            padding_bottom=card_content_padding_bottom, 
        ),
        
        # --- SPACER: Pushes the footer down ---
        rx.box(flex_grow=1), 
        
        # --- Divider: Placed right before the button ---
        rx.divider(margin_y="0"),
        
        # Dialog Trigger Section (The anchored footer button)
        rx.box(
            project_dialog(project), # Pass the static project object
            width="100%",
        ),
        
        # Card styling
        width="100%",
        height="100%",
        flex_grow=1, 
        align_items="flex-start", 
        border_radius="xl",
        padding="0", 
        
        background=rx.color_mode_cond("white", "#1e1e1e"),
        box_shadow=rx.color_mode_cond("lg", "lg"), 
        border=rx.color_mode_cond("1px solid var(--gray-4)", "1px solid rgba(255, 255, 255, 0.1)"), 
        transition="all 0.2s ease-in-out",
        _hover={
            "box_shadow": rx.color_mode_cond("xl", "xl"),
            "transform": "translateY(-2px)",
            "border": hover_border_color 
        }
    )

# --- STATIC PROJECT CARD GENERATION ---
# This list comprehension replaces the main rx.foreach loop.
STATIC_PROJECTS_CARDS = [
    rx.card(
        project_card(project), # Pass the static project object
        width="100%",
        padding="0",
    )
    for project in PROJECTS_DATA_LIST
]


# --- MAIN PAGE COMPONENT (CHILD) ---

def projects(*args, **kwargs) -> rx.Component:
    """
    Displays project cards in a responsive grid layout using static components.
    """
    return rx.center(
        rx.vstack(
            rx.grid(
                *STATIC_PROJECTS_CARDS, # Unpack the static components
                
                # Responsive columns: 1 column on mobile, 2 on tablet, 3 on desktop
                columns={"base": "1", "md": "2", "lg": "3"},
                spacing="5",
                width="100%", 
                align_items="stretch", 
            ),
            width="90%",
            max_width="100%",
            padding_top="10px", 
            padding_bottom="40px",
        ),
        width="100%",
        padding_x="20px",
        padding_y="10px", 
        id="projects",
    )


def projects_page() -> rx.Component: 
    # return base_page(projects())
    return projects()