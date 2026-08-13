"""
Transferrable Assessment - UI Layer
Flet UI construction and page wiring.
"""

import flet as ft

from transferrable_logic import TransferrableSkillsAssessment


def create_transferrable_assessment_ui(page: ft.Page):
    """
    Create the Transferrable Skills Assessment UI.
    
    Args:
        page: The Flet page object
        
    Returns:
        A container with the complete assessment UI
    """
    # Initialize the assessment logic
    assessment = TransferrableSkillsAssessment()
    
    # Create the main container first
    container = ft.Container(
        content=ft.Text("Loading..."),
        padding=20,
        expand=True
    )
    
    # Track if we're showing results
    showing_results = [False]
    
    # Container for the view results button that persists
    results_button_container = ft.Container(margin=ft.Margin.only(top=20))

    def get_status_color(status):
        """Get the color for a given status."""
        colors = {
            'highly_transferable': ft.Colors.GREEN_700,
            'moderately_transferable': ft.Colors.BLUE_700,
            'developing': ft.Colors.AMBER_700,
            'narrowly_specialised': ft.Colors.RED_700,
            'incomplete': ft.Colors.GREY_600
        }
        return colors.get(status, ft.Colors.GREY_400)
    
    def get_status_text(status):
        """Get descriptive text for a status."""
        texts = {
            'highly_transferable': '✓ Highly Transferable',
            'moderately_transferable': '✓ Moderately Transferable',
            'developing': 'Developing',
            'narrowly_specialised': '⚠ Narrowly Specialised',
            'incomplete': 'Incomplete'
        }
        return texts.get(status, status)
    
    def update_completion_display(do_update=True):
        """Update the completion percentage display."""
        answered = len(assessment.responses)
        total = len(assessment.QUESTIONS)
        is_complete = answered == total
        
        # print(f"Update completion: complete={is_complete}, answered={answered}/{total}, do_update={do_update}")
        
        # Update view results button in the container
        if do_update:
            if is_complete:
                # print("Creating View Results button")
                def on_view_results(e):
                    showing_results[0] = True
                    container.content = create_results_page()
                    container.update()
                
                results_button_container.content = ft.Row([
                    ft.Button(
                        "View Results",
                        icon=ft.Icons.EMOJI_EVENTS,
                        on_click=on_view_results,
                        bgcolor=ft.Colors.BLUE_700,
                        color=ft.Colors.WHITE,
                        height=45,
                        style=ft.ButtonStyle(
                            text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
                        ),
                    ),
                ], alignment=ft.MainAxisAlignment.CENTER)
            else:
                # print("Hiding View Results button")
                results_button_container.content = None
            
            results_button_container.update()
            # print("Button container updated")
    
    def on_rating_changed(question_index, rating):
        """Handle when user changes rating."""
        assessment.set_response(question_index, rating)
        # print(f"Rating changed. Complete: {assessment.is_complete()}, Answered: {len(assessment.responses)}/{len(assessment.QUESTIONS)}")
        update_completion_display()
    
    def create_question_row(question_index):
        """Create a row for a single question with 1-5 rating scale."""
        question = assessment.QUESTIONS[question_index]
        current_value = assessment.get_response(question_index)
        
        def on_radio_change(e):
            on_rating_changed(question_index, int(e.control.value))
        
        # Create radio buttons for 1-5 rating (5=Always true, 1=Not true)
        radio_group = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="5", label="Always", label_style=ft.TextStyle(size=13)),
                ft.Radio(value="4", label="Often", label_style=ft.TextStyle(size=13)),
                ft.Radio(value="3", label="Sometimes", label_style=ft.TextStyle(size=13)),
                ft.Radio(value="2", label="Rarely", label_style=ft.TextStyle(size=13)),
                ft.Radio(value="1", label="Not true", label_style=ft.TextStyle(size=13)),
            ], spacing=12),
            value=str(current_value) if current_value else None,
            on_change=on_radio_change
        )
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text(
                        f"{question_index + 1}.",
                        size=14,
                        color=ft.Colors.GREY_700,
                        width=25,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Container(
                        content=ft.Text(
                            question["text"],
                            size=14,
                            color=ft.Colors.BLACK87,
                            weight=ft.FontWeight.W_400
                        ),
                        expand=True,
                    ),
                ], spacing=10),
                ft.Container(
                    content=radio_group,
                    margin=ft.Margin.only(left=35),
                ),
            ], spacing=8),
            padding=ft.Padding.symmetric(horizontal=10, vertical=12),
            border=ft.Border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_300))
        )
    
    def create_domain_section(domain_id):
        """Create a section for a domain with its questions."""
        domain = assessment.DOMAINS[domain_id]
        
        # Header
        header = ft.Container(
            content=ft.Column([
                ft.Text(
                    domain["title"],
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_700
                ),
                ft.Text(
                    domain["description"],
                    size=13,
                    color=ft.Colors.GREY_600,
                    italic=True
                ),
            ], spacing=3),
            padding=ft.Padding.only(left=10, right=10, top=15, bottom=10),
            bgcolor=ft.Colors.BLUE_50,
            border_radius=ft.BorderRadius(10, 10, 0, 0),
        )
        
        # Questions for this domain
        question_rows = []
        for idx in domain["questions"]:
            question_rows.append(create_question_row(idx))
        
        questions_container = ft.Container(
            content=ft.Column(question_rows, spacing=0),
            bgcolor=ft.Colors.WHITE,
        )
        
        return ft.Container(
            content=ft.Column([
                header,
                questions_container,
            ], spacing=0),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            margin=ft.Margin.only(bottom=15)
        )
    
    def create_assessment_view():
        """Create the main assessment view with all questions."""
        # Title
        title_container = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.BOOK, size=28, color=ft.Colors.BLUE_700),
                ft.Text(
                    "Transferrable Skills Assessment",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK
                ),
            ], spacing=10),
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
                        "Rate each statement based on how well it describes you",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                ], spacing=10),
                ft.Text(
                    "Your transferrable skills are abilities that stay valuable no matter where you work. Use the scale: Always true, Often true, Sometimes true, Rarely true, Not true",
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
        
        # Domain sections
        domain_sections = []
        for domain_id in assessment.DOMAINS:
            domain_sections.append(create_domain_section(domain_id))
        
        # Completion status
        answered = len(assessment.responses)
        total = len(assessment.QUESTIONS)
        is_complete = answered == total
        
        completion_container = ft.Container(
            content=ft.Row([
                ft.Icon(
                    ft.Icons.CHECK_CIRCLE if is_complete else ft.Icons.PENDING,
                    size=20,
                    color=ft.Colors.GREEN_700 if is_complete else ft.Colors.GREY_600
                ),
                ft.Text(
                    f"Progress: {answered}/{total} questions answered",
                    size=14,
                    color=ft.Colors.GREY_700,
                    weight=ft.FontWeight.BOLD
                ),
            ], spacing=8),
            padding=10,
            margin=ft.Margin.only(bottom=20)
        )
        
        # Set up the persistent results button container
        if is_complete:
            def on_view_results(e):
                showing_results[0] = True
                container.content = create_results_page()
                container.update()
            
            results_button_container.content = ft.Row([
                ft.Button(
                    "View Results",
                    icon=ft.Icons.EMOJI_EVENTS,
                    on_click=on_view_results,
                    bgcolor=ft.Colors.BLUE_700,
                    color=ft.Colors.WHITE,
                    height=45,
                    style=ft.ButtonStyle(
                        text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
                    ),
                ),
            ], alignment=ft.MainAxisAlignment.CENTER)
        else:
            results_button_container.content = None
        
        return ft.Column([
            title_container,
            instructions,
            *domain_sections,
            completion_container,
            results_button_container,
        ], scroll=ft.ScrollMode.AUTO, expand=True)
    
    def create_results_page():
        """Create the results page showing scores and recommendations."""
        # Calculate scores
        total_score, max_total, completion = assessment.calculate_overall_score()
        overall_status = assessment.get_overall_status()
        
        # Title
        title_container = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.EMOJI_EVENTS, size=32, color=ft.Colors.BLUE_700),
                ft.Text(
                    "Your Transferrable Skills Profile",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK
                ),
            ], spacing=10),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=10,
            margin=ft.Margin.only(bottom=20)
        )
        
        # Overall score summary
        overall_card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.ASSESSMENT, size=32, color=ft.Colors.BLUE_700),
                    ft.Text(
                        "Overall Assessment",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                ], spacing=10),
                ft.Divider(height=1, color=ft.Colors.GREY_300),
                
                ft.Row([
                    ft.Column([
                        ft.Text(
                            f"Total Score: {total_score}/{max_total}",
                            size=18,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_700
                        ),
                        ft.Text(
                            get_status_text(overall_status),
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=get_status_color(overall_status)
                        ),
                    ], spacing=5),
                ], alignment=ft.MainAxisAlignment.START),
                
                ft.Container(
                    content=ft.Text(
                        assessment.get_status_description(overall_status),
                        size=14,
                        color=ft.Colors.GREY_700,
                        italic=True
                    ),
                    bgcolor=ft.Colors.BLUE_50,
                    padding=15,
                    border_radius=10,
                    margin=ft.Margin.only(top=10)
                ),
            ], spacing=10),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            margin=ft.Margin.only(bottom=20)
        )
        
        # Domain scores
        category_cards = []
        for domain_id in assessment.DOMAINS:
            domain = assessment.DOMAINS[domain_id]
            score, max_possible, answered, total = assessment.calculate_domain_score(domain_id)
            
            # Calculate percentage for progress bar
            percentage = (score / max_possible * 100) if max_possible > 0 else 0
            
            category_card = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(
                            domain["title"],
                            size=15,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK
                        ),
                        ft.Container(expand=True),
                        ft.Text(
                            f"{score}/{max_possible}",
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_700
                        ),
                    ]),
                    ft.Text(
                        domain["description"],
                        size=12,
                        color=ft.Colors.GREY_600,
                        italic=True
                    ),
                    ft.Container(
                        content=ft.ProgressBar(
                            value=percentage / 100,
                            color=ft.Colors.BLUE_700,
                            bgcolor=ft.Colors.GREY_300,
                            height=8,
                        ),
                        margin=ft.Margin.only(top=5)
                    ),
                ], spacing=5),
                bgcolor=ft.Colors.WHITE,
                padding=15,
                border_radius=10,
                border=ft.Border.all(1, ft.Colors.GREY_300),
                margin=ft.Margin.only(bottom=10)
            )
            category_cards.append(category_card)
        
        # CareerWise Insight section
        insight_card = ft.Container(
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
                            "Your Skills Mobility Framework",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            "Your top transferrable skills are your passport between careers and industries. "
                            "These versatile abilities demonstrate your adaptability and value across different roles.",
                            size=14,
                            color=ft.Colors.GREY_800,
                        ),
                        ft.Container(height=12),
                        ft.Row([
                            ft.Icon(ft.Icons.TIPS_AND_UPDATES, size=20, color=ft.Colors.DEEP_PURPLE_600),
                            ft.Text(
                                "Career Transition Strategy:",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.DEEP_PURPLE_700
                            ),
                        ], spacing=8),
                        ft.Text(
                            "Focus on your strongest transferrable skills when exploring new career paths. "
                            "These skills reduce risk for employers and accelerate your transition timeline. "
                            "Use concrete examples of how you've applied these skills across different contexts "
                            "to demonstrate your versatility and problem-solving capabilities.",
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
        
        # Navigation buttons
        def on_back_to_assessment(e):
            showing_results[0] = False
            container.content = create_assessment_view()
            container.update()
        
        def on_reset_clicked(e):
            """Handle reset button click."""
            assessment.reset()
            showing_results[0] = False
            container.content = build_assessment_content()
            container.update()
        
        back_button = ft.Button(
            "Back to Assessment",
            icon=ft.Icons.ARROW_BACK,
            on_click=on_back_to_assessment,
            bgcolor=ft.Colors.GREY_700,
            color=ft.Colors.WHITE,
        )
        
        reset_button = ft.Button(
            "Reset Assessment",
            icon=ft.Icons.REFRESH,
            on_click=on_reset_clicked,
            bgcolor=ft.Colors.ORANGE_700,
            color=ft.Colors.WHITE,
        )
        
        navigation = ft.Row([
            back_button,
            ft.Container(expand=True),
            reset_button,
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        
        return ft.Column([
            title_container,
            overall_card,
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Domain Breakdown",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                    ft.Container(height=10),
                    *category_cards,
                ], spacing=0),
                bgcolor=ft.Colors.WHITE,
                padding=20,
                border_radius=10,
                border=ft.Border.all(1, ft.Colors.GREY_300),
                margin=ft.Margin.only(bottom=20)
            ),
            insight_card,
            navigation,
        ], scroll=ft.ScrollMode.AUTO, expand=True)
    
    def build_assessment_content():
        """Build the main assessment content."""
        # Check if assessment is complete and results should be shown
        if showing_results[0] and assessment.is_complete():
            return create_results_page()
        
        # Show welcome page if starting
        if not any(assessment.get_response(i) is not None for i in range(len(assessment.QUESTIONS))):
            # Initial welcome screen
            def on_start(e):
                container.content = create_assessment_view()
                container.update()
            
            welcome_screen = ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.BOOK, size=48, color=ft.Colors.BLUE_700),
                        ft.Text(
                            "Transferrable Skills Assessment",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK
                        ),
                        ft.Text(
                            "Discover the strengths you can take anywhere",
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
                            "Your transferrable skills are the abilities that stay valuable no matter where you work — in any job, team, or industry. They include how you solve problems, manage tasks, adapt to change, and communicate with others.",
                            size=14,
                            color=ft.Colors.GREY_800,
                        ),
                        ft.Container(height=10),
                        ft.Row([
                            ft.Icon(ft.Icons.LOOKS_ONE, size=24, color=ft.Colors.BLUE_700),
                            ft.Text(
                                f"Answer {len(assessment.QUESTIONS)} questions across 5 key domains",
                                size=14,
                                color=ft.Colors.GREY_800,
                                expand=True
                            ),
                        ], spacing=10),
                        ft.Row([
                            ft.Icon(ft.Icons.LOOKS_TWO, size=24, color=ft.Colors.BLUE_700),
                            ft.Text(
                                "Rate each statement: Always true → Not true",
                                size=14,
                                color=ft.Colors.GREY_800,
                                expand=True
                            ),
                        ], spacing=10),
                        ft.Row([
                            ft.Icon(ft.Icons.LOOKS_3, size=24, color=ft.Colors.BLUE_700),
                            ft.Text(
                                "Discover your strongest portable skills and where to grow",
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
        
        # Show assessment view
        return create_assessment_view()
    
    # Build and set initial content
    container.content = build_assessment_content()
    
    return container


def create_transferrable_page(page: ft.Page):
    """Entry point for creating the transferrable skills assessment page."""
    return create_transferrable_assessment_ui(page)

def _run_standalone(page: ft.Page):
    page.title = "CareerWise - Transferrable Skills"
    page.add(create_transferrable_assessment_ui(page))
