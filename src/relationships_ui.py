"""
Relationships Assessment - UI Layer
Flet UI construction and page wiring.
"""

import flet as ft

from relationships_logic import RelationshipsAssessment


def create_relationships_assessment_ui(page: ft.Page):
    """
    Create the Relationships Assessment UI with reflection cards.
    
    Args:
        page: The Flet page object
        
    Returns:
        A container with the complete assessment UI
    """
    # Initialize the assessment logic
    assessment = RelationshipsAssessment()
    
    # Create the main container
    container = ft.Container(
        content=ft.Text("Loading..."),
        padding=20,
        expand=True
    )
    
    # Track current view
    current_view = ['welcome']  # 'welcome', 'selector', 'reflection', 'results'
    current_relationship_index = [None]
    
    # Validation feedback controls
    error_banner = ft.Banner(
        bgcolor=ft.Colors.RED_100,
        leading=ft.Icon(ft.Icons.ERROR_OUTLINE, color=ft.Colors.RED_700, size=40),
        content=ft.Text("", color=ft.Colors.RED_900),
        actions=[
            ft.TextButton("Close", on_click=lambda e: setattr(error_banner, 'open', False) or page.update()),
        ],
    )
    
    warning_banner = ft.Banner(
        bgcolor=ft.Colors.ORANGE_100,
        leading=ft.Icon(ft.Icons.WARNING_OUTLINED, color=ft.Colors.ORANGE_700, size=40),
        content=ft.Text("", color=ft.Colors.ORANGE_900),
        actions=[
            ft.TextButton("Close", on_click=lambda e: setattr(warning_banner, 'open', False) or page.update()),
        ],
    )
    
    page.overlay.extend([error_banner, warning_banner])
    
    def show_error_dialog(message):
        """Show an error message."""
        error_banner.content.value = message
        error_banner.open = True
        page.update()
    
    def show_warning_dialog(message):
        """Show a warning message."""
        warning_banner.content.value = message
        warning_banner.open = True
        page.update()
    
    def show_balance_warning():
        """Check and show balance warning if needed."""
        warning = assessment.get_balance_warning()
        if warning:
            show_warning_dialog(warning)
    
    def build_welcome_screen():
        """Build the welcome/introduction screen."""
        def on_start(e):
            current_view[0] = 'selector'
            container.content = build_selector_screen()
            container.update()
        
        return ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.PEOPLE, size=48, color=ft.Colors.BLUE_700),
                    ft.Text(
                        "Past Relationships Review",
                        size=28,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                    ft.Text(
                        "Discover what your past work relationships reveal about your values and collaboration patterns",
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
                        "Purpose",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                    ft.Text(
                        "This reflection helps you understand what kinds of people and environments bring out your best—and which patterns of interaction tend to create frustration. By exploring a few key relationships, you'll uncover the values, boundaries, and expectations that shape how you connect and collaborate at work.",
                        size=14,
                        color=ft.Colors.GREY_700
                    ),
                ], spacing=10),
                bgcolor=ft.Colors.WHITE,
                padding=20,
                border_radius=10,
                border=ft.Border.all(1, ft.Colors.GREY_300),
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
                            "Choose up to 6 significant working relationships (at least 1 positive and 1 challenging)",
                            size=14,
                            color=ft.Colors.GREY_800,
                            expand=True
                        ),
                    ], spacing=10),
                    ft.Row([
                        ft.Icon(ft.Icons.LOOKS_TWO, size=24, color=ft.Colors.BLUE_700),
                        ft.Text(
                            "Reflect on each relationship through 5 guided prompts",
                            size=14,
                            color=ft.Colors.GREY_800,
                            expand=True
                        ),
                    ], spacing=10),
                    ft.Row([
                        ft.Icon(ft.Icons.LOOKS_3, size=24, color=ft.Colors.BLUE_700),
                        ft.Text(
                            "Write freely about your experiences and observations",
                            size=14,
                            color=ft.Colors.GREY_800,
                            expand=True
                        ),
                    ], spacing=10),
                    ft.Row([
                        ft.Icon(ft.Icons.LOOKS_4, size=24, color=ft.Colors.BLUE_700),
                        ft.Text(
                            "Discover your core relational values through pattern analysis",
                            size=14,
                            color=ft.Colors.GREY_800,
                            expand=True
                        ),
                    ], spacing=10),
                    ft.Container(height=10),
                    ft.Container(
                        content=ft.Text(
                            "Minimum Required: At least 1 positive and 1 challenging relationship to view results",
                            size=13,
                            color=ft.Colors.ORANGE_800,
                            italic=True,
                            weight=ft.FontWeight.BOLD
                        ),
                        bgcolor=ft.Colors.ORANGE_50,
                        padding=10,
                        border_radius=5,
                    ),
                ], spacing=12),
                padding=20,
                bgcolor=ft.Colors.WHITE,
                border_radius=10,
                border=ft.Border.all(1, ft.Colors.GREY_300),
                margin=ft.Margin.only(bottom=20)
            ),
            
            ft.Row([
                ft.Button(
                    "Begin Reflection",
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
        ], scroll=ft.ScrollMode.AUTO, expand=True)
    
    def create_relationship_card(index):
        """Create a card for a relationship."""
        relationship = assessment.relationships[index]
        is_complete = assessment.is_relationship_complete(index)
        completed, total = assessment.get_relationship_progress(index)
        
        # Card color based on type
        card_color = ft.Colors.GREEN_50 if relationship['type'] == 'positive' else ft.Colors.ORANGE_50
        icon = ft.Icons.THUMB_UP if relationship['type'] == 'positive' else ft.Icons.WARNING
        icon_color = ft.Colors.GREEN_700 if relationship['type'] == 'positive' else ft.Colors.ORANGE_700
        
        def on_card_click(e):
            current_relationship_index[0] = index
            current_view[0] = 'reflection'
            container.content = build_reflection_screen(index)
            container.update()
        
        def on_delete(e):
            e.control.disabled = True
            assessment.remove_relationship(index)
            current_view[0] = 'selector'
            container.content = build_selector_screen()
            container.update()
        
        return ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(icon, size=20, color=icon_color),
                    ft.Text(
                        relationship['name'],
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK,
                        expand=True
                    ),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_size=18,
                        on_click=on_delete,
                        tooltip="Delete relationship"
                    ),
                ], spacing=10),
                ft.Text(
                    relationship['type'].capitalize(),
                    size=12,
                    color=ft.Colors.GREY_600,
                    italic=True
                ),
                ft.Container(height=5),
                ft.Row([
                    ft.Text(
                        f"Progress: {completed}/{total}",
                        size=13,
                        color=ft.Colors.GREY_700
                    ),
                    ft.Container(expand=True),
                    ft.Text(
                        "Click to edit" if not is_complete else "Click to view",
                        size=12,
                        color=ft.Colors.BLUE_700,
                        italic=True,
                    ),
                    ft.Container(width=5),
                    ft.Icon(
                        ft.Icons.CHECK_CIRCLE if is_complete else ft.Icons.RADIO_BUTTON_UNCHECKED,
                        size=16,
                        color=ft.Colors.GREEN_700 if is_complete else ft.Colors.GREY_400
                    ),
                ]),
            ], spacing=8),
            bgcolor=card_color,
            padding=15,
            border_radius=10,
            border=ft.Border.all(2, icon_color if is_complete else ft.Colors.GREY_300),
            on_click=on_card_click,
            ink=True,
        )
    
    def build_selector_screen():
        """Build the relationship selector screen."""
        status = assessment.get_completion_status()
        
        # Create cards for existing relationships
        relationship_cards = []
        for i in range(assessment.get_total_relationships()):
            relationship_cards.append(create_relationship_card(i))
        
        # Add new relationship section
        def on_add_positive(e):
            try:
                # Check if can add more relationships
                can_add, msg = assessment.can_add_relationship('positive')
                if not can_add:
                    show_error_dialog(msg)
                    return
                
                name = f"Positive Relationship {assessment.get_positive_count() + 1}"
                assessment.add_relationship(name, 'positive')
                
                # Show balance warning if needed
                balance_warning = assessment.get_balance_warning()
                if balance_warning:
                    show_balance_warning(balance_warning)
                
                current_view[0] = 'selector'
                container.content = build_selector_screen()
                container.update()
            except ValueError as ex:
                show_error_dialog(str(ex))
        
        def on_add_challenging(e):
            try:
                # Check if can add more relationships
                can_add, msg = assessment.can_add_relationship('challenging')
                if not can_add:
                    show_error_dialog(msg)
                    return
                
                name = f"Challenging Relationship {assessment.get_challenging_count() + 1}"
                assessment.add_relationship(name, 'challenging')
                
                # Show balance warning if needed
                balance_warning = assessment.get_balance_warning()
                if balance_warning:
                    show_balance_warning(balance_warning)
                
                current_view[0] = 'selector'
                container.content = build_selector_screen()
                container.update()
            except ValueError as ex:
                show_error_dialog(str(ex))
        
        def on_view_results(e):
            if assessment.can_view_results():
                current_view[0] = 'results'
                container.content = build_results_screen()
                container.update()
        
        # Header
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.PEOPLE, size=28, color=ft.Colors.BLUE_700),
                    ft.Text(
                        "Your Relationships",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                ], spacing=10),
                ft.Text(
                    "Add and reflect on your working relationships",
                    size=14,
                    color=ft.Colors.GREY_700
                ),
            ], spacing=5),
            bgcolor=ft.Colors.BLUE_50,
            padding=20,
            border_radius=10,
            margin=ft.Margin.only(bottom=20)
        )
        
        # Progress indicator
        progress_text = []
        if status['positive_needed'] > 0:
            progress_text.append(f"Complete {status['positive_needed']} positive relationship(s)")
        if status['challenging_needed'] > 0:
            progress_text.append(f"Complete {status['challenging_needed']} challenging relationship(s)")
        
        progress_message = " and ".join(progress_text) if progress_text else "Requirements met! Complete reflections to view results."
        
        progress_container = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Progress to Results",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK
                ),
                ft.Text(
                    progress_message,
                    size=14,
                    color=ft.Colors.ORANGE_800 if progress_text else ft.Colors.GREEN_700
                ),
                ft.Container(height=5),
                ft.Text(
                    f"Positive: {status['positive_complete']}/1 complete  |  Challenging: {status['challenging_complete']}/1 complete",
                    size=13,
                    color=ft.Colors.GREY_700
                ),
            ], spacing=8),
            bgcolor=ft.Colors.ORANGE_50 if progress_text else ft.Colors.GREEN_50,
            padding=15,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.ORANGE_300 if progress_text else ft.Colors.GREEN_300),
            margin=ft.Margin.only(bottom=20)
        )
        
        # Relationship cards grid
        cards_section = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Your Relationships",
                    size=18,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK
                ),
                ft.Container(height=10),
                ft.Column(relationship_cards, spacing=10) if relationship_cards else ft.Text(
                    "No relationships added yet. Start by adding a positive or challenging relationship below.",
                    size=14,
                    color=ft.Colors.GREY_600,
                    italic=True
                ),
            ], spacing=0),
            margin=ft.Margin.only(bottom=20)
        )

        can_add_positive, positive_msg = assessment.can_add_relationship('positive')
        can_add_challenging, challenging_msg = assessment.can_add_relationship('challenging')
        
        # Add buttons
        add_buttons = ft.Row([
            ft.Button(
                "Add Positive Relationship",
                icon=ft.Icons.ADD,
                on_click=on_add_positive,
                bgcolor=ft.Colors.GREEN_700,
                color=ft.Colors.WHITE,
                disabled=not can_add_positive,
                tooltip=positive_msg if not can_add_positive else None
            ),
            ft.Button(
                "Add Challenging Relationship",
                icon=ft.Icons.ADD,
                on_click=on_add_challenging,
                bgcolor=ft.Colors.ORANGE_700,
                color=ft.Colors.WHITE,
                disabled=not can_add_challenging,
                tooltip=challenging_msg if not can_add_challenging else None
            ),
        ], spacing=10, wrap=True)
        
        # View results button
        results_button = ft.Row([
            ft.Button(
                "View Results",
                icon=ft.Icons.EMOJI_EVENTS,
                on_click=on_view_results,
                bgcolor=ft.Colors.BLUE_700 if status['can_view_results'] else ft.Colors.GREY_300,
                color=ft.Colors.WHITE,
                disabled=not status['can_view_results'],
                height=50,
                style=ft.ButtonStyle(
                    text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
                ),
            ),
        ], alignment=ft.MainAxisAlignment.CENTER)
        
        return ft.Column([
            header,
            progress_container,
            cards_section,
            add_buttons,
            ft.Container(height=10),
            results_button,
        ], scroll=ft.ScrollMode.AUTO, expand=True)
    
    def build_reflection_screen(relationship_index):
        """Build the reflection screen for a specific relationship."""
        relationship = assessment.relationships[relationship_index]
        prompts = RelationshipsAssessment.POSITIVE_PROMPTS if relationship['type'] == 'positive' else RelationshipsAssessment.CHALLENGING_PROMPTS
        
        # Header
        icon = ft.Icons.THUMB_UP if relationship['type'] == 'positive' else ft.Icons.WARNING
        icon_color = ft.Colors.GREEN_700 if relationship['type'] == 'positive' else ft.Colors.ORANGE_700
        
        # Name edit field with validation
        def on_name_change(e):
            try:
                assessment.update_relationship_name(relationship_index, e.control.value)
                e.control.error_text = None
                e.control.update()
            except ValueError as ex:
                e.control.error_text = str(ex)
                e.control.update()
        
        name_field = ft.TextField(
            value=relationship['name'],
            label="Relationship Name",
            border_color=icon_color,
            on_change=on_name_change,
            on_blur=on_name_change
        )
        
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(icon, size=28, color=icon_color),
                    ft.Text(
                        f"Reflecting on: {relationship['type'].capitalize()} Relationship",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                ], spacing=10),
                name_field,
            ], spacing=10),
            bgcolor=ft.Colors.GREEN_50 if relationship['type'] == 'positive' else ft.Colors.ORANGE_50,
            padding=20,
            border_radius=10,
            margin=ft.Margin.only(bottom=20)
        )
        
        # Create reflection prompt fields with validation
        reflection_fields = []
        
        def create_reflection_field(idx, prompt):
            """Create a validated reflection text field."""
            current_text = assessment.get_reflection(relationship_index, idx)
            
            def on_reflection_change(e):
                text = e.control.value
                assessment.set_reflection(relationship_index, idx, text)
                e.control.update()
            
            def on_reflection_blur(e):
                text = e.control.value
                is_valid, error, warning = assessment.validate_reflection_text(
                    text, 
                    relationship['type']
                )
                
                if text.strip():  # Only show errors if user has entered something
                    if not is_valid:
                        e.control.error_text = error
                    else:
                        e.control.error_text = None
                        if warning:
                            show_warning_dialog(warning)
                else:
                    e.control.error_text = None
                
                e.control.update()
            
            text_field = ft.TextField(
                label=f"Prompt {idx+1}",
                value=current_text,
                multiline=True,
                min_lines=3,
                max_lines=8,
                hint_text=prompt,
                border_color=ft.Colors.BLUE_300,
                on_change=on_reflection_change,
                on_blur=on_reflection_blur,
                helper="Minimum 50 characters"
            )
            
            return ft.Container(
                content=ft.Column([
                    ft.Text(
                        prompt,
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                    text_field,
                ], spacing=8),
                bgcolor=ft.Colors.WHITE,
                padding=15,
                border_radius=10,
                border=ft.Border.all(1, ft.Colors.GREY_300),
                margin=ft.Margin.only(bottom=15)
            )
        
        for i, prompt in enumerate(prompts):
            reflection_fields.append(create_reflection_field(i, prompt))
        
        # Progress indicator
        completed, total = assessment.get_relationship_progress(relationship_index)
        progress = ft.Container(
            content=ft.Row([
                ft.Icon(
                    ft.Icons.CHECK_CIRCLE if completed == total else ft.Icons.RADIO_BUTTON_UNCHECKED,
                    size=20,
                    color=ft.Colors.GREEN_700 if completed == total else ft.Colors.GREY_400
                ),
                ft.Text(
                    f"Progress: {completed}/{total} prompts completed",
                    size=14,
                    color=ft.Colors.GREY_700,
                    weight=ft.FontWeight.BOLD
                ),
            ], spacing=10),
            padding=10,
            margin=ft.Margin.only(bottom=20)
        )
        
        # Back button with validation
        def on_back(e):
            # Validate all required fields before allowing navigation
            relationship = assessment.relationships[relationship_index]
            
            # Check name
            if not relationship['name'].strip():
                show_error_dialog("Please enter a name for this relationship before continuing.")
                return
            
            # Validate name
            is_valid, error_msg = assessment.validate_relationship_name(
                relationship['name'], 
                exclude_index=relationship_index
            )
            if not is_valid:
                show_error_dialog(error_msg)
                return
            
            # Check reflections (at least one should be filled and valid)
            has_content = False
            errors = []
            
            # Reflections are stored as a dictionary with prompt_index as keys
            for prompt_index, reflection in relationship['reflections'].items():
                # Convert to string if needed (handles both string and int)
                reflection_text = str(reflection) if reflection else ""
                
                # Only validate if there's content
                if reflection_text.strip():
                    is_valid, error, warning = assessment.validate_reflection_text(
                        reflection_text,
                        relationship['type']
                    )
                    if is_valid:
                        has_content = True
                    else:
                        errors.append(f"Prompt {prompt_index+1}: {error}")
            
            if not has_content:
                show_error_dialog("Please complete at least one reflection prompt before continuing.")
                return
            
            if errors:
                show_error_dialog("Please fix the following issues:\n\n" + "\n".join(errors))
                return
            
            # Show balance warning if needed
            balance_warning = assessment.get_balance_warning()
            if balance_warning:
                show_balance_warning(balance_warning)
            
            # Navigation successful
            current_view[0] = 'selector'
            container.content = build_selector_screen()
            container.update()
        
        back_button = ft.Button(
            "Back to Relationships",
            icon=ft.Icons.ARROW_BACK,
            on_click=on_back,
            bgcolor=ft.Colors.GREY_700,
            color=ft.Colors.WHITE,
        )
        
        return ft.Column([
            header,
            progress,
            *reflection_fields,
            back_button,
        ], scroll=ft.ScrollMode.AUTO, expand=True)
    
    def build_results_screen():
        """Build the results screen with pattern analysis."""
        # Run analysis
        analysis = assessment.analyze_patterns()
        values = analysis['values']
        frustrations = analysis['frustrations']
        summary = assessment.generate_summary(analysis)
        
        # Header
        header = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.EMOJI_EVENTS, size=32, color=ft.Colors.BLUE_700),
                    ft.Text(
                        "Your Relational Values and Frustrations",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                ], spacing=10),
            ], spacing=5),
            bgcolor=ft.Colors.BLUE_50,
            padding=20,
            border_radius=10,
            margin=ft.Margin.only(bottom=20)
        )
        
        # Introduction
        intro = ft.Container(
            content=ft.Text(
                "Based on your reflections, we've identified the values you appreciate most and the traits that frustrate you. These patterns reveal the conditions that help you build trust, perform well, and stay motivated.",
                size=14,
                color=ft.Colors.GREY_700
            ),
            bgcolor=ft.Colors.WHITE,
            padding=15,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            margin=ft.Margin.only(bottom=20)
        )
        
        # Top themes
        top_theme_cards = []
        for i, theme_id in enumerate(values['top_themes']):
            theme = RelationshipsAssessment.THEMES[theme_id]
            score = values['theme_scores'][theme_id]
            
            top_theme_cards.append(
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(
                                f"{i+1}",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_700,
                                width=40
                            ),
                            ft.Column([
                                ft.Text(
                                    theme['title'],
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLACK
                                ),
                                ft.Text(
                                    theme['description'],
                                    size=14,
                                    color=ft.Colors.GREY_700
                                ),
                                ft.Text(
                                    f"Mentions: {int(score)}",
                                    size=12,
                                    color=ft.Colors.GREY_600,
                                    italic=True
                                ),
                            ], expand=True, spacing=5),
                        ], spacing=10),
                    ], spacing=8),
                    bgcolor=ft.Colors.WHITE,
                    padding=20,
                    border_radius=10,
                    border=ft.Border.all(2, ft.Colors.BLUE_700 if i == 0 else ft.Colors.GREY_300),
                    margin=ft.Margin.only(bottom=15)
                )
            )

        if top_theme_cards:
            values_block = [
                ft.Container(
                    content=ft.Text(
                        "Your Top Values",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK,
                    ),
                    margin=ft.Margin.only(bottom=10),
                ),
                *top_theme_cards,
            ]
        else:
            values_block = [
                ft.Container(
                    content=ft.Text(
                        "Your Top Values",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK,
                    ),
                    margin=ft.Margin.only(bottom=10),
                ),
                ft.Container(
                    content=ft.Text(
                        "Add more specific detail in positive reflections to surface relational values.",
                        size=13,
                        color=ft.Colors.GREY_600,
                        italic=True,
                    ),
                    bgcolor=ft.Colors.BLUE_50,
                    padding=15,
                    border_radius=10,
                    border=ft.Border.all(1, ft.Colors.BLUE_200),
                    margin=ft.Margin.only(bottom=15),
                ),
            ]

        # Frustrating traits
        frustration_cards = []
        for i, theme_id in enumerate(frustrations['top_themes']):
            theme = RelationshipsAssessment.FRUSTRATION_THEMES[theme_id]
            score = frustrations['theme_scores'][theme_id]

            frustration_cards.append(
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(
                                f"{i+1}",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.ORANGE_700,
                                width=40
                            ),
                            ft.Column([
                                ft.Text(
                                    theme['title'],
                                    size=18,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLACK
                                ),
                                ft.Text(
                                    theme['description'],
                                    size=14,
                                    color=ft.Colors.GREY_700
                                ),
                                ft.Text(
                                    f"Mentions: {int(score)}",
                                    size=12,
                                    color=ft.Colors.GREY_600,
                                    italic=True
                                ),
                            ], expand=True, spacing=5),
                        ], spacing=10),
                    ], spacing=8),
                    bgcolor=ft.Colors.WHITE,
                    padding=20,
                    border_radius=10,
                    border=ft.Border.all(2, ft.Colors.ORANGE_700 if i == 0 else ft.Colors.GREY_300),
                    margin=ft.Margin.only(bottom=15)
                )
            )

        if frustration_cards:
            frustrations_block = [
                ft.Container(
                    content=ft.Text(
                        "Common Frustrations",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK,
                    ),
                    margin=ft.Margin.only(bottom=10)
                ),
                *frustration_cards,
            ]
        else:
            frustrations_block = [
                ft.Container(
                    content=ft.Text(
                        "Common Frustrations",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK,
                    ),
                    margin=ft.Margin.only(bottom=10)
                ),
                ft.Container(
                    content=ft.Text(
                        "Add more detail in challenging reflections to surface frustrating traits.",
                        size=13,
                        color=ft.Colors.GREY_600,
                        italic=True
                    ),
                    bgcolor=ft.Colors.ORANGE_50,
                    padding=15,
                    border_radius=10,
                    border=ft.Border.all(1, ft.Colors.ORANGE_200),
                    margin=ft.Margin.only(bottom=15)
                ),
            ]
        
        # Summary
        summary_container = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.LIGHTBULB, size=24, color=ft.Colors.AMBER_700),
                    ft.Text(
                        "What This Suggests",
                        size=18,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK
                    ),
                ], spacing=10),
                ft.Container(height=10),
                ft.Text(
                    summary,
                    size=14,
                    color=ft.Colors.GREY_800
                ),
            ], spacing=0),
            bgcolor=ft.Colors.AMBER_50,
            padding=20,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.AMBER_300),
            margin=ft.Margin.only(bottom=20)
        )
        
        # Closing reflection prompt
        closing_prompt = ft.Container(
            content=ft.Column([
                ft.Text(
                    "Reflection Question",
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLACK
                ),
                ft.Text(
                    "Based on these insights, what can you do to build more of your best-relationship conditions into your current or future roles?",
                    size=14,
                    color=ft.Colors.GREY_700,
                    italic=True
                ),
            ], spacing=8),
            bgcolor=ft.Colors.WHITE,
            padding=15,
            border_radius=10,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            margin=ft.Margin.only(bottom=20)
        )
        
        # Navigation buttons
        def on_back_to_relationships(e):
            current_view[0] = 'selector'
            container.content = build_selector_screen()
            container.update()
        
        def on_reset(e):
            assessment.reset()
            current_view[0] = 'welcome'
            container.content = build_welcome_screen()
            container.update()
        
        nav_buttons = ft.Row([
            ft.Button(
                "Back to Relationships",
                icon=ft.Icons.ARROW_BACK,
                on_click=on_back_to_relationships,
                bgcolor=ft.Colors.GREY_700,
                color=ft.Colors.WHITE,
            ),
            ft.Button(
                "Start Over",
                icon=ft.Icons.REFRESH,
                on_click=on_reset,
                bgcolor=ft.Colors.ORANGE_700,
                color=ft.Colors.WHITE,
            ),
        ], spacing=10, wrap=True)
        
        return ft.Column([
            header,
            intro,
            *values_block,
            *frustrations_block,
            summary_container,
            closing_prompt,
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
                                "Your Relationship Capital Strategy",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK
                            ),
                            ft.Container(height=8),
                            ft.Text(
                                "Your networking and relationship preferences reveal how you naturally build professional connections. "
                                "Understanding these patterns helps you develop authentic networking strategies that feel comfortable and effective.",
                                size=14,
                                color=ft.Colors.GREY_800,
                            ),
                            ft.Container(height=12),
                            ft.Row([
                                ft.Icon(ft.Icons.TIPS_AND_UPDATES, size=20, color=ft.Colors.DEEP_PURPLE_600),
                                ft.Text(
                                    "Network Building Focus:",
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.DEEP_PURPLE_700
                                ),
                            ], spacing=8),
                            ft.Text(
                                "Leverage your strongest relationship preferences while gradually expanding your comfort zone. "
                                "Professional success often requires diverse relationship types and networking approaches. "
                                "Focus on building genuine connections aligned with your values rather than transactional networking.",
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
            nav_buttons,
        ], scroll=ft.ScrollMode.AUTO, expand=True)
    
    # Build and set initial content
    container.content = build_welcome_screen()
    
    return container


def create_relationships_page(page: ft.Page):
    """Entry point for creating the relationships assessment page."""
    return create_relationships_assessment_ui(page)

def _run_standalone(page: ft.Page):
    page.title = "CareerWise - Past Relationships Review"
    page.add(create_relationships_assessment_ui(page))
