"""
Relationships Assessment - Data Layer
Static assessment data definitions.
"""


# Theme definitions with keyword clusters and descriptions (positive values)
THEMES = {
    "integrity": {
        "title": "Integrity",
        "description": "You value honesty, fairness, and loyalty in your professional relationships. Trust is your foundation for collaboration.",
        "keywords": [
            "honest", "honesty", "trustworthy", "trust", "loyal", "loyalty",
            "fair", "fairness", "sincere", "sincerity", "transparent", "transparency",
            "authentic", "authenticity", "truthful", "genuine", "straightforward",
            "ethical", "integrity", "principled", "candid", "open"
        ],
        "weight": 1.0
    },
    "accountability": {
        "title": "Accountability",
        "description": "You thrive with people who take ownership and deliver on commitments. You respect reliability above excuses.",
        "keywords": [
            "reliable", "reliability", "responsible", "responsibility", "accountable",
            "accountability", "ownership", "own", "deliver", "delivered", "follow through",
            "followed through", "commitment", "committed", "dependable", "consistent",
            "consistency", "kept promises", "kept word", "duty"
        ],
        "weight": 1.0
    },
    "performance": {
        "title": "Performance",
        "description": "You are inspired by high standards and goal-oriented peers. You value excellence and results.",
        "keywords": [
            "excellence", "excellent", "high standards", "quality", "performance",
            "results", "achieve", "achieved", "goal", "goals", "ambitious",
            "successful", "success", "top performer", "best", "exceptional",
            "outstanding", "skilled", "competent", "professional", "productive"
        ],
        "weight": 1.0
    },
    "drive": {
        "title": "Drive",
        "description": "You're energised by proactive, ambitious colleagues who take initiative and move things forward.",
        "keywords": [
            "initiative", "proactive", "ambitious", "ambition", "driven", "drive",
            "motivated", "motivation", "self-starter", "go-getter", "energetic",
            "dynamic", "action-oriented", "forward-thinking", "pioneering",
            "entrepreneurial", "took charge", "led", "leadership", "visionary"
        ],
        "weight": 1.0
    },
    "empathy": {
        "title": "Empathy",
        "description": "You value kindness, patience, and emotional intelligence. You work best in respectful, people-centred environments.",
        "keywords": [
            "empathy", "empathetic", "kind", "kindness", "compassionate", "compassion",
            "supportive", "support", "caring", "care", "understanding", "patient",
            "patience", "respectful", "respect", "considerate", "thoughtful",
            "warm", "friendly", "listening", "listened", "emotional intelligence"
        ],
        "weight": 1.0
    },
    "composure": {
        "title": "Composure",
        "description": "You appreciate calm, steady people who stay balanced under pressure. You bring stability to tense situations.",
        "keywords": [
            "calm", "composed", "composure", "steady", "stable", "stability",
            "balanced", "level-headed", "even-tempered", "patient", "patience",
            "cool under pressure", "collected", "measured", "controlled",
            "unflappable", "resilient", "grace", "poised", "rational"
        ],
        "weight": 1.0
    },
    "clarity": {
        "title": "Clarity",
        "description": "You value open communication and clear expectations. You thrive when everyone knows what's going on.",
        "keywords": [
            "clear", "clarity", "communicate", "communication", "transparent",
            "transparency", "open", "direct", "explicit", "articulate",
            "straightforward", "honest feedback", "clear expectations",
            "informative", "explained", "communicated well", "kept informed",
            "shared information", "accessible", "approachable"
        ],
        "weight": 1.0
    }
}

# Frustrating trait definitions for challenging relationships
FRUSTRATION_THEMES = {
    "dishonesty": {
        "title": "Dishonesty",
        "description": "You are frustrated by insincerity, politics, or hidden agendas that erode trust.",
        "keywords": [
            "dishonest", "dishonesty", "lie", "lies", "lying", "lied", "deceit", "deceitful",
            "insincere", "insincerity", "fake", "two-faced", "manipulative", "manipulation",
            "political", "hidden agenda", "backstabbing", "untrustworthy", "betrayal", "betrayed",
            "gossip"
        ],
        "weight": 1.0
    },
    "unreliability": {
        "title": "Unreliability",
        "description": "You struggle with people who avoid accountability or fail to deliver on commitments.",
        "keywords": [
            "unreliable", "unreliability", "irresponsible", "careless", "inconsistent",
            "inconsistency", "excuses", "blame", "no accountability", "didn't deliver",
            "failed to deliver", "missed deadlines", "late", "lateness", "flaky", "flake",
            "dropped the ball", "forgot"
        ],
        "weight": 1.0
    },
    "poor_communication": {
        "title": "Poor Communication",
        "description": "You feel blocked by unclear, vague, or withheld communication.",
        "keywords": [
            "unclear", "vague", "confusing", "miscommunication", "poor communication",
            "no communication", "withheld", "kept in the dark", "silent", "ignored",
            "no feedback", "lack of feedback", "didn't explain", "ghosted"
        ],
        "weight": 1.0
    },
    "disrespect": {
        "title": "Disrespect",
        "description": "You are discouraged by dismissive or condescending behavior.",
        "keywords": [
            "disrespectful", "rude", "condescending", "dismissive", "belittling",
            "insulting", "talked over", "undervalued", "micromanaging", "bullying"
        ],
        "weight": 1.0
    },
    "disorganization": {
        "title": "Disorganization",
        "description": "You find chaos and poor planning disruptive to effective work.",
        "keywords": [
            "disorganized", "disorganization", "chaotic", "chaos", "messy",
            "last minute", "no plan", "unstructured", "poor planning", "disarray"
        ],
        "weight": 1.0
    },
    "volatility": {
        "title": "Volatility",
        "description": "You are drained by emotional outbursts, drama, or unpredictable reactions.",
        "keywords": [
            "volatile", "explosive", "angry", "anger", "temper", "outburst",
            "drama", "dramatic", "moody", "mood swings", "passive aggressive",
            "toxic", "yelling", "shouting"
        ],
        "weight": 1.0
    }
}

# Reflection prompts for positive relationships
POSITIVE_PROMPTS = [
    "What made this relationship work so well?",
    "What did you admire most about this person?",
    "What values or attitudes did you share?",
    "How did this person bring out your best qualities?",
    "What might this relationship reveal about what you value in teamwork or leadership?"
]

# Reflection prompts for challenging relationships
CHALLENGING_PROMPTS = [
    "What made collaboration difficult?",
    "What behaviours or attitudes frustrated you?",
    "What values or boundaries felt violated?",
    "What would you do differently if faced with a similar situation again?",
    "What might this relationship reveal about what you need to feel respected or effective?"
]

# Negation words to detect negative context
NEGATION_WORDS = [
    "not", "no", "never", "neither", "none", "nobody", "nothing",
    "nowhere", "lack", "lacking", "lacks", "lacked", "without",
    "absent", "missing", "failed", "failure", "unable", "cannot",
    "can't", "couldn't", "wouldn't", "shouldn't", "didn't", "doesn't",
    "don't", "wasn't", "weren't", "isn't", "aren't", "rarely", "seldom"
]
