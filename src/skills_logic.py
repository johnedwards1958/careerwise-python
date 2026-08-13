"""
Job Search Skills Assessment - Logic Layer
Scoring and result interpretation.
"""

from skills_data import (
    CATEGORIES as SKILLS_CATEGORIES,
    CATEGORY_FEEDBACK,
    DETAILED_FEEDBACK,
)

def get_detailed_feedback(category_id, question_index, rating):
    """
    Get specific feedback for a question based on the rating given.
    
    Args:
        category_id: The category identifier (e.g., 'skills_abilities')
        question_index: The question number within the category (0-based)
        rating: The score value (1-5)
        
    Returns:
        Detailed feedback text specific to this question and rating
    """
    try:
        return DETAILED_FEEDBACK[category_id][question_index][rating]
    except (KeyError, TypeError):
        # Fallback if feedback not found
        return f"Continue working on this area to strengthen your job search skills."


def get_category_feedback(category_id, status):
    """
    Get helpful feedback and recommendations for a category based on status.
    
    Args:
        category_id: The category identifier (e.g., 'skills_abilities')
        status: The category status (e.g., 'good', 'needs_improvement')
        
    Returns:
        Feedback text for this category and status
    """
    return CATEGORY_FEEDBACK.get(category_id, {}).get(status, "Continue to develop this area.")


class SkillsAssessment:
    """
    Manages the job search skills assessment logic.
    Handles data structure, scoring calculations, and result interpretation.
    """

    CATEGORIES = SKILLS_CATEGORIES

    # Overall scoring thresholds
    OVERALL_GOOD_THRESHOLD = 151
    OVERALL_NEEDS_IMPROVEMENT_THRESHOLD = 126

    def __init__(self):
        """Initialize the assessment with empty responses."""
        self.responses = {}  # Format: {(category_id, question_index): score}
        
    def set_response(self, category_id, question_index, score):
        """
        Set a response for a specific question.
        
        Args:
            category_id: The category identifier (e.g., 'skills_abilities')
            question_index: The question number within the category (0-based)
            score: The score value (1-5)
        """
        if category_id not in self.CATEGORIES:
            raise ValueError(f"Unknown category: {category_id}")

        question_count = len(self.CATEGORIES[category_id]["questions"])
        if (
            isinstance(question_index, bool)
            or not isinstance(question_index, int)
            or question_index not in range(question_count)
        ):
            raise ValueError(
                f"Question index must be between 0 and {question_count - 1} "
                f"for category {category_id}"
            )

        if isinstance(score, bool) or not isinstance(score, int) or score not in range(1, 6):
            raise ValueError("Score must be between 1 and 5")
        self.responses[(category_id, question_index)] = score
    
    def get_response(self, category_id, question_index):
        """
        Get the response for a specific question.
        
        Returns:
            The score (1-5) or None if not answered
        """
        return self.responses.get((category_id, question_index))
    
    def calculate_category_score(self, category_id):
        """
        Calculate the total score for a category.
        
        Args:
            category_id: The category identifier
            
        Returns:
            Tuple of (score, max_possible_score, answered_count, total_questions)
        """
        category = self.CATEGORIES[category_id]
        total_questions = len(category["questions"])
        score = 0
        answered_count = 0
        
        for i in range(total_questions):
            response = self.get_response(category_id, i)
            if response is not None:
                score += response
                answered_count += 1
        
        max_possible = total_questions * 5
        return score, max_possible, answered_count, total_questions
    
    def get_category_status(self, category_id):
        """
        Determine if a category score is good or needs improvement.
        
        Returns:
            'good', 'needs_improvement', 'incomplete', or 'not_started'
        """
        score, max_possible, answered_count, total_questions = self.calculate_category_score(category_id)
        category = self.CATEGORIES[category_id]
        
        if answered_count == 0:
            return 'not_started'
        elif answered_count < total_questions:
            return 'incomplete'
        elif score >= category["good_threshold"]:
            return 'good'
        elif score <= category["needs_improvement_threshold"]:
            return 'needs_improvement'
        else:
            return 'acceptable'
    
    def calculate_overall_score(self):
        """
        Calculate the total score across all categories.
        
        Returns:
            Tuple of (score, max_possible_score, completion_percentage)
        """
        total_score = 0
        total_questions = 0
        answered_questions = 0
        
        for category_id in self.CATEGORIES:
            score, max_possible, answered_count, question_count = self.calculate_category_score(category_id)
            total_score += score
            total_questions += question_count
            answered_questions += answered_count
        
        max_possible = total_questions * 5
        completion_percentage = (answered_questions / total_questions * 100) if total_questions > 0 else 0
        
        return total_score, max_possible, completion_percentage
    
    def get_overall_status(self):
        """
        Determine the overall assessment status.
        
        Returns:
            'excellent', 'good', 'needs_improvement', or 'incomplete'
        """
        score, max_possible, completion = self.calculate_overall_score()
        
        if completion < 100:
            return 'incomplete'
        elif score >= self.OVERALL_GOOD_THRESHOLD:
            return 'excellent'
        elif score <= self.OVERALL_NEEDS_IMPROVEMENT_THRESHOLD:
            return 'needs_improvement'
        else:
            return 'good'
    
    def reset(self):
        """Clear all responses."""
        self.responses = {}
    
    def is_complete(self):
        """Check if all questions have been answered."""
        return all(
            self.get_response(category_id, question_index) is not None
            for category_id, category in self.CATEGORIES.items()
            for question_index in range(len(category["questions"]))
        )
    
    def get_completion_percentage(self):
        """Get the percentage of questions answered."""
        total_questions = sum(len(cat["questions"]) for cat in self.CATEGORIES.values())
        answered = sum(
            self.get_response(category_id, question_index) is not None
            for category_id, category in self.CATEGORIES.items()
            for question_index in range(len(category["questions"]))
        )
        return (answered / total_questions * 100) if total_questions > 0 else 0

