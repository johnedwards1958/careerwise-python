"""
Path Assessment - Logic Layer
Scoring and result interpretation logic.
"""

from datetime import datetime
from path_data import CATEGORIES, STATEMENTS, REVERSE_ITEMS


class CareerPathAssessment:
    """Assessment logic container."""

    CATEGORIES = CATEGORIES
    STATEMENTS = STATEMENTS
    REVERSE_ITEMS = REVERSE_ITEMS

    def __init__(self):
        """Initialize the assessment with empty responses."""
        self.responses = {}  # Format: {(category, statement_index): score (1-5)}
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")

    @staticmethod
    def _is_valid_score(score):
        """Return whether a value is a valid stored Likert score."""
        return (
            isinstance(score, int)
            and not isinstance(score, bool)
            and score in range(1, 6)
        )
        
    def set_response(self, category, statement_index, score):
        """
        Set a response for a specific statement.
        Automatically handles reverse scoring for reverse-keyed items.
        
        Args:
            category: The RIASEC category letter (R, I, A, S, E, or C)
            statement_index: The statement number within the category (0-based)
            score: The score value (1-5)
        """
        if category not in self.CATEGORIES:
            raise ValueError(f"Invalid category: {category}")
        if (
            not isinstance(statement_index, int)
            or isinstance(statement_index, bool)
            or not 0 <= statement_index < len(self.STATEMENTS[category])
        ):
            raise ValueError(f"Invalid statement index for category {category}")
        if not self._is_valid_score(score):
            raise ValueError("Score must be an integer between 1 and 5")
        
        # Apply reverse scoring if this is a reverse-keyed item
        if statement_index in self.REVERSE_ITEMS.get(category, []):
            # Reverse the score: 1->5, 2->4, 3->3, 4->2, 5->1
            score = 6 - score
        
        self.responses[(category, statement_index)] = score
    
    def get_response(self, category, statement_index):
        """
        Get the response for a specific statement.
        
        Returns:
            Integer score (1-5) if answered, None if not answered
        """
        if category not in self.STATEMENTS:
            return None
        if (
            not isinstance(statement_index, int)
            or isinstance(statement_index, bool)
            or not 0 <= statement_index < len(self.STATEMENTS[category])
        ):
            return None

        score = self.responses.get((category, statement_index))
        return score if self._is_valid_score(score) else None
    
    def get_raw_response(self, category, statement_index):
        """
        Get the raw response before any reverse scoring was applied.
        Useful for display purposes.
        
        Returns:
            Integer score (1-5) if answered, None if not answered
        """
        score = self.get_response(category, statement_index)
        if score is not None and statement_index in self.REVERSE_ITEMS.get(category, []):
            # Reverse it back to get the original
            return 6 - score
        return score
    
    def calculate_category_score(self, category):
        """
        Calculate the total score for a category.
        
        Args:
            category: The RIASEC category letter
            
        Returns:
            Tuple of (score, max_possible_score, answered_count, total_statements, percentage)
        """
        total_statements = len(self.STATEMENTS[category])
        score = 0
        answered_count = 0
        
        for i in range(total_statements):
            response = self.get_response(category, i)
            if self._is_valid_score(response):
                answered_count += 1
                score += response  # Sum the 1-5 scores (already reverse-scored if needed)
        
        max_possible = total_statements * 5
        percentage = (score / max_possible * 100) if max_possible > 0 else 0
        
        return score, max_possible, answered_count, total_statements, percentage
    
    def get_all_scores(self):
        """
        Get scores for all categories.
        
        Returns:
            Dictionary mapping category letter to (score, max_possible, answered, total, percentage)
        """
        scores = {}
        for category in self.CATEGORIES:
            scores[category] = self.calculate_category_score(category)
        return scores
    
    def get_interest_code(self):
        """
        Get the categories occupying the top 3 score positions.
        Uses normalized percentages for fair comparison across categories with different item counts.
        
        Returns:
            Tuple of (code_string, top_ranked_list, is_complete)
            - code_string: e.g., "RIA", "RI(A/S)" for a third-place
              tie, or "???" if incomplete
            - top_ranked_list: List of (category, score, percentage) tuples.
              It can contain more than 3 entries when the cutoff is tied.
            - is_complete: Boolean indicating if all statements answered
        """
        # Get all scores with percentages
        score_data = {}
        total_answered = 0
        total_statements = 0
        
        for category in self.CATEGORIES:
            score, max_possible, answered, total, percentage = self.calculate_category_score(category)
            score_data[category] = (score, percentage)
            total_answered += answered
            total_statements += total
        
        is_complete = (total_answered == total_statements)
        
        # Preserve the assessment's canonical RIASEC order when scores are tied.
        category_order = {category: index for index, category in enumerate(self.CATEGORIES)}
        sorted_categories = sorted(
            score_data.items(), 
            key=lambda item: (
                -item[1][1],
                -item[1][0],
                category_order[item[0]],
            ),
        )
        
        ranked_categories = [
            (category, score, percentage)
            for category, (score, percentage) in sorted_categories
        ]

        # A tie at the third position is part of the result. Retaining every
        # category at the cutoff avoids silently choosing one by letter/order.
        top_ranked = ranked_categories[:3]
        cutoff_score = (top_ranked[-1][1], top_ranked[-1][2])
        top_ranked.extend(
            item
            for item in ranked_categories[3:]
            if (item[1], item[2]) == cutoff_score
        )
        
        # Create code string
        if is_complete:
            score_groups = []
            for category, score, percentage in top_ranked:
                score_key = (score, percentage)
                if not score_groups or score_groups[-1][0] != score_key:
                    score_groups.append((score_key, [category]))
                else:
                    score_groups[-1][1].append(category)

            code_string = "".join(
                categories[0]
                if len(categories) == 1
                else f"({'/'.join(categories)})"
                for _, categories in score_groups
            )
        else:
            code_string = "???"
        
        return code_string, top_ranked, is_complete
    
    def get_completion_percentage(self):
        """Get the percentage of statements answered."""
        total_statements = sum(len(statements) for statements in self.STATEMENTS.values())
        answered = sum(
            self._is_valid_score(self.get_response(category, statement_index))
            for category, statements in self.STATEMENTS.items()
            for statement_index in range(len(statements))
        )
        return (answered / total_statements * 100) if total_statements > 0 else 0
    
    def get_completion_counts(self):
        """Get the count of answered vs total statements."""
        total_statements = sum(len(statements) for statements in self.STATEMENTS.values())
        answered = sum(
            self._is_valid_score(self.get_response(category, statement_index))
            for category, statements in self.STATEMENTS.items()
            for statement_index in range(len(statements))
        )
        return answered, total_statements
    
    def is_complete(self):
        """Check if all statements have been answered."""
        answered, total_statements = self.get_completion_counts()
        return answered == total_statements
    
    def reset(self):
        """Clear all responses and generate new session ID."""
        self.responses = {}
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    def get_unanswered_questions(self):
        """
        Get a list of all unanswered questions.
        
        Returns:
            List of tuples (category, statement_index, statement_text)
        """
        unanswered = []
        for category in self.CATEGORIES:
            for i, statement in enumerate(self.STATEMENTS[category]):
                if not self._is_valid_score(self.get_response(category, i)):
                    unanswered.append((category, i, statement))
        return unanswered
    
    def calculate_cronbach_alpha(self, category, responses_matrix):
        """
        Calculate Cronbach's alpha for a specific category.
        Requires multiple respondents' data.
        
        Args:
            category: The RIASEC category letter
            responses_matrix: List of lists, where each inner list contains raw
                            responses for all items in this category from one respondent.
                            Example: [[5,4,3,5,4,...], [4,5,4,3,5,...], ...]
        
        Returns:
            Tuple of (alpha, n_items, n_respondents) or None if insufficient data
        """
        if not responses_matrix or len(responses_matrix) < 2:
            return None  # Need at least 2 respondents
        
        n_items = len(self.STATEMENTS[category])
        
        # Verify all responses have correct length
        if not all(len(resp) == n_items for resp in responses_matrix):
            return None

        # Cronbach's alpha requires every item variance and the total-score
        # variance to be based on the same respondents. Use complete rows only.
        complete_responses = [
            list(response)
            for response in responses_matrix
            if all(value is not None for value in response)
        ]
        if len(complete_responses) < 2:
            return None

        if not all(
            isinstance(value, int)
            and not isinstance(value, bool)
            and value in range(1, 6)
            for response in complete_responses
            for value in response
        ):
            return None

        # Reverse-keyed items must be oriented in the same direction as the
        # other items before their covariance is assessed.
        reverse_items = set(self.REVERSE_ITEMS.get(category, []))
        scored_responses = [
            [
                6 - value if item_index in reverse_items else value
                for item_index, value in enumerate(response)
            ]
            for response in complete_responses
        ]
        n_respondents = len(scored_responses)
        
        # Calculate variance of each item
        item_variances = []
        for item_idx in range(n_items):
            item_scores = [response[item_idx] for response in scored_responses]
            mean = sum(item_scores) / len(item_scores)
            variance = sum((x - mean) ** 2 for x in item_scores) / len(item_scores)
            item_variances.append(variance)
        
        # Calculate total score variance
        total_scores = [sum(response) for response in scored_responses]
        
        mean_total = sum(total_scores) / len(total_scores)
        variance_total = sum((x - mean_total) ** 2 for x in total_scores) / len(total_scores)
        
        # Calculate Cronbach's alpha
        sum_item_variances = sum(item_variances)
        if variance_total == 0:
            return None
        
        alpha = (n_items / (n_items - 1)) * (1 - (sum_item_variances / variance_total))
        
        return alpha, n_items, n_respondents
    
    def get_alpha_interpretation(self, alpha):
        """
        Get interpretation of Cronbach's alpha value.
        
        Args:
            alpha: The alpha coefficient value
            
        Returns:
            String interpretation
        """
        if alpha >= 0.90:
            return "Excellent (may indicate redundancy)"
        elif alpha >= 0.80:
            return "Good"
        elif alpha >= 0.70:
            return "Acceptable"
        elif alpha >= 0.60:
            return "Questionable"
        else:
            return "Poor"
    
    def get_first_unanswered_page(self):
        """
        Get the page index (0 or 1) that contains the first unanswered question.
        
        Returns:
            Page index (0 or 1) or None if all answered
        """
        pages = self.get_statements_by_page()
        
        for page_idx, page_statements in enumerate(pages):
            for category, statement_index, statement_text in page_statements:
                if self.get_response(category, statement_index) is None:
                    return page_idx
        
        return None
    
    def get_statements_by_page(self):
        """
        Get statements organized by page (matching PDF layout).
        
        Returns:
            List of two pages, each containing statements from all categories
        """
        # Page 1: First ~3-4 statements from each category
        page1 = []
        page2 = []
        
        # Interleave statements as they appear in the PDF
        # Page 1 order: R, I, A, S, E, C (repeating)
        page1_indices = {
            "R": [0, 1, 2, 3],
            "I": [0, 1, 2, 3],
            "A": [0, 1],
            "S": [0, 1, 2, 3],
            "E": [0, 1, 2, 3],
            "C": [0, 1, 2]
        }
        
        page2_indices = {
            "R": [4, 5, 6, 7, 8],
            "I": [4, 5, 6, 7, 8],
            "A": [2, 3, 4, 5, 6, 7, 8],
            "S": [4, 5, 6, 7, 8],
            "E": [4, 5, 6, 7, 8],
            "C": [3, 4, 5, 6, 7, 8]
        }
        
        # Build page 1
        for cat in ["R", "I", "A", "S", "E", "C"]:
            for idx in page1_indices[cat]:
                if idx < len(self.STATEMENTS[cat]):
                    page1.append((cat, idx, self.STATEMENTS[cat][idx]))
        
        # Build page 2
        for cat in ["R", "I", "A", "S", "E", "C"]:
            for idx in page2_indices[cat]:
                if idx < len(self.STATEMENTS[cat]):
                    page2.append((cat, idx, self.STATEMENTS[cat][idx]))
        
        return [page1, page2]
    
    def get_career_narrative(self):
        """
        Get a personalized career narrative based on the assessment results.
        
        Returns:
            A detailed narrative string explaining the user's career interests and recommendations
        """
        code_string, top_three, is_complete = self.get_interest_code()
        
        if not is_complete:
            return "Complete the assessment to receive your personalized career narrative."
        
        return generate_career_narrative(code_string, top_three)


def generate_career_narrative(interest_code, top_three_scores):
    """
    Generate a personalized narrative summary based on the user's RIASEC results.
    
    Args:
        interest_code: The RIASEC code (e.g., "RIA" or "RI(A/S)" when tied)
        top_three_scores: List of (category, score, percentage) tuples for the
            categories occupying the top 3 positions, including cutoff ties
        
    Returns:
        A detailed narrative text explaining the user's career personality and recommendations
    """
    if not top_three_scores or len(top_three_scores) < 3:
        return "Complete the assessment to receive your personalized career narrative."

    ranking_keys = [(score, percentage) for _, score, percentage in top_three_scores]
    has_tied_ranks = len(set(ranking_keys)) < len(ranking_keys)
    if has_tied_ranks or len(top_three_scores) > 3:
        categories = CareerPathAssessment.CATEGORIES
        profile_details = ", ".join(
            f"{categories[category]['name']} ({category}, {percentage:.1f}%)"
            for category, _, percentage in top_three_scores
        )
        interest_names = ", ".join(
            categories[category]["name"].lower()
            for category, _, _ in top_three_scores
        )
        return "\n\n".join([
            f"Your RIASEC Interest Profile is '{interest_code}'. Parentheses group equally scored areas, "
            "so this result does not assign an arbitrary order within a tie.",
            f"Your leading interest areas are {profile_details}. Similar scores indicate that these interests "
            "may be equally important when you evaluate work and learning opportunities.",
            f"Explore careers that combine {interest_names} activities. Look for roles where these interests "
            "naturally intersect, and compare several options rather than treating one tied area as dominant.",
            "Remember that this profile is a starting point for career exploration, not a limitation. "
            "Research occupations, educational pathways, and work environments that match your preferences, "
            "and test them through conversations, volunteering, internships, or project work.",
        ])
    
    # Extract the primary, secondary, and tertiary interests
    primary_cat, primary_score, primary_pct = top_three_scores[0]
    secondary_cat, secondary_score, secondary_pct = top_three_scores[1]
    tertiary_cat, tertiary_score, tertiary_pct = top_three_scores[2]
    
    # Get category information
    categories = CareerPathAssessment.CATEGORIES
    primary_info = categories[primary_cat]
    secondary_info = categories[secondary_cat]
    tertiary_info = categories[tertiary_cat]
    
    # Build the narrative
    narrative_parts = []
    
    # Opening paragraph - overall profile
    narrative_parts.append(
        f"Your RIASEC Interest Code is '{interest_code}', which reveals a unique combination of career interests and working style preferences. "
        f"This code represents your strongest areas of interest, with '{primary_info['name']}' as your primary interest area, "
        f"followed by '{secondary_info['name']}' and '{tertiary_info['name']}' orientations."
    )
    
    # Primary interest analysis
    narrative_parts.append(
        f"Your dominant '{primary_info['name']} ({primary_cat})' orientation (scoring {primary_pct:.1f}%) suggests you are among those "
        f"{primary_info['description'].lower()} This primary interest indicates you would thrive in environments where "
        f"you can engage with these core activities regularly."
    )
    
    # Secondary interest support
    narrative_parts.append(
        f"Your secondary '{secondary_info['name']} ({secondary_cat})' interest (scoring {secondary_pct:.1f}%) complements your primary orientation by adding "
        f"{secondary_info['description'].lower()} This combination suggests you would excel in roles that blend "
        f"both {primary_info['name'].lower()} and {secondary_info['name'].lower()} elements."
    )
    
    # Code-specific insights based on common combinations
    code_insights = _get_code_specific_insights(interest_code, primary_cat, secondary_cat, tertiary_cat)
    if code_insights:
        narrative_parts.append(code_insights)
    
    # Career pathway recommendations
    narrative_parts.append(
        f"Based on your '{interest_code}' profile, you should explore careers that allow you to combine "
        f"{primary_info['name'].lower()}, {secondary_info['name'].lower()}, and {tertiary_info['name'].lower()} activities. "
        f"Look for roles in industries where these interests naturally intersect, and consider positions that offer "
        f"variety and the opportunity to develop skills across all three areas."
    )
    
    # Final encouragement and next steps
    narrative_parts.append(
        f"Remember that your interest code is a starting point for career exploration, not a limitation. "
        f"Use this profile to research specific occupations, educational pathways, and work environments that align with your "
        f"{interest_code} preferences. Consider informational interviews with professionals in fields that combine your top interests, "
        f"and look for opportunities to gain experience through internships, volunteering, or project work."
    )
    
    return "\n\n".join(narrative_parts)


def _get_code_specific_insights(code, primary, secondary, tertiary):
    """Generate insights specific to common RIASEC code combinations."""
    
    # Common code combination insights
    insights = {
        # Realistic-dominant codes
        ("R", "I"): "Your combination of Realistic and Investigative interests suggests you enjoy hands-on problem-solving with technical or scientific applications. Consider engineering, research and development, or technical fields where you can build and analyze.",
        
        ("R", "A"): "The blend of Realistic and Artistic interests is perfect for creative fields that involve making or building. Architecture, industrial design, crafts, or multimedia production could be ideal fits.",
        
        ("R", "S"): "Your Realistic-Social combination suggests you enjoy helping others through practical, hands-on activities. Consider healthcare fields, coaching, outdoor education, or community service roles.",
        
        ("R", "E"): "Realistic-Enterprising individuals often excel in business roles that involve tangible products or services. Construction management, sales of technical products, or entrepreneurship in practical fields may appeal to you.",
        
        ("R", "C"): "Your Realistic-Conventional combination suggests you appreciate structured, systematic approaches to hands-on work. Quality assurance, technical documentation, or operations management could be strong fits.",
        
        # Investigative-dominant codes
        ("I", "R"): "This combination indicates you enjoy research and analysis applied to practical, technical problems. Engineering research, product development, or applied sciences could be excellent career paths.",
        
        ("I", "A"): "Investigative-Artistic individuals often thrive in creative fields that require research and intellectual rigor. Consider scientific illustration, digital media, or research in creative industries.",
        
        ("I", "S"): "Your blend of analytical thinking and people orientation suggests psychology, social research, or healthcare fields where you can study and help others simultaneously.",
        
        ("I", "E"): "This combination suits roles where you can research market opportunities and lead innovative projects. Management consulting, business analysis, or tech entrepreneurship may appeal to you.",
        
        ("I", "C"): "Investigative-Conventional individuals excel at systematic research and data analysis. Market research, statistical analysis, or quality control in research settings could be ideal.",
        
        # Artistic-dominant codes
        ("A", "S"): "Your Artistic-Social combination suggests you enjoy creative expression that serves or inspires others. Teaching arts, therapy through creative expression, or community arts programs could be fulfilling.",
        
        ("A", "E"): "This blend indicates entrepreneurial creativity - you may excel at bringing artistic ideas to market. Creative agencies, arts administration, or creative entrepreneurship could be strong fits.",
        
        ("A", "I"): "Artistic-Investigative individuals often thrive in fields requiring creative research and intellectual exploration. Academic research in creative fields, scientific visualization, or innovative design may appeal to you.",
        
        # Social-dominant codes
        ("S", "E"): "Your Social-Enterprising combination suggests leadership in people-focused organizations. Management in nonprofits, HR leadership, or social entrepreneurship could be excellent paths.",
        
        ("S", "A"): "This blend of helping others and creative expression suits roles in expressive therapies, arts education, or community creative programs.",
        
        ("S", "C"): "Social-Conventional individuals often excel in organized helping roles. School administration, healthcare administration, or social services coordination could be strong fits.",
        
        # Enterprising-dominant codes
        ("E", "C"): "Your Enterprising-Conventional combination suggests you excel at leading organized, systematic business activities. Business operations, finance, or corporate management could be ideal.",
        
        ("E", "A"): "This creative leadership combination suits roles in creative industries where you can guide artistic projects and teams. Entertainment management, creative agency leadership, or arts administration may appeal to you.",
        
        # Conventional-dominant codes
        ("C", "E"): "Conventional-Enterprising individuals often thrive in business environments requiring systematic leadership. Operations management, business administration, or financial services could be excellent fits.",
        
        ("C", "S"): "Your combination of organizational skills and people orientation suits administrative roles in helping professions. School administration, healthcare administration, or nonprofit management could be ideal."
    }
    
    # Look for matching patterns
    primary_secondary = (primary, secondary)
    if primary_secondary in insights:
        return insights[primary_secondary]
    
    # Do not substitute an insight for a different secondary type. The generic
    # narrative remains accurate when a specific pairing has not been authored.
    return None
