"""
Priorities Assessment - UI Layer
Flet UI construction and page wiring.
"""

import flet as ft

from priorities_logic import PrioritiesAssessment


def create_priorities_assessment_ui(page: ft.Page):
    """
    Create the Career Priorities Assessment UI.
    
    Args:
        page: The Flet page object
        
    Returns:
        A container with the complete assessment UI
    """
    # Initialize the assessment logic
    assessment = PrioritiesAssessment()
    
    # Create the main container first
    container = ft.Container(
        content=ft.Text("Loading..."),
        padding=20,
        expand=True
    )
    
    # Track current anchor being viewed
    current_anchor_index = [0]  # Use list to allow modification in nested functions
    anchor_ids = list(PrioritiesAssessment.ANCHORS.keys())
    
    # References to UI elements that need updating
    next_button = None

    def update_anchor_completion(anchor_id, do_update=True):
        """Update the anchor completion display."""
        answered = sum(1 for i in range(len(PrioritiesAssessment.ANCHORS[anchor_id]["questions"])) 
                      if assessment.get_response(anchor_id, i) is not None)
        total = len(PrioritiesAssessment.ANCHORS[anchor_id]["questions"])
        is_complete = answered == total
        
        # Update next button state
        if next_button and do_update:
            next_button.disabled = not is_complete
            next_button.bgcolor = ft.Colors.BLUE_700 if is_complete else ft.Colors.GREY_300
            if hasattr(page, 'update'):
                next_button.update()
    
    def on_rating_changed(anchor_id, question_index, rating):
        """Handle when user changes rating."""
        assessment.set_response(anchor_id, question_index, rating)
        update_anchor_completion(anchor_id)
    
    def create_question_row(anchor_id, question_index, question_text):
        """Create a row for a single question with 1-5 rating scale."""
        current_value = assessment.get_response(anchor_id, question_index)
        
        def on_radio_change(e):
            on_rating_changed(anchor_id, question_index, int(e.control.value))
        
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
                    ft.Text("Very much like me", size=12, color=ft.Colors.GREY_700, width=130),
                    radio_group,
                    ft.Text("Not like me", size=12, color=ft.Colors.GREY_700),
                ], alignment=ft.MainAxisAlignment.START),
            ], spacing=8),
            padding=ft.Padding.symmetric(horizontal=10, vertical=12),
            border=ft.Border.only(bottom=ft.BorderSide(1, ft.Colors.GREY_300))
        )
    
    def create_anchor_view(anchor_id):
        """Create the view for a single anchor (career anchor)."""
        anchor_number = list(PrioritiesAssessment.ANCHORS.keys()).index(anchor_id) + 1
        anchor = PrioritiesAssessment.ANCHORS[anchor_id]
        is_last_anchor = anchor_number == len(PrioritiesAssessment.ANCHORS)
        
        # Header
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.ANCHOR, size=28, color=ft.Colors.BLUE_700),
                    ft.Text(
                        f"Career Anchor {anchor_number} of {len(PrioritiesAssessment.ANCHORS)}",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                ], spacing=10),
                ft.Text(
                    anchor["title"],
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
                        "Rate each statement based on how accurately it describes you",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                ], spacing=10),
                ft.Text(
                    "Use the scale: 5 = Very much like me, 4 = Quite like me, 3 = Somewhat like me, 2 = A little like me, 1 = Not like me",
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
        
        # Questions container
        question_rows = []
        for i, question_text in enumerate(anchor["questions"]):
            question_rows.append(create_question_row(anchor_id, i, question_text))
        
        questions_container = ft.Container(
            content=ft.Column(question_rows, spacing=0),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            margin=ft.Margin.only(bottom=20)
        )
        
        # Anchor total
        answered = sum(1 for i in range(len(anchor["questions"])) 
                      if assessment.get_response(anchor_id, i) is not None)
        total = len(anchor["questions"])
        
        total_container = ft.Container(
            content=ft.Text(
                f"Answered: {answered}/{total} questions",
                size=14,
                color=ft.Colors.GREY_700,
                weight=ft.FontWeight.BOLD
            ),
            padding=10,
            margin=ft.Margin.only(bottom=20)
        )
        
        # Navigation
        def on_prev(e):
            if current_anchor_index[0] > 0:
                current_anchor_index[0] -= 1
                container.content = build_assessment_content()
                container.update()
        
        def on_next(e):
            is_complete = all(assessment.get_response(anchor_id, i) is not None 
                            for i in range(len(anchor["questions"])))
            if is_complete:
                if current_anchor_index[0] < len(anchor_ids) - 1:
                    current_anchor_index[0] += 1
                    container.content = build_assessment_content()
                    container.update()
                elif assessment.is_complete():
                    # All anchors complete, show results
                    container.content = create_results_page()
                    container.update()
        
        prev_button = ft.Button(
            "Previous",
            icon=ft.Icons.ARROW_BACK,
            on_click=on_prev,
            disabled=anchor_number == 1,
            bgcolor=ft.Colors.GREY_300 if anchor_number == 1 else ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
        )
        
        next_button_text = "View Results" if is_last_anchor else "Next Anchor"
        is_anchor_complete = all(assessment.get_response(anchor_id, i) is not None 
                                for i in range(len(anchor["questions"])))
        
        # Store reference to next button for updates
        nonlocal next_button
        next_button = ft.Button(
            next_button_text,
            icon=ft.Icons.ARROW_FORWARD if not is_last_anchor else ft.Icons.EMOJI_EVENTS,
            on_click=on_next,
            disabled=not is_anchor_complete,
            bgcolor=ft.Colors.BLUE_700 if is_anchor_complete else ft.Colors.GREY_300,
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
        """Create the results page showing anchor scores and top anchors."""
        # Calculate scores
        all_scores = assessment.get_all_anchor_scores()
        top_anchors = assessment.get_top_anchors(2)
        
        # Title
        title_container = ft.Container(
            content=ft.Text(
                "Career Priorities Assessment Results",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLACK
            ),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=10,
            margin=ft.Margin.only(bottom=20)
        )
        
        # Top anchors summary. get_top_anchors() includes every anchor tied at
        # the cutoff, so equal scores are labelled jointly rather than being
        # assigned an arbitrary primary/secondary order.
        highest_score = top_anchors[0][1]
        primary_count = sum(score == highest_score for _, score in top_anchors)
        secondary_count = len(top_anchors) - primary_count
        top_anchors_cards = []

        for anchor_id, score in top_anchors:
            anchor = PrioritiesAssessment.ANCHORS[anchor_id]
            max_score = len(anchor['questions']) * 5
            is_primary = score == highest_score
            tied_count = primary_count if is_primary else secondary_count
            rank_name = "Primary" if is_primary else "Secondary"
            if tied_count > 1:
                rank_name = f"Joint {rank_name}"
            rank_number = "1" if is_primary else "2"
            accent = ft.Colors.BLUE_700 if is_primary else ft.Colors.GREEN_700
            tint = ft.Colors.BLUE_50 if is_primary else ft.Colors.GREEN_50
            border_color = ft.Colors.BLUE_200 if is_primary else ft.Colors.GREEN_200

            top_anchors_cards.append(
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Container(
                                content=ft.Text(
                                    rank_number,
                                    size=20,
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
                                    f"{rank_name} Career Anchor: {anchor['title']}",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=accent,
                                ),
                                ft.Text(
                                    f"Score: {score}/{max_score} points",
                                    size=14,
                                    color=ft.Colors.GREY_700,
                                ),
                            ], spacing=2, expand=True),
                        ], spacing=15),
                        ft.Divider(height=1, color=ft.Colors.GREY_300),
                        ft.Text(
                            anchor['interpretation'],
                            size=14,
                            color=ft.Colors.BLACK87,
                            weight=ft.FontWeight.W_500,
                        ),
                    ], spacing=10),
                    bgcolor=tint,
                    padding=20,
                    border_radius=10,
                    border=ft.Border.all(2, border_color),
                    margin=ft.Margin.only(bottom=15),
                )
            )
        
        top_anchors_container = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.EMOJI_EVENTS, size=32, color=ft.Colors.AMBER_700),
                    ft.Text(
                        "Your Primary Career Anchor(s)",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                ], spacing=10),
                ft.Text(
                    "The value or motivation you are least willing to sacrifice in your career",
                    size=13,
                    color=ft.Colors.GREY_700,
                    italic=True
                ),
                ft.Container(height=10),
                *top_anchors_cards,
            ], spacing=0),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            margin=ft.Margin.only(bottom=20)
        )
        
        # All anchor scores
        anchor_score_items = []
        sorted_anchors = sorted(all_scores.items(), key=lambda x: x[1], reverse=True)
        top_anchor_ids = {anchor_id for anchor_id, _ in top_anchors}
        rank_by_anchor = {}
        previous_score = None
        current_rank = 0
        for position, (anchor_id, score) in enumerate(sorted_anchors, start=1):
            if score != previous_score:
                current_rank = position
                previous_score = score
            rank_by_anchor[anchor_id] = current_rank
        
        for i, (anchor_id, score) in enumerate(sorted_anchors):
            anchor = PrioritiesAssessment.ANCHORS[anchor_id]
            is_top = anchor_id in top_anchor_ids
            max_score = len(anchor['questions']) * 5
            
            # Calculate percentage
            percentage = (score / max_score) * 100 if max_score else 0
            
            anchor_card = ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Container(
                            content=ft.Column([
                                ft.Text(
                                    f"{score}",
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.WHITE
                                ),
                                ft.Text(
                                    f"/{max_score}",
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
                                    anchor['title'],
                                    size=15,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLACK
                                ),
                                ft.Container(
                                    content=ft.Text(
                                        f"#{rank_by_anchor[anchor_id]}",
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
                                anchor['interpretation'],
                                size=12,
                                color=ft.Colors.GREY_700
                            ),
                            # Progress bar
                            ft.Container(
                                content=ft.ProgressBar(
                                    value=percentage / 100,
                                    color=ft.Colors.BLUE_700 if is_top else ft.Colors.GREY_500,
                                    bgcolor=ft.Colors.GREY_200,
                                    height=8,
                                ),
                                width=250,
                                margin=ft.Margin.only(top=5)
                            ),
                        ], spacing=3, expand=True)
                    ], spacing=15),
                ], spacing=5),
                padding=12,
                border=ft.Border.all(2 if is_top else 1, ft.Colors.BLUE_200 if is_top else ft.Colors.GREY_300),
                border_radius=8,
                bgcolor=ft.Colors.BLUE_50 if is_top else ft.Colors.WHITE,
                margin=ft.Margin.only(bottom=8)
            )
            anchor_score_items.append(anchor_card)
        
        all_scores_container = ft.Container(
            content=ft.Column([
                ft.Text(
                    "All Career Anchor Scores",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK
                ),
                ft.Text(
                    "Your scores across all 8 career anchors (maximum 25 points per anchor)",
                    size=13,
                    color=ft.Colors.GREY_700,
                    italic=True
                ),
                ft.Container(height=10),
                ft.Column(anchor_score_items, spacing=0),
            ]),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            margin=ft.Margin.only(bottom=20)
        )
        
        # Interpretation guide
        interpretation_container = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.LIGHTBULB_OUTLINE, size=28, color=ft.Colors.AMBER_700),
                    ft.Text(
                        "Understanding Your Results",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                ], spacing=10),
                ft.Divider(height=1, color=ft.Colors.GREY_300),
                ft.Text(
                    "Your highest-scoring area represents your primary career anchor — the value or motivation you are least willing to sacrifice. You may have one or two dominant anchors.",
                    size=14,
                    color=ft.Colors.BLACK87
                ),
                ft.Container(height=5),
                ft.Text(
                    "There are no 'right' or 'wrong' anchors. Recognising your anchor helps you choose work that aligns with who you are — and that's where long-term satisfaction comes from.",
                    size=14,
                    color=ft.Colors.BLACK87,
                    weight=ft.FontWeight.W_500
                ),
            ], spacing=10),
            bgcolor=ft.Colors.AMBER_50,
            padding=20,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.AMBER_200),
            margin=ft.Margin.only(bottom=20)
        )
        
        # Reset button
        def on_reset_clicked(e):
            """Handle reset button click."""
            assessment.reset()
            current_anchor_index[0] = 0
            container.content = build_assessment_content()
            container.update()
        
        reset_button = ft.Button(
            "Reset Assessment",
            icon=ft.Icons.REFRESH,
            on_click=on_reset_clicked,
            bgcolor=ft.Colors.ORANGE_700,
            color=ft.Colors.WHITE,
        )
        
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
                            "Your Values-Driven Career Framework",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK
                        ),
                        ft.Container(height=8),
                        ft.Text(
                            "Your career anchors reveal what truly matters to you in work and life. "
                            "These core values act as your internal compass for making career decisions with confidence.",
                            size=14,
                            color=ft.Colors.GREY_800,
                        ),
                        ft.Container(height=12),
                        ft.Row([
                            ft.Icon(ft.Icons.TIPS_AND_UPDATES, size=20, color=ft.Colors.DEEP_PURPLE_600),
                            ft.Text(
                                "Career Decision Strategy:",
                                size=14,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.DEEP_PURPLE_700
                            ),
                        ], spacing=8),
                        ft.Text(
                            "Use your strongest anchors as non-negotiable criteria when evaluating opportunities. "
                            "Career satisfaction comes from alignment between your values and your work environment. "
                            "When facing difficult decisions, return to these core priorities to guide your choice.",
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
            top_anchors_container,
            all_scores_container,
            interpretation_container,
            insight_container,
            ft.Row([
                reset_button,
            ], alignment=ft.MainAxisAlignment.CENTER),
        ], scroll=ft.ScrollMode.AUTO, expand=True)
    
    def build_assessment_content():
        """Build the main assessment content."""
        # Check if assessment is complete - if so, show results
        if assessment.is_complete():
            return create_results_page()
        
        # Show welcome page if starting
        if current_anchor_index[0] == 0 and not any(
            assessment.get_response(anchor_ids[0], i) is not None 
            for i in range(len(PrioritiesAssessment.ANCHORS[anchor_ids[0]]["questions"]))
        ):
            # Initial welcome screen
            def on_start(e):
                container.content = create_anchor_view(anchor_ids[0])
                container.update()
            
            welcome_screen = ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.ANCHOR, size=48, color=ft.Colors.BLUE_700),
                        ft.Text(
                            "Career Priorities Assessment",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK
                        ),
                        ft.Text(
                            "Discover what drives you at work using Edgar Schein's Career Anchors model",
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
                                f"You'll work through {len(PrioritiesAssessment.ANCHORS)} career anchors, each with 5 statements",
                                size=14,
                                color=ft.Colors.GREY_800,
                                expand=True
                            ),
                        ], spacing=10),
                        ft.Row([
                            ft.Icon(ft.Icons.LOOKS_TWO, size=24, color=ft.Colors.BLUE_700),
                            ft.Text(
                                "Rate each statement from 1-5 based on how accurately it describes you",
                                size=14,
                                color=ft.Colors.GREY_800,
                                expand=True
                            ),
                        ], spacing=10),
                        ft.Row([
                            ft.Icon(ft.Icons.LOOKS_3, size=24, color=ft.Colors.BLUE_700),
                            ft.Text(
                                "Use the scale: 5 = Very much like me, 3 = Somewhat like me, 1 = Not like me",
                                size=14,
                                color=ft.Colors.GREY_800,
                                expand=True
                            ),
                        ], spacing=10),
                        ft.Row([
                            ft.Icon(ft.Icons.LOOKS_4, size=24, color=ft.Colors.BLUE_700),
                            ft.Text(
                                "Discover your primary career anchor(s) and what motivates you most",
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
        
        # Show current anchor
        return create_anchor_view(anchor_ids[current_anchor_index[0]])
    
    # Build and set initial content
    container.content = build_assessment_content()
    
    return container


def create_priorities_page(page: ft.Page):
    """Entry point for creating the priorities assessment page."""
    return create_priorities_assessment_ui(page)

def _run_standalone(page: ft.Page):
    page.title = "CareerWise - Career Priorities"
    page.add(create_priorities_assessment_ui(page))
