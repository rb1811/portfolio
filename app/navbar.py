import reflex as rx
import json
import os
import typing

# --- Data Loading for Static Assets ---

def get_resume_path() -> str:
    """
    Reads the 'resume' filename from assets/contact_me.json and returns 
    the root-relative URL path to the resume asset.
    """
    file_path = os.path.join("assets", "contact_me.json")
    try:
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                data = json.load(f)
                filename = data.get('resume', "")
                if filename:
                    return f"/{filename.lstrip('/')}"
        return "" 
    except Exception as e:
        print(f"Error reading contact_me.json or parsing resume path: {e}")
        return "" 


# --- Component Functions (Unchanged) ---

def get_nav_link_href(text: str) -> str:
    """Determines the correct URL path for a navigation item."""
    if text == "Contact-Me":
        return "/contact"
    return f"/{text.lower().replace('-', '')}"


def navbar_icons_item(text: str, icon: str) -> rx.Component:
    return rx.link(
        rx.hstack(
            rx.icon(icon), 
            rx.text(
                text, 
                size="5", 
                weight="medium",
                white_space="nowrap",
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
    """Renders the printer icon wrapped in a Reflex link for external navigation."""
    is_available = get_resume_path() != ""
    icon_size = 24
    
    tooltip_content: typing.Union[str, rx.Var] = rx.cond(
        is_available,
        "Download Me", 
        "Resume link not available",
    )
    
    icon_element = rx.icon(
        "printer", 
        size=icon_size, 
        color=rx.cond(is_available, "var(--gray-12)", "var(--gray-7)"),
    )
    
    return rx.tooltip( 
        rx.link(
            icon_element,
            href=rx.cond(
                is_available,
                get_resume_path(), 
                "#" # Use '#' as a fallback if the link isn't available
            ),
            is_external=True, 
            target="_blank",  # Opens the PDF in a new browser tab
            
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
                    rx.color_mode.button(), 
                    
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
        
        # --- CRITICAL FIXES APPLIED HERE (Affects the Color Mode Button Functionality) ---
        bg=rx.color("accent", 3),
        padding="1em",
        width="100%",
        max_width="100%", 
        z_index="999", # Added: Ensures the navbar (and the button) is above other content
    )