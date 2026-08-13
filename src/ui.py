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

SMALL_SCREEN_BREAKPOINT = 900
RESIZE_FOR_SMALL_SCREENS_KEY = "careerwise.resize_for_small_screens"


def should_hide_assessments_sidebar(
    resize_for_small_screens: bool,
    page_width: float | None,
) -> bool:
    """Return whether the Assessments sidebar should be hidden."""
    return bool(
        resize_for_small_screens
        and page_width is not None
        and page_width < SMALL_SCREEN_BREAKPOINT
    )


def set_assessments_sidebar_visibility(
    sidebar,
    divider,
    resize_for_small_screens: bool,
    page_width: float | None,
    temporary_show_button=None,
) -> bool:
    """Update responsive navigation controls and report whether any changed."""
    visible = not should_hide_assessments_sidebar(
        resize_for_small_screens,
        page_width,
    )
    changed = sidebar.visible != visible or divider.visible != visible
    sidebar.visible = visible
    divider.visible = visible

    if temporary_show_button is not None:
        button_visible = not visible
        changed = changed or temporary_show_button.visible != button_visible
        temporary_show_button.visible = button_visible

    return changed


async def main(page: ft.Page):
    # Basic page setup
    page.title = "CareerWise"
    page.window.width = 1280
    page.window.height = 720
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = ft.Colors.WHITE
    page.theme = ft.Theme(color_scheme=ft.ColorScheme(on_surface=ft.Colors.BLACK))

    preferences = ft.SharedPreferences()
    try:
        stored_resize_setting = await preferences.get(
            RESIZE_FOR_SMALL_SCREENS_KEY
        )
    except (RuntimeError, TimeoutError):
        stored_resize_setting = None
    resize_for_small_screens = stored_resize_setting is True
    last_page_width = page.width

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

    temporary_drawer_open = False

    def handle_assessments_drawer_dismiss(e):
        nonlocal temporary_drawer_open
        temporary_drawer_open = False

    async def close_assessments_drawer(e=None):
        nonlocal temporary_drawer_open
        if temporary_drawer_open:
            temporary_drawer_open = False
            await page.close_drawer()

    async def handle_assessments_drawer_change(e):
        selected_index = e.control.selected_index
        if 0 <= selected_index < len(assessment_items):
            load_assessment(assessment_items[selected_index][0])

        e.control.selected_index = -1
        e.control.update()
        await close_assessments_drawer()

    assessments_drawer = ft.NavigationDrawer(
        width=300,
        selected_index=-1,
        controls=[
            ft.Container(
                content=ft.Row(
                    [
                        ft.Text(
                            "Assessments",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            expand=True,
                        ),
                        ft.IconButton(
                            icon=ft.Icons.CLOSE,
                            tooltip="Close Assessments",
                            on_click=close_assessments_drawer,
                        ),
                    ]
                ),
                padding=ft.Padding.only(left=24, right=8, top=12, bottom=8),
            ),
            *[
                ft.NavigationDrawerDestination(
                    label=title,
                    icon=material_icon,
                )
                for title, material_icon, _ in assessment_items
            ],
        ],
        on_change=handle_assessments_drawer_change,
        on_dismiss=handle_assessments_drawer_dismiss,
    )
    page.drawer = assessments_drawer

    async def open_assessments_drawer(e):
        nonlocal temporary_drawer_open
        temporary_drawer_open = True
        await page.show_drawer()

    temporary_show_assessments_button = ft.IconButton(
        icon=ft.Icons.MENU,
        tooltip="Show Assessments sidebar",
        visible=False,
        on_click=open_assessments_drawer,
    )
    
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
    left_nav_container = ft.Container(
        width=275,
        content=left_nav,
        bgcolor=ft.Colors.WHITE10,
    )
    left_nav_divider = ft.VerticalDivider(width=1, color=ft.Colors.BLACK26)

    def apply_responsive_layout(page_width):
        nonlocal last_page_width
        if page_width is not None:
            last_page_width = page_width

        visibility_changed = set_assessments_sidebar_visibility(
            left_nav_container,
            left_nav_divider,
            resize_for_small_screens,
            last_page_width,
            temporary_show_assessments_button,
        )
        if visibility_changed:
            page.update()
        return not left_nav_container.visible

    async def handle_page_resize(e):
        sidebar_hidden = apply_responsive_layout(e.width)
        if not sidebar_hidden:
            await close_assessments_drawer()

    page.on_resize = handle_page_resize

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

    async def handle_resize_setting_change(e):
        nonlocal resize_for_small_screens
        resize_for_small_screens = e.control.value is True
        sidebar_hidden = apply_responsive_layout(page.width)
        if not sidebar_hidden:
            await close_assessments_drawer()
        try:
            await preferences.set(
                RESIZE_FOR_SMALL_SCREENS_KEY,
                resize_for_small_screens,
            )
        except (RuntimeError, TimeoutError):
            pass

    resize_for_small_screens_switch = ft.Switch(
        label="Resize for small screens",
        value=resize_for_small_screens,
        on_change=handle_resize_setting_change,
    )

    app_settings_dialog = ft.AlertDialog(
        modal=True,
        title=ft.Text("App Settings"),
        content=ft.Column(
            [
                resize_for_small_screens_switch,
                ft.Text(
                    "Hide the Assessments sidebar when the window is narrower "
                    f"than {SMALL_SCREEN_BREAKPOINT} pixels. Use the menu button "
                    "to open it temporarily.",
                    size=12,
                    color=ft.Colors.BLACK54,
                ),
            ],
            tight=True,
            spacing=4,
        ),
        actions=[
            ft.TextButton("Close", on_click=lambda e: page.pop_dialog()),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def open_app_settings(e):
        resize_for_small_screens_switch.value = resize_for_small_screens
        page.show_dialog(app_settings_dialog)

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
                        on_click=open_app_settings,
                    )
                ],
            ),
        ],
    )
    
    page.add(
        ft.Row(
            [temporary_show_assessments_button, menubar],
            spacing=0,
        )
    )

    # Layout
    page.add(
        ft.Column(
            [
                ft.Divider(height=1, color=ft.Colors.BLACK26),
                ft.Row(
                    [
                        left_nav_container,
                        left_nav_divider,
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
    apply_responsive_layout(page.width)


if __name__ == "__main__":
    ft.app(target=main)
