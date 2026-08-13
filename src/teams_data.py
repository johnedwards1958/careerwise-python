"""
Teams Assessment - Data Layer
Static assessment data definitions.
"""


# Team role definitions
ROLES = {
    "SH": {
        "name": "Shaper",
        "description": "Challenging, dynamic, thrives on pressure. Has the drive and courage to overcome obstacles.",
        "strengths": "Driven to challenge the team, dynamic and usually extrovert.",
        "weaknesses": "Can be prone to provocation and may offend people's feelings."
    },
    "CO": {
        "name": "Coordinator",
        "description": "Mature, confident, identifies talent. Clarifies goals, delegates effectively.",
        "strengths": "Good at seeing the big picture. Sees all options and judges accurately.",
        "weaknesses": "Can be seen as manipulative and might offload their own work."
    },
    "PL": {
        "name": "Plant",
        "description": "Creative, imaginative, free-thinking. Generates ideas and solves difficult problems.",
        "strengths": "Creative and inventive. Comes up with original ideas and solves complex problems.",
        "weaknesses": "May ignore incidentals and be too preoccupied to communicate effectively."
    },
    "RI": {
        "name": "Resource Investigator",
        "description": "Outgoing, enthusiastic, communicative. Explores opportunities and develops contacts.",
        "strengths": "Extrovert and communicative. Explores new opportunities and makes contacts.",
        "weaknesses": "Can be over-optimistic and lose interest once the initial enthusiasm has passed."
    },
    "ME": {
        "name": "Monitor Evaluator",
        "description": "Sober, strategic, discerning. Sees all options and judges accurately.",
        "strengths": "Strategic and discerning. Sees all options and is good at analyzing.",
        "weaknesses": "Can lack drive and the ability to inspire others and can be overly critical."
    },
    "IM": {
        "name": "Implementer",
        "description": "Practical, reliable, efficient. Turns ideas into actions and organizes work.",
        "strengths": "Practical and efficient. Good at turning ideas into practical actions.",
        "weaknesses": "Can be inflexible and slow to respond to new possibilities."
    },
    "TW": {
        "name": "Teamworker",
        "description": "Cooperative, perceptive, diplomatic. Listens and averts friction.",
        "strengths": "Cooperative and diplomatic. Listens well and averts friction.",
        "weaknesses": "Can be indecisive in crunch situations and tends to avoid confrontation."
    },
    "CF": {
        "name": "Completer Finisher",
        "description": "Painstaking, conscientious, anxious. Searches out errors. Polishes and perfects.",
        "strengths": "Perfectionist who ensures work is completed thoroughly and on time.",
        "weaknesses": "Can worry unduly and be reluctant to delegate."
    }
}

# Section definitions with their questions
SECTIONS = {
    "A": {
        "title": "When involved in a project with other people:",
        "questions": [
            "I'm good at organising work tasks for others.",
            "I'm good at spotting mistakes.",
            "I'm good at keeping people focused on their task.",
            "I can come up with good ideas.",
            "I can see the 'good' and 'bad' in other people's ideas.",
            "I am keen to find out the latest ideas and developments.",
            "I'm good at organising people.",
            "I am always ready to support good suggestions."
        ]
    },
    "B": {
        "title": "In seeking satisfaction through my work:",
        "questions": [
            "I like to have a strong influence on decisions.",
            "I can work with a high degree of attention and concentration.",
            "I like to help colleagues with their problems.",
            "I like to make critical discrimination between alternatives.",
            "I tend to have a creative approach to problem-solving.",
            "I'm good at seeing both sides of an argument.",
            "I'm more interested in getting the job done than looking at new ideas.",
            "I enjoy learning new skills and talking about new ideas."
        ]
    },
    "C": {
        "title": "When the team is trying to solve a particularly complex problem:",
        "questions": [
            "I can easily see where a task might get tricky.",
            "I look at ideas that could be used to solve other problems.",
            "I like to think carefully about ideas before choosing the best one.",
            "I'm good at organizing other people's skills.",
            "I don't let work pressure affect my performance.",
            "I often come up with new ideas to solve tricky problems.",
            "I don't mind annoying others to make them notice my ideas.",
            "I am ready to help whenever I can."
        ]
    },
    "D": {
        "title": "In carrying out my day-to-day work:",
        "questions": [
            "I always make sure that I know exactly what I'm expected to do.",
            "I always make sure people know what I think about an idea.",
            "I can work with all sorts of people as long as they have something to offer.",
            "I try to follow up on interesting ideas and people.",
            "I'm good at arguing against bad ideas.",
            "I tend to see patterns where others would see items as unconnected.",
            "Being busy gives me real satisfaction.",
            "I like getting to know people better."
        ]
    },
    "E": {
        "title": "If I am suddenly given a difficult task with limited time & unfamiliar people:",
        "questions": [
            "I can't always think of good ideas when working in a group.",
            "I'm good at helping people to agree on things.",
            "I don't often let my emotions affect my judgment.",
            "I try to organize tasks so that work gets done quickly.",
            "I can work with many types of people.",
            "I don't mind being unpopular if it means I can push my ideas.",
            "I know a few people that can be helpful with a difficult task.",
            "I tend to want to get things done quickly."
        ]
    },
    "F": {
        "title": "When suddenly asked to consider a new project:",
        "questions": [
            "I'm usually good at finding ways to start new tasks.",
            "I prefer to finish a task before starting a new one.",
            "I begin new tasks carefully and logically.",
            "I'm good at getting other people to help me with tasks.",
            "I can see new ways of solving problems.",
            "I'm happy to lead a team when this is helpful.",
            "I'm usually able to see the good in other people's ideas.",
            "I need tasks to be set out for me."
        ]
    },
    "G": {
        "title": "In contributing to group projects in general:",
        "questions": [
            "I'm good at completing tasks even with unclear instructions.",
            "I take my time to make decisions but I usually get it right.",
            "I need to feel that I can always ask a lot of people to help with a task.",
            "I have an eye for getting the details right.",
            "I try to leave an impression on groups I work with.",
            "I can see how ideas and techniques can be used in different situations.",
            "I see both sides of a problem and take a decision acceptable to all.",
            "I get on well with others and work hard for the team."
        ]
    }
}

# Mapping grid: section -> question_index (1-based) -> role
# This represents which question number maps to which role in each section
ROLE_MAPPING = {
    "A": {1: "IM", 2: "CF", 3: "SH", 4: "PL", 5: "ME", 6: "RI", 7: "CO", 8: "TW"},
    "B": {1: "SH", 2: "CF", 3: "TW", 4: "ME", 5: "PL", 6: "CO", 7: "IM", 8: "RI"},
    "C": {1: "CF", 2: "RI", 3: "ME", 4: "CO", 5: "IM", 6: "PL", 7: "SH", 8: "TW"},
    "D": {1: "IM", 2: "SH", 3: "CO", 4: "RI", 5: "ME", 6: "PL", 7: "CF", 8: "TW"},
    "E": {1: "PL", 2: "TW", 3: "ME", 4: "IM", 5: "CO", 6: "SH", 7: "RI", 8: "CF"},
    "F": {1: "RI", 2: "CF", 3: "ME", 4: "CO", 5: "PL", 6: "SH", 7: "TW", 8: "IM"},
    "G": {1: "IM", 2: "ME", 3: "RI", 4: "CF", 5: "SH", 6: "PL", 7: "CO", 8: "TW"}
}

POINTS_PER_SECTION = 10

