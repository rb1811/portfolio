import reflex as rx

config = rx.Config(
    # This is correct: 'app' directory, 'app.py' file -> 'app.app' module
    app_name="app", 
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
    base_path="/portfolio/", 
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ]
)