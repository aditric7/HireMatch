import re
from typing import List, Dict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ---------------------------------------------------------
# SKILL DICTIONARY
# ---------------------------------------------------------

SKILLS = [
    "python",
    "java",
    "c",
    "c++",
    "c#",
    "javascript",
    "typescript",
    "html",
    "css",
    "react",
    "node.js",
    "flask",
    "django",
    "sql",
    "mysql",
    "postgresql",
    "mongodb",
    "pandas",
    "numpy",
    "matplotlib",
    "scikit-learn",
    "machine learning",
    "deep learning",
    "nlp",
    "tensorflow",
    "pytorch",
    "git",
    "github",
    "docker",
    "aws",
    "azure",
    "linux",
    "rest api",
    "api",
    "excel",
    "power bi",
    "tableau",
    "data analysis",
    "data visualization",
    "communication",
    "problem solving",
    "data structures",
    "algorithms",
    "oops",
]


# ---------------------------------------------------------
# PREPARATION ROADMAP DATABASE
# ---------------------------------------------------------

ROADMAPS = {

    "algorithms": {
        "priority": "High",
        "why": "Algorithms are commonly tested in coding interviews and are important for problem-solving roles.",
        "topics": [
            "Searching and sorting",
            "Two pointers and sliding window",
            "Binary search",
            "Greedy algorithms",
            "Recursion and backtracking",
            "Basic dynamic programming"
        ],
        "practice": [
            "Solve 5 easy algorithm problems",
            "Solve 3 medium algorithm problems",
            "Practice one timed coding problem"
        ]
    },

    "data analysis": {
        "priority": "High",
        "why": "Data analysis skills help you understand, clean, transform and interpret datasets.",
        "topics": [
            "Data cleaning",
            "Pandas DataFrames",
            "Handling missing values",
            "Exploratory data analysis",
            "Data visualization",
            "Basic statistical analysis"
        ],
        "practice": [
            "Clean a small CSV dataset",
            "Perform exploratory data analysis using Pandas",
            "Create charts from a dataset"
        ]
    },

    "python": {
        "priority": "High",
        "why": "Python is widely used for automation, data analysis, machine learning and backend development.",
        "topics": [
            "Python syntax and control flow",
            "Functions",
            "Lists, dictionaries and sets",
            "Object-oriented programming",
            "File handling",
            "Exception handling"
        ],
        "practice": [
            "Build small Python programs",
            "Solve Python coding problems",
            "Create one Python mini-project"
        ]
    },

    "sql": {
        "priority": "High",
        "why": "SQL is important for working with relational databases and is frequently tested in technical interviews.",
        "topics": [
            "SELECT and filtering",
            "GROUP BY and aggregation",
            "JOIN operations",
            "Subqueries",
            "Constraints",
            "Basic database design"
        ],
        "practice": [
            "Solve SQL query problems",
            "Practice different JOIN queries",
            "Work with a sample relational database"
        ]
    },

    "machine learning": {
        "priority": "High",
        "why": "Machine learning fundamentals are important for roles involving predictive models and intelligent applications.",
        "topics": [
            "Supervised and unsupervised learning",
            "Regression",
            "Classification",
            "Decision trees",
            "Model evaluation",
            "Feature preprocessing"
        ],
        "practice": [
            "Train a classification model",
            "Evaluate a model using appropriate metrics",
            "Build one end-to-end ML project"
        ]
    },

    "deep learning": {
        "priority": "Medium",
        "why": "Deep learning is useful for advanced AI applications involving neural networks and large datasets.",
        "topics": [
            "Neural network fundamentals",
            "Activation functions",
            "Loss functions",
            "Backpropagation",
            "CNN fundamentals",
            "Model training and evaluation"
        ],
        "practice": [
            "Build a small neural network",
            "Train a basic image classification model",
            "Experiment with model evaluation"
        ]
    },

    "nlp": {
        "priority": "High",
        "why": "NLP is useful for applications involving text, documents, search and language understanding.",
        "topics": [
            "Text preprocessing",
            "Tokenization",
            "TF-IDF",
            "Text classification",
            "Word embeddings",
            "Basic transformer concepts"
        ],
        "practice": [
            "Build a text classification project",
            "Create a document similarity system",
            "Experiment with an NLP dataset"
        ]
    },

    "data structures": {
        "priority": "High",
        "why": "Data structures are fundamental for efficient programming and technical interviews.",
        "topics": [
            "Arrays and strings",
            "Linked lists",
            "Stacks and queues",
            "Hash tables",
            "Trees",
            "Graphs"
        ],
        "practice": [
            "Solve basic data structure problems",
            "Practice implementation from scratch",
            "Solve coding interview questions"
        ]
    },

    "git": {
        "priority": "Medium",
        "why": "Git is essential for version control and collaborative software development.",
        "topics": [
            "Repositories",
            "Commits",
            "Branches",
            "Merging",
            "Pull requests",
            "Resolving merge conflicts"
        ],
        "practice": [
            "Create a Git repository",
            "Create and merge a branch",
            "Make a pull request"
        ]
    },

    "github": {
        "priority": "Medium",
        "why": "GitHub is commonly used to showcase projects and collaborate on software.",
        "topics": [
            "Repositories",
            "README files",
            "Branches",
            "Issues",
            "Pull requests",
            "GitHub project organization"
        ],
        "practice": [
            "Create a clean project repository",
            "Write a professional README",
            "Make a contribution to an open-source project"
        ]
    },

    "pandas": {
        "priority": "High",
        "why": "Pandas is widely used for data manipulation and analysis in Python.",
        "topics": [
            "Series and DataFrames",
            "Reading CSV files",
            "Filtering and sorting",
            "Grouping data",
            "Handling missing values",
            "Data transformation"
        ],
        "practice": [
            "Analyze a CSV dataset",
            "Clean a real-world dataset",
            "Perform exploratory data analysis"
        ]
    },

    "numpy": {
        "priority": "Medium",
        "why": "NumPy provides the numerical computing foundation used by many Python data and ML tools.",
        "topics": [
            "Arrays",
            "Array indexing",
            "Vectorized operations",
            "Broadcasting",
            "Matrix operations",
            "Basic numerical computations"
        ],
        "practice": [
            "Practice NumPy array operations",
            "Implement basic mathematical operations",
            "Work with matrices"
        ]
    },

    "scikit-learn": {
        "priority": "High",
        "why": "Scikit-learn provides practical tools for building and evaluating machine learning models.",
        "topics": [
            "Dataset preparation",
            "Train-test splitting",
            "Classification",
            "Regression",
            "Model evaluation",
            "Pipelines"
        ],
        "practice": [
            "Train a classification model",
            "Compare two ML algorithms",
            "Evaluate a model on a dataset"
        ]
    },

    "tensorflow": {
        "priority": "Medium",
        "why": "TensorFlow is a deep learning framework used for developing and training neural networks.",
        "topics": [
            "Tensor fundamentals",
            "Neural networks",
            "Model creation",
            "Training",
            "Validation",
            "Model evaluation"
        ],
        "practice": [
            "Build a simple neural network",
            "Train a small classification model",
            "Evaluate the model"
        ]
    },

    "pytorch": {
        "priority": "Medium",
        "why": "PyTorch is widely used for deep learning and AI experimentation.",
        "topics": [
            "Tensors",
            "Datasets and DataLoaders",
            "Neural networks",
            "Training loops",
            "Loss functions",
            "Optimizers"
        ],
        "practice": [
            "Build a small neural network",
            "Write a basic training loop",
            "Train a classification model"
        ]
    }
}


# ---------------------------------------------------------
# TEXT CLEANING
# ---------------------------------------------------------

def clean_text(text: str) -> str:
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


# ---------------------------------------------------------
# SKILL DETECTION
# ---------------------------------------------------------

def contains_skill(text: str, skill: str) -> bool:
    text = clean_text(text)
    skill = skill.lower()

    if re.fullmatch(r"[a-z0-9]+", skill):
        return bool(
            re.search(
                rf"\b{re.escape(skill)}\b",
                text
            )
        )

    return skill in text


def extract_skills(text: str) -> List[str]:
    return [
        skill
        for skill in SKILLS
        if contains_skill(text, skill)
    ]


# ---------------------------------------------------------
# EVIDENCE EXTRACTION
# ---------------------------------------------------------

def find_skill_evidence(
    text: str,
    skill: str
) -> str:

    if not text.strip():
        return ""

    # First try sentence-level evidence
    sentences = re.split(
        r"(?<=[.!?])\s+|\n+",
        text
    )

    for sentence in sentences:
        if contains_skill(sentence, skill):
            sentence = sentence.strip()

            if sentence:
                return sentence

    # Fallback: search individual lines
    lines = text.splitlines()

    for line in lines:
        if contains_skill(line, skill):
            line = line.strip()

            if line:
                return line

    return ""


def get_skill_evidence(
    resume_text: str,
    skills: List[str]
) -> Dict[str, str]:

    evidence = {}

    for skill in skills:

        found = find_skill_evidence(
            resume_text,
            skill
        )

        if found:
            evidence[skill] = found
        else:
            evidence[skill] = (
                "The skill was found in the resume, "
                "but specific evidence could not be extracted."
            )

    return evidence


# ---------------------------------------------------------
# TF-IDF SIMILARITY
# ---------------------------------------------------------

def calculate_similarity(
    resume_text: str,
    job_text: str
) -> float:

    documents = [
        clean_text(resume_text),
        clean_text(job_text)
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english"
    )

    matrix = vectorizer.fit_transform(
        documents
    )

    score = cosine_similarity(
        matrix[0:1],
        matrix[1:2]
    )[0][0]

    return float(score)


# ---------------------------------------------------------
# ROADMAP GENERATOR
# ---------------------------------------------------------

def generate_roadmap(
    missing_skills: List[str]
) -> Dict[str, Dict]:

    roadmap = {}

    for skill in missing_skills:

        if skill in ROADMAPS:
            roadmap[skill] = ROADMAPS[skill]

        else:
            roadmap[skill] = {
                "priority": "Medium",
                "why": (
                    f"{skill.title()} is mentioned in "
                    "the target job description."
                ),
                "topics": [
                    f"Understand {skill.title()} fundamentals",
                    f"Learn common {skill.title()} concepts",
                    f"Practice {skill.title()} with examples",
                    f"Build a small project using {skill.title()}"
                ],
                "practice": [
                    f"Complete beginner exercises for {skill.title()}",
                    f"Apply {skill.title()} in a small project",
                    f"Review interview questions related to {skill.title()}"
                ]
            }

    return roadmap


# ---------------------------------------------------------
# MAIN MATCH ANALYSIS
# ---------------------------------------------------------

def analyze_match(
    resume_text: str,
    job_text: str
) -> Dict:

    similarity = calculate_similarity(
        resume_text,
        job_text
    )

    resume_skills = set(
        extract_skills(resume_text)
    )

    job_skills = set(
        extract_skills(job_text)
    )

    matching_skills = sorted(
        resume_skills.intersection(
            job_skills
        )
    )

    missing_skills = sorted(
        job_skills.difference(
            resume_skills
        )
    )

    skill_evidence = get_skill_evidence(
        resume_text,
        matching_skills
    )

    roadmap = generate_roadmap(
        missing_skills
    )

    return {
        "match_percentage": similarity * 100,

        "resume_skills": sorted(
            resume_skills
        ),

        "job_skills": sorted(
            job_skills
        ),

        "matching_skills": matching_skills,

        "missing_skills": missing_skills,

        "skill_evidence": skill_evidence,

        "roadmap": roadmap,
    }