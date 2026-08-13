"""
Teams Assessment - Logic Layer
Scoring and result interpretation logic.
"""

from math import isclose

from teams_data import ROLES, SECTIONS, ROLE_MAPPING, POINTS_PER_SECTION


class TeamsAssessment:
    """Assessment logic container."""

    ROLES = ROLES
    SECTIONS = SECTIONS
    ROLE_MAPPING = ROLE_MAPPING
    POINTS_PER_SECTION = POINTS_PER_SECTION

    def __init__(self):
        """Initialize the assessment with empty responses."""
        # Store 1-5 ratings: {(section_id, question_index): rating}
        self.ratings = {}
    
    def set_rating(self, section_id, question_index, rating):
        """
        Set rating for a specific question.
        
        Args:
            section_id: Section identifier (A-G)
            question_index: Question index within section (0-based)
            rating: Rating value (1-5)
        """
        if section_id not in self.SECTIONS:
            raise ValueError(f"Unknown section: {section_id}")

        question_count = len(self.SECTIONS[section_id]["questions"])
        if (
            isinstance(question_index, bool)
            or not isinstance(question_index, int)
            or question_index not in range(question_count)
        ):
            raise ValueError(
                f"Question index must be between 0 and {question_count - 1} "
                f"for section {section_id}"
            )

        if isinstance(rating, bool) or not isinstance(rating, int) or rating not in range(1, 6):
            raise ValueError("Rating must be between 1 and 5")
        
        self.ratings[(section_id, question_index)] = rating
    
    def get_rating(self, section_id, question_index):
        """
        Get rating for a specific question.
        
        Returns:
            Rating (1-5) or None if not set
        """
        return self.ratings.get((section_id, question_index))
    
    def get_section_ratings(self, section_id):
        """
        Get all ratings for a section.
        
        Returns:
            List of ratings for each question in the section
        """
        num_questions = len(self.SECTIONS[section_id]["questions"])
        return [self.get_rating(section_id, i) for i in range(num_questions)]
    
    def convert_ratings_to_allocations(self, section_id):
        """
        Convert 1-5 ratings to equivalent 10-point allocations for a section.
        
        Args:
            section_id: Section identifier (A-G)
            
        Returns:
            List of point allocations (floats) that sum to 10, or None if section incomplete
        """
        ratings = self.get_section_ratings(section_id)
        
        # Check if all questions are answered
        if any(rating is None for rating in ratings):
            return None
        
        # Calculate total rating points
        total_rating = sum(ratings)
        
        section_points = float(self.POINTS_PER_SECTION)

        # Handle edge case where all ratings are 0 (shouldn't happen with 1-5 scale)
        if total_rating == 0:
            # Distribute evenly
            return [section_points / len(ratings)] * len(ratings)
        
        # Convert to proportional allocations that sum to the section budget
        allocations = [
            (rating / total_rating) * section_points for rating in ratings
        ]
        
        # Ensure the exact configured total despite floating point precision
        allocation_sum = sum(allocations)
        if allocation_sum != section_points:
            # Adjust the largest allocation to make the sum exact
            max_index = allocations.index(max(allocations))
            allocations[max_index] += section_points - allocation_sum
        
        return allocations
    
    def get_allocation(self, section_id, question_index):
        """
        Get effective point allocation for a specific question.
        Converts from 1-5 rating to equivalent point allocation.
        
        Returns:
            Points allocated (0-10) or 0 if not rated
        """
        allocations = self.convert_ratings_to_allocations(section_id)
        if allocations is None:
            return 0
        return allocations[question_index]
    
    def get_section_total(self, section_id):
        """
        Calculate total points allocated in a section.
        
        Returns:
            Total points allocated (should be 10 when complete)
        """
        allocations = self.convert_ratings_to_allocations(section_id)
        if allocations is None:
            return 0
        return sum(allocations)
    
    def is_section_valid(self, section_id):
        """
        Check if a section has all questions answered (equivalent to having 10 points allocated).
        
        Returns:
            True if all questions in section are answered
        """
        ratings = self.get_section_ratings(section_id)
        return all(rating is not None for rating in ratings)
    
    def is_section_complete(self, section_id):
        """
        Check if a section is considered complete.
        
        Returns:
            True if all questions are answered
        """
        return self.is_section_valid(section_id)
    
    def calculate_role_scores(self):
        """
        Calculate total score for each role across all sections.
        Uses converted allocations from 1-5 ratings.
        
        Returns:
            Dictionary mapping role_id -> total_score
        """
        scores = {role_id: 0 for role_id in self.ROLES}
        
        for section_id in self.SECTIONS:
            allocations = self.convert_ratings_to_allocations(section_id)
            if allocations is not None:
                for question_index, points in enumerate(allocations):
                    # Convert 0-based index to 1-based for mapping lookup
                    question_number = question_index + 1
                    role_id = self.ROLE_MAPPING[section_id][question_number]
                    scores[role_id] += points
        
        return scores
    
    def get_top_roles(self, n=2, include_ties=True):
        """
        Get the top N roles by score without arbitrarily breaking cutoff ties.
        
        Args:
            n: Number of top roles to return (default 2 for primary and secondary)
            include_ties: Include every role tied with the final selected role
            
        Returns:
            List of tuples (role_id, score) sorted by score descending
        """
        if isinstance(n, bool) or not isinstance(n, int) or n < 0:
            raise ValueError("n must be a non-negative integer")
        if not isinstance(include_ties, bool):
            raise ValueError("include_ties must be a boolean")
        if n == 0:
            return []

        scores = self.calculate_role_scores()
        sorted_roles = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        selected = sorted_roles[:n]
        if not include_ties or n >= len(sorted_roles):
            return selected

        cutoff_score = selected[-1][1]
        return [
            role
            for role in sorted_roles
            if role[1] > cutoff_score
            or isclose(role[1], cutoff_score, rel_tol=1e-9, abs_tol=1e-9)
        ]

    def get_ranked_role_groups(self):
        """Return roles grouped by score so tied results share the same rank."""
        sorted_roles = sorted(
            self.calculate_role_scores().items(),
            key=lambda item: item[1],
            reverse=True,
        )
        ranked_groups = []

        for role in sorted_roles:
            if not ranked_groups or not isclose(
                role[1], ranked_groups[-1][0][1], rel_tol=1e-9, abs_tol=1e-9
            ):
                ranked_groups.append([])
            ranked_groups[-1].append(role)

        return ranked_groups
    
    def get_completion_status(self):
        """
        Get overall completion status.
        
        Returns:
            Tuple of (completed_sections, total_sections, completion_percentage)
        """
        total_sections = len(self.SECTIONS)
        completed_sections = sum(1 for section_id in self.SECTIONS if self.is_section_complete(section_id))
        completion_percentage = (completed_sections / total_sections * 100) if total_sections > 0 else 0
        
        return completed_sections, total_sections, completion_percentage
    
    def is_complete(self):
        """
        Check if all sections are complete.
        
        Returns:
            True if all sections have valid allocations
        """
        return all(self.is_section_complete(section_id) for section_id in self.SECTIONS)
    
    def reset(self):
        """Clear all ratings."""
        self.ratings = {}
    
    def get_section_allocations(self, section_id):
        """
        Get effective allocations for a section (converted from ratings).
        
        Returns:
            List of point allocations for each question in the section
        """
        allocations = self.convert_ratings_to_allocations(section_id)
        if allocations is None:
            num_questions = len(self.SECTIONS[section_id]["questions"])
            return [0] * num_questions
        return allocations
