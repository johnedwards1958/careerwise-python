"""
Transferrable Assessment - Data Layer
Static assessment data definitions.
"""


# Assessment questions with their skill codes
QUESTIONS = [
    {"text": "When tasks are unclear, I quickly find out what's expected and take action.", "code": "IN"},
    {"text": "I can explain technical or complex ideas so others easily understand them.", "code": "CO"},
    {"text": "When a plan fails, I look for lessons and new approaches instead of blaming others.", "code": "AD"},
    {"text": "I enjoy learning new systems or technologies, even if they're unfamiliar at first.", "code": "LG"},
    {"text": "I notice when others on the team need help and step in when I can.", "code": "TW"},
    {"text": "I keep track of deadlines and deliver on time without constant reminders.", "code": "OR"},
    {"text": "I can use data or evidence to back up my opinions or decisions.", "code": "AN"},
    {"text": "I'm comfortable presenting ideas or results to a group.", "code": "PR"},
    {"text": "When people disagree, I can usually find a workable compromise.", "code": "CR"},
    {"text": "I look for ways to improve efficiency or simplify tasks.", "code": "PS"},
    {"text": "I adapt easily when company priorities change.", "code": "AD"},
    {"text": "I maintain professionalism even under pressure.", "code": "PRF"},
    {"text": "I keep clear records or documentation of my work.", "code": "OR"},
    {"text": "I take feedback constructively and act on it.", "code": "LG"},
    {"text": "I often help connect people or information across departments.", "code": "NW"},
    {"text": "I use digital tools efficiently to manage my work.", "code": "DG"},
    {"text": "I understand the customer's or end-user's perspective.", "code": "EM"},
    {"text": "I find creative solutions when resources are limited.", "code": "CRV"},
    {"text": "I can manage multiple priorities without losing focus.", "code": "TM"},
    {"text": "I motivate myself to complete difficult or repetitive tasks.", "code": "SM"},
]

# Domain definitions with skill codes
DOMAINS = {
    "communication_collaboration": {
        "title": "Communication & Collaboration",
        "description": "Expressing ideas clearly and working well with others",
        "codes": ["CO", "TW", "CR", "NW"],
        "questions": [1, 4, 8, 14]  # 0-based indices
    },
    "organisation_reliability": {
        "title": "Organisation & Reliability",
        "description": "Managing tasks, time, and follow-through effectively",
        "codes": ["OR", "TM", "PRF", "SM"],
        "questions": [5, 12, 18, 11, 19]
    },
    "adaptability_learning": {
        "title": "Adaptability & Learning",
        "description": "Adjusting to change and learning from experience",
        "codes": ["AD", "LG", "IN"],
        "questions": [2, 10, 3, 13, 0]  # 5 questions (AD appears twice)
    },
    "problem_solving_creativity": {
        "title": "Problem-Solving & Creativity",
        "description": "Using logic and creativity to improve results",
        "codes": ["PS", "AN", "CRV"],
        "questions": [9, 6, 17]
    },
    "digital_professional": {
        "title": "Digital & Professional Skills",
        "description": "Using tools and maintaining professional standards",
        "codes": ["DG", "EM", "PR"],
        "questions": [15, 16, 7]
    }
}

# Overall scoring thresholds
HIGHLY_TRANSFERABLE = 80
MODERATELY_TRANSFERABLE = 60
DEVELOPING = 40

