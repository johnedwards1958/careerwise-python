"""
Priorities Assessment - Logic Layer
Scoring and result interpretation logic.
"""

from priorities_data import ANCHORS


class PrioritiesAssessment:
    """Assessment logic container."""

    ANCHORS = ANCHORS

    def __init__(self):
        """Initialize the assessment with empty responses."""
        self.responses = {}  # Format: {(anchor_id, question_index): rating}
    
    def set_response(self, anchor_id, question_index, rating):
        """
        Set a response for a specific question.
        
        Args:
            anchor_id: The anchor identifier (e.g., 'technical_functional')
            question_index: The question number within the anchor (0-based)
            rating: The rating value (1-5)
        """
        if anchor_id not in self.ANCHORS:
            raise ValueError(f"Invalid anchor: {anchor_id}")

        question_count = len(self.ANCHORS[anchor_id]["questions"])
        if type(question_index) is not int or not 0 <= question_index < question_count:
            raise ValueError(f"Invalid question index: {question_index}")

        # bool is a subclass of int, so use an exact type check rather than only
        # testing membership in range(1, 6).
        if type(rating) is not int or rating not in range(1, 6):
            raise ValueError("Rating must be between 1 and 5")
        self.responses[(anchor_id, question_index)] = rating
    
    def get_response(self, anchor_id, question_index):
        """
        Get the response for a specific question.
        
        Returns:
            The rating (1-5) or None if not answered
        """
        return self.responses.get((anchor_id, question_index))
    
    def calculate_anchor_score(self, anchor_id):
        """
        Calculate the total score for an anchor.
        
        Args:
            anchor_id: The anchor identifier
            
        Returns:
            Tuple of (score, max_possible_score, answered_count, total_questions)
        """
        anchor = self.ANCHORS[anchor_id]
        total_questions = len(anchor["questions"])
        score = 0
        answered_count = 0
        
        for i in range(total_questions):
            response = self.get_response(anchor_id, i)
            if response is not None:
                score += response
                answered_count += 1
        
        max_possible = total_questions * 5
        return score, max_possible, answered_count, total_questions
    
    def is_anchor_complete(self, anchor_id):
        """
        Check if all questions in an anchor have been answered.
        
        Returns:
            True if all questions answered, False otherwise
        """
        anchor = self.ANCHORS[anchor_id]
        total_questions = len(anchor["questions"])
        
        for i in range(total_questions):
            if self.get_response(anchor_id, i) is None:
                return False
        
        return True
    
    def get_all_anchor_scores(self):
        """
        Get scores for all anchors.
        
        Returns:
            Dictionary of {anchor_id: score}
        """
        scores = {}
        for anchor_id in self.ANCHORS:
            score, _, _, _ = self.calculate_anchor_score(anchor_id)
            scores[anchor_id] = score
        
        return scores
    
    def get_top_anchors(self, count=2):
        """
        Get the top N anchors by score.
        
        Args:
            count: Number of top anchors to return
            
        Returns:
            List of tuples (anchor_id, score) sorted by score descending.
            Anchors tied with the item at the requested cutoff are included so
            an insertion-order accident cannot decide a user's result.
        """
        if type(count) is not int or count < 0:
            raise ValueError("Count must be a non-negative integer")
        if count == 0:
            return []

        scores = self.get_all_anchor_scores()
        sorted_anchors = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        if count >= len(sorted_anchors):
            return sorted_anchors

        cutoff_score = sorted_anchors[count - 1][1]
        return [item for item in sorted_anchors if item[1] >= cutoff_score]
    
    def is_complete(self):
        """Check if all questions have been answered."""
        for anchor_id in self.ANCHORS:
            if not self.is_anchor_complete(anchor_id):
                return False
        return True
    
    def get_completion_status(self):
        """
        Get the completion status across all anchors.
        
        Returns:
            Tuple of (completed_anchors, total_anchors, percentage)
        """
        completed = sum(1 for anchor_id in self.ANCHORS if self.is_anchor_complete(anchor_id))
        total = len(self.ANCHORS)
        percentage = (completed / total * 100) if total > 0 else 0
        
        return completed, total, percentage
    
    def reset(self):
        """Clear all responses."""
        self.responses = {}

