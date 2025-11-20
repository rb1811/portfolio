import reflex as rx
import json
import os
import typing

# --- Data Loading and State for Static Assets ---

def get_resume_path() -> str:
    """
    Loads contact data to find the resume path. 
    
    Returns:
        str: The path to the resume (e.g., "/prabhat_racherla_resume.pdf") 
             or an empty string ("") if the file is missing or the 'resume' key is absent.
    """
    # This assumes 'assets/contact_me.json' is the standard path
    file_path = os.path.join("assets", "contact_me.json")
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
                resume_file = data.get('resume')
                if resume_file:
                    # Prepend / for Reflex to correctly serve the asset from the root
                    return f"/{resume_file}"
        
        # If file doesn't exist or 'resume' key is missing, return empty string.
        return "" 
        
    except Exception as e:
        print(f"Error reading contact_me.json: {e}")
        # Return empty string on error
        return "" 


class NavbarState(rx.State):
    """State to hold static asset links for the navbar."""
    resume_path: str = get_resume_path()


# --- Component Functions ---

def get_nav_link_href(text: str) -> str:
    """
    Determines the correct URL path for a navigation item.
    """
    if text == "Contact-Me":
        return "/contact"
    # Converts "Work", "Projects" to "/work", "/projects"
    return f"/{text.lower().replace('-', '')}"


def navbar_icons_item(text: str, icon: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon), 
            rx.text(
                text, 
                size="5", 
                weight="medium",
                white_space="nowrap", # Ensures text stays on one line
            )
        ), 
        href=get_nav_link_href(text) # Use corrected function
    )


def navbar_icons_menu_item(text: str, icon: str) -> rx.Component:
    return rx.menu.item(
        rx.link(
            rx.hstack(
                rx.icon(icon, size=16), 
                rx.text(text, size="4", weight="medium")
            ),
            href=get_nav_link_href(text) # Use corrected function
        )
    )


def resume_download_icon() -> rx.Component:
    """
    Renders the printer icon wrapped in a Reflex Tooltip.
    Uses an rx.box as a consistent, larger hover target.
    """
    is_available = NavbarState.resume_path != ""
    icon_size = 24
    
    # 1. Define the Tooltip Content
    tooltip_content: typing.Union[str, rx.Var] = rx.cond(
        is_available,
        "Download Me",
        "Resume link not available",
    )
    
    # 2. Define the Icon Component
    icon_element = rx.icon(
        "printer", 
        size=icon_size, 
        color=rx.cond(is_available, "var(--gray-12)", "var(--gray-7)"),
    )
    
    # 3. Define the Clickable/Hoverable Trigger Box
    trigger_box = rx.box(
        icon_element,
        padding="4px",
        border_radius="md",
        # Use pointer cursor if available, otherwise 'not-allowed'
        cursor=rx.cond(is_available, "pointer", "not-allowed"),
        opacity=rx.cond(is_available, 1.0, 0.6),
        # Add visual feedback on hover only if available
        _hover=rx.cond(
            is_available, 
            {"background_color": rx.color("accent", 5), "opacity": 0.8}, 
            {} # No hover effect if not available
        ),
        # Handle the click action (for both desktop and mobile taps)
        on_click=rx.cond(is_available, rx.redirect(NavbarState.resume_path, is_external=True), None), 
    )

    # 4. Wrap the trigger box in the tooltip
    return rx.tooltip( 
        trigger_box, 
        content=tooltip_content, 
        side="bottom",
        # Keep the z_index high for visibility over the navbar
        z_index="9999", 
        # Minimal delay to aid reliable detection
        delay_duration=100, 
        # Force it to render even if the trigger is slightly obscured (though z_index should handle this)
        # Using rx.box instead of rx.link inside the tooltip simplifies the DOM structure for the trigger.
    )


def navbar_icons() -> rx.Component:
    """The main navbar component."""
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                # 1. Name/Logo (Left)
                rx.link(
                    rx.hstack(
                        rx.heading(
                            "Prabhat Racherla", 
                            size="7", 
                            weight="bold",
                            white_space="nowrap",
                        ),
                        align_items="center",
                    ),
                    href="/about"
                ),
                
                # Use the new dedicated component for the icon/tooltip
                rx.box(
                    resume_download_icon(),
                    margin_left="5px",
                ),
                
                # 2. Navigation Links Group (Centered)
                rx.hstack(
                    navbar_icons_item("Work", "briefcase-business"),
                    navbar_icons_item("Education", "school"),
                    navbar_icons_item("Skills", "chart-bar"),
                    navbar_icons_item("Projects", "folder-git-2"),
                    navbar_icons_item("Contact-Me", "contact-round"),
                    spacing="7", 
                    flex_grow=1, 
                    justify="center", 
                ),
                
                # 3. Empty Placeholder (Right)
                rx.box(), 

                # Set main properties on the outer desktop Hstack
                justify="between",
                align_items="center",
                width="100%", 
            ),
        ),
        
        rx.mobile_and_tablet(
            rx.hstack(
                rx.link(
                    rx.hstack(
                        rx.heading("Prabhat Racherla", size="6", weight="bold"),
                        align_items="center",
                    ),
                    href="/about"
                ),
                
                # Use the new dedicated component for the icon/tooltip
                rx.box(
                    resume_download_icon(),
                    margin_right="3", 
                ),
                
                rx.menu.root(
                    rx.menu.trigger(rx.icon("menu", size=30)),
                    rx.menu.content(
                        navbar_icons_menu_item("Work", "briefcase-business"),
                        navbar_icons_menu_item("Education", "school"),
                        navbar_icons_menu_item("Skills", "chart-bar"),
                        navbar_icons_menu_item("Projects", "folder-git-2"),
                        navbar_icons_menu_item("Contact-Me", "contact-round"),
                    ),
                    justify="end",
                ),
                justify="between",
                align_items="center",
            ),
        ),
        bg=rx.color("accent", 3),
        padding="1em",
        width="100%",
        max_width="100%", # Ensures full width
    )