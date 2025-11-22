import reflex as rx

config = rx.Config(
    app_name="app",
    db_url="sqlite:///reflex.db",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    # show_built_with_reflex=False
)