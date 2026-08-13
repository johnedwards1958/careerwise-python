"""
Preferred Work Environment Assessment - Logic Layer
Scoring and interpretation logic.
"""

from environment_data import FACTORS, PROFILES, REFLECTION_PROMPTS


class EnvironmentAssessment:
    """
    Manages the preferred work environment assessment logic.
    Handles data structure, scoring calculations, and result interpretation.
    """

    FACTORS = FACTORS
    PROFILES = PROFILES
    REFLECTION_PROMPTS = REFLECTION_PROMPTS

    def __init__(self):
        """Initialize the assessment with empty responses."""
        self.responses = {}  # Format: {factor_index: option ('A', 'B', or 'C')}
    
    def set_response(self, factor_index, option):
        """
        Set a response for a specific factor.
        
        Args:
            factor_index: The factor number (0-11)
            option: The selected option ('A', 'B', or 'C')
        """
        # Reject bool explicitly: False and True otherwise compare equal to the
        # integer factor keys 0 and 1.
        if type(factor_index) is not int or factor_index not in self.FACTORS:
            raise ValueError(f"Invalid factor index: {factor_index}")
        if option not in ['A', 'B', 'C']:
            raise ValueError(f"Invalid option: {option}. Must be 'A', 'B', or 'C'")
        self.responses[factor_index] = option
    
    def get_response(self, factor_index):
        """
        Get the response for a specific factor.
        
        Returns:
            The selected option ('A', 'B', or 'C') or None if not answered
        """
        return self.responses.get(factor_index)
    
    def get_pattern_counts(self):
        """
        Count how many times each option was selected.
        
        Returns:
            Dictionary with counts: {'A': count, 'B': count, 'C': count}
        """
        counts = {'A': 0, 'B': 0, 'C': 0}
        # Count only the defined factor slots. This keeps externally supplied or
        # stale response keys from changing a result.
        for factor_index in self.FACTORS:
            option = self.responses.get(factor_index)
            if option in counts:
                counts[option] += 1
        return counts

    def get_dominant_patterns(self):
        """
        Return every joint-highest response pattern.

        Returns:
            A list of ``(option, count, profile_key)`` tuples, or an empty list
            while the assessment is incomplete.
        """
        if not self.is_complete():
            return []

        counts = self.get_pattern_counts()
        dominant_count = max(counts.values())
        profile_map = {
            'A': 'structured',
            'B': 'balanced',
            'C': 'autonomous',
        }
        return [
            (option, dominant_count, profile_map[option])
            for option in ('A', 'B', 'C')
            if counts[option] == dominant_count
        ]
    
    def get_dominant_pattern(self):
        """
        Determine which pattern (A, B, or C) is most dominant.
        
        Returns:
            Tuple of (dominant_option, count, profile_key), or None if the
            assessment is incomplete or has a tie. Use
            :meth:`get_dominant_patterns` when joint-highest patterns matter.
        """
        dominant_patterns = self.get_dominant_patterns()
        if len(dominant_patterns) != 1:
            return None

        return dominant_patterns[0]
    
    def get_interpretation(self):
        """
        Get the interpretation based on the dominant pattern.
        
        Returns:
            Dictionary with profile information or None if incomplete
        """
        dominant_patterns = self.get_dominant_patterns()
        if not dominant_patterns:
            return None

        dominant_options = [item[0] for item in dominant_patterns]
        count = dominant_patterns[0][1]
        profile_keys = [item[2] for item in dominant_patterns]

        if len(dominant_patterns) == 1:
            profile_key = profile_keys[0]
            profile = self.PROFILES[profile_key]
            title = profile['title']
            description = profile['description']
            typical_pattern = profile['typical_pattern']
            dominant_option = dominant_options[0]
        else:
            profile_key = 'mixed'
            profile_titles = [self.PROFILES[key]['title'] for key in profile_keys]
            if len(profile_titles) == 2:
                title_list = f"{profile_titles[0]} and {profile_titles[1]}"
                option_list = f"Options {dominant_options[0]} and {dominant_options[1]}"
            else:
                title_list = f"{', '.join(profile_titles[:-1])}, and {profile_titles[-1]}"
                option_list = f"Options {', '.join(dominant_options[:-1])}, and {dominant_options[-1]}"
            title = f"Mixed: {title_list}"
            description = (
                "Your selections are evenly split across these profiles. Rather "
                "than forcing a single label, review the individual factors to "
                "identify which conditions matter most in different situations."
            )
            typical_pattern = f"Joint-highest pattern: {option_list}"
            dominant_option = None

        return {
            'profile_key': profile_key,
            'profile_keys': profile_keys,
            'title': title,
            'description': description,
            'typical_pattern': typical_pattern,
            'dominant_option': dominant_option,
            'dominant_options': dominant_options,
            'count': count,
            'total': len(self.FACTORS)
        }
    
    def is_complete(self):
        """
        Check if all factors have been answered.
        
        Returns:
            True if all 12 factors answered, False otherwise
        """
        return all(
            self.responses.get(factor_index) in ('A', 'B', 'C')
            for factor_index in self.FACTORS
        )
    
    def get_completion_status(self):
        """
        Get the completion status of the assessment.
        
        Returns:
            Tuple of (answered_count, total_count, percentage)
        """
        answered = sum(
            1
            for factor_index in self.FACTORS
            if self.responses.get(factor_index) in ('A', 'B', 'C')
        )
        total = len(self.FACTORS)
        percentage = (answered / total * 100) if total > 0 else 0
        return answered, total, percentage
    
    def reset(self):
        """Clear all responses."""
        self.responses = {}
