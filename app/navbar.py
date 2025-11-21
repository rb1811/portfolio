import reflex as rx
import json
import os
import typing

# --- Data Loading and State for Static Assets ---

# The hardcoded base URL has been removed. 
# The application will now rely on the filename being resolved 
# relative to the app's root path.

def get_resume_path() -> str:
    """
    Reads the 'resume' filename from assets/contact_me.json and returns 
    the root-relative URL path to the resume asset (e.g., "/prabhat_racherla_resume.pdf").
    """
    file_path = os.path.join("assets", "contact_me.json")
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
                
                # Get the filename from the JSON, e.g., "prabhat_racherla_resume.pdf"
                filename = data.get('resume', "")
                
                if filename:
                    # Return the path prefixed with a slash to be root-relative
                    # This should resolve to the correct asset path managed by Reflex.
                    return f"/{filename.lstrip('/')}"
        
        return "" 
        
    except Exception as e:
        # Print error message for debugging purposes
        print(f"Error reading contact_me.json or parsing resume path: {e}")
        return "" 


class NavbarState(rx.State):
    """State to hold static asset links for the navbar."""
    # State now holds the root-relative path
    resume_path: str = get_resume_path()

    # The custom download_resume function is removed, as linking is handled by rx.link.


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
        href=get_nav_link_href(text)
    )


def navbar_icons_menu_item(text: str, icon: str) -> rx.Component:
    return rx.menu.item(
        rx.link(
            rx.hstack(
                rx.icon(icon, size=16), 
                rx.text(text, size="4", weight="medium")
            ),
            href=get_nav_link_href(text)
        )
    )


def resume_download_icon() -> rx.Component:
    """
    Renders the printer icon wrapped in a Reflex link for external navigation.
    """
    # Use Reflex-compatible comparison: check if the path variable is non-empty.
    # We must use rx.Var comparison to avoid VarTypeError
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
    
    # 3. Define the Link Trigger
    return rx.tooltip( 
        rx.link( # Using rx.link for the download target
            icon_element,
            # Use the root-relative path directly as the href
            href=rx.cond(
                is_available,
                NavbarState.resume_path, 
                "#" # Use '#' as a fallback if the link isn't available
            ),
            # is_external is important to make sure it functions as a native <a> tag link
            is_external=True, 
            target="_blank",  # Opens the PDF in a new browser tab
            
            # Styling for the hoverable area
            padding="4px",
            border_radius="md",
            cursor=rx.cond(is_available, "pointer", "not-allowed"),
            opacity=rx.cond(is_available, 1.0, 0.6),
            
            _hover=rx.cond(
                is_available, 
                {"background_color": rx.color("accent", 5), "opacity": 0.8}, 
                {}
            ),
        ),
        content=tooltip_content, 
        side="bottom",
        z_index="9999", 
        delay_duration=100, 
    )


def navbar_icons() -> rx.Component:
    """The main navbar component."""
    
    # Updated icons to use valid Lucide names (kebab-case)
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
                
                # Resume Icon
                rx.box(
                    resume_download_icon(),
                    margin_left="5px",
                ),
                
                # Color Mode Button
                rx.color_mode.button(), 
                
                # 2. Navigation Links Group (Centered)
                rx.hstack(
                    navbar_icons_item("Work", "briefcase-business"),
                    navbar_icons_item("Education", "school"),
                    navbar_icons_item("Skills", "bar-chart"), 
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
                # --- Grouping the Name, Printer, and Color Mode ---
                rx.hstack(
                    # 1. Name
                    rx.link(
                        rx.hstack(
                            rx.heading("Prabhat Racherla", size="6", weight="bold"),
                            align_items="center",
                        ),
                        href="/about"
                    ),
                    
                    # 2. Printer Icon
                    rx.box(
                        resume_download_icon(),
                        margin_left="2", 
                    ),
                    
                    # 3. Color Mode Button
                    # rx.color_mode.button(), 
                    
                    spacing="3", # Spacing between Name, Printer, and Mode Button
                    align_items="center",
                    flex_shrink=0, # Prevents this group from shrinking
                ),
                # --- END Grouping ---
                
                # The Menu Button remains separate to be pushed to the right
                rx.menu.root(
                    rx.menu.trigger(rx.icon("menu", size=30)),
                    rx.menu.content(
                        navbar_icons_menu_item("Work", "briefcase-business"),
                        rx.menu.separator(),
                        navbar_icons_menu_item("Education", "school"),
                        rx.menu.separator(),
                        navbar_icons_menu_item("Skills", "bar-chart"), 
                        rx.menu.separator(),
                        navbar_icons_menu_item("Projects", "folder-git-2"),
                        rx.menu.separator(),
                        navbar_icons_menu_item("Contact-Me", "contact-round"), 
                    ),
                ),
                
                # This ensures the new Left Group and the Menu are far apart
                justify="between", 
                align_items="center",
                width="100%", # Ensure the mobile Hstack takes full width
            ),
        ),
        bg=rx.color("accent", 3),
        padding="1em",
        width="100%",
        max_width="100%", # Ensures full width
    )