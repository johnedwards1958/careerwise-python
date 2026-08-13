"""
Preferred Work Environment Assessment - Data Layer
Assessment factors, profile definitions, and reflection prompts.
"""

# Work environment factors with three options each
FACTORS = {
    0: {
        "name": "Work Pace",
        "options": {
            "A": "Fast-paced",
            "B": "Moderate",
            "C": "Slow-paced"
        }
    },
    1: {
        "name": "Structure",
        "options": {
            "A": "Highly structured",
            "B": "Some structure",
            "C": "Unstructured"
        }
    },
    2: {
        "name": "Collaboration",
        "options": {
            "A": "Team-based",
            "B": "Mix of team & solo",
            "C": "Independent"
        }
    },
    3: {
        "name": "Supervision",
        "options": {
            "A": "Close supervision",
            "B": "Occasional guidance",
            "C": "Full autonomy"
        }
    },
    4: {
        "name": "Decision-Making",
        "options": {
            "A": "Clear rules & hierarchy",
            "B": "Shared decisions",
            "C": "Free & informal"
        }
    },
    5: {
        "name": "Work Setting",
        "options": {
            "A": "City centre / corporate",
            "B": "No preference",
            "C": "Suburban / remote"
        }
    },
    6: {
        "name": "Noise Level",
        "options": {
            "A": "Lively & energetic",
            "B": "Balanced",
            "C": "Quiet & calm"
        }
    },
    7: {
        "name": "Work Hours",
        "options": {
            "A": "Fixed & predictable",
            "B": "Some flexibility",
            "C": "Variable / project-based"
        }
    },
    8: {
        "name": "Innovation Level",
        "options": {
            "A": "Traditional / established",
            "B": "Moderately innovative",
            "C": "Highly experimental"
        }
    },
    9: {
        "name": "Goal Orientation",
        "options": {
            "A": "Short-term results",
            "B": "Balance of both",
            "C": "Long-term vision"
        }
    },
    10: {
        "name": "Team Size",
        "options": {
            "A": "Large teams",
            "B": "Medium",
            "C": "Small / solo"
        }
    },
    11: {
        "name": "Risk Tolerance",
        "options": {
            "A": "Risk-averse",
            "B": "Moderate",
            "C": "High-risk / dynamic"
        }
    }
}

# Interpretation profiles
PROFILES = {
    "structured": {
        "title": "Structured / Team-centred",
        "description": "You tend to prefer clear expectations, established ways of working, active shared settings, and defined accountability. Larger, team-based organisations and operational environments may fit well.",
        "typical_pattern": "Mostly Option A"
    },
    "balanced": {
        "title": "Balanced / Adaptive",
        "description": "Comfortable in moderately paced, mixed environments. Can adjust between structure and freedom.",
        "typical_pattern": "Mostly Option B"
    },
    "autonomous": {
        "title": "Autonomous / Flexible",
        "description": "You tend to prefer independence, informal decision-making, small or remote settings, and freedom to experiment or organise work around projects and longer-term goals.",
        "typical_pattern": "Mostly Option C"
    }
}

# Reflection prompts
REFLECTION_PROMPTS = [
    "Which aspects of your current or past work environments matched your preferences?",
    "Where were the biggest mismatches?",
    "If you could change one environmental factor in your next job, what would it be?",
    "How might you adapt if you can't have your ideal environment immediately?"
]
