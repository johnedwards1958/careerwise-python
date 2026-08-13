"""
Influence Archetypes Assessment - Logic Layer
Scoring and result interpretation.
"""

from archetypes_data import ARCHETYPE_INFO, CLUSTERS, STATEMENTS


class InfluenceArchetypesAssessment:
    """
    Manages the influence archetypes assessment logic.
    Handles data structure, scoring calculations, and result interpretation.
    """

    STATEMENTS = STATEMENTS
    CLUSTERS = CLUSTERS
    ARCHETYPE_INFO = ARCHETYPE_INFO

    def __init__(self):
        """Initialize the assessment with empty responses."""
        # Store responses as {archetype: {statement_index: rating}}
        self.responses = {archetype: {} for archetype in self.STATEMENTS.keys()}

    @staticmethod
    def _is_valid_rating(rating):
        """Return whether a value is a valid stored Likert rating."""
        return (
            isinstance(rating, int)
            and not isinstance(rating, bool)
            and rating in range(1, 6)
        )
    
    def set_response(self, archetype, statement_index, rating):
        """
        Set a response for a specific statement.
        
        Args:
            archetype: The archetype name
            statement_index: Index of the statement (0-2)
            rating: Rating value (1-5)
        """
        if archetype not in self.STATEMENTS:
            raise ValueError(f"Invalid archetype: {archetype}")
        if (
            not isinstance(statement_index, int)
            or isinstance(statement_index, bool)
            or not 0 <= statement_index < len(self.STATEMENTS[archetype])
        ):
            raise ValueError(f"Invalid statement index for archetype {archetype}")
        if not self._is_valid_rating(rating):
            raise ValueError("Rating must be an integer between 1 and 5")

        self.responses[archetype][statement_index] = rating
    
    def get_response(self, archetype, statement_index):
        """
        Get the response for a specific statement.
        
        Args:
            archetype: The archetype name
            statement_index: Index of the statement (0-2)
            
        Returns:
            The rating value or None if not answered
        """
        if archetype in self.responses:
            rating = self.responses[archetype].get(statement_index)
            return rating if self._is_valid_rating(rating) else None
        return None
    
    def calculate_archetype_score(self, archetype):
        """
        Calculate the score for a specific archetype (average of 3 statements).
        
        Args:
            archetype: The archetype name
            
        Returns:
            Tuple of (average_score, answered_count)
        """
        if archetype not in self.STATEMENTS or archetype not in self.responses:
            return 0.0, 0
        
        answered = []
        for statement_index in range(len(self.STATEMENTS[archetype])):
            rating = self.get_response(archetype, statement_index)
            if self._is_valid_rating(rating):
                answered.append(rating)
        
        if not answered:
            return 0.0, 0
        
        return sum(answered) / len(answered), len(answered)
    
    def calculate_all_archetype_scores(self):
        """
        Calculate scores for all archetypes.
        
        Returns:
            Dictionary of {archetype: average_score}
        """
        scores = {}
        for archetype in self.STATEMENTS.keys():
            score, _ = self.calculate_archetype_score(archetype)
            scores[archetype] = score
        return scores
    
    def calculate_cluster_scores(self):
        """
        Calculate average scores for each cluster.
        
        Returns:
            Dictionary of {cluster: average_score}
        """
        cluster_scores = {}
        
        for cluster, archetypes in self.CLUSTERS.items():
            archetype_scores = []
            for archetype in archetypes:
                score, answered = self.calculate_archetype_score(archetype)
                if answered > 0:
                    archetype_scores.append(score)
            
            if archetype_scores:
                cluster_scores[cluster] = sum(archetype_scores) / len(archetype_scores)
            else:
                cluster_scores[cluster] = 0.0
        
        return cluster_scores
    
    def get_top_archetypes(self, count=2, include_ties=True):
        """
        Get the top N archetypes based on scores.
        
        Args:
            count: Number of score positions to return
            include_ties: Include every archetype tied at the final position
            
        Returns:
            List of tuples (archetype, score) sorted by score descending
        """
        if (
            not isinstance(count, int)
            or isinstance(count, bool)
            or count < 0
        ):
            raise ValueError("Count must be a non-negative integer")
        if not isinstance(include_ties, bool):
            raise ValueError("include_ties must be a boolean")
        if count == 0:
            return []

        scores = self.calculate_all_archetype_scores()
        sorted_archetypes = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        selected = sorted_archetypes[:count]
        if not include_ties or count >= len(sorted_archetypes):
            return selected

        cutoff_score = selected[-1][1]
        return [
            (archetype, score)
            for archetype, score in sorted_archetypes
            if score >= cutoff_score
        ]
    
    def get_completion_percentage(self):
        """
        Calculate the percentage of statements answered.
        
        Returns:
            Completion percentage (0-100)
        """
        total_statements = sum(len(statements) for statements in self.STATEMENTS.values())
        answered = sum(
            self._is_valid_rating(self.get_response(archetype, statement_index))
            for archetype, statements in self.STATEMENTS.items()
            for statement_index in range(len(statements))
        )
        return (answered / total_statements * 100) if total_statements > 0 else 0
    
    def is_complete(self):
        """
        Check if all statements have been answered.
        
        Returns:
            True if complete, False otherwise
        """
        return self.get_completion_percentage() == 100
    
    def reset(self):
        """Reset all responses."""
        self.responses = {archetype: {} for archetype in self.STATEMENTS.keys()}
