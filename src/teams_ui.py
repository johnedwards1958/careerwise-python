"""
Teams Assessment - UI Layer
Flet UI construction and page wiring.
"""

import flet as ft

from teams_logic import TeamsAssessment


def create_teams_assessment_ui(page: ft.Page):
    """
    Create the Team Roles Assessment UI.
    
    Args:
        page: The Flet page object
        
    Returns:
        A container with the complete assessment UI
    """
    # Initialize the assessment logic
    assessment = TeamsAssessment()
    
    # Create the main container first
    container = ft.Container(
        content=ft.Text("Loading..."),
        padding=20,
        expand=True
    )
    
    # Track current section being viewed/edited
    current_section_index = [0]  # Use list to allow modification in nested functions
    section_ids = list(TeamsAssessment.SECTIONS.keys())
    
    # References to UI elements that need updating
    progress_bar = None
    progress_text = None
    section_total_display = None
    section_validation_text = None
    next_button = None
    
    def update_progress():
        """Update the overall progress display."""
        completed, total, percentage = assessment.get_completion_status()
        
        if progress_bar:
            progress_bar.value = percentage / 100
            try:
                progress_bar.update()
            except:
                pass  # Progress bar not in page (e.g., moved from welcome to section view)
        
        if progress_text:
            progress_text.value = f"{completed}/{total} sections complete ({int(percentage)}%)"
            try:
                progress_text.update()
            except:
                pass  # Progress text not in page
    
    def update_section_total(section_id, do_update=True):
        """Update the section total display and validation message."""
        ratings = assessment.get_section_ratings(section_id)
        num_answered = sum(1 for rating in ratings if rating is not None)
        total_questions = len(ratings)
        is_complete = assessment.is_section_complete(section_id)
        
        if section_total_display:
            section_total_display.value = f"Answered: {num_answered}/{total_questions} questions"
            if is_complete:
                section_total_display.color = ft.Colors.GREEN_700
            else:
                section_total_display.color = ft.Colors.AMBER_700
            if do_update:
                try:
                    section_total_display.update()
                except:
                    pass  # Control not yet added to page
        
        if section_validation_text:
            if is_complete:
                section_validation_text.value = "✓ Section complete"
                section_validation_text.color = ft.Colors.GREEN_700
            elif num_answered == 0:
                section_validation_text.value = "Rate all statements to continue"
                section_validation_text.color = ft.Colors.GREY_600
            else:
                remaining = total_questions - num_answered
                section_validation_text.value = f"Rate {remaining} more statement(s)"
                section_validation_text.color = ft.Colors.AMBER_700
            if do_update:
                try:
                    section_validation_text.update()
                except:
                    pass  # Control not yet added to page
        
        # Update next button state
        if next_button and do_update:
            next_button.disabled = not is_complete
            next_button.bgcolor = ft.Colors.BLUE_700 if is_complete else ft.Colors.GREY_300
            try:
                next_button.update()
            except:
                pass  # Button not yet added to page
        
        if do_update:
            update_progress()
    
    def on_rating_changed(section_id, question_index, rating):
        """Handle when user changes rating."""
        assessment.set_rating(section_id, question_index, rating)
        update_section_total(section_id)
    
    def create_question_row(section_id, question_index, question_text):
        """Create a row for a single question with 1-5 rating scale."""
        current_value = assessment.get_rating(section_id, question_index)
        
        def on_radio_change(e):
            on_rating_changed(section_id, question_index, int(e.control.value))
        
        # Create radio buttons for 1-5 rating
        radio_group = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="5", label="5", label_style=ft.TextStyle(size=14)),
                ft.Radio(value="4", label="4", label_style=ft.TextStyle(size=14)),
                ft.Radio(value="3", label="3", label_style=ft.TextStyle(size=14)),
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
                        f"{question_index + 1}.",
                        size=14,
                        color=ft.Colors.GREY_700,
                        width=25,
                        weight=ft.FontWeight.BOLD
                    ),
                    ft.Container(
                        content=ft.Text(
                            question_text,
                            size=14,
                            color=ft.Colors.BLACK87,
                            weight=ft.FontWeight.W_400
                        ),
                        expand=True,
                    ),
                ], spacing=10),
                ft.Row([
                    ft.Text("Strongly Agree", size=12, color=ft.Colors.GREY_700, width=120),
                    radio_group,
                    ft.Text("Strongly Disagree", size=12, color=ft.Colors.GREY_700),
                ], alignment=ft.MainAxisAlignment.START),
            ], spacing=8),
            padding=ft.Padding.symmetric(horizontal=10, vertical=12),
            border=ft.Border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_300))
        )
    
    def create_section_view(section_id):
        """Create the view for a single section."""
        section = TeamsAssessment.SECTIONS[section_id]
        
        # Create all question rows
        question_rows = []
        for i, question_text in enumerate(section["questions"]):
            question_rows.append(create_question_row(section_id, i, question_text))
        
        # Section header
        section_number = section_ids.index(section_id) + 1
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.ASSIGNMENT, size=28, color=ft.Colors.BLUE_700),
                    ft.Text(
                        f"Section {section_number} of {len(section_ids)}",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                ], spacing=10),
                ft.Text(
                    section["title"],
                    size=16,
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
                        "Rate each statement based on how well it describes you",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                ], spacing=10),
                ft.Text(
                    "Use the scale: 5 = Strongly Agree, 4 = Agree, 3 = Neutral, 2 = Disagree, 1 = Strongly Disagree",
                    size=13,
                    color=ft.Colors.GREY_700
                ),
            ], spacing=8),
            bgcolor=ft.Colors.WHITE,
            padding=15,
            border_radius=8,
            border=ft.Border.all(1, ft.Colors.BLUE_200),
            margin=ft.Margin.only(bottom=15)
        )
        
        # Questions container
        questions_container = ft.Container(
            content=ft.Column(question_rows, spacing=0),
            bgcolor=ft.Colors.WHITE,
            border_radius=8,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            margin=ft.Margin.only(bottom=15)
        )
        
        # Section total and validation
        nonlocal section_total_display, section_validation_text
        section_total_display = ft.Text(
            "Total: 0/10 points",
            size=18,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.GREY_600
        )
        section_validation_text = ft.Text(
            "Allocate 10 points across the statements",
            size=14,
            color=ft.Colors.GREY_600
        )
        
        total_container = ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.CALCULATE, size=24, color=ft.Colors.BLUE_700),
                ft.Column([
                    section_total_display,
                    section_validation_text,
                ], spacing=2),
            ], spacing=10),
            bgcolor=ft.Colors.BLUE_50,
            padding=15,
            border_radius=8,
            margin=ft.Margin.only(bottom=20)
        )
        
        # Update displays with current values (don't call .update() yet as controls aren't in page)
        update_section_total(section_id, do_update=False)
        
        # Navigation buttons
        def on_previous(e):
            if current_section_index[0] > 0:
                current_section_index[0] -= 1
                container.content = build_assessment_content()
                container.update()
        
        def on_next(e):
            if assessment.is_section_valid(section_id):
                if current_section_index[0] < len(section_ids) - 1:
                    current_section_index[0] += 1
                    container.content = build_assessment_content()
                    container.update()
                elif assessment.is_complete():
                    # All sections complete, show results
                    container.content = create_results_page()
                    container.update()
        
        prev_button = ft.Button(
            "Previous",
            icon=ft.Icons.ARROW_BACK,
            on_click=on_previous,
            disabled=current_section_index[0] == 0,
            bgcolor=ft.Colors.GREY_300 if current_section_index[0] == 0 else ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
        )
        
        is_last_section = current_section_index[0] == len(section_ids) - 1
        next_button_text = "View Results" if is_last_section else "Next Section"
        
        # Store reference to next button for updates
        nonlocal next_button
        next_button = ft.Button(
            next_button_text,
            icon=ft.Icons.ARROW_FORWARD if not is_last_section else ft.Icons.EMOJI_EVENTS,
            on_click=on_next,
            disabled=not assessment.is_section_valid(section_id),
            bgcolor=ft.Colors.BLUE_700 if assessment.is_section_valid(section_id) else ft.Colors.GREY_300,
            color=ft.Colors.WHITE,
        )
        
        navigation = ft.Row([
            prev_button,
            ft.Container(expand=True),
            next_button,
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        
        return ft.Column([
            header,
            instructions,
            questions_container,
            total_container,
            navigation,
        ], scroll=ft.ScrollMode.AUTO, expand=True)
    
    def create_results_page():
        """Create the results page showing role scores and top roles."""
        # Calculate scores
        role_scores = assessment.calculate_role_scores()
        ranked_role_groups = assessment.get_ranked_role_groups()
        preferred_role_groups = ranked_role_groups[:2]
        total_assessment_points = (
            len(assessment.SECTIONS) * assessment.POINTS_PER_SECTION
        )
        
        # Title
        title_container = ft.Container(
            content=ft.Text(
                "Team Roles Assessment Results",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLACK
            ),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=10,
            margin=ft.Margin.only(bottom=20)
        )
        
        # Top roles summary. Show every role in a tied score group rather than
        # inventing an order from the role dictionary's insertion order.
        def create_preferred_role_card(role_id, score, rank, is_tied):
            role = TeamsAssessment.ROLES[role_id]
            is_primary = rank == 1
            accent = ft.Colors.BLUE_700 if is_primary else ft.Colors.GREEN_700
            background = ft.Colors.BLUE_50 if is_primary else ft.Colors.GREEN_50
            border = ft.Colors.BLUE_200 if is_primary else ft.Colors.GREEN_200
            tier_name = "primary" if is_primary else "secondary"
            label = f"Joint {tier_name}" if is_tied else tier_name.capitalize()

            return ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Text(
                                f"={rank}" if is_tied else str(rank),
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE,
                            ),
                            width=40,
                            height=40,
                            bgcolor=accent,
                            border_radius=20,
                            alignment=ft.Alignment.CENTER,
                        ),
                        ft.Column([
                            ft.Text(
                                f"{label}: {role['name']}",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=accent,
                            ),
                            ft.Text(
                                f"Score: {score:.1f} points",
                                size=14,
                                color=ft.Colors.GREY_700,
                            ),
                        ], spacing=2),
                    ], spacing=15),
                    ft.Text(
                        role['description'],
                        size=14,
                        color=ft.Colors.BLACK87,
                    ),
                    ft.Container(
                        content=ft.Column([
                            ft.Text(
                                "Strengths:",
                                size=13,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.GREEN_700,
                            ),
                            ft.Text(role['strengths'], size=13, color=ft.Colors.GREY_800),
                            ft.Text(
                                "Allowable weaknesses:",
                                size=13,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.ORANGE_700,
                            ),
                            ft.Text(role['weaknesses'], size=13, color=ft.Colors.GREY_800),
                        ], spacing=5),
                        padding=10,
                        bgcolor=ft.Colors.GREY_50,
                        border_radius=8,
                        margin=ft.Margin.only(top=10),
                    ),
                ], spacing=10),
                padding=15,
                bgcolor=background,
                border_radius=8,
                border=ft.Border.all(2, border),
                margin=ft.Margin.only(bottom=15),
            )

        preferred_role_cards = []
        for rank, group in enumerate(preferred_role_groups, start=1):
            is_tied = len(group) > 1
            for role_id, score in group:
                preferred_role_cards.append(
                    create_preferred_role_card(role_id, score, rank, is_tied)
                )
        
        top_roles_card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.EMOJI_EVENTS, size=32, color=ft.Colors.AMBER_700),
                    ft.Text(
                        "Your Preferred Team Roles",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                ], spacing=10),
                ft.Divider(height=1, color=ft.Colors.GREY_300),
                *preferred_role_cards,
            ], spacing=15),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            margin=ft.Margin.only(bottom=20)
        )
        
        # All role scores
        role_score_items = []
        sorted_roles = [role for group in ranked_role_groups for role in group]
        role_ranks = {
            role_id: rank
            for rank, group in enumerate(ranked_role_groups, start=1)
            for role_id, _ in group
        }
        preferred_role_ids = {
            role_id for group in preferred_role_groups for role_id, _ in group
        }
        
        for role_id, score in sorted_roles:
            role = TeamsAssessment.ROLES[role_id]
            rank = role_ranks[role_id]
            is_top = role_id in preferred_role_ids
            is_tied = len(ranked_role_groups[rank - 1]) > 1
            
            role_card = ft.Container(
                content=ft.Row([
                    ft.Container(
                        content=ft.Column([
                            ft.Text(
                                f"{score:.1f}",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE
                            ),
                            ft.Text(
                                "pts",
                                size=11,
                                color=ft.Colors.WHITE
                            )
                        ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        width=55,
                        height=55,
                        bgcolor=ft.Colors.BLUE_700 if is_top else ft.Colors.GREY_500,
                        border_radius=8,
                        alignment=ft.Alignment.CENTER
                    ),
                    ft.Column([
                        ft.Row([
                            ft.Text(
                                role['name'],
                                size=15,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK
                            ),
                            ft.Container(
                                content=ft.Text(
                                    f"=#{rank}" if is_tied else f"#{rank}",
                                    size=11,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE
                                ),
                                bgcolor=ft.Colors.BLUE_700 if is_top else ft.Colors.GREY_500,
                                padding=ft.Padding.symmetric(horizontal=8, vertical=2),
                                border_radius=10
                            ) if is_top else ft.Container(),
                        ], spacing=10),
                        ft.Text(
                            role['description'],
                            size=12,
                            color=ft.Colors.GREY_700
                        ),
                    ], spacing=3, expand=True)
                ], spacing=15),
                padding=12,
                border=ft.Border.all(2 if is_top else 1, ft.Colors.BLUE_200 if is_top else ft.Colors.GREY_300),
                border_radius=8,
                bgcolor=ft.Colors.BLUE_50 if is_top else ft.Colors.WHITE,
                margin=ft.Margin.only(bottom=8)
            )
            role_score_items.append(role_card)
        
        all_scores_container = ft.Container(
            content=ft.Column([
                ft.Text(
                    "All Role Scores",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK
                ),
                ft.Text(
                    f"Each section contributes {assessment.POINTS_PER_SECTION:g} "
                    "relative-preference points; "
                    f"all 8 role scores total {total_assessment_points:g} points.",
                    size=13,
                    color=ft.Colors.GREY_700,
                    italic=True
                ),
                ft.Container(height=10),
                ft.Column(role_score_items, spacing=0),
            ]),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            margin=ft.Margin.only(bottom=20)
        )
        
        # Reset button
        def on_reset(e):
            assessment.reset()
            current_section_index[0] = 0
            container.content = build_assessment_content()
            container.update()
        
        reset_button = ft.Row([
            ft.Button(
                "Start New Assessment",
                icon=ft.Icons.RESTART_ALT,
                on_click=on_reset,
                bgcolor=ft.Colors.RED_400,
                color=ft.Colors.WHITE,
            ),
        ], alignment=ft.MainAxisAlignment.END)
        
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
                            "Your Team Dynamics Blueprint",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            "Your team role preferences reveal how you naturally contribute to group success. "
                            "Understanding these tendencies helps you choose roles where you'll thrive and add maximum value.",
                            size=14,
                            color=ft.Colors.GREY_800,
                        ),
                        ft.Container(height=12),
                        ft.Row([
                            ft.Icon(ft.Icons.TIPS_AND_UPDATES, size=20, color=ft.Colors.DEEP_PURPLE_600),
                            ft.Text(
                                "Team Effectiveness Strategy:",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.DEEP_PURPLE_700
                            ),
                        ], spacing=8),
                        ft.Text(
                            "Seek opportunities that leverage your strongest team roles while developing secondary ones. "
                            "Great team players understand their natural style but can adapt when the team needs different contributions. "
                            "Communicate your preferred roles to help others understand how to best work with you.",
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
            top_roles_card,
            all_scores_container,
            insight_container,
            reset_button,
        ], scroll=ft.ScrollMode.AUTO, expand=True)
    
    def build_assessment_content():
        """Build the assessment UI based on completion status."""
        # Check if complete
        if assessment.is_complete():
            return create_results_page()
        
        # Show instructions and progress overview if starting
        if current_section_index[0] == 0 and not any(
            assessment.get_rating(section_ids[0], i) is not None 
            for i in range(len(TeamsAssessment.SECTIONS[section_ids[0]]["questions"]))
        ):
            # Initial welcome screen
            def on_start(e):
                container.content = create_section_view(section_ids[0])
                container.update()
            
            welcome_screen = ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.GROUPS, size=48, color=ft.Colors.BLUE_700),
                        ft.Text(
                            "Team Roles Assessment",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK
                        ),
                        ft.Text(
                            "Discover your preferred team roles and how you contribute to team success",
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
                                "You'll work through 7 sections, each with 8 statements",
                                size=14,
                                color=ft.Colors.GREY_800,
                                expand=True
                            ),
                        ], spacing=10),
                        ft.Row([
                            ft.Icon(ft.Icons.LOOKS_TWO, size=24, color=ft.Colors.BLUE_700),
                            ft.Text(
                                "Rate each statement from 1-5 based on how well it describes you",
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
                                "Discover your top 2 preferred team roles based on your responses",
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
        
        # Show current section
        section_id = section_ids[current_section_index[0]]
        return create_section_view(section_id)
    
    # Initialize and return
    container.content = build_assessment_content()
    return container

def _run_standalone(page: ft.Page):
    page.title = "CareerWise - Team Roles"
    page.add(create_teams_assessment_ui(page))
