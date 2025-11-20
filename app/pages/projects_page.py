import reflex as rx
import typing
import json
import os
from pydantic import Field 
from .base_page import base_page


# Define a single, consistent color scheme.
DEFAULT_COLOR = "indigo"

# --- Structured Data Class Definition ---
class ProjectData(rx.Base):
    """
    Defines the structure of a single project item using rx.Base (Pydantic).
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
    
    # NOTE: In a Reflex app, assets should be placed in the project root's 'assets' folder
    # and Reflex handles compilation/access. Use the direct path for Python loading.
    file_path = os.path.join(os.getcwd(), "assets", "projects_data.json")
    
    projects_dicts: typing.List[dict] = []
    
    # 1. Try to load JSON data
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                projects_dicts = json.load(f)
            print(f"Successfully loaded {len(projects_dicts)} raw project items.")
        else:
            print(f"Error: Project data file not found at: {file_path}")
            
    except json.JSONDecodeError as e:
        print(f"Error decoding project data JSON: {e}")
        return []
    except Exception as e:
        print(f"General error loading project data: {e}") 
        return []

    # 2. Process and validate projects
    processed_projects: typing.List[ProjectData] = []
    
    for project_dict in projects_dicts:
        try:
            project = ProjectData(**project_dict)
            project.tech_stack = project.languages_used
            processed_projects.append(project)
        except Exception as e:
            # Added robust error handling for individual item validation failures
            print(f"Validation Error for item: {project_dict.get('title', 'Unknown Project')}. Error: {e}")

    print(f"Successfully processed {len(processed_projects)} valid project items.")
    return processed_projects


# Load data into a constant list
PROJECTS_DATA_LIST: typing.List[ProjectData] = load_projects_data()

# --- STATE MANAGEMENT ---
class ProjectState(rx.State):
    """State to manage and iterate over project data."""
    projects_data: typing.List[ProjectData] = PROJECTS_DATA_LIST


# --- HELPER COMPONENTS: PROJECT DIALOG ---

def project_dialog(project: rx.Var[ProjectData]) -> rx.Component:
    """A dialog component to show full project details."""
    
    # Define common padding for content indentation inside the dialog
    dialog_padding_x = "4"
    
    # Create a component to render the full description as an unordered list
    full_description_list = rx.unordered_list(
        rx.foreach(
            project.full_description,
            lambda item: rx.list.item(
                item,
                margin_bottom="10px",
                color=rx.color_mode_cond("gray.700", "gray.300"),
                size="3", # Increased font size for better readability
            ),
        ),
        margin_top="20px",
        padding_x=dialog_padding_x,
        margin_bottom="10px",
    )
    
    # Conditional image display component
    project_image = rx.cond(
        project.image, # If the image field is not None/empty
        rx.center(
            rx.image(
                # Fixed the previous error by directly binding the image path string.
                src=project.image.to(str),
                # Styling for full width and mid-height (max 300px)
                width="100%", 
                max_height="300px",
                object_fit="contain", # Ensures the image fits without cropping
                border_radius="xl",
                box_shadow="lg",
                margin_y="6", # Add spacing above and below the image
                alt=project.title, # Added alt text for accessibility
            ),
            width="100%",
            padding_x=dialog_padding_x,
            padding_y="10px",
        )
    )
    
    # NEW: Determine the display name for the extra link
    extra_link_name = rx.cond(
        project.extra_href_display_name,
        project.extra_href_display_name.to(str) + ": ",
        rx.text("Research Paper: ", weight="bold", white_space="nowrap") # Default fallback text
    )

    # NEW: Research Paper Link Section uses the dynamic name
    research_paper_link_section = rx.cond(
        project.extra_href, 
        rx.hstack(
            rx.text(
                rx.cond(
                    project.extra_href_display_name,
                    project.extra_href_display_name + ": ",
                    "Research Paper: "
                ),
                weight="bold", 
                white_space="nowrap"
            ),
            rx.link(
                "Link", 
                href=project.extra_href.to(str), 
                is_external=True,
                color_scheme=project.color, 
                text_decoration="underline",
                _hover={"color": project.color + ".8"},
                on_click=rx.stop_propagation
            ),
            align_items="center",
            padding_x=dialog_padding_x,
            margin_y="3",
            margin_bottom="30px" 
        )
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
            # --- Fixed padding placement ---
            rx.dialog.title(project.title, size="5"),
            
            # Divider after title - Increased margin_y for more space below title
            rx.divider(margin_y="8"),
            
            # Consolidated content section for uniform padding/spacing
            rx.vstack(
                # Full Description 
                rx.box(
                    full_description_list,
                    width="100%",
                    text_align="left", 
                    padding="0", 
                ),
                
                # Source Code Link Section
                rx.hstack(
                    rx.text("Source Code: ", weight="bold", white_space="nowrap"),
                    rx.link(
                        project.href,
                        href=project.href.to(str),
                        is_external=True,
                        color_scheme=project.color,
                        text_decoration="underline",
                        _hover={"color": project.color + ".8"},
                        on_click=rx.stop_propagation
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

            # Divider before footer
            rx.divider(margin_y="5"),
            
            # Close button at bottom left
            rx.flex(
                rx.dialog.close(
                    rx.button("Close", variant="soft", color_scheme="gray"),
                ),
                justify="start", 
                width="100%",
                margin_top="20px",
                padding_x=dialog_padding_x, 
            ),
            
            # Keyword argument placement
            padding="24px", 
        ),
        # Increased max_width to make dialog bigger 
        max_width="800px" 
    )


# --- HELPER COMPONENTS: PROJECT CARD ---

def project_card(project: rx.Var[ProjectData]) -> rx.Component:
    """
    A card displaying a single project.
    """
    
    teamsize_condition = project.teamsize == 1
    
    # Team size badge (Placed below the title)
    teamsize_badge = rx.badge(
        rx.cond(
            teamsize_condition,
            "Individual",
            "Team of " + project.teamsize.to(str)
        ),
        variant="soft", 
        color_scheme=project.color,
        size="2",
        font_weight="bold",
        align_self="flex-start",
        margin_top="3", 
        margin_bottom="4", 
    )

    # 1. Tech stack display (Label + Badges) 
    tech_stack_content = rx.cond(
        # Check if the list length is > 0
        project.tech_stack.length() > 0,
        rx.vstack(
            rx.text("Tech Stack:", size="2", weight="bold", color=rx.color_mode_cond("gray.600", "gray.400"), margin_bottom="1"),
            rx.hstack(
                rx.foreach(
                    project.tech_stack, 
                    lambda tech: rx.badge(
                        tech,
                        color_scheme=project.color,
                        variant="outline",
                        size="1",
                    ),
                ),
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
        # Change title color based on color mode
        color=rx.color_mode_cond("gray.900", "white"), 
        _hover={"color": project.color + ".8"},
        # Apply negative margin to pull title further left for indentation effect
        margin_left="-15px" 
    )
    
    # Short Description
    short_description_text = rx.text(
        project.short_description,
        size="3",
        # Change description color based on color mode
        color=rx.color_mode_cond("gray.600", "gray.400"), 
        margin_top="3", 
        text_align="left", 
        width="100%",
    )
    
    # Source Code link
    source_code_link = rx.hstack(
        # Change label color based on color mode
        rx.text("Source Code:", size="2", weight="bold", color=rx.color_mode_cond("gray.600", "gray.400")),
        rx.link(
            "Link", 
            href=project.href.to(str),
            is_external=True,
            color_scheme=project.color,
            text_decoration="underline",
            _hover={"color": project.color + ".8"},
            on_click=rx.stop_propagation
        ),
        align_items="center",
        align_self="flex-start", 
        margin_top="4", # Vertical spacing
    )
    
    # Calculate hover border color
    hover_border_color = "1px solid var(--link-" + project.color + "-6)"
    
    # Common horizontal padding for card content (increased for more padding/indentation)
    card_content_padding_x = "30px" 
    
    # Define a consistent bottom padding
    card_content_padding_bottom = "20px"

    return rx.vstack(
        # --- Content Wrapper: Contains everything except the button/footer ---
        rx.box(
            rx.vstack(
                title_text,      
                rx.divider(margin_y="0"), # Divider below title
                teamsize_badge,  
                
                # --- Main Content Block (gets flex_grow) ---
                rx.vstack(
                    short_description_text,
                    rx.box(flex_grow=1), # Pushes the tech stack/link down for short descriptions
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
            padding_top="20px", # Added top padding for consistency
            padding_bottom=card_content_padding_bottom, 
        ),
        
        # --- SPACER: Takes up all remaining space in the card, pushing the footer down ---
        rx.box(flex_grow=1), 
        
        # --- Divider: Placed right before the button ---
        rx.divider(margin_y="0"),
        
        # Dialog Trigger Section (The anchored footer button)
        rx.box(
            project_dialog(project),
            width="100%",
        ),
        
        # Card styling
        width="100%",
        height="100%",
        flex_grow=1, # Allows the card to stretch to the height of its row
        align_items="flex-start", 
        border_radius="xl",
        padding="0", 
        
        # Make card background, shadow, and border conditional based on color mode
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

# --- MAIN PAGE COMPONENT (CHILD) ---

def projects(*args, **kwargs) -> rx.Component:
    """
    Displays project cards in a responsive grid layout.
    """
    return rx.center(
        rx.vstack(
            rx.grid(
                rx.foreach(
                    ProjectState.projects_data,
                    lambda project: rx.card(
                        project_card(project),
                        width="100%",
                        padding="0",
                    ),
                ), 
                
                # Responsive columns: 1 column on mobile, 2 on tablet, 3 on desktop
                columns={"base": "1", "md": "2", "lg": "3"},
                spacing="5",
                width="100%", 
                align_items="stretch", # Ensures all cards in a row match the height of the tallest card
            ),
            width="90%",
            max_width="1200px"
        ),
        width="100%",
        padding_x="20px",
        padding_y="10px", 
    )


def projects_page() -> rx.Component: 
    return base_page(projects())