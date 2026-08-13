"""
Influence Archetypes Assessment - UI Layer
Flet UI construction and page wiring.
"""

import flet as ft

from archetypes_logic import InfluenceArchetypesAssessment


class InfluenceArchetypesUI:
    """
    Provides the UI for the Influence Archetypes assessment.
    Includes welcome page, assessment interface, and results page.
    """
    
    def __init__(self, page: ft.Page):
        """Initialize the UI with a page reference."""
        self.page = page
        self.assessment = InfluenceArchetypesAssessment()
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
                            ft.Icon(ft.Icons.PERSON_OUTLINE, size=48, color=ft.Colors.BLUE_700),
                            ft.Text(
                                "Influence Archetypes Assessment",
                                size=28,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK,
                            ),
                            ft.Text(
                                "Discover your natural influence style and how you persuade others",
                                size=16,
                                color=ft.Colors.GREY_700,
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
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
                                        "You'll rate 27 statements across 3 influence clusters: Analytical, Relational, and Inspirational",
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
                                        "Rate each statement from 1-5 based on how well it describes you",
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
                                        "Use the scale: 5 = Always true, 3 = Sometimes, 1 = Never true",
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
                                        "Discover your Influence Signature — your top 2 score positions from 9 archetypes (ties included)",
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
    
    def create_statement_row(self, archetype, statement_index, statement_text):
        """Create a single statement row with rating options."""
        current_rating = self.assessment.get_response(archetype, statement_index)
        
        # Create radio buttons for ratings 5-1
        radio_group = ft.RadioGroup(
            content=ft.Row(
                [
                    ft.Radio(value="5", label="5"),
                    ft.Radio(value="4", label="4"),
                    ft.Radio(value="3", label="3"),
                    ft.Radio(value="2", label="2"),
                    ft.Radio(value="1", label="1"),
                ],
                spacing=15,
            ),
            value=str(current_rating) if current_rating else None,
            on_change=lambda e, arch=archetype, idx=statement_index: self.on_rating_change(arch, idx, e),
        )
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(
                        statement_text,
                        size=14,
                        color=ft.Colors.GREY_800,
                        weight=ft.FontWeight.W_500,
                    ),
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Text("Always", size=12, color=ft.Colors.GREY_600),
                                width=60,
                            ),
                            radio_group,
                            ft.Container(
                                content=ft.Text("Never", size=12, color=ft.Colors.GREY_600),
                                width=60,
                            ),
                        ],
                        spacing=10,
                        alignment=ft.MainAxisAlignment.START,
                    ),
                ],
                spacing=10,
            ),
            padding=15,
            border=ft.Border.all(1, ft.Colors.GREY_300),
            border_radius=8,
            bgcolor=ft.Colors.WHITE,
        )
    
    def on_rating_change(self, archetype, statement_index, e):
        """Handle rating change for a statement."""
        rating = int(e.control.value)
        self.assessment.set_response(archetype, statement_index, rating)
        
        # Update the results button visibility if assessment is now complete
        if self.assessment.is_complete():
            self.results_button_container.content = ft.Row(
                [
                    ft.Button(
                        "View Results",
                        icon=ft.Icons.EMOJI_EVENTS,
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
        
        # No need to rebuild entire content, just update the page
        self.page.update()
    
    def create_all_statements_content(self):
        """Create the full assessment with all statements grouped by archetype."""
        statement_rows = []
        
        # Create statements grouped by archetype
        for archetype, statements in self.assessment.STATEMENTS.items():
            # Add archetype header
            info = self.assessment.ARCHETYPE_INFO[archetype]
            statement_rows.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(info["icon"], size=24),
                            ft.Text(
                                f"{archetype} – {info['title']}",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_700,
                            ),
                        ],
                        spacing=10,
                    ),
                    margin=ft.Margin.only(top=20, bottom=10),
                )
            )
            
            # Add statements for this archetype
            for idx, statement in enumerate(statements):
                statement_rows.append(
                    self.create_statement_row(archetype, idx, statement)
                )
        
        # Add "View Results" button if assessment is complete
        if self.assessment.is_complete():
            self.results_button_container.content = ft.Row(
                [
                    ft.Button(
                        "View Results",
                        icon=ft.Icons.EMOJI_EVENTS,
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
        
        statement_rows.append(self.results_button_container)
        
        return ft.Column(
            [
                ft.Text(
                    "🧭 Influence Archetypes Assessment",
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_700,
                ),
                ft.Text(
                    "Rate how true each statement is for you at work or in group settings",
                    size=14,
                    color=ft.Colors.GREY_700,
                ),
                ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
                ft.Column(
                    statement_rows,
                    spacing=15,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
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
    
    def create_archetype_result_card(self, archetype, score, rank=None, is_top=None):
        """Create a result card for a single archetype."""
        info = self.assessment.ARCHETYPE_INFO[archetype]
        
        # Determine if this is a top archetype
        if is_top is None:
            is_top = rank is not None and rank <= 2
        border_color = ft.Colors.BLUE_700 if is_top else ft.Colors.GREY_300
        bg_color = ft.Colors.BLUE_50 if is_top else ft.Colors.WHITE
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(info["icon"], size=32),
                            ft.Column(
                                [
                                    ft.Text(
                                        archetype,
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                        color=ft.Colors.BLUE_700,
                                    ),
                                    ft.Text(
                                        info["title"],
                                        size=14,
                                        color=ft.Colors.GREY_700,
                                        italic=True,
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.Text(
                                f"{max(0, ((score - 1) / 4.0 * 100)):.0f}%",
                                size=24,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_700,
                            ),
                        ],
                        spacing=15,
                    ),
                    ft.Divider(height=10, color=ft.Colors.TRANSPARENT),
                    ft.Text(
                        info["description"],
                        size=13,
                        color=ft.Colors.GREY_800,
                    ),
                    ft.Divider(height=5, color=ft.Colors.TRANSPARENT),
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.STAR, size=16, color=ft.Colors.GREEN_700),
                            ft.Text(
                                f"Strengths: {info['strengths']}",
                                size=12,
                                color=ft.Colors.GREY_800,
                            ),
                        ],
                        spacing=5,
                    ),
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.TRENDING_UP, size=16, color=ft.Colors.ORANGE_700),
                            ft.Text(
                                f"Try developing: {info['development']}",
                                size=12,
                                color=ft.Colors.GREY_800,
                            ),
                        ],
                        spacing=5,
                    ),
                ],
                spacing=8,
            ),
            padding=20,
            border=ft.Border.all(2 if is_top else 1, border_color),
            border_radius=10,
            bgcolor=bg_color,
        )
    
    def create_results_page(self):
        """Create the results page showing archetype scores and clusters."""
        # Get all scores
        archetype_scores = self.assessment.calculate_all_archetype_scores()
        sorted_archetypes = sorted(archetype_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Get cluster scores
        cluster_scores = self.assessment.calculate_cluster_scores()
        
        # Rescale helper for 1-5 -> 0-100%
        def scaled_pct(avg_score: float) -> float:
            return max(0.0, ((avg_score - 1.0) / 4.0) * 100.0)
        
        # Detect "no endorsement" (all ratings == 1 on average)
        no_endorsement = all(score <= 1.0 for score in archetype_scores.values())
        
        # Create optional notice banner
        notice_banner = None
        if no_endorsement:
            notice_banner = ft.Container(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.INFO, color=ft.Colors.ORANGE_700),
                        ft.Text(
                            "No dominant archetype identified yet. All responses were rated \"Never\". "
                            "Consider revisiting a few statements and choosing the option that best reflects your typical behaviour.",
                            size=13,
                            color=ft.Colors.GREY_900,
                            expand=True,
                        ),
                    ],
                    spacing=10,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=15,
                bgcolor=ft.Colors.ORANGE_50,
                border=ft.Border.all(1, ft.Colors.ORANGE_200),
                border_radius=8,
                margin=ft.Margin.only(bottom=15),
            )
        
        # Build Influence Signature section conditionally
        signature_section = []
        if no_endorsement:
            # Show only title and helper text (no cards)
            signature_section.extend([
                ft.Text(
                    "✨ Your Influence Signature",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_700,
                ),
                ft.Text(
                    "No primary styles detected. Adjust a few responses to see your top archetypes.",
                    size=14,
                    color=ft.Colors.GREY_700,
                ),
            ])
        else:
            # Include every archetype tied at the second score position rather
            # than presenting an arbitrary tied style as non-primary.
            top_two = self.assessment.get_top_archetypes(count=2, include_ties=True)
            top_archetype_names = {archetype for archetype, _ in top_two}
            top_cards = [
                self.create_archetype_result_card(
                    archetype,
                    score,
                    rank=rank,
                    is_top=True,
                )
                for rank, (archetype, score) in enumerate(top_two, start=1)
            ]
            if len(top_two) > 2:
                signature_description = (
                    f"{len(top_two)} archetypes share your top two score positions; "
                    "all are included in your Influence Signature:"
                )
            else:
                signature_description = (
                    "Your top two archetypes define your primary influence style:"
                )
            signature_section.extend([
                ft.Text(
                    "✨ Your Influence Signature",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color=ft.Colors.BLUE_700,
                ),
                ft.Text(
                    signature_description,
                    size=14,
                    color=ft.Colors.GREY_700,
                ),
                ft.Column(top_cards, spacing=15),
            ])
        
        # Create all archetypes section
        if no_endorsement:
            top_archetype_names = set()
        all_cards = []
        for rank, (archetype, score) in enumerate(sorted_archetypes, start=1):
            all_cards.append(
                self.create_archetype_result_card(
                    archetype,
                    score,
                    rank=rank,
                    is_top=archetype in top_archetype_names,
                )
            )
        
        # Create cluster scores section with rescaling
        cluster_rows = []
        for cluster, score in sorted(cluster_scores.items(), key=lambda x: x[1], reverse=True):
            cluster_rows.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(
                                cluster,
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_700,
                                expand=True,
                            ),
                            ft.Text(
                                f"{scaled_pct(score):.0f}%",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLUE_700,
                            ),
                        ],
                        spacing=10,
                    ),
                    padding=15,
                    border=ft.Border.all(1, ft.Colors.BLUE_200),
                    border_radius=8,
                    bgcolor=ft.Colors.BLUE_50,
                )
            )
        
        # Build the results layout
        results_layout = [
            ft.Text(
                "🧭 Your Influence Archetypes Results",
                size=28,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_700,
            ),
            ft.Divider(height=20, color=ft.Colors.TRANSPARENT),
        ]
        
        # Add optional notice banner
        if notice_banner:
            results_layout.append(notice_banner)
        
        # Add signature section
        results_layout.extend(signature_section)
        
        # Continue with rest of results
        results_layout.extend([
            ft.Divider(height=30, color=ft.Colors.GREY_300),
            
            # Cluster Scores
            ft.Text(
                "📊 Cluster Scores",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_700,
            ),
            ft.Text(
                "Your average scores across the three influence clusters:",
                size=14,
                color=ft.Colors.GREY_700,
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text(
                        "Cluster scores show your preferred influence approach by grouping related archetypes:",
                        size=13,
                        color=ft.Colors.GREY_800,
                    ),
                    ft.Text(
                        "• Analytical: Logic-based influence (Analyst, Enforcer, Negotiator)",
                        size=12,
                        color=ft.Colors.GREY_700,
                    ),
                    ft.Text(
                        "• Relational: People-focused influence (Communicator, Socialiser, Ally)",
                        size=12,
                        color=ft.Colors.GREY_700,
                    ),
                    ft.Text(
                        "• Inspirational: Vision-driven influence (Collaborator, Networker, Visionary)",
                        size=12,
                        color=ft.Colors.GREY_700,
                    ),
                ], spacing=5),
                padding=15,
                bgcolor=ft.Colors.BLUE_50,
                border=ft.Border.all(1, ft.Colors.BLUE_200),
                border_radius=8,
                margin=ft.Margin.only(bottom=15),
            ),
            ft.Column(cluster_rows, spacing=10),
            
            ft.Divider(height=30, color=ft.Colors.GREY_300),
            
            # All Archetypes
            ft.Text(
                "🎯 All Archetype Scores",
                size=20,
                weight=ft.FontWeight.BOLD,
                color=ft.Colors.BLUE_700,
            ),
            ft.Text(
                "Your complete profile across all nine influence archetypes:",
                size=14,
                color=ft.Colors.GREY_700,
            ),
            ft.Column(all_cards, spacing=15),
            
            ft.Divider(height=30, color=ft.Colors.GREY_300),
            
            # Disclaimer
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Icon(ft.Icons.INFO_OUTLINE, size=20, color=ft.Colors.AMBER_700),
                        ft.Text(
                            "Important Note",
                            size=16,
                            weight=ft.FontWeight.BOLD,
                            color=ft.Colors.AMBER_700,
                        ),
                    ], spacing=8),
                    ft.Text(
                        "These results show your preferred ways of working with others. "
                        "They describe tendencies, not fixed traits, and can change depending on your team, role, or situation. "
                        "They are reliable for reflection and discussion, but not a personality test.",
                        size=13,
                        color=ft.Colors.GREY_800,
                    ),
                ], spacing=8),
                padding=20,
                bgcolor=ft.Colors.AMBER_50,
                border=ft.Border.all(1, ft.Colors.AMBER_200),
                border_radius=8,
                margin=ft.Margin.only(bottom=20),
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
                                "Your Influence Leadership Profile",
                                size=16,
                                weight=ft.FontWeight.BOLD,
                                color=ft.Colors.BLACK
                            ),
                            ft.Container(height=8),
                            ft.Text(
                                "Your archetype profile reveals your natural influence style and leadership approach. "
                                "Understanding these patterns helps you leverage your strengths and adapt your style for maximum impact.",
                                size=14,
                                color=ft.Colors.GREY_800,
                            ),
                            ft.Container(height=12),
                            ft.Row([
                                ft.Icon(ft.Icons.TIPS_AND_UPDATES, size=20, color=ft.Colors.DEEP_PURPLE_600),
                                ft.Text(
                                    "Leadership Development Focus:",
                                    size=14,
                                    weight=ft.FontWeight.BOLD,
                                    color=ft.Colors.DEEP_PURPLE_700
                                ),
                            ], spacing=8),
                            ft.Text(
                                "Focus on developing your strongest archetypes while building awareness of others. "
                                "Great leaders can flex between different influence styles based on situation and audience. "
                                "Practice incorporating elements from other clusters to expand your leadership versatility and effectiveness.",
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
        ])
        
        return ft.Column(
            results_layout,
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
            self.main_container.controls.append(self.create_all_statements_content())
    
    def get_view(self):
        """Return the main container for this assessment."""
        self.build_assessment_content()
        return ft.Container(
            content=self.main_container,
            padding=20,
            expand=True
        )


def create_influence_archetypes_assessment_ui(page: ft.Page):
    """Create and return the Influence Archetypes assessment UI."""
    return InfluenceArchetypesUI(page).get_view()


def _run_standalone(page: ft.Page):
    page.title = "CareerWise - Influence Archetypes"
    page.add(create_influence_archetypes_assessment_ui(page))
