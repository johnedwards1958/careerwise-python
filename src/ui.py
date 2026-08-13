import flet as ft

from archetypes import create_influence_archetypes_assessment_ui
from environment import create_environment_assessment_ui
from learning import create_learning_preference_assessment_ui
from path import create_career_path_assessment_ui
from priorities import create_priorities_assessment_ui
from relationships import create_relationships_assessment_ui
from skills_ui import create_skills_assessment_ui
from teams import create_teams_assessment_ui
from transferrable import create_transferrable_assessment_ui

def main(page: ft.Page):
    # Basic page setup
    page.title = "CareerWise"
    page.window.width = 1280
    page.window.height = 720
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE
    page.theme = ft.Theme(color_scheme=ft.ColorScheme(on_surface=ft.Colors.BLACK))

    # Assessment navigation items
    assessment_items = [
        ("Job Search Skills", ft.Icons.PSYCHOLOGY, create_skills_assessment_ui),
        ("Career Path", ft.Icons.TIMELINE, create_career_path_assessment_ui),
        ("Team Roles", ft.Icons.GROUPS, create_teams_assessment_ui),
        ("Career Priorities", ft.Icons.PRIORITY_HIGH, create_priorities_assessment_ui),
        ("Influence Archetypes", ft.Icons.PERSON_OUTLINE, create_influence_archetypes_assessment_ui),
        ("Learning Preference", ft.Icons.SCHOOL, create_learning_preference_assessment_ui),
        ("Past Relationships Review", ft.Icons.WORK_HISTORY, create_relationships_assessment_ui),
        ("Preferred Work Environment", ft.Icons.BUSINESS, create_environment_assessment_ui),
        ("Transferrable Skills", ft.Icons.BOOK, create_transferrable_assessment_ui),
    ]

    assessment_factories = {title: factory for title, _, factory in assessment_items}

    # Function to load different assessments
    def load_assessment(assessment_name):
        """Load the selected assessment into the main content area."""
        factory = assessment_factories.get(assessment_name)

        if factory:
            main_content.content = factory(page)
        else:
            main_content.content = ft.Text("This assessment is coming soon.")
        main_content.update()
    
    # Build left navigation
    def rebuild_left_nav():
        controls = [ft.Text("Assessments", 
        weight=ft.FontWeight.BOLD, size=16)]
        
        def on_hover(e):
            if e.data == "true":
                e.control.bgcolor = ft.Colors.BLACK12
            else:
                e.control.bgcolor = None
            e.control.update()
        
        # These buttons will be added to the list, 'controls'
        for title, material_icon, _ in assessment_items:
            def create_click_handler(assessment_title):
                return lambda e: load_assessment(assessment_title)
            
            btn = ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(material_icon, size=22, color=ft.Colors.BLACK),
                        ft.Text(title, size=16, color=ft.Colors.BLACK)
                    ],
                    spacing=8,
                ),
                padding=ft.Padding.symmetric(vertical=8, horizontal=12),
                border_radius=8,
                on_hover=on_hover,
                on_click=create_click_handler(title),
                ink=True,
            )
            controls.append(btn)

        left_nav.controls = controls
        left_nav.update()

    left_nav = ft.Column(spacing=5)

    # Main content area
    main_content = ft.Container(
        expand=True,
        bgcolor=ft.Colors.WHITE,
        content=ft.Text(
            "CareerWise home",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK,
        ),
        alignment=ft.Alignment(0, -1),
    )

    # Footer/Status bar (empty)
    footer_bar = ft.Row(
        controls=[ft.Text("", size=16, color=ft.Colors.BLACK)],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )
    footer_container = ft.Container(
        content=footer_bar,
        bgcolor="#ECEEF4",
        border_radius=ft.BorderRadius(8, 8, 8, 8),
        padding=ft.Padding.symmetric(horizontal=12, vertical=4),
    )

    # Menubar
    def handle_menu_item_click(e):
        pass  # No functionality yet

    menubar = ft.MenuBar(
        expand=True,
        style=ft.MenuStyle(
            alignment=ft.Alignment(-1, -1), 
            bgcolor="#ECEEF4", 
            elevation=0
        ),
        controls=[
            ft.SubmenuButton(
                content=ft.Text("File"),
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("About"),
                        leading=ft.Icon(ft.Icons.INFO),
                        on_click=handle_menu_item_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Save"),
                        leading=ft.Icon(ft.Icons.SAVE),
                        on_click=handle_menu_item_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Quit"),
                        leading=ft.Icon(ft.Icons.CLOSE),
                        on_click=handle_menu_item_click,
                    ),
                ],
            ),
            ft.SubmenuButton(
                content=ft.Text("View"),
                controls=[
                    ft.SubmenuButton(
                        content=ft.Text("Zoom"),
                        controls=[
                            ft.MenuItemButton(
                                content=ft.Text("Magnify"),
                                leading=ft.Icon(ft.Icons.ZOOM_IN),
                                on_click=handle_menu_item_click,
                            ),
                            ft.MenuItemButton(
                                content=ft.Text("Minify"),
                                leading=ft.Icon(ft.Icons.ZOOM_OUT),
                                on_click=handle_menu_item_click,
                            ),
                        ],
                    ),
                ],
            ),
            ft.SubmenuButton(
                content=ft.Text("Search"),
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Search Item"),
                        on_click=handle_menu_item_click
                    ),
                ],
            ),
            ft.SubmenuButton(
                content=ft.Text("Actions"),
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("Action 1"),
                        leading=ft.Icon(ft.Icons.CREATE),
                        on_click=handle_menu_item_click,
                    ),
                    ft.MenuItemButton(
                        content=ft.Text("Action 2"),
                        leading=ft.Icon(ft.Icons.DELETE),
                        on_click=handle_menu_item_click,
                    ),
                ],
            ),
            ft.SubmenuButton(
                content=ft.Text("Settings"),
                controls=[
                    ft.MenuItemButton(
                        content=ft.Text("App Settings"),
                        leading=ft.Icon(ft.Icons.SETTINGS),
                        on_click=handle_menu_item_click
                    )
                ],
            ),
        ],
    )
    
    page.add(ft.Row([menubar]))

    # Layout
    page.add(
        ft.Column(
            [
                ft.Divider(height=1, color=ft.Colors.BLACK26),
                ft.Row(
                    [
                        ft.Container(width=275, content=left_nav, 
                        bgcolor=ft.Colors.WHITE10),
                        ft.VerticalDivider(width=1, color=ft.Colors.BLACK26),
                        main_content,
                    ],
                    expand=True,
                ),
                ft.Divider(height=1, color=ft.Colors.BLACK26),
                footer_container,
            ],
            expand=True,
        )
    )

    # Initialize navigation
    rebuild_left_nav()


if __name__ == "__main__":
    ft.app(target=main)
