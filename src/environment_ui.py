"""
Preferred Work Environment Assessment - UI Layer
Flet UI construction and page wiring.
"""

import flet as ft

from environment_logic import EnvironmentAssessment


def create_environment_assessment_ui(page: ft.Page):
    """
    Create the Preferred Work Environment Assessment UI.
    
    Args:
        page: The Flet page object
        
    Returns:
        A container with the complete assessment UI
    """
    # Initialize the assessment logic
    assessment = EnvironmentAssessment()
    
    # Create the main container first
    container = ft.Container(
        content=ft.Text("Loading..."),
        padding=20,
        expand=True
    )
    
    # Reference to UI elements that need updating
    complete_button = None
    progress_text = None
    
    def update_progress():
        """Update the progress display and button state."""
        answered, total, percentage = assessment.get_completion_status()
        
        if progress_text:
            progress_text.value = f"Answered: {answered}/{total} factors ({percentage:.0f}%)"
            progress_text.update()
        
        if complete_button:
            is_complete = assessment.is_complete()
            complete_button.disabled = not is_complete
            complete_button.bgcolor = ft.Colors.BLUE_700 if is_complete else ft.Colors.GREY_300
            complete_button.update()
    
    def on_option_selected(factor_index, option):
        """Handle when user selects an option."""
        assessment.set_response(factor_index, option)
        update_progress()
    
    def create_factor_row(factor_index):
        """Create a row for a single factor with A, B, C options."""
        factor = EnvironmentAssessment.FACTORS[factor_index]
        current_value = assessment.get_response(factor_index)
        
        def on_radio_change(e):
            on_option_selected(factor_index, e.control.value)
        
        # Create radio buttons for A, B, C options
        radio_group = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(
                    value="A",
                    label=f"A: {factor['options']['A']}",
                    label_style=ft.TextStyle(size=14, weight=ft.FontWeight.W_500)
                ),
                ft.Radio(
                    value="B",
                    label=f"B: {factor['options']['B']}",
                    label_style=ft.TextStyle(size=14, weight=ft.FontWeight.W_500)
                ),
                ft.Radio(
                    value="C",
                    label=f"C: {factor['options']['C']}",
                    label_style=ft.TextStyle(size=14, weight=ft.FontWeight.W_500)
                ),
            ], spacing=10),
            value=current_value if current_value else None,
            on_change=on_radio_change
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Container(
                        content=ft.Text(
                            str(factor_index + 1),
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE
                        ),
                        width=35,
                        height=35,
                        bgcolor=ft.Colors.BLUE_700,
                        border_radius=17,
                        alignment=ft.Alignment.CENTER
                    ),
                    ft.Text(
                        factor["name"],
                        size=16,
                        color=ft.Colors.BLACK,
                        weight=ft.FontWeight.BOLD
                    ),
                ], spacing=12),
                ft.Container(
                    content=radio_group,
                    padding=ft.Padding.only(left=47, top=5)
                ),
            ], spacing=10),
            padding=15,
            border=ft.Border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_300))
        )
    
    def create_assessment_view():
        """Create the main assessment view with all factors."""
        # Header
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.BUSINESS, size=28, color=ft.Colors.BLUE_700),
                    ft.Text(
                        "Preferred Work Environment Assessment",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                ], spacing=10),
                ft.Text(
                    "Select the option that best describes your preferred work environment",
                    size=14,
                    color=ft.Colors.GREY_700,
                    italic=True
                ),
            ], spacing=5),
            bgcolor=ft.Colors.BLUE_50,
            padding=20,
            border_radius=10,
            margin=ft.Margin.only(bottom=15)
        )
        
        # Instructions card
        instructions = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.INFO_OUTLINE, size=24, color=ft.Colors.BLUE_700),
                    ft.Text(
                        "For each factor, choose Option A, Option B, or Option C",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                ], spacing=10),
                ft.Text(
                    "There are no right or wrong answers. Choose based on what you truly prefer, not what you think you should prefer.",
                    size=13,
                    color=ft.Colors.GREY_700
                ),
            ], spacing=8),
            bgcolor=ft.Colors.WHITE,
            padding=15,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            margin=ft.Margin.only(bottom=20)
        )
        
        # All factor rows
        factor_rows = []
        for i in range(len(EnvironmentAssessment.FACTORS)):
            factor_rows.append(create_factor_row(i))
        
        factors_container = ft.Container(
            content=ft.Column(factor_rows, spacing=0),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            margin=ft.Margin.only(bottom=20)
        )
        
        # Progress display
        answered, total, percentage = assessment.get_completion_status()
        
        nonlocal progress_text
        progress_text = ft.Text(
            f"Answered: {answered}/{total} factors ({percentage:.0f}%)",
            size=14,
            color=ft.Colors.GREY_700,
            weight=ft.FontWeight.BOLD
        )
        
        progress_container = ft.Container(
            content=progress_text,
            padding=10,
            margin=ft.Margin.only(bottom=20)
        )
        
        # View Results button
        def on_view_results(e):
            if assessment.is_complete():
                container.content = create_results_page()
                container.update()
        
        nonlocal complete_button
        complete_button = ft.Button(
            "View Results",
            icon=ft.Icons.EMOJI_EVENTS,
            on_click=on_view_results,
            disabled=not assessment.is_complete(),
            bgcolor=ft.Colors.BLUE_700 if assessment.is_complete() else ft.Colors.GREY_300,
            color=ft.Colors.WHITE,
            height=45,
            style=ft.ButtonStyle(
                text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
            ),
        )
        
        button_row = ft.Row([
            complete_button,
        ], alignment=ft.MainAxisAlignment.CENTER)
        
        return ft.Column([
            header,
            instructions,
            factors_container,
            progress_container,
            button_row,
        ], scroll=ft.ScrollMode.AUTO, expand=True)
    
    def create_results_page():
        """Create the results page showing profile and interpretation."""
        interpretation = assessment.get_interpretation()
        counts = assessment.get_pattern_counts()
        
        # Title
        title_container = ft.Container(
            content=ft.Text(
                "Preferred Work Environment Results",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLACK
            ),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=10,
            margin=ft.Margin.only(bottom=20)
        )
        
        # Pattern breakdown visualization
        pattern_cards = []
        
        # Map options to colors
        option_colors = {
            'A': ft.Colors.BLUE_700,
            'B': ft.Colors.GREEN_700,
            'C': ft.Colors.PURPLE_700
        }
        
        option_titles = {
            'A': 'Option A — Structured / Team-centred',
            'B': 'Option B — Balanced / Adaptive',
            'C': 'Option C — Autonomous / Flexible'
        }

        dominant_options = set(interpretation['dominant_options'])
        has_tied_result = len(dominant_options) > 1
        
        for option in ['A', 'B', 'C']:
            count = counts[option]
            percentage = (count / len(EnvironmentAssessment.FACTORS)) * 100
            is_dominant = option in dominant_options
            
            card = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Text(
                                option,
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE
                            ),
                            width=50,
                            height=50,
                            bgcolor=option_colors[option],
                            border_radius=25,
                            alignment=ft.Alignment.CENTER
                        ),
                        ft.Column([
                            ft.Row([
                                ft.Text(
                                    option_titles[option],
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLACK
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        "JOINT HIGHEST" if has_tied_result else "DOMINANT",
                                        size=11,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.WHITE
                                    ),
                                    bgcolor=option_colors[option],
                                    padding=ft.Padding.symmetric(horizontal=8, vertical=3),
                                    border_radius=10
                                ) if is_dominant else ft.Container(),
                            ], spacing=10),
                            ft.Text(
                                f"{count} selections ({percentage:.0f}%)",
                                size=14,
                                color=ft.Colors.GREY_700
                            ),
                        ], spacing=3, expand=True),
                    ], spacing=15),
                    ft.Container(
                        content=ft.ProgressBar(
                            value=percentage / 100,
                            color=option_colors[option],
                            bgcolor=ft.Colors.GREY_200,
                            height=10,
                        ),
                        margin=ft.Margin.only(top=10)
                    ),
                ], spacing=5),
                padding=15,
                border=ft.Border.all(2 if is_dominant else 1, option_colors[option] if is_dominant else ft.Colors.GREY_300),
                border_radius=10,
                bgcolor=ft.Colors.with_opacity(0.1, option_colors[option]) if is_dominant else ft.Colors.WHITE,
                margin=ft.Margin.only(bottom=10)
            )
            pattern_cards.append(card)
        
        pattern_container = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Your Response Pattern",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK
                ),
                ft.Text(
                    "Distribution of your selections across the three option types",
                    size=13,
                    color=ft.Colors.GREY_700,
                    italic=True
                ),
                ft.Container(height=10),
                *pattern_cards,
            ]),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            margin=ft.Margin.only(bottom=20)
        )
        
        # Profile interpretation card
        profile_color_map = {
            'structured': ft.Colors.BLUE_700,
            'balanced': ft.Colors.GREEN_700,
            'autonomous': ft.Colors.PURPLE_700,
            'mixed': ft.Colors.AMBER_800,
        }
        
        profile_icon_map = {
            'structured': ft.Icons.ACCOUNT_TREE,
            'balanced': ft.Icons.BALANCE,
            'autonomous': ft.Icons.EXPLORE,
            'mixed': ft.Icons.TUNE,
        }
        
        profile_color = profile_color_map[interpretation['profile_key']]
        profile_icon = profile_icon_map[interpretation['profile_key']]
        
        profile_container = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(profile_icon, size=32, color=profile_color),
                    ft.Text(
                        "Your Work Environment Profile",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                ], spacing=10),
                ft.Divider(height=1, color=ft.Colors.GREY_300),
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            interpretation['title'],
                            size=22,
                            weight=ft.FontWeight.BOLD,
                            color=profile_color
                        ),
                        ft.Text(
                            interpretation['typical_pattern'],
                            size=13,
                            color=ft.Colors.GREY_600,
                            italic=True
                        ),
                        ft.Container(height=10),
                        ft.Text(
                            interpretation['description'],
                            size=15,
                            color=ft.Colors.BLACK87,
                            weight=ft.FontWeight.W_500
                        ),
                    ], spacing=5),
                    padding=20,
                    bgcolor=ft.Colors.with_opacity(0.1, profile_color),
                    border_radius=10,
                    border=ft.Border.all(2, profile_color),
                    margin=ft.Margin.only(top=15)
                ),
            ], spacing=10),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            margin=ft.Margin.only(bottom=20)
        )
        
        # Reflection prompts
        reflection_items = []
        for i, prompt in enumerate(EnvironmentAssessment.REFLECTION_PROMPTS):
            reflection_items.append(
                ft.Row([
                    ft.Container(
                        content=ft.Text(
                            str(i + 1),
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE
                        ),
                        width=28,
                        height=28,
                        bgcolor=ft.Colors.AMBER_700,
                        border_radius=14,
                        alignment=ft.Alignment.CENTER
                    ),
                    ft.Text(
                        prompt,
                        size=14,
                        color=ft.Colors.BLACK87,
                        expand=True
                    ),
                ], spacing=12)
            )
        
        reflection_container = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.LIGHTBULB_OUTLINE, size=28, color=ft.Colors.AMBER_700),
                    ft.Text(
                        "Reflection Questions",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                ], spacing=10),
                ft.Text(
                    "Consider these questions to help you apply your results",
                    size=13,
                    color=ft.Colors.GREY_700,
                    italic=True
                ),
                ft.Divider(height=1, color=ft.Colors.GREY_300),
                ft.Column(reflection_items, spacing=15),
            ], spacing=10),
            bgcolor=ft.Colors.AMBER_50,
            padding=20,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.AMBER_200),
            margin=ft.Margin.only(bottom=20)
        )
        
        # Reset and return buttons
        def on_reset_clicked(e):
            """Handle reset button click."""
            assessment.reset()
            container.content = build_initial_content()
            container.update()
        
        def on_return_to_assessment(e):
            """Return to assessment view to review answers."""
            container.content = create_assessment_view()
            container.update()
        
        buttons_row = ft.Row([
            ft.Button(
                "Review Answers",
                icon=ft.Icons.EDIT,
                on_click=on_return_to_assessment,
                bgcolor=ft.Colors.BLUE_700,
                color=ft.Colors.WHITE,
            ),
            ft.Button(
                "Reset Assessment",
                icon=ft.Icons.REFRESH,
                on_click=on_reset_clicked,
                bgcolor=ft.Colors.ORANGE_700,
                color=ft.Colors.WHITE,
            ),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=15)
        
        # CareerWise Insight section
        insight_container = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.INSIGHTS, size=28, color=ft.Colors.DEEP_PURPLE_700),
                    ft.Text(
                        "CareerWise Insight",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.DEEP_PURPLE_700
                    ),
                ], spacing=10),
                ft.Divider(height=1, color=ft.Colors.DEEP_PURPLE_200),
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            "Your Workplace Culture Compass",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            "Your work environment preferences reveal the conditions where you naturally thrive and perform at your best. "
                            "Understanding these needs helps you evaluate opportunities for cultural fit and long-term satisfaction.",
                            size=14,
                            color=ft.Colors.GREY_800,
                        ),
                        ft.Container(height=12),
                        ft.Row([
                            ft.Icon(ft.Icons.TIPS_AND_UPDATES, size=20, color=ft.Colors.DEEP_PURPLE_600),
                            ft.Text(
                                "Environment Selection Strategy:",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.DEEP_PURPLE_700
                            ),
                        ], spacing=8),
                        ft.Text(
                            "Use your environment preferences as key criteria when evaluating job opportunities and company cultures. "
                            "Ask specific questions during interviews to assess cultural fit. "
                            "Remember: skills can be developed, but cultural misalignment often leads to career dissatisfaction regardless of other factors.",
                            size=14,
                            color=ft.Colors.GREY_800,
                            italic=True
                        ),
                    ]),
                    padding=ft.Padding.all(15),
                    bgcolor=ft.Colors.DEEP_PURPLE_50,
                    border_radius=8,
                    border=ft.Border.all(1, ft.Colors.DEEP_PURPLE_200),
                ),
            ], spacing=10),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            margin=ft.Margin.only(bottom=20)
        )
        
        return ft.Column([
            title_container,
            pattern_container,
            profile_container,
            reflection_container,
            insight_container,
            buttons_row,
        ], scroll=ft.ScrollMode.AUTO, expand=True)
    
    def build_initial_content():
        """Build the initial welcome screen or assessment view."""
        # Check if any responses exist
        if len(assessment.responses) > 0:
            return create_assessment_view()
        
        # Show welcome screen
        def on_start(e):
            container.content = create_assessment_view()
            container.update()
        
        welcome_screen = ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.BUSINESS, size=48, color=ft.Colors.BLUE_700),
                    ft.Text(
                        "Preferred Work Environment Assessment",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK,
                        text_align=ft.TextAlign.CENTER
                    ),
                    ft.Text(
                        "Identify the type of work environment in which you perform best",
                        size=16,
                        color=ft.Colors.GREY_700,
                        text_align=ft.TextAlign.CENTER
                    ),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                padding=30,
                bgcolor=ft.Colors.BLUE_50,
                border_radius=10,
                margin=ft.Margin.only(bottom=20),
                alignment=ft.Alignment.CENTER
            ),
            
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "About This Assessment",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                    ft.Container(height=10),
                    ft.Text(
                        "This assessment explores 12 key factors that shape your ideal work environment, including:",
                        size=14,
                        color=ft.Colors.GREY_800
                    ),
                    ft.Container(height=5),
                    ft.Row([
                        ft.Icon(ft.Icons.CHECK_CIRCLE, size=20, color=ft.Colors.BLUE_700),
                        ft.Text(
                            "Work pace, structure, and collaboration style",
                            size=14,
                            color=ft.Colors.GREY_800,
                            expand=True
                        ),
                    ], spacing=10),
                    ft.Row([
                        ft.Icon(ft.Icons.CHECK_CIRCLE, size=20, color=ft.Colors.BLUE_700),
                        ft.Text(
                            "Supervision preferences and decision-making approach",
                            size=14,
                            color=ft.Colors.GREY_800,
                            expand=True
                        ),
                    ], spacing=10),
                    ft.Row([
                        ft.Icon(ft.Icons.CHECK_CIRCLE, size=20, color=ft.Colors.BLUE_700),
                        ft.Text(
                            "Work setting, noise level, and schedule flexibility",
                            size=14,
                            color=ft.Colors.GREY_800,
                            expand=True
                        ),
                    ], spacing=10),
                    ft.Row([
                        ft.Icon(ft.Icons.CHECK_CIRCLE, size=20, color=ft.Colors.BLUE_700),
                        ft.Text(
                            "Innovation level, goal orientation, and risk tolerance",
                            size=14,
                            color=ft.Colors.GREY_800,
                            expand=True
                        ),
                    ], spacing=10),
                ], spacing=8),
                padding=20,
                bgcolor=ft.Colors.WHITE,
                border_radius=10,
                border=ft.Border.all(1, ft.Colors.GREY_300),
                margin=ft.Margin.only(bottom=20)
            ),
            
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "How It Works",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                    ft.Container(height=5),
                    ft.Text(
                        "For each of the 12 factors, choose from three options (A, B, or C) that best describes your preference. There are no right or wrong answers — this is about understanding what works best for you.",
                        size=14,
                        color=ft.Colors.GREY_800
                    ),
                ], spacing=5),
                padding=15,
                bgcolor=ft.Colors.BLUE_50,
                border_radius=10,
                border=ft.Border.all(1, ft.Colors.BLUE_200),
                margin=ft.Margin.only(bottom=20)
            ),
            
            ft.Row([
                ft.Button(
                    "Begin Assessment",
                    icon=ft.Icons.PLAY_ARROW,
                    on_click=on_start,
                    bgcolor=ft.Colors.BLUE_700,
                    color=ft.Colors.WHITE,
                    height=50,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
                    ),
                ),
            ], alignment=ft.MainAxisAlignment.CENTER),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, alignment=ft.MainAxisAlignment.START, scroll=ft.ScrollMode.AUTO, expand=True)
        
        return welcome_screen
    
    # Build and set initial content
    container.content = build_initial_content()
    
    return container


def create_environment_page(page: ft.Page):
    """Entry point for creating the environment assessment page."""
    return create_environment_assessment_ui(page)

def _run_standalone(page: ft.Page):
    page.title = "CareerWise - Preferred Work Environment"
    page.add(create_environment_assessment_ui(page))
