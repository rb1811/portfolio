import reflex as rx


def navbar_icons_item(text: str, icon: str, url: str) -> rx.Component:
    # CRITICAL FIX: Add white_space="nowrap" to prevent text wrapping
    return rx.link(
        rx.hstack(
            rx.icon(icon), 
            rx.text(
                text, 
                size="4", 
                weight="medium",
                white_space="nowrap", # Ensures text stays on one line
            )
        ), 
        href=url
    )


def navbar_icons_menu_item(text: str, icon: str, url: str) -> rx.Component:
    return rx.link(
        rx.hstack(rx.icon(icon, size=16), rx.text(text, size="3", weight="medium")),
        href=url,
    )


def navbar_icons() -> rx.Component:
    return rx.box(
        rx.desktop_only(
            rx.hstack(
                
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
                
                # 2. Navigation Links Group (Centered in the available space)
                # CRITICAL CHANGE: This rx.hstack now uses the majority of the space
                # and centers its children.
                rx.hstack(
                    navbar_icons_item("Work", "briefcase-business", "/work"),
                    navbar_icons_item("Education", "school", "/education"),
                    navbar_icons_item("Skills", "chart-bar", "/skills"),
                    navbar_icons_item("Projects", "folder-git-2", "/projects"),
                    navbar_icons_item("Contact-Me", "contact-round", "/contact"),
                    spacing="7", 
                    # KEY FIX: Force this hstack to take up maximum space (flex-grow)
                    flex_grow=1, 
                    # KEY FIX: Center the items within the space it takes up
                    justify="center", 
                ),
                
                # 3. Empty Placeholder (STAYS RIGHT, but empty)
                # This empty box is added as a third child to make the main 
                # hstack have three sections (Left, Center, Right), allowing 
                # justify="between" to work properly.
                rx.box(), 

                # Set main properties on the outer desktop Hstack
                # KEY FIX: Using "between" now correctly separates the three children:
                # 1. Name, 2. Links Group (which is centered), and 3. Empty Box.
                justify="between",
                align_items="center",
                width="100%", 
            ),
        ),
        rx.mobile_and_tablet(
            # ... (Mobile code remains the same)
            rx.hstack(
                rx.link(
                    rx.hstack(
                        rx.heading("Prabhat Racherla", size="6", weight="bold"),
                        align_items="center",
                    ),
                    href="/about"
                ),
                rx.menu.root(
                    rx.menu.trigger(rx.icon("menu", size=30)),
                    rx.menu.content(
                        navbar_icons_menu_item("Work", "briefcase-business", "/work"),
                        navbar_icons_menu_item("Education", "school", "/education"),
                        navbar_icons_menu_item("Skills", "chart-bar", "/skills"),
                        navbar_icons_menu_item("Projects", "folder-git-2", "/projects"),
                        navbar_icons_menu_item("Contact-Me", "contact-round", "/contact"),
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