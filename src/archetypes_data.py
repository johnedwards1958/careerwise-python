"""
Influence Archetypes Assessment - Data Layer
Assessment statements, clusters, and archetype metadata.
"""

STATEMENTS = {
    "Analyst": [
        "I use facts and data to convince others.",
        "I explain the logic behind my ideas in detail.",
        "I persuade by presenting evidence step-by-step."
    ],
    "Enforcer": [
        "I refer to rules, policies, or standards when explaining my view.",
        "I believe consistency and fairness matter most in decisions.",
        "I feel confident referring to rules or authority when needed."
    ],
    "Negotiator": [
        "I like to find win-win outcomes where everyone benefits.",
        "I enjoy negotiating trades or compromises.",
        "I'm comfortable offering something in return for cooperation."
    ],
    "Communicator": [
        "I state my opinions clearly and directly.",
        "I make sure others understand exactly what I'm asking for.",
        "I'm direct and clear when expressing disagreement."
    ],
    "Socialiser": [
        "I build a friendly rapport before getting down to business.",
        "I enjoy social conversation that helps people feel comfortable.",
        "I make an effort to keep interactions warm and positive."
    ],
    "Ally": [
        "I rely on trusted relationships to get things done.",
        "I count on long-term relationships when I need cooperation.",
        "People know they can rely on my loyalty and support."
    ],
    "Collaborator": [
        "I ask for others' input before deciding.",
        "I involve others early so they feel ownership of a plan.",
        "I seek shared ownership of decisions rather than dictating."
    ],
    "Networker": [
        "I connect people or teams who can help each other.",
        "I build alliances or partnerships to achieve shared goals.",
        "I'm good at bringing different groups together."
    ],
    "Visionary": [
        "I motivate others by linking ideas to a larger purpose.",
        "I appeal to people's values or ideals to gain commitment.",
        "I inspire others by talking about purpose and vision."
    ]
}

# Archetype clusters
CLUSTERS = {
    "Analytical": ["Analyst", "Enforcer", "Negotiator"],
    "Relational": ["Communicator", "Socialiser", "Ally"],
    "Inspirational": ["Collaborator", "Networker", "Visionary"]
}

# Archetype descriptions
ARCHETYPE_INFO = {
    "Analyst": {
        "title": "The Rational Persuader",
        "icon": "🧠",
        "description": "You convince others through logic, structure, and evidence.",
        "strengths": "Credibility, clarity, problem-solving.",
        "development": "Emotional connection and flexibility."
    },
    "Enforcer": {
        "title": "The Rule Keeper",
        "icon": "⚖️",
        "description": "You influence by appealing to fairness, consistency, and authority.",
        "strengths": "Integrity, order, reliability.",
        "development": "Adaptability and empathy."
    },
    "Negotiator": {
        "title": "The Deal Maker",
        "icon": "🤝",
        "description": "You seek balance and mutual gain.",
        "strengths": "Pragmatism, diplomacy, fairness.",
        "development": "Standing firm on principles when needed."
    },
    "Communicator": {
        "title": "The Straight Talker",
        "icon": "💬",
        "description": "You influence through clear, assertive expression.",
        "strengths": "Transparency, decisiveness.",
        "development": "Listening and patience."
    },
    "Socialiser": {
        "title": "The Connector",
        "icon": "🌷",
        "description": "You win others over through warmth and friendliness.",
        "strengths": "Approachability, positivity.",
        "development": "Managing conflict directly."
    },
    "Ally": {
        "title": "The Trusted Partner",
        "icon": "🧡",
        "description": "You rely on strong personal bonds to get things done.",
        "strengths": "Loyalty, reliability, supportiveness.",
        "development": "Objectivity in tough decisions."
    },
    "Collaborator": {
        "title": "The Inclusive Leader",
        "icon": "🤲",
        "description": "You influence by seeking input and co-creating solutions.",
        "strengths": "Empowering, democratic, engaging.",
        "development": "Decisiveness and speed."
    },
    "Networker": {
        "title": "The Bridge Builder",
        "icon": "🌐",
        "description": "You form alliances and connect people strategically.",
        "strengths": "Political awareness, big-picture thinking.",
        "development": "Consistency and follow-through."
    },
    "Visionary": {
        "title": "The Inspirer",
        "icon": "🌟",
        "description": "You motivate others by linking work to a higher purpose.",
        "strengths": "Passion, creativity, motivation.",
        "development": "Attention to detail and practical planning."
    }
}
