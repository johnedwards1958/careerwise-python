"""
Path Assessment - Data Layer
Static assessment data definitions.
"""


# RIASEC category information
CATEGORIES = {
    "R": {
        "name": "Realistic",
        "description": "People who like hands-on, practical work with tools, machines, plants, and animals. They prefer working outdoors and building or fixing things.",
        "careers": "Examples: Engineer, Mechanic, Carpenter, Farmer, Electrician"
    },
    "I": {
        "name": "Investigative",
        "description": "People who like to observe, learn, analyze, and solve problems. They enjoy working with ideas and thinking rather than physical activity.",
        "careers": "Examples: Scientist, Researcher, Mathematician, Analyst, Doctor"
    },
    "A": {
        "name": "Artistic",
        "description": "People who like creative activities such as art, music, writing, and drama. They value beauty, originality, and self-expression.",
        "careers": "Examples: Artist, Writer, Musician, Designer, Actor"
    },
    "S": {
        "name": "Social",
        "description": "People who like to help, teach, counsel, or serve others. They enjoy working with people and promoting learning and personal development.",
        "careers": "Examples: Teacher, Counselor, Nurse, Social Worker, Trainer"
    },
    "E": {
        "name": "Enterprising",
        "description": "People who like to lead, persuade, and manage others. They enjoy business, taking risks, and making decisions.",
        "careers": "Examples: Manager, Sales Person, Lawyer, Entrepreneur, Politician"
    },
    "C": {
        "name": "Conventional",
        "description": "People who like to work with data, files, and records in an organized way. They prefer clear procedures and working in structured environments.",
        "careers": "Examples: Accountant, Secretary, Bank Teller, Administrator, Data Analyst"
    }
}

# All statements organized by category
STATEMENTS = {
    "R": [
        "I like to work with tools and mechanical equipment",
        "I enjoy building or constructing things",
        "I like putting things together or assembling things",
        "I enjoy working with machinery or mechanical equipment",
        "I like to repair or fix things when they break",
        "I am a practical person who likes hands-on work",
        "I like working outdoors with equipment or materials",
        "I enjoy working on technical or mechanical projects",
        "I prefer to avoid hands-on technical work"  # Reverse-keyed
    ],
    "I": [
        "I enjoy solving complex analytical problems",
        "I like to conduct research and investigate topics deeply",
        "I enjoy science and learning about how things work",
        "I like analyzing information to find patterns",
        "I enjoy researching and learning about scientific topics",
        "I like working with data and conducting analysis",
        "I like to study theories and understand systems",
        "I enjoy trying to figure out how things work",
        "I dislike working with abstract ideas"  # Reverse-keyed
    ],
    "A": [
        "I enjoy expressing myself through creative activities",
        "I enjoy creative writing or storytelling",
        "I am a creative person who likes original ideas",
        "I appreciate and critique artistic works (art, music, literature)",
        "I like to create visual art or designs",
        "I value beauty and aesthetic experiences",
        "I prefer creative work over routine tasks",
        "I like to read about art and music",
        "I am not interested in creative activities"  # Reverse-keyed
    ],
    "S": [
        "I enjoy mentoring or teaching others",
        "I like to teach or train people",
        "I like trying to help people solve their problems",
        "I am interested in healing people",
        "I enjoy learning about other cultures",
        "I like to get into discussions about issues",
        "I like helping people",
        "I enjoy working with people to support their growth",
        "I avoid activities that involve helping others"  # Reverse-keyed
    ],
    "E": [
        "I enjoy leading and managing others",
        "I like to try to influence or persuade people",
        "I like selling things or promoting ideas",
        "I am quick to take on new responsibilities",
        "I would like to start my own business",
        "I like to lead and take charge of situations",
        "I enjoy motivating and influencing others",
        "I am comfortable in competitive business situations",
        "I dislike persuading or influencing others"  # Reverse-keyed
    ],
    "C": [
        "I like to organize files, records, and information",
        "I enjoy following established procedures and guidelines",
        "I enjoy organizing data and maintaining records",
        "I prefer predictable, structured work environments",
        "I like to do filing, data entry, or clerical work",
        "I am good at keeping accurate records",
        "I would like to work in a structured office environment",
        "I like working with detailed information systems",
        "I prefer unstructured work environments"  # Reverse-keyed
    ]
}

# Indices of reverse-keyed items for each category
REVERSE_ITEMS = {
    "R": [8],  # "I prefer to avoid hands-on technical work"
    "I": [8],  # "I dislike working with abstract ideas"
    "A": [8],  # "I am not interested in creative activities"
    "S": [8],  # "I avoid activities that involve helping others"
    "E": [8],  # "I dislike persuading or influencing others"
    "C": [8]   # "I prefer unstructured work environments"
}

