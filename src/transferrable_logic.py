"""
Transferrable Assessment - Logic Layer
Scoring and result interpretation logic.
"""

from transferrable_data import QUESTIONS, DOMAINS, HIGHLY_TRANSFERABLE, MODERATELY_TRANSFERABLE, DEVELOPING


class TransferrableSkillsAssessment:
    """Assessment logic container."""

    QUESTIONS = QUESTIONS
    DOMAINS = DOMAINS
    HIGHLY_TRANSFERABLE = HIGHLY_TRANSFERABLE
    MODERATELY_TRANSFERABLE = MODERATELY_TRANSFERABLE
    DEVELOPING = DEVELOPING

    def __init__(self):
        """Initialize the assessment with empty responses."""
        self.responses = {}  # Format: {question_index: score}
        
    def set_response(self, question_index, score):
        """
        Set a response for a specific question.
        
        Args:
            question_index: The question number (0-based)
            score: The score value (1-5)
        """
        if (
            isinstance(question_index, bool)
            or not isinstance(question_index, int)
            or question_index not in range(len(self.QUESTIONS))
        ):
            raise ValueError(
                f"Question index must be between 0 and {len(self.QUESTIONS) - 1}"
            )

        if isinstance(score, bool) or not isinstance(score, int) or score not in range(1, 6):
            raise ValueError("Score must be between 1 and 5")
        self.responses[question_index] = score
    
    def get_response(self, question_index):
        """
        Get the response for a specific question.
        
        Returns:
            The score (1-5) or None if not answered
        """
        return self.responses.get(question_index)
    
    def calculate_domain_score(self, domain_id):
        """
        Calculate the total score for a domain.
        
        Args:
            domain_id: The domain identifier
            
        Returns:
            Tuple of (score, max_possible_score, answered_count, total_questions)
        """
        domain = self.DOMAINS[domain_id]
        question_indices = domain["questions"]
        total_questions = len(question_indices)
        score = 0
        answered_count = 0
        
        for idx in question_indices:
            response = self.get_response(idx)
            if response is not None:
                score += response
                answered_count += 1
        
        max_possible = total_questions * 5
        return score, max_possible, answered_count, total_questions
    
    def calculate_overall_score(self):
        """
        Calculate the total score across all questions.
        
        Returns:
            Tuple of (score, max_possible_score, completion_percentage)
        """
        total_score = 0
        total_questions = len(self.QUESTIONS)
        answered_questions = 0
        
        for i in range(total_questions):
            response = self.get_response(i)
            if response is not None:
                total_score += response
                answered_questions += 1
        
        max_possible = total_questions * 5
        completion_percentage = (answered_questions / total_questions * 100) if total_questions > 0 else 0
        
        return total_score, max_possible, completion_percentage
    
    def get_overall_status(self):
        """
        Determine the overall assessment status.
        
        Returns:
            'highly_transferable', 'moderately_transferable', 'developing', 'narrowly_specialised', or 'incomplete'
        """
        score, max_possible, completion = self.calculate_overall_score()
        
        if completion < 100:
            return 'incomplete'
        elif score >= self.HIGHLY_TRANSFERABLE:
            return 'highly_transferable'
        elif score >= self.MODERATELY_TRANSFERABLE:
            return 'moderately_transferable'
        elif score >= self.DEVELOPING:
            return 'developing'
        else:
            return 'narrowly_specialised'
    
    def get_status_description(self, status):
        """
        Get a descriptive text for a status.
        
        Args:
            status: The status identifier
            
        Returns:
            A descriptive string
        """
        descriptions = {
            'highly_transferable': 'Highly transferable — A strong portfolio of abilities that fit almost any role or sector.',
            'moderately_transferable': 'Moderately transferable — Solid, adaptable skills. Target roles that build on these strengths.',
            'developing': 'Developing — Many skills are emerging; focus on strengthening weaker domains.',
            'narrowly_specialised': 'Narrowly specialised — Your skills may be job-specific. Broaden your competencies for mobility.',
            'incomplete': 'Assessment not yet complete. Please answer all questions.'
        }
        return descriptions.get(status, status)
    
    def reset(self):
        """Clear all responses."""
        self.responses = {}
    
    def is_complete(self):
        """Check if all questions have been answered."""
        return all(
            self.get_response(question_index) is not None
            for question_index in range(len(self.QUESTIONS))
        )
    
    def get_completion_percentage(self):
        """Get the percentage of questions answered."""
        total_questions = len(self.QUESTIONS)
        answered = sum(
            self.get_response(question_index) is not None
            for question_index in range(total_questions)
        )
        return (answered / total_questions * 100) if total_questions > 0 else 0

