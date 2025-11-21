import reflex as rx

config = rx.Config(
    app_name="app",
    db_url="sqlite:///reflex.db",
    env=rx.Env.DEV,
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
    watermark=False,
    tailwind_config={
        'theme': {
            'extend': {},
        },
        'plugins': ['@tailwindcss/typography'],
    },
    suppress_build_web_path_warning=True,
)