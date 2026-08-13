"""
Path Assessment - UI Layer
Flet UI construction and page wiring.
"""

import flet as ft

from path_logic import CareerPathAssessment


def create_career_path_assessment_ui(page: ft.Page):
    """
    Create the Career Path (RIASEC) Assessment UI.
    
    Args:
        page: The Flet page object
        
    Returns:
        A container with the complete assessment UI
    """
    # Initialize the assessment logic
    assessment = CareerPathAssessment()
    
    # References to UI elements
    score_displays = {}
    progress_indicator = [None]  # Reference to progress indicator
    scroll_ref = ft.Ref[ft.Column]()  # Reference to scrollable column for auto-scroll
    
    # Track current page for navigation
    current_page_index = [0]
    show_welcome = [True]  # Flag to control welcome page display
    show_results = [False]  # Flag to control when to show results
    
    # Category colors for visual distinction
    CATEGORY_COLORS = {
        "R": ft.Colors.BLUE_700,
        "I": ft.Colors.PURPLE_700,
        "A": ft.Colors.PINK_700,
        "S": ft.Colors.GREEN_700,
        "E": ft.Colors.ORANGE_700,
        "C": ft.Colors.BROWN_700
    }
    
    def update_progress_indicator():
        """Update the progress indicator chip."""
        if progress_indicator[0] is not None:
            answered, total = assessment.get_completion_counts()
            percentage = assessment.get_completion_percentage()
            progress_indicator[0].label = ft.Text(f"{answered}/{total} answered • {percentage:.0f}%")
            try:
                progress_indicator[0].update()
            except Exception:
                pass
    
    def show_skip_warning():
        """Show dialog warning about skipped questions."""
        def close_dialog(e):
            dialog.open = False
            page.update()
            # Navigate to first page with unanswered questions
            first_unanswered_page = assessment.get_first_unanswered_page()
            if first_unanswered_page is not None:
                current_page_index[0] = first_unanswered_page
                container.content = build_assessment_content()
                container.update()
        
        unanswered_count = len(assessment.get_unanswered_questions())
        
        dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Incomplete Assessment"),
            content=ft.Text(
                f"You have skipped {unanswered_count} question{'s' if unanswered_count != 1 else ''}. "
                "Please answer all questions to complete the assessment.",
                size=14
            ),
            actions=[
                ft.TextButton("OK", on_click=close_dialog),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        
        page.dialog = dialog
        dialog.open = True
        page.update()
    
    def update_scores():
        """Update all score displays and progress indicator."""
        # Update score displays if they exist
        all_scores = assessment.get_all_scores()
        for category, (score, max_possible, answered, total, percentage) in all_scores.items():
            if category in score_displays and score_displays[category] is not None:
                try:
                    score_displays[category].value = f"{percentage:.1f}%"
                    score_displays[category].update()
                except Exception:
                    pass
        
        # Update progress indicator
        update_progress_indicator()
        
        # If all questions are answered, refresh UI to show the Get Results button
        if assessment.is_complete():
            container.content = build_assessment_content()
            container.update()
            # Auto-scroll to bottom to show the View Results button
            if scroll_ref.current:
                try:
                    scroll_ref.current.scroll_to(offset=-1, duration=500)
                except Exception:
                    pass
    
    def on_answer_changed(category, statement_index, score):
        """Handle when a user selects an answer."""
        try:
            assessment.set_response(category, statement_index, score)
            update_scores()
        except Exception as e:
            print(f"Error updating answer: {e}")
            pass
    
    def on_reset_clicked(e):
        """Handle reset button click."""
        assessment.reset()
        show_welcome[0] = True
        show_results[0] = False
        container.content = build_assessment_content()
        container.update()
    
    def create_statement_row(category, statement_index, statement_text):
        """Create a row for a single statement with rating buttons."""
        # Use get_raw_response to display the original selection (before reverse scoring)
        current_value = assessment.get_raw_response(category, statement_index)
        
        def on_radio_change(e):
            try:
                if e.control and e.control.value:
                    on_answer_changed(category, statement_index, int(e.control.value))
            except Exception as ex:
                print(f"Error in radio change handler: {ex}")
                pass
        
        # Create radio buttons for 1-5 rating with tooltips
        radio_group = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="5", label="5", label_style=ft.TextStyle(size=14)),
                ft.Radio(value="4", label="4", label_style=ft.TextStyle(size=14)),
                ft.Radio(value="3", label="3", label_style=ft.TextStyle(size=14), tooltip="Neutral"),
                ft.Radio(value="2", label="2", label_style=ft.TextStyle(size=14)),
                ft.Radio(value="1", label="1", label_style=ft.TextStyle(size=14)),
            ], spacing=15),
            value=str(current_value) if current_value else None,
            on_change=on_radio_change
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(
                        statement_text,
                        size=14,
                        color=ft.Colors.BLACK87,
                        weight=ft.FontWeight.W_400
                    ),
                    ft.Container(expand=True),
                    ft.Container(
                        content=ft.Text(
                            category,
                            size=12,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.WHITE
                        ),
                        bgcolor=CATEGORY_COLORS[category],
                        padding=ft.Padding.symmetric(horizontal=8, vertical=2),
                        border_radius=4
                    )
                ], spacing=10),
                ft.Row([
                    ft.Container(
                        content=ft.Text("Strongly Agree", size=12, color=ft.Colors.GREY_700),
                        width=120,
                        tooltip="5 = High interest in this activity"
                    ),
                    radio_group,
                    ft.Container(
                        content=ft.Text("Strongly Disagree", size=12, color=ft.Colors.GREY_700),
                        tooltip="1 = Low interest in this activity"
                    ),
                ], alignment=ft.MainAxisAlignment.START),
            ], spacing=8),
            padding=ft.Padding.symmetric(horizontal=10, vertical=12),
            border=ft.Border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_300))
        )
    
    def create_all_statements_content():
        """Create content with all statements in one scrollable page."""
        all_statements = []
        
        # Get all statements from all categories
        for category in ["R", "I", "A", "S", "E", "C"]:
            statements = assessment.STATEMENTS[category]
            for i, statement_text in enumerate(statements):
                all_statements.append((category, i, statement_text))
        
        # Create statement rows
        statement_rows = []
        for category, statement_index, statement_text in all_statements:
            statement_rows.append(create_statement_row(category, statement_index, statement_text))
        
        # Add Get Results button if assessment is complete
        if assessment.is_complete():
            def on_get_results(e):
                show_results[0] = True
                container.content = build_assessment_content()
                container.update()
            
            get_results_button = ft.Container(
                content=ft.Row([
                    ft.Button(
                        "View Results",
                        icon=ft.Icons.INSIGHTS,
                        on_click=on_get_results,
                        bgcolor=ft.Colors.BLUE_700,
                        color=ft.Colors.WHITE,
                        height=50,
                        style=ft.ButtonStyle(
                            text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
                        ),
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER),
                padding=ft.Padding.only(top=30, bottom=20),
            )
            statement_rows.append(get_results_button)
        
        return ft.Container(
            content=ft.Column(statement_rows, spacing=0),
            border=ft.Border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            bgcolor=ft.Colors.WHITE,
            padding=10
        )
    
    def create_score_display():
        """Create the scoring summary display."""
        score_rows = []
        
        for category in ["R", "I", "A", "S", "E", "C"]:
            cat_info = assessment.CATEGORIES[category]
            score, max_possible, answered, total, percentage = assessment.calculate_category_score(category)
            
            score_text = ft.Text(
                f"{percentage:.1f}%",
                size=18,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.WHITE
            )
            score_displays[category] = score_text
            
            score_rows.append(
                ft.Container(
                    content=ft.Row([
                        ft.Container(
                            content=ft.Column([
                                ft.Text(
                                    category,
                                    size=20,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE
                                ),
                                score_text
                            ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            width=80,
                            height=80,
                            bgcolor=CATEGORY_COLORS[category],
                            border_radius=8,
                            alignment=ft.Alignment.CENTER
                        ),
                        ft.Column([
                            ft.Text(
                                cat_info["name"],
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK
                            ),
                            ft.Text(
                                cat_info["description"][:80] + "...",
                                size=12,
                                color=ft.Colors.GREY_700
                            ),
                        ], spacing=2, expand=True)
                    ], spacing=15),
                    padding=10,
                    border=ft.Border.all(1, ft.Colors.GREY_300),
                    border_radius=8,
                    bgcolor=ft.Colors.WHITE
                )
            )
        
        return ft.Column(score_rows, spacing=10)
    
    def create_interest_code_card():
        """Create the interest code result card."""
        code_string, top_ranked, is_complete = assessment.get_interest_code()
        
        if not is_complete:
            answered, total = assessment.get_completion_counts()
            placeholder = ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.LOCK_OUTLINE, size=48, color=ft.Colors.GREY_400),
                    ft.Text(
                        "Complete Assessment to View Results",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREY_700
                    ),
                    ft.Text(
                        f"Answer all {total} statements to discover your Interest Code",
                        size=14,
                        color=ft.Colors.GREY_600,
                        text_align=ft.TextAlign.CENTER
                    )
                ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                bgcolor=ft.Colors.GREY_100,
                padding=40,
                border_radius=10,
                border=ft.Border.all(2, ft.Colors.GREY_300)
            )
            return placeholder
        
        # Show full results when complete with percentages
        code_text = ft.Text(
            code_string,
            size=36 if len(code_string) > 5 else 48,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLUE_700
        )
        
        # Add detailed descriptions for the top three positions, retaining ties.
        rank_keys = [(score, percentage) for _, score, percentage in top_ranked]
        rank_counts = {key: rank_keys.count(key) for key in set(rank_keys)}
        detailed_descriptions = []
        previous_key = None
        display_rank = 0
        for position, (cat, score, percentage) in enumerate(top_ranked):
            rank_key = (score, percentage)
            if rank_key != previous_key:
                display_rank = position + 1
                previous_key = rank_key
            tie_suffix = " (tie)" if rank_counts[rank_key] > 1 else ""
            cat_info = assessment.CATEGORIES[cat]
            detailed_descriptions.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(
                            f"#{display_rank}{tie_suffix}: {cat_info['name']} ({cat})",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=CATEGORY_COLORS[cat]
                        ),
                        ft.Text(
                            f"Score: {score} points ({percentage:.1f}%)",
                            size=14,
                            color=ft.Colors.GREY_700
                        ),
                        ft.Text(
                            cat_info['description'],
                            size=13,
                            color=ft.Colors.GREY_600
                        ),
                        ft.Text(
                            cat_info['careers'],
                            size=12,
                            color=ft.Colors.GREY_500,
                            italic=True
                        )
                    ], spacing=5),
                    padding=15,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=8,
                    border=ft.Border.all(2, CATEGORY_COLORS[cat])
                )
            )
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.CELEBRATION, size=32, color=ft.Colors.BLUE_700),
                    ft.Text(
                        "Your Interest Code",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                ], spacing=10),
                code_text,
                ft.Divider(height=1, color=ft.Colors.GREY_300),
                ft.Text(
                    "Your Top-Ranked Career Interest Areas:",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK
                ),
                ft.Column(detailed_descriptions, spacing=10),
                ft.Divider(height=1, color=ft.Colors.GREY_300),
                ft.Text(
                    (
                        "Parentheses and matching rank numbers identify equal scores; tied areas are not arbitrarily ordered. "
                        "Use the full profile to explore matching career pathways and educational programs."
                        if len(set(rank_keys)) < len(rank_keys)
                        else
                        "Your interest code represents your top 3 career interest areas. Use this code to explore matching career pathways and educational programs."
                    ),
                    size=12,
                    color=ft.Colors.GREY_600,
                    italic=True
                )
            ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            bgcolor=ft.Colors.BLUE_50,
            padding=20,
            border_radius=10,
            border=ft.Border.all(2, ft.Colors.BLUE_200)
        )
    
    def create_career_narrative_card():
        """Create the career narrative summary card."""
        narrative_text = assessment.get_career_narrative()
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.AUTO_STORIES, size=28, color=ft.Colors.GREEN_700),
                    ft.Text(
                        "Your Career Personality Summary",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                ], spacing=10),
                ft.Divider(height=1, color=ft.Colors.GREY_300),
                ft.Text(
                    narrative_text,
                    size=14,
                    color=ft.Colors.GREY_800,
                    text_align=ft.TextAlign.JUSTIFY,
                ),
            ], spacing=15),
            bgcolor=ft.Colors.GREEN_50,
            padding=20,
            border_radius=10,
            border=ft.Border.all(2, ft.Colors.GREEN_200),
            margin=ft.Margin.only(bottom=20)
        )
    
    def create_results_page():
        """Create the results page showing all scores and interest code."""
        title_container = ft.Container(
            content=ft.Text(
                "Career Path Assessment (RIASEC Interest Inventory)",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLACK
            ),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=10,
            margin=ft.Margin.only(bottom=20)
        )
        
        return ft.Column([
            title_container,
            create_interest_code_card(),
            create_career_narrative_card(),
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Detailed Category Scores",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                    ft.Container(height=10),
                    create_score_display(),
                ], spacing=10),
                bgcolor=ft.Colors.WHITE,
                padding=20,
                border_radius=10,
                border=ft.Border.all(1, ft.Colors.GREY_300),
                margin=ft.Margin.only(bottom=20)
            ),
            # CareerWise Insight section
            ft.Container(
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
                                "Your Career Exploration Compass",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK
                            ),
                            ft.Container(height=8),
                            ft.Text(
                                "Your RIASEC interest code reveals your natural work preferences and motivations. "
                                "These interests are reliable predictors of career satisfaction and performance.",
                                size=14,
                                color=ft.Colors.GREY_800,
                            ),
                            ft.Container(height=12),
                            ft.Row([
                                ft.Icon(ft.Icons.TIPS_AND_UPDATES, size=20, color=ft.Colors.DEEP_PURPLE_600),
                                ft.Text(
                                    "Career Development Strategy:",
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.DEEP_PURPLE_700
                                ),
                            ], spacing=8),
                            ft.Text(
                                "Use your highest interest areas to guide career exploration and decision-making. "
                                "Look for roles that combine multiple strong interests for maximum engagement. "
                                "Remember: interests predict satisfaction, but skills determine performance. "
                                "Develop both to create your ideal career path.",
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
            ),
            ft.Row([
                ft.Button(
                    "Reset Assessment",
                    icon=ft.Icons.RESTART_ALT,
                    on_click=on_reset_clicked,
                    bgcolor=ft.Colors.RED_400,
                    color=ft.Colors.WHITE,
                ),
            ], alignment=ft.MainAxisAlignment.END),
        ], scroll=ft.ScrollMode.AUTO)
    
    def build_assessment_content():
        """Build the complete assessment UI content."""
        if show_results[0]:
            return create_results_page()
        
        if show_welcome[0] and not any(assessment.responses.values()):
            return create_welcome_page()
        
        # Get progress info
        answered, total = assessment.get_completion_counts()
        percentage = assessment.get_completion_percentage()
        
        # Create progress chip
        progress_chip = ft.Chip(
            label=ft.Text(f"{answered}/{total} answered • {percentage:.0f}%"),
            bgcolor=ft.Colors.BLUE_100,
            disabled_color=ft.Colors.BLUE_100,
        )
        progress_indicator[0] = progress_chip
        
        # Instructions with progress
        instructions = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(
                        "Career Path Assessment (RIASEC Interest Inventory)",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                    ft.Container(expand=True),
                    progress_chip,
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Text(
                    "Rate each statement on a scale of 1-5, where 5 means 'Strongly Agree' and 1 means 'Strongly Disagree'. Your responses will help identify your career interests.",
                    size=14,
                    color=ft.Colors.GREY_700
                ),
            ], spacing=10),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=10,
            margin=ft.Margin.only(bottom=20)
        )
        
        statements_header = ft.Text(
            "Statements",
            size=18,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.BLACK
        )
        
        statements_container = create_all_statements_content()
        
        return ft.Column([
            instructions,
            statements_header,
            statements_container,
        ], scroll=ft.ScrollMode.AUTO, expand=True, ref=scroll_ref)
    
    def create_welcome_page():
        """Create the welcome page with How It Works explanation."""
        def on_start(e):
            show_welcome[0] = False
            container.content = build_assessment_content()
            container.update()
        
        answered, total = assessment.get_completion_counts()
        
        welcome_screen = ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.EXPLORE, size=48, color=ft.Colors.BLUE_700),
                    ft.Text(
                        "Career Path Assessment",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                    ft.Text(
                        "Discover your career interests using the RIASEC Interest Inventory",
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
                        "How It Works",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                    ft.Container(height=10),
                    ft.Row([
                        ft.Icon(ft.Icons.LOOKS_ONE, size=24, color=ft.Colors.BLUE_700),
                        ft.Text(
                            f"You'll rate {total} statements about activities and interests",
                            size=14,
                            color=ft.Colors.GREY_800,
                            expand=True
                        ),
                    ], spacing=10),
                    ft.Row([
                        ft.Icon(ft.Icons.LOOKS_TWO, size=24, color=ft.Colors.BLUE_700),
                        ft.Text(
                            "Rate each statement from 1-5 based on your interest level",
                            size=14,
                            color=ft.Colors.GREY_800,
                            expand=True
                        ),
                    ], spacing=10),
                    ft.Row([
                        ft.Icon(ft.Icons.LOOKS_3, size=24, color=ft.Colors.BLUE_700),
                        ft.Text(
                            "Use the scale: 5 = Strongly Agree, 3 = Neutral, 1 = Strongly Disagree",
                            size=14,
                            color=ft.Colors.GREY_800,
                            expand=True
                        ),
                    ], spacing=10),
                    ft.Row([
                        ft.Icon(ft.Icons.LOOKS_4, size=24, color=ft.Colors.BLUE_700),
                        ft.Text(
                            "Get your RIASEC code and discover matching career pathways",
                            size=14,
                            color=ft.Colors.GREY_800,
                            expand=True
                        ),
                    ], spacing=10),
                ], spacing=12),
                padding=20,
                bgcolor=ft.Colors.WHITE,
                border_radius=10,
                border=ft.Border.all(1, ft.Colors.GREY_300),
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
    
    # Create the main container
    container = ft.Container(
        content=build_assessment_content(),
        padding=20,
        expand=True
    )
    
    return container

def _run_standalone(page: ft.Page):
    page.title = "CareerWise - Career Path"
    page.add(create_career_path_assessment_ui(page))
