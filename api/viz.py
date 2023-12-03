from IPython.core.display import HTML

def add_tailwind():
    return HTML(f"""
            <link
                href="https://fonts.googleapis.com/css2?family=Figtree:wght@300;400;500;600;700;800&family=Roboto+Mono&display=swap"
                rel="stylesheet"
                async
            />
            <script src='https://cdn.tailwindcss.com'></script>
            <style>
                * {{
                    font-family: 'Figtree', serif;
                }}
            </style>
        """)