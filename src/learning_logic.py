"""
Learning Preferences Assessment - Logic Layer
Scoring and result interpretation.
"""

from learning_data import QUESTIONS, STYLES


class LearningPreferenceAssessment:
    """
    Manages the learning preferences assessment logic.
    Handles data structure, scoring calculations, and result interpretation.
    """

    STYLES = STYLES
    QUESTIONS = QUESTIONS

    def __init__(self):
        """Initialize the assessment with empty responses."""
        # Store responses as {question_index: option_index} for single selection
        self.responses = {}
    
    def set_response(self, question_index, option_index):
        """
        Set response for a specific question.
        
        Args:
            question_index: The question number (0-15)
            option_index: The selected option index (0-3)
        """
        if (
            not isinstance(question_index, int)
            or isinstance(question_index, bool)
            or not 0 <= question_index < len(self.QUESTIONS)
        ):
            raise ValueError("Invalid question index")

        options = self.QUESTIONS[question_index]["options"]
        if (
            not isinstance(option_index, int)
            or isinstance(option_index, bool)
            or not 0 <= option_index < len(options)
        ):
            raise ValueError(f"Invalid option index for question {question_index}")

        self.responses[question_index] = option_index
    
    def get_response(self, question_index):
        """
        Get the response for a specific question.
        
        Args:
            question_index: The question number (0-15)
            
        Returns:
            The selected option index or None if not answered
        """
        if (
            not isinstance(question_index, int)
            or isinstance(question_index, bool)
            or not 0 <= question_index < len(self.QUESTIONS)
        ):
            return None

        option_index = self.responses.get(question_index)
        if (
            isinstance(option_index, int)
            and not isinstance(option_index, bool)
            and 0 <= option_index < len(self.QUESTIONS[question_index]["options"])
        ):
            return option_index
        return None
    
    def calculate_style_scores(self):
        """
        Calculate the total score for each learning style.
        
        Returns:
            Dictionary of {style: count} where count is out of 16
        """
        scores = {"V": 0, "A": 0, "R": 0, "K": 0}
        
        for question_index, question in enumerate(self.QUESTIONS):
            option_index = self.get_response(question_index)
            if (
                isinstance(option_index, int)
                and not isinstance(option_index, bool)
                and 0 <= option_index < len(question["options"])
            ):
                style = question["options"][option_index]["style"]
                if style in scores:
                    scores[style] += 1
        
        return scores
    
    def get_dominant_style(self):
        """
        Determine the dominant learning style(s).
        
        Returns:
            Tuple of (style_type, styles) where:
            - style_type is "Dominant", "Bimodal", or "Multimodal"
            - styles is a list of the dominant style codes
        """
        scores = self.calculate_style_scores()
        
        # Sort by score descending
        sorted_styles = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        
        max_score = sorted_styles[0][1]
        
        # If no responses yet
        if max_score == 0:
            return "Incomplete", []
        
        # Count how many styles have the max score or are close to it
        threshold = max_score - 2  # Within 2 points is considered close
        top_styles = [style for style, score in sorted_styles if score >= threshold and score > 0]
        
        if len(top_styles) == 1:
            return "Dominant", top_styles
        elif len(top_styles) == 2:
            return "Bimodal", top_styles
        else:
            return "Multimodal", top_styles
    
    def get_completion_status(self):
        """
        Get the completion status of the assessment.
        
        Returns:
            Tuple of (answered_count, total_questions)
        """
        answered = sum(
            self.get_response(question_index) is not None
            for question_index in range(len(self.QUESTIONS))
        )
        total = len(self.QUESTIONS)
        return answered, total
    
    def is_complete(self):
        """
        Check if all questions have been answered.
        
        Returns:
            True if all questions answered, False otherwise
        """
        answered, total = self.get_completion_status()
        return answered == total
    
    def get_interpretation(self, style_type):
        """
        Get interpretation text based on the style type.
        
        Args:
            style_type: "Dominant", "Bimodal", or "Multimodal"
            
        Returns:
            Interpretation text
        """
        interpretations = {
            "Dominant": "One style clearly highest → You prefer this mode most of the time.",
            "Bimodal": "Two close scores → You flex comfortably between two learning modes.",
            "Multimodal": "Three or four similar scores → You adapt easily; variety helps you learn best."
        }
        return interpretations.get(style_type, "")
    
    def reset(self):
        """Reset all responses."""
        self.responses = {}
