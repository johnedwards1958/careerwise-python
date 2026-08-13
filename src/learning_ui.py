"""
Learning Preferences Assessment - UI Layer
Flet UI construction and page wiring.
"""

import flet as ft

from learning_logic import LearningPreferenceAssessment


class LearningPreferenceUI:
    """
    Provides the UI for the Learning Preferences assessment.
    Includes welcome page, assessment interface, and results page.
    """
    
    def __init__(self, page: ft.Page):
        """Initialize the UI with a page reference."""
        self.page = page
        self.assessment = LearningPreferenceAssessment()
        self.show_welcome = True
        self.show_results = False
        self.main_container = ft.Column(spacing=20, expand=True, alignment=ft.MainAxisAlignment.START)
        self.results_button_container = ft.Container()  # Container for the results button
    
    def create_welcome_page(self):
        """Create the welcome page with instructions and How It Works section."""
        return ft.Column(
            [
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.SCHOOL, size=48, color=ft.Colors.BLUE_700),
                            ft.Text(
                                "Learning Preferences Assessment",
                                size=28,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK,
                            ),
                            ft.Text(
                                "Discover how you prefer to learn and process information",
                                size=16,
                                color=ft.Colors.GREY_700,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    padding=30,
                    bgcolor=ft.Colors.BLUE_50,
                    border_radius=10,
                    margin=ft.Margin.only(bottom=20),
                    alignment=ft.Alignment.CENTER,
                ),
                
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                "How It Works",
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK,
                            ),
                            ft.Container(height=10),
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.LOOKS_ONE, size=24, color=ft.Colors.BLUE_700),
                                    ft.Text(
                                        "Answer 16 questions about how you prefer to learn and respond in different situations",
                                        size=14,
                                        color=ft.Colors.GREY_800,
                                        expand=True,
                                    ),
                                ],
                                spacing=10,
                            ),
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.LOOKS_TWO, size=24, color=ft.Colors.BLUE_700),
                                    ft.Text(
                                        "Select ONE option per question that best describes your preference",
                                        size=14,
                                        color=ft.Colors.GREY_800,
                                        expand=True,
                                    ),
                                ],
                                spacing=10,
                            ),
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.LOOKS_3, size=24, color=ft.Colors.BLUE_700),
                                    ft.Text(
                                        "Discover your learning style: Visual, Auditory, Read/Write, or Kinesthetic",
                                        size=14,
                                        color=ft.Colors.GREY_800,
                                        expand=True,
                                    ),
                                ],
                                spacing=10,
                            ),
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.LOOKS_4, size=24, color=ft.Colors.BLUE_700),
                                    ft.Text(
                                        "Learn whether you have a dominant style, are bimodal, or multimodal in your learning",
                                        size=14,
                                        color=ft.Colors.GREY_800,
                                        expand=True,
                                    ),
                                ],
                                spacing=10,
                            ),
                        ],
                        spacing=12,
                    ),
                    padding=20,
                    bgcolor=ft.Colors.WHITE,
                    border_radius=10,
                    border=ft.Border.all(1, ft.Colors.GREY_300),
                    margin=ft.Margin.only(bottom=20),
                ),
                
                ft.Row(
                    [
                        ft.Button(
                            "Begin Assessment",
                            icon=ft.Icons.PLAY_ARROW,
                            on_click=self.on_begin_assessment,
                            bgcolor=ft.Colors.BLUE_700,
                            color=ft.Colors.WHITE,
                            height=50,
                            style=ft.ButtonStyle(
                                text_style=ft.TextStyle(size=16, weight=ft.FontWeight.BOLD)
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.START,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
    
    def on_begin_assessment(self, e):
        """Handle Begin Assessment button click."""
        self.show_welcome = False
        self.build_assessment_content()
        self.page.update()
    
    def create_question_card(self, question_index):
        """Create a single question card with radio button options."""
        question = self.assessment.QUESTIONS[question_index]
        selected_option = self.assessment.get_response(question_index)
        
        # Create radio buttons for each option
        radio_buttons = []
        for option_index, option in enumerate(question["options"]):
            radio_buttons.append(
                ft.Radio(
                    value=str(option_index),
                    label=option["text"],
                )
            )
        
        radio_group = ft.RadioGroup(
            content=ft.Column(radio_buttons, spacing=8),
            value=str(selected_option) if selected_option is not None else None,
            on_change=lambda e, q_idx=question_index: self.on_option_change(q_idx, e),
        )
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        f"Question {question_index + 1}",
                        size=12,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLUE_700,
                    ),
                    ft.Text(
                        question["text"],
                        size=16,
                        color=ft.Colors.BLACK,
                        weight=ft.FontWeight.W_500,
                    ),
                    ft.Container(height=10),
                    radio_group,
                ],
                spacing=10,
            ),
            padding=20,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            border_radius=10,
            bgcolor=ft.Colors.WHITE,
        )
    
    def on_option_change(self, question_index, e):
        """Handle radio button change for an option."""
        option_index = int(e.control.value)
        self.assessment.set_response(question_index, option_index)
        
        # Update the results button visibility if assessment is now complete
        if self.assessment.is_complete():
            self.results_button_container.content = ft.Row(
                [
                    ft.Button(
                        "View Results",
                        icon=ft.Icons.ASSESSMENT,
                        on_click=self.on_get_results,
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.BLUE_700,
                            padding=15,
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
            self.results_button_container.margin = ft.Margin.only(top=30, bottom=20)
            self.results_button_container.update()
        
        self.page.update()
    
    def create_all_questions_content(self):
        """Create the full assessment with all questions."""
        question_cards = []
        
        # Create a card for each question
        for i in range(len(self.assessment.QUESTIONS)):
            question_cards.append(self.create_question_card(i))
        
        # Add "View Results" button if assessment is complete
        if self.assessment.is_complete():
            self.results_button_container.content = ft.Row(
                [
                    ft.Button(
                        "View Results",
                        icon=ft.Icons.ASSESSMENT,
                        on_click=self.on_get_results,
                        style=ft.ButtonStyle(
                            color=ft.Colors.WHITE,
                            bgcolor=ft.Colors.BLUE_700,
                            padding=15,
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
            self.results_button_container.margin = ft.Margin.only(top=30, bottom=20)
        else:
            self.results_button_container.content = None
            self.results_button_container.margin = None
        
        return ft.Column(
            [
                ft.Row(
                    [
                        ft.Text(
                            "📚 Learning Preferences Assessment",
                            size=24,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.BLUE_700,
                        ),
                    ],
                ),
                ft.Text(
                    "Select the ONE option that best describes how you would prefer to learn or respond in each situation.",
                    size=14,
                    color=ft.Colors.GREY_700,
                ),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.Column(
                    question_cards,
                    spacing=15,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
                self.results_button_container,
            ],
            spacing=10,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        )
    
    def on_get_results(self, e):
        """Handle View Results button click."""
        self.show_results = True
        self.build_assessment_content()
        self.page.update()
    
    def create_style_card(self, style_code, score, is_dominant=False):
        """Create a result card for a learning style."""
        style_info = self.assessment.STYLES[style_code]
        
        # Determine card styling
        border_color = ft.Colors.BLUE_700 if is_dominant else ft.Colors.GREY_300
        bg_color = ft.Colors.BLUE_50 if is_dominant else ft.Colors.WHITE
        border_width = 2 if is_dominant else 1
        
        # Create progress bar
        progress_percentage = (score / 16) * 100
        
        # Create strategies list
        strategies_list = []
        for strategy in style_info["strategies"]:
            strategies_list.append(
                ft.Row(
                    [
                        ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE, size=16, color=ft.Colors.GREEN_700),
                        ft.Text(
                            strategy,
                            size=12,
                            color=ft.Colors.GREY_800,
                            expand=True,
                        ),
                    ],
                    spacing=5,
                )
            )
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                style_info["icon"],
                                size=32,
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        style_info["name"],
                                        size=20,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.BLUE_700,
                                    ),
                                    ft.Text(
                                        style_info["description"],
                                        size=13,
                                        color=ft.Colors.GREY_700,
                                        italic=True,
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.Text(
                                f"{score}/16",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_700,
                            ),
                        ],
                        spacing=15,
                    ),
                    ft.Container(height=10),
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Container(
                                            bgcolor=ft.Colors.BLUE_700,
                                            border_radius=4,
                                        ),
                                        width=progress_percentage * 2,  # Scale to 200px max
                                        height=8,
                                        border_radius=4,
                                    ),
                                ],
                            ),
                            ft.Text(
                                f"{progress_percentage:.0f}% of possible selections",
                                size=11,
                                color=ft.Colors.GREY_600,
                            ),
                        ],
                        spacing=5,
                    ),
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        "Suggested Learning Strategies:",
                        size=14,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.BLACK,
                    ),
                    ft.Column(
                        strategies_list,
                        spacing=6,
                    ),
                ],
                spacing=10,
            ),
            padding=20,
            border=ft.Border.all(border_width, border_color),
            border_radius=10,
            bgcolor=bg_color,
        )
    
    def create_results_page(self):
        """Create the results page showing learning style scores."""
        # Get scores and dominant style
        scores = self.assessment.calculate_style_scores()
        style_type, dominant_styles = self.assessment.get_dominant_style()
        interpretation = self.assessment.get_interpretation(style_type)
        
        # Sort styles by score
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        # Create style cards
        style_cards = []
        for style_code, score in sorted_scores:
            is_dominant = style_code in dominant_styles
            style_cards.append(self.create_style_card(style_code, score, is_dominant))
        
        # Create dominant styles display
        dominant_styles_text = ", ".join([self.assessment.STYLES[s]["name"] for s in dominant_styles])
        
        return ft.Column(
            [
                ft.Text(
                    "📚 Your Learning Preferences Results",
                    size=28,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_700,
                ),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                
                # Learning style type
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Text(
                                f"Your Learning Style: {style_type}",
                                size=22,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_700,
                            ),
                            ft.Text(
                                interpretation,
                                size=15,
                                color=ft.Colors.GREY_800,
                            ),
                            ft.Container(height=10),
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.STAR, size=24, color=ft.Colors.AMBER_700),
                                    ft.Text(
                                        f"Primary Style(s): {dominant_styles_text}",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.BLACK,
                                    ),
                                ],
                                spacing=10,
                            ),
                        ],
                        spacing=8,
                    ),
                    padding=20,
                    bgcolor=ft.Colors.BLUE_50,
                    border_radius=10,
                    border=ft.Border.all(2, ft.Colors.BLUE_700),
                    margin=ft.Margin.only(bottom=30),
                ),
                
                # All style scores
                ft.Text(
                    "📊 Your Complete Learning Profile",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_700,
                ),
                ft.Text(
                    "Scores show how many times you selected each learning mode (out of 16 possible):",
                    size=14,
                    color=ft.Colors.GREY_700,
                ),
                ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                ft.Column(
                    style_cards,
                    spacing=15,
                ),
                
                ft.Divider(height=30, color=ft.Colors.TRANSPARENT),
                
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
                                    "Your Personal Learning Architecture",
                                    size=16,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.BLACK
                                ),
                                ft.Container(height=8),
                                ft.Text(
                                    "Your learning style preferences reveal how you naturally acquire and process new information. "
                                    "Understanding these patterns helps you choose development opportunities that maximize your growth potential.",
                                    size=14,
                                    color=ft.Colors.GREY_800,
                                ),
                                ft.Container(height=12),
                                ft.Row([
                                    ft.Icon(ft.Icons.TIPS_AND_UPDATES, size=20, color=ft.Colors.DEEP_PURPLE_600),
                                    ft.Text(
                                        "Learning Optimization Strategy:",
                                        size=14,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.DEEP_PURPLE_700
                                    ),
                                ], spacing=8),
                                ft.Text(
                                    "Design your development plan around your strongest learning preferences while occasionally challenging yourself with other styles. "
                                    "Diverse learning approaches build cognitive flexibility and prepare you for varied workplace situations. "
                                    "Communicate your learning preferences to mentors and managers to maximize training effectiveness.",
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
                
                # Reset button
                ft.Button(
                    "Reset Assessment",
                    icon=ft.Icons.REFRESH,
                    on_click=self.on_reset,
                    style=ft.ButtonStyle(
                        color=ft.Colors.WHITE,
                        bgcolor=ft.Colors.ORANGE_700,
                        padding=15,
                    ),
                ),
            ],
            spacing=15,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
    
    def on_reset(self, e):
        """Handle Reset Assessment button click."""
        self.assessment.reset()
        self.show_welcome = True
        self.show_results = False
        self.build_assessment_content()
        self.page.update()
    
    def build_assessment_content(self):
        """Build the main assessment content based on current state."""
        self.main_container.controls.clear()
        
        if self.show_welcome:
            self.main_container.controls.append(self.create_welcome_page())
        elif self.show_results:
            self.main_container.controls.append(self.create_results_page())
        else:
            self.main_container.controls.append(self.create_all_questions_content())
    
    def get_view(self):
        """Return the main container for this assessment."""
        self.build_assessment_content()
        return ft.Container(
            content=self.main_container,
            padding=20,
            expand=True
        )


def create_learning_preference_assessment_ui(page: ft.Page):
    """Create and return the Learning Preferences assessment UI."""
    return LearningPreferenceUI(page).get_view()


def _run_standalone(page: ft.Page):
    page.title = "CareerWise - Learning Preferences"
    page.add(create_learning_preference_assessment_ui(page))
