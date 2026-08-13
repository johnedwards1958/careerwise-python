"""
Learning Preferences Assessment - Data Layer
Learning style metadata and assessment question bank.
"""

# Learning style descriptions
STYLES = {
    "V": {
        "name": "Visual",
        "description": "Learns through seeing, color, and spatial organization.",
        "icon": "👁️",
        "strategies": [
            "Use infographics, charts, and diagrams",
            "Color-code your notes and materials",
            "Create mind maps and flowcharts",
            "Watch videos and visual demonstrations",
            "Use symbols and spatial arrangements"
        ]
    },
    "A": {
        "name": "Auditory",
        "description": "Prefers hearing, discussion, and explanation.",
        "icon": "👂",
        "strategies": [
            "Join discussions and study groups",
            "Listen to podcasts and audio materials",
            "Talk through ideas out loud",
            "Record lectures and replay them",
            "Explain concepts to others verbally"
        ]
    },
    "R": {
        "name": "Read/Write",
        "description": "Likes reading and writing information.",
        "icon": "📝",
        "strategies": [
            "Make detailed outlines and summaries",
            "Write and rewrite key ideas",
            "Create lists and bullet points",
            "Read textbooks and articles thoroughly",
            "Take comprehensive written notes"
        ]
    },
    "K": {
        "name": "Kinesthetic",
        "description": "Learns by doing, touching, and experiencing.",
        "icon": "🤲",
        "strategies": [
            "Use hands-on practice and role-plays",
            "Take breaks to move around while studying",
            "Work with real-life examples and cases",
            "Build models or demonstrations",
            "Apply concepts through practical tasks"
        ]
    }
}

# Questions with their options mapped to learning styles
# Based on the scoring chart from the assessment PDF
QUESTIONS = [
    {
        "text": "A colleague asks how to find a client's office. You would:",
        "options": [
            {"text": "Walk them through it in person.", "style": "K"},
            {"text": "Explain the route verbally.", "style": "A"},
            {"text": "Write down the directions.", "style": "R"},
            {"text": "Show them on a map or diagram.", "style": "V"}
        ]
    },
    {
        "text": "You're watching an online tutorial that includes spoken explanations, text, and diagrams. You learn most from:",
        "options": [
            {"text": "The diagrams and visual examples.", "style": "V"},
            {"text": "Listening to the commentary.", "style": "A"},
            {"text": "Reading the on-screen instructions.", "style": "R"},
            {"text": "Watching the process being demonstrated.", "style": "K"}
        ]
    },
    {
        "text": "You want feedback from your team about a new project plan. You would:",
        "options": [
            {"text": "Describe the highlights in conversation.", "style": "A"},
            {"text": "Use a chart or map to show the stages.", "style": "V"},
            {"text": "Share a written summary or outline.", "style": "R"},
            {"text": "Meet in person to walk through it together.", "style": "K"}
        ]
    },
    {
        "text": "You're preparing a special meal for friends. You would:",
        "options": [
            {"text": "Follow a detailed written recipe.", "style": "R"},
            {"text": "Ask friends for tips and ideas.", "style": "A"},
            {"text": "Look at photos or videos of the dish.", "style": "V"},
            {"text": "Cook something familiar and adjust as you go.", "style": "K"}
        ]
    },
    {
        "text": "Visitors ask about local parks or attractions. You would:",
        "options": [
            {"text": "Talk with them about what they'll see.", "style": "A"},
            {"text": "Show them pictures or maps.", "style": "V"},
            {"text": "Take them there and explore together.", "style": "K"},
            {"text": "Give them a brochure or guidebook.", "style": "R"}
        ]
    },
    {
        "text": "You're buying a new phone or laptop. What most influences your choice?",
        "options": [
            {"text": "Testing it yourself.", "style": "K"},
            {"text": "Reading the technical details or reviews.", "style": "R"},
            {"text": "Its appearance and design.", "style": "V"},
            {"text": "A salesperson's explanation.", "style": "A"}
        ]
    },
    {
        "text": "You're learning a new tool or procedure at work. You learn best by:",
        "options": [
            {"text": "Watching someone demonstrate it.", "style": "V"},
            {"text": "Listening and asking questions.", "style": "A"},
            {"text": "Reading the manual or online guide.", "style": "R"},
            {"text": "Trying it out hands-on.", "style": "K"}
        ]
    },
    {
        "text": "Your doctor is explaining a diagnosis. You would prefer:",
        "options": [
            {"text": "Written information to read later.", "style": "R"},
            {"text": "A model or physical example to illustrate it.", "style": "K"},
            {"text": "A clear verbal explanation.", "style": "A"},
            {"text": "A diagram showing what's happening.", "style": "V"}
        ]
    },
    {
        "text": "You're learning to use a new computer program. You would:",
        "options": [
            {"text": "Read the help file or documentation.", "style": "R"},
            {"text": "Talk with someone who already knows it.", "style": "A"},
            {"text": "Experiment with the controls and menus.", "style": "K"},
            {"text": "Follow illustrated steps or screenshots.", "style": "V"}
        ]
    },
    {
        "text": "When browsing websites, you're drawn to:",
        "options": [
            {"text": "Interactive elements you can click or explore.", "style": "K"},
            {"text": "Clean visuals and appealing layout.", "style": "V"},
            {"text": "Well-written explanations and lists.", "style": "R"},
            {"text": "Embedded audio or podcasts.", "style": "A"}
        ]
    },
    {
        "text": "You're choosing a non-fiction book to buy. You would be most influenced by:",
        "options": [
            {"text": "Its cover design and layout.", "style": "V"},
            {"text": "Reading a few pages to get the feel.", "style": "R"},
            {"text": "A friend's spoken recommendation.", "style": "A"},
            {"text": "Real-life stories and case studies.", "style": "K"}
        ]
    },
    {
        "text": "You want to improve your photography skills. You'd prefer:",
        "options": [
            {"text": "Talking with others or asking questions.", "style": "A"},
            {"text": "A written guide with steps and bullet points.", "style": "R"},
            {"text": "Diagrams showing camera parts and functions.", "style": "V"},
            {"text": "Real examples comparing good and poor photos.", "style": "K"}
        ]
    },
    {
        "text": "You learn best from a trainer who uses:",
        "options": [
            {"text": "Demonstrations or practical sessions.", "style": "K"},
            {"text": "Group discussions or Q&A.", "style": "A"},
            {"text": "Handouts or reading materials.", "style": "R"},
            {"text": "Charts, graphs, or visual slides.", "style": "V"}
        ]
    },
    {
        "text": "After finishing a project, you'd like feedback:",
        "options": [
            {"text": "With concrete examples of what you did.", "style": "K"},
            {"text": "As a written report or notes.", "style": "R"},
            {"text": "Through a conversation with your supervisor.", "style": "A"},
            {"text": "As a chart or graphic summary.", "style": "V"}
        ]
    },
    {
        "text": "At a restaurant, you would choose:",
        "options": [
            {"text": "Something you've tried before.", "style": "K"},
            {"text": "Ask the server or friends for recommendations.", "style": "A"},
            {"text": "Read the menu descriptions carefully.", "style": "R"},
            {"text": "Look at photos of the dishes.", "style": "V"}
        ]
    },
    {
        "text": "You're preparing a presentation for work. You would:",
        "options": [
            {"text": "Create visuals or graphs to illustrate points.", "style": "V"},
            {"text": "Write key phrases and rehearse aloud.", "style": "A"},
            {"text": "Prepare a full written script and read it through.", "style": "R"},
            {"text": "Include real examples and stories to make it relatable.", "style": "K"}
        ]
    }
]
