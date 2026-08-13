"""
Relationships Assessment - Logic Layer
Scoring and result interpretation logic.
"""

import re
from relationships_data import THEMES, FRUSTRATION_THEMES, POSITIVE_PROMPTS, CHALLENGING_PROMPTS, NEGATION_WORDS


class RelationshipsAssessment:
    """Assessment logic container."""

    THEMES = THEMES
    FRUSTRATION_THEMES = FRUSTRATION_THEMES
    POSITIVE_PROMPTS = POSITIVE_PROMPTS
    CHALLENGING_PROMPTS = CHALLENGING_PROMPTS
    NEGATION_WORDS = NEGATION_WORDS

    def __init__(self):
        """Initialize the assessment with empty relationships."""
        self.relationships = []  # List of relationship dictionaries
        self.max_relationships = 6  # Maximum total relationships allowed
    
    def validate_relationship_name(self, name, exclude_index=None):
        """
        Validate a relationship name.
        
        Args:
            name: The name to validate
            exclude_index: Optional index to exclude from duplicate check (for updates)
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        # Check if empty or whitespace
        if not name or not name.strip():
            return False, "Relationship name cannot be empty."
        
        name = name.strip()
        
        # Check length constraints
        if len(name) < 2:
            return False, "Relationship name must be at least 2 characters long."
        
        if len(name) > 50:
            return False, "Relationship name must be 50 characters or less."
        
        # Check for at least one alphanumeric character
        if not any(c.isalnum() for c in name):
            return False, "Relationship name must contain at least one letter or number."
        
        # Check for duplicates (case-insensitive)
        name_lower = name.lower()
        for i, relationship in enumerate(self.relationships):
            if i != exclude_index and relationship['name'].lower() == name_lower:
                return False, f"You already have a relationship named '{relationship['name']}'. Please use a different name."
        
        return True, ""
    
    def validate_reflection_text(self, text, relationship_type=None):
        """
        Validate reflection text for quality and completeness.
        
        Args:
            text: The reflection text to validate
            relationship_type: Optional type ('positive' or 'challenging') for type-specific checks
            
        Returns:
            Tuple of (is_valid, error_message, warning_message)
        """
        # Check if empty or whitespace
        if not text or not text.strip():
            return False, "Reflection cannot be empty. Please share your thoughts.", None
        
        text = text.strip()
        
        # Character count validation
        if len(text) < 50:
            return False, "Please provide a more detailed reflection (at least 50 characters).", None
        
        if len(text) > 2000:
            return False, "Reflection is too long. Please keep it under 2000 characters.", None
        
        # Sentence count validation (rough check using periods, exclamations, questions)
        sentence_endings = text.count('.') + text.count('!') + text.count('?')
        if sentence_endings < 1:
            return False, "Please write at least one complete sentence.", None
        
        # Type-specific warnings
        warning = None
        if relationship_type:
            text_lower = text.lower()
            
            # Negative keywords that might indicate misclassification
            negative_keywords = ['terrible', 'awful', 'hated', 'horrible', 'worst', 'nightmare', 'toxic']
            
            if relationship_type == 'positive':
                # Check if positive relationship contains too many negative words
                negative_count = sum(1 for keyword in negative_keywords if keyword in text_lower)
                if negative_count >= 2:
                    warning = "This reflection contains several negative words. Consider if this should be a 'Challenging' relationship instead."
        
        return True, "", warning
    
    def can_add_relationship(self, relationship_type=None):
        """
        Check if user can add more relationships.
        
        Args:
            relationship_type: Optional type ('positive' or 'challenging') for rule checks
        
        Returns:
            Tuple of (can_add, message)
        """
        total = len(self.relationships)
        if total >= self.max_relationships:
            return False, f"You've reached the maximum of {self.max_relationships} relationships. Complete or delete existing ones to add more."

        if relationship_type in ['positive', 'challenging']:
            positive_count = self.get_positive_count()
            challenging_count = self.get_challenging_count()
            remaining_slots = self.max_relationships - total

            if relationship_type == 'positive' and challenging_count == 0 and remaining_slots == 1:
                return False, "Add a challenging relationship to meet the minimum of one positive and one challenging."
            if relationship_type == 'challenging' and positive_count == 0 and remaining_slots == 1:
                return False, "Add a positive relationship to meet the minimum of one positive and one challenging."

        return True, ""
    
    def get_balance_warning(self):
        """
        Check if relationships are heavily skewed and return a warning.
        
        Returns:
            Warning message or None
        """
        positive_count = self.get_positive_count()
        challenging_count = self.get_challenging_count()
        total = positive_count + challenging_count
        
        if total < 2:
            return None
        
        # Warn if more than 75% are one type
        if positive_count == 0 and challenging_count >= 3:
            return "You've only added challenging relationships. Consider adding at least one positive relationship for balance."
        
        if challenging_count == 0 and positive_count >= 3:
            return "You've only added positive relationships. Consider adding at least one challenging relationship for deeper insights."
        
        if total >= 4:
            ratio = positive_count / total if total > 0 else 0
            if ratio > 0.75:
                return "Most of your relationships are positive. Adding more challenging relationships can provide valuable learning insights."
            elif ratio < 0.25:
                return "Most of your relationships are challenging. Adding positive relationships can highlight what works well for you."
        
        return None
    
    def add_relationship(self, name, relationship_type):
        """
        Add a new relationship with validation.
        
        Args:
            name: The name/label for the relationship
            relationship_type: 'positive' or 'challenging'
            
        Returns:
            The index of the newly added relationship
            
        Raises:
            ValueError: If validation fails
        """
        if relationship_type not in ['positive', 'challenging']:
            raise ValueError("Relationship type must be 'positive' or 'challenging'")

        # Check if can add more relationships
        can_add, message = self.can_add_relationship(relationship_type)
        if not can_add:
            raise ValueError(message)
        
        # Validate name
        is_valid, error = self.validate_relationship_name(name)
        if not is_valid:
            raise ValueError(error)
        
        relationship = {
            'name': name.strip(),
            'type': relationship_type,
            'reflections': {}  # Format: {prompt_index: response_text}
        }
        self.relationships.append(relationship)
        return len(self.relationships) - 1
    
    def update_relationship_name(self, index, name):
        """Update the name of a relationship with validation."""
        if 0 <= index < len(self.relationships):
            is_valid, error = self.validate_relationship_name(name, exclude_index=index)
            if not is_valid:
                raise ValueError(error)
            self.relationships[index]['name'] = name.strip()
    
    def update_relationship_type(self, index, relationship_type):
        """Update the type of a relationship."""
        if 0 <= index < len(self.relationships):
            if relationship_type not in ['positive', 'challenging']:
                raise ValueError("Relationship type must be 'positive' or 'challenging'")
            self.relationships[index]['type'] = relationship_type
    
    def remove_relationship(self, index):
        """Remove a relationship by index."""
        if 0 <= index < len(self.relationships):
            self.relationships.pop(index)
    
    def set_reflection(self, relationship_index, prompt_index, text):
        """
        Set a reflection response for a specific prompt.
        
        Args:
            relationship_index: Index of the relationship
            prompt_index: Index of the prompt (0-4)
            text: The reflection text
        """
        if type(relationship_index) is not int or not 0 <= relationship_index < len(self.relationships):
            raise ValueError(f"Invalid relationship index: {relationship_index}")

        relationship = self.relationships[relationship_index]
        prompts = (
            self.POSITIVE_PROMPTS
            if relationship['type'] == 'positive'
            else self.CHALLENGING_PROMPTS
        )
        if type(prompt_index) is not int or not 0 <= prompt_index < len(prompts):
            raise ValueError(f"Invalid prompt index: {prompt_index}")
        if not isinstance(text, str):
            raise ValueError("Reflection text must be a string")

        relationship['reflections'][prompt_index] = text
    
    def get_reflection(self, relationship_index, prompt_index):
        """Get a reflection response."""
        if 0 <= relationship_index < len(self.relationships):
            return self.relationships[relationship_index]['reflections'].get(prompt_index, '')
        return ''
    
    def is_relationship_complete(self, index):
        """Check if every required prompt contains a valid reflection."""
        if type(index) is int and 0 <= index < len(self.relationships):
            relationship = self.relationships[index]
            prompts = (
                self.POSITIVE_PROMPTS
                if relationship['type'] == 'positive'
                else self.CHALLENGING_PROMPTS
            )
            for prompt_index in range(len(prompts)):
                text = relationship['reflections'].get(prompt_index, '')
                if not isinstance(text, str):
                    return False
                is_valid, _, _ = self.validate_reflection_text(
                    text, relationship['type']
                )
                if not is_valid:
                    return False
            return True
        return False
    
    def get_relationship_progress(self, index):
        """Get the number of required prompts with valid reflections."""
        if type(index) is int and 0 <= index < len(self.relationships):
            relationship = self.relationships[index]
            prompts = (
                self.POSITIVE_PROMPTS
                if relationship['type'] == 'positive'
                else self.CHALLENGING_PROMPTS
            )
            completed = 0
            for prompt_index in range(len(prompts)):
                text = relationship['reflections'].get(prompt_index, '')
                if not isinstance(text, str):
                    continue
                is_valid, _, _ = self.validate_reflection_text(
                    text, relationship['type']
                )
                if is_valid:
                    completed += 1
            return completed, len(prompts)
        return 0, len(self.POSITIVE_PROMPTS)
    
    def can_view_results(self):
        """
        Check if user can view results.
        Requires at least 1 positive and 1 challenging relationship completed.
        """
        positive_complete = sum(
            1
            for index, relationship in enumerate(self.relationships)
            if relationship['type'] == 'positive'
            and self.is_relationship_complete(index)
        )
        challenging_complete = sum(
            1
            for index, relationship in enumerate(self.relationships)
            if relationship['type'] == 'challenging'
            and self.is_relationship_complete(index)
        )
        return positive_complete >= 1 and challenging_complete >= 1
    
    def get_completion_status(self):
        """Get overall completion status."""
        positive_complete = sum(
            1
            for index, relationship in enumerate(self.relationships)
            if relationship['type'] == 'positive'
            and self.is_relationship_complete(index)
        )
        challenging_complete = sum(
            1
            for index, relationship in enumerate(self.relationships)
            if relationship['type'] == 'challenging'
            and self.is_relationship_complete(index)
        )
        
        positive_needed = max(0, 1 - positive_complete)
        challenging_needed = max(0, 1 - challenging_complete)
        
        return {
            'positive_complete': positive_complete,
            'challenging_complete': challenging_complete,
            'positive_needed': positive_needed,
            'challenging_needed': challenging_needed,
            'can_view_results': self.can_view_results()
        }
    
    def _has_negation_before(self, text, keyword_pos):
        """
        Check if a keyword is preceded by a negation word.
        
        Args:
            text: The full text
            keyword_pos: The position where the keyword starts
            
        Returns:
            True if negation detected within 5 words before keyword
        """
        # Negation does not carry over from a previous sentence. Limiting the
        # scope here avoids suppressing a positive keyword merely because the
        # preceding sentence contained "not" or "never".
        preceding_text = text[:keyword_pos].lower().replace('’', "'")
        sentence_start = max(
            preceding_text.rfind(boundary)
            for boundary in ('.', '!', '?', ';', '\n')
        )
        preceding_text = preceding_text[sentence_start + 1:]

        # Keep apostrophes inside contractions so entries such as "didn't" in
        # NEGATION_WORDS can actually be matched.
        words = re.findall(r"\b\w+(?:'\w+)?\b", preceding_text)
        
        # Check last 5 words for negation
        recent_words = words[-5:] if len(words) >= 5 else words
        
        negations = {word.lower().replace('’', "'") for word in self.NEGATION_WORDS}
        for negation in negations:
            if negation in recent_words:
                return True
        
        return False
    
    def _count_keyword_in_text(self, text, keyword):
        """
        Count occurrences of a keyword in text, excluding negated instances.
        
        Args:
            text: The text to search in
            keyword: The keyword to search for
            
        Returns:
            Count of non-negated keyword occurrences
        """
        text_lower = text.lower()
        count = 0
        
        # Use word boundaries to match whole words or phrases
        pattern = r'\b' + re.escape(keyword.lower()) + r'\b'
        
        for match in re.finditer(pattern, text_lower):
            # Check if this match is negated
            if not self._has_negation_before(text_lower, match.start()):
                count += 1
        
        return count
    
    def _collect_reflections(self, relationship_type=None):
        """Collect reflection text for completed relationships, optionally filtered by type."""
        collected = []

        for index, relationship in enumerate(self.relationships):
            if relationship_type and relationship['type'] != relationship_type:
                continue
            if self.is_relationship_complete(index):
                prompts = (
                    self.POSITIVE_PROMPTS
                    if relationship['type'] == 'positive'
                    else self.CHALLENGING_PROMPTS
                )
                for prompt_index in range(len(prompts)):
                    collected.append(relationship['reflections'][prompt_index])

        return collected

    def _analyze_text(self, texts, themes):
        """
        Analyze a list of texts against the provided themes.
        Returns a dict with theme scores and top themes.
        """
        if not texts:
            return {'theme_scores': {}, 'top_themes': [], 'total_matches': 0}

        theme_scores = {}

        for theme_id, theme_data in themes.items():
            score = 0

            # Duplicate keywords in a theme definition must not double a score.
            unique_keywords = dict.fromkeys(
                keyword.lower() for keyword in theme_data['keywords']
            )
            for text in texts:
                for keyword in unique_keywords:
                    score += self._count_keyword_in_text(text, keyword)

            score = score * theme_data['weight']
            theme_scores[theme_id] = score

        total_matches = sum(theme_scores.values())
        if total_matches == 0:
            return {'theme_scores': theme_scores, 'top_themes': [], 'total_matches': 0}

        sorted_themes = sorted(theme_scores.items(), key=lambda x: x[1], reverse=True)
        matched_themes = [item for item in sorted_themes if item[1] > 0]
        significant_themes = [item for item in matched_themes if item[1] >= 3]

        # Prefer up to five well-supported themes. With sparse text, show up to
        # three actual matches. Include all themes tied at the cutoff rather
        # than choosing a winner based on dictionary insertion order.
        candidates = significant_themes if len(significant_themes) >= 3 else matched_themes
        target_count = 5 if len(significant_themes) >= 3 else 3
        if candidates:
            cutoff_index = min(target_count, len(candidates)) - 1
            cutoff_score = candidates[cutoff_index][1]
            top_themes = [
                theme_id for theme_id, score in candidates if score >= cutoff_score
            ]
        else:
            top_themes = []

        return {
            'theme_scores': theme_scores,
            'top_themes': top_themes,
            'total_matches': total_matches
        }

    def analyze_patterns(self):
        """
        Analyze reflections to detect positive values and frustrating traits.
        
        Returns:
            Dictionary with separate analyses for values and frustrations
        """
        values_text = self._collect_reflections('positive')
        frustrations_text = self._collect_reflections('challenging')

        return {
            'values': self._analyze_text(values_text, self.THEMES),
            'frustrations': self._analyze_text(frustrations_text, self.FRUSTRATION_THEMES)
        }
    
    def generate_summary(self, analysis_results):
        """
        Generate a narrative summary based on values and frustrations analysis.
        
        Args:
            analysis_results: The results from analyze_patterns()
             
        Returns:
            A string with the summary text
        """
        values = analysis_results.get('values', {})
        frustrations = analysis_results.get('frustrations', {})
        top_values = values.get('top_themes', [])
        top_frustrations = frustrations.get('top_themes', [])

        if not top_values and not top_frustrations:
            return "Complete more reflections to generate insights."

        def format_list(items):
            if len(items) == 1:
                return items[0]
            if len(items) == 2:
                return f"{items[0]} and {items[1]}"
            return f"{items[0]}, {items[1]}, and {items[2]}"

        summary_parts = []

        if top_values:
            value_names = [self.THEMES[t]['title'].lower() for t in top_values[:3]]
            summary_parts.append(
                f"You work best in teams that value {format_list(value_names)}."
            )

        if top_frustrations:
            frustration_names = [self.FRUSTRATION_THEMES[t]['title'].lower() for t in top_frustrations[:3]]
            summary_parts.append(
                f"You tend to disengage when you encounter {format_list(frustration_names)}."
            )

        if top_values:
            key_values = [self.THEMES[t]['title'].lower() for t in top_values[:3]]
            if len(key_values) >= 3:
                summary_parts.append(
                    f"Future environments that reward {', '.join(key_values[:-1])} and {key_values[-1]} "
                    "will likely bring out your best."
                )
            else:
                summary_parts.append(
                    f"Future environments that reward {format_list(key_values)} will likely bring out your best."
                )

        return ' '.join(summary_parts)
    
    def reset(self):
        """Clear all relationships."""
        self.relationships = []
    
    def get_total_relationships(self):
        """Get total number of relationships."""
        return len(self.relationships)
    
    def get_positive_count(self):
        """Get count of positive relationships."""
        return sum(1 for r in self.relationships if r['type'] == 'positive')
    
    def get_challenging_count(self):
        """Get count of challenging relationships."""
        return sum(1 for r in self.relationships if r['type'] == 'challenging')
