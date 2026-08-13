"""
Job Search Skills Assessment - UI Layer
Flet UI construction and page wiring.
"""

import flet as ft

from skills_logic import SkillsAssessment, get_category_feedback, get_detailed_feedback

def create_skills_assessment_ui(page: ft.Page):
    """
    Create the Skills Assessment UI.
    
    Args:
        page: The Flet page object
        
    Returns:
        A container with the complete assessment UI
    """
    # Initialize the assessment logic
    assessment = SkillsAssessment()
    
    # Create the main container first
    container = ft.Container(
        content=ft.Text("Loading..."),
        padding=20,
        expand=True
    )
    
    # Track current section being viewed/edited
    current_section_index = [0]  # Use list to allow modification in nested functions
    section_ids = list(SkillsAssessment.CATEGORIES.keys())
    
    # References to UI elements that need updating
    next_button = None
    progress_text = None

    def get_status_color(status):
        """Get the color for a given status."""
        colors = {
            'good': ft.Colors.GREEN_700,
            'excellent': ft.Colors.GREEN_700,
            'acceptable': ft.Colors.AMBER_700,
            'needs_improvement': ft.Colors.RED_700,
            'incomplete': ft.Colors.GREY_600,
            'not_started': ft.Colors.GREY_400
        }
        return colors.get(status, ft.Colors.GREY_400)
    
    def get_status_text(status):
        """Get descriptive text for a status."""
        texts = {
            'good': '\u2713 Good',
            'excellent': '\u2713 Excellent',
            'acceptable': 'Acceptable',
            'needs_improvement': '\u26A0 Needs Improvement',
            'incomplete': 'Incomplete',
            'not_started': 'Not Started'
        }
        return texts.get(status, status)
    
    def update_section_total(section_id, do_update=True):
        """Update the section completion display."""
        answered = sum(1 for i in range(len(SkillsAssessment.CATEGORIES[section_id]["questions"])) 
                      if assessment.get_response(section_id, i) is not None)
        total = len(SkillsAssessment.CATEGORIES[section_id]["questions"])
        is_complete = answered == total
        
        # Update progress text
        if progress_text and do_update:
            progress_text.value = f"Answered: {answered}/{total} questions"
            if hasattr(page, 'update'):
                progress_text.update()
        
        # Update next button state
        if next_button and do_update:
            next_button.disabled = not is_complete
            next_button.bgcolor = ft.Colors.BLUE_700 if is_complete else ft.Colors.GREY_300
            if hasattr(page, 'update'):
                next_button.update()
    
    def on_rating_changed(section_id, question_index, rating):
        """Handle when user changes rating."""
        assessment.set_response(section_id, question_index, rating)
        update_section_total(section_id)
    
    def create_question_row(section_id, question_index, question_text):
        """Create a row for a single question with 1-5 rating scale."""
        current_value = assessment.get_response(section_id, question_index)
        
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
        section_number = list(SkillsAssessment.CATEGORIES.keys()).index(section_id) + 1
        section = SkillsAssessment.CATEGORIES[section_id]
        is_last_section = section_number == len(SkillsAssessment.CATEGORIES)
        
        # Header
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.PSYCHOLOGY, size=28, color=ft.Colors.BLUE_700),
                    ft.Text(
                        f"Section {section_number} of {len(SkillsAssessment.CATEGORIES)}",
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
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            margin=ft.Margin.only(bottom=20)
        )
        
        # Questions container
        question_rows = []
        for i, question_text in enumerate(section["questions"]):
            question_rows.append(create_question_row(section_id, i, question_text))
        
        questions_container = ft.Container(
            content=ft.Column(question_rows, spacing=0),
            bgcolor=ft.Colors.WHITE,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            margin=ft.Margin.only(bottom=20)
        )
        
        # Section total
        answered = sum(1 for i in range(len(section["questions"])) 
                      if assessment.get_response(section_id, i) is not None)
        total = len(section["questions"])
        
        # Create progress text reference for updates
        nonlocal progress_text
        progress_text = ft.Text(
            f"Answered: {answered}/{total} questions",
            size=14,
            color=ft.Colors.GREY_700,
            weight=ft.FontWeight.BOLD
        )
        
        total_container = ft.Container(
            content=progress_text,
            padding=10,
            margin=ft.Margin.only(bottom=20)
        )
        
        # Navigation
        def on_prev(e):
            if current_section_index[0] > 0:
                current_section_index[0] -= 1
                container.content = build_assessment_content()
                container.update()
        
        def on_next(e):
            is_complete = all(assessment.get_response(section_id, i) is not None 
                            for i in range(len(section["questions"])))
            if is_complete:
                if current_section_index[0] < len(section_ids) - 1:
                    current_section_index[0] += 1
                    container.content = build_assessment_content()
                    container.update()
                elif assessment.is_complete():
                    # All sections complete, show results
                    container.content = create_results_page()
                    container.update()
        
        prev_button = ft.Button(
            "Previous Section",
            icon=ft.Icons.ARROW_BACK,
            on_click=on_prev,
            disabled=section_number == 1,
            bgcolor=ft.Colors.GREY_300 if section_number == 1 else ft.Colors.BLUE_700,
            color=ft.Colors.WHITE,
        )
        
        next_button_text = "View Results" if is_last_section else "Next Section"
        is_section_complete = all(assessment.get_response(section_id, i) is not None 
                                for i in range(len(section["questions"])))
        
        # Store reference to next button for updates
        nonlocal next_button
        next_button = ft.Button(
            next_button_text,
            icon=ft.Icons.ARROW_FORWARD if not is_last_section else ft.Icons.EMOJI_EVENTS,
            on_click=on_next,
            disabled=not is_section_complete,
            bgcolor=ft.Colors.BLUE_700 if is_section_complete else ft.Colors.GREY_300,
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
        """Create the results page showing scores and recommendations."""
        # Calculate scores
        total_score, max_total, completion = assessment.calculate_overall_score()
        overall_status = assessment.get_overall_status()
        
        # Title
        title_container = ft.Container(
            content=ft.Text(
                "Job Search Skills Assessment Results",
                size=24,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLACK
            ),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=10,
            margin=ft.Margin.only(bottom=20)
        )
        
        # Overall score summary
        overall_card = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.PSYCHOLOGY, size=32, color=ft.Colors.BLUE_700),
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
                            f"Total Score: {total_score:.1f}/{max_total}",
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
            ], spacing=10),
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            margin=ft.Margin.only(bottom=20)
        )
        
        # Category scores
        category_cards = []
        for category_id in SkillsAssessment.CATEGORIES:
            category = SkillsAssessment.CATEGORIES[category_id]
            score, max_possible, answered, total = assessment.calculate_category_score(category_id)
            status = assessment.get_category_status(category_id)
            feedback = get_category_feedback(category_id, status)
            
            category_card = ft.Container(
                content=ft.Column([
                    ft.Text(
                        category["title"],
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                    ft.Row([
                        ft.Text(
                            f"Score: {score:.1f}/{max_possible}",
                            size=14,
                            color=ft.Colors.GREY_700
                        ),
                        ft.Container(expand=True),
                        ft.Text(
                            get_status_text(status),
                            size=14,
                            weight=ft.FontWeight.BOLD,
                            color=get_status_color(status)
                        ),
                    ]),
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    ft.Container(
                        content=ft.Text(
                            feedback,
                            size=13,
                            color=ft.Colors.GREY_800,
                            weight=ft.FontWeight.W_400,
                        ),
                        padding=ft.Padding.only(left=10, right=10, top=5, bottom=5),
                        bgcolor=ft.Colors.BLUE_50,
                        border_radius=8,
                        border=ft.Border.all(1, ft.Colors.BLUE_200),
                    ),
                ], spacing=8),
                bgcolor=ft.Colors.WHITE,
                padding=15,
                border_radius=10,
                border=ft.Border.all(1, ft.Colors.GREY_300),
                margin=ft.Margin.only(bottom=10)
            )
            category_cards.append(category_card)
        
        # Build detailed advice section
        detailed_advice_items = []
        
        for category_id in SkillsAssessment.CATEGORIES:
            category = SkillsAssessment.CATEGORIES[category_id]
            questions = category["questions"]
            
            # Category header
            category_header = ft.Container(
                content=ft.Text(
                    category["title"].upper(),
                    size=15,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_700
                ),
                margin=ft.Margin.only(top=15, bottom=10)
            )
            detailed_advice_items.append(category_header)
            
            # Question feedback for each question in this category
            for question_index, question_text in enumerate(questions):
                rating = assessment.get_response(category_id, question_index)
                
                if rating:
                    # Get the detailed feedback for this specific question and rating
                    feedback_text = get_detailed_feedback(category_id, question_index, rating)
                    
                    # Create visual indicator based on rating
                    def get_rating_color(r):
                        if r >= 4:
                            return ft.Colors.GREEN_700
                        elif r == 3:
                            return ft.Colors.AMBER_700
                        else:
                            return ft.Colors.RED_700
                    
                    def get_rating_icon(r):
                        if r >= 4:
                            return ft.Icons.THUMB_UP
                        elif r == 3:
                            return ft.Icons.HORIZONTAL_RULE
                        else:
                            return ft.Icons.THUMB_DOWN
                    
                    question_feedback = ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(
                                    get_rating_icon(rating),
                                    size=20,
                                    color=get_rating_color(rating)
                                ),
                                ft.Text(
                                    f"Rating: {rating}/5",
                                    size=13,
                                    weight=ft.FontWeight.BOLD,
                                    color=get_rating_color(rating)
                                ),
                            ], spacing=8),
                            ft.Text(
                                question_text,
                                size=13,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK,
                                italic=True
                            ),
                            ft.Container(height=5),
                            ft.Text(
                                feedback_text,
                                size=13,
                                color=ft.Colors.GREY_800,
                            ),
                        ], spacing=5),
                        bgcolor=ft.Colors.GREY_50,
                        padding=12,
                        border_radius=8,
                        border=ft.Border.all(1, ft.Colors.GREY_300),
                        margin=ft.Margin.only(bottom=8)
                    )
                    detailed_advice_items.append(question_feedback)
        
        # Reset button
        def on_reset_clicked(e):
            """Handle reset button click."""
            assessment.reset()
            current_section_index[0] = 0
            container.content = build_assessment_content()
            container.update()
        
        reset_button = ft.Button(
            "Reset Assessment",
            icon=ft.Icons.REFRESH,
            on_click=on_reset_clicked,
            bgcolor=ft.Colors.ORANGE_700,
            color=ft.Colors.WHITE,
        )
        
        return ft.Column([
            title_container,
            overall_card,
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Category Breakdown",
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
            # Detailed advice section
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.LIGHTBULB_OUTLINE, size=28, color=ft.Colors.AMBER_700),
                        ft.Text(
                            "Your Detailed Advice",
                            size=20,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK
                        ),
                    ], spacing=10),
                    ft.Divider(height=1, color=ft.Colors.GREY_300),
                    ft.Text(
                        "Personalized recommendations for each question based on your responses:",
                        size=14,
                        color=ft.Colors.GREY_700,
                        italic=True
                    ),
                    *detailed_advice_items,
                ], spacing=5),
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
                                "Your Job Search Success Framework",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK
                            ),
                            ft.Container(height=8),
                            ft.Text(
                                "This assessment covers the 6 essential pillars of effective job searching. "
                                "Your strongest areas represent competitive advantages to leverage, while areas "
                                "needing improvement offer the highest potential for transforming your job search results.",
                                size=14,
                                color=ft.Colors.GREY_800,
                            ),
                            ft.Container(height=12),
                            ft.Row([
                                ft.Icon(ft.Icons.TIPS_AND_UPDATES, size=20, color=ft.Colors.DEEP_PURPLE_600),
                                ft.Text(
                                    "Key Success Principle:",
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.DEEP_PURPLE_700
                                ),
                            ], spacing=8),
                            ft.Text(
                                "Job searching is a systematic skill that can be learned and improved. "
                                "Focus on strengthening your weakest category first - it will yield the "
                                "greatest improvement in overall results. Remember: 70% of jobs come "
                                "through networking, not job boards. Combine strong fundamentals "
                                "(CV, interview skills) with strategic relationship building for optimal outcomes.",
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
                reset_button,
            ], alignment=ft.MainAxisAlignment.CENTER),
        ], scroll=ft.ScrollMode.AUTO, expand=True)
    
    def build_assessment_content():
        """Build the main assessment content."""
        # Check if assessment is complete - if so, show results
        if assessment.is_complete():
            return create_results_page()
        
        # Show welcome page if starting
        if current_section_index[0] == 0 and not any(
            assessment.get_response(section_ids[0], i) is not None 
            for i in range(len(SkillsAssessment.CATEGORIES[section_ids[0]]["questions"]))
        ):
            # Initial welcome screen
            def on_start(e):
                container.content = create_section_view(section_ids[0])
                container.update()
            
            welcome_screen = ft.Column([
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.PSYCHOLOGY, size=48, color=ft.Colors.BLUE_700),
                        ft.Text(
                            "Job Search Skills Assessment",
                            size=28,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLACK
                        ),
                        ft.Text(
                            "Evaluate your job search skills and identify areas for improvement",
                            size=16,
                            color=ft.Colors.GREY_700,
                            text_align=ft.TextAlign.CENTER
                        ),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                    padding=30,
                    bgcolor=ft.Colors.BLUE_50,
                    border_radius=10,
                    margin=ft.Margin.only(bottom=20)
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
                                f"You'll work through {len(SkillsAssessment.CATEGORIES)} categories of job search skills",
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
                                "Use the scale: 5 = Strongly Agree, 4 = Agree, 3 = Neutral, 2 = Disagree, 1 = Strongly Disagree",
                                size=14,
                                color=ft.Colors.GREY_800,
                                expand=True
                            ),
                        ], spacing=10),
                        ft.Row([
                            ft.Icon(ft.Icons.LOOKS_4, size=24, color=ft.Colors.BLUE_700),
                            ft.Text(
                                "Get personalized feedback on your strengths and areas to improve",
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
        return create_section_view(section_ids[current_section_index[0]])
    
    # Build and set initial content
    container.content = build_assessment_content()
    
    return container


def create_skills_page(page: ft.Page):
    """Entry point for creating the skills assessment page."""
    return create_skills_assessment_ui(page)

def _run_standalone(page: ft.Page):
    page.title = "CareerWise - Job Search Skills"
    page.add(create_skills_assessment_ui(page))


if __name__ == "__main__":
    ft.app(target=_run_standalone)

