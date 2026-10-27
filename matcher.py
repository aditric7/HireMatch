import re
from functools import lru_cache
from typing import Dict, List, Optional

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# =========================================================
# SKILL DICTIONARY
# =========================================================

SKILLS = [
    "python", "java", "c", "c++", "c#", "javascript", "typescript",
    "html", "css", "react", "node.js", "flask", "django", "fastapi",
    "sql", "mysql", "postgresql", "mongodb", "sqlite", "pandas",
    "numpy", "matplotlib", "seaborn", "scikit-learn",
    "machine learning", "deep learning", "nlp",
    "natural language processing", "tensorflow", "pytorch", "keras",
    "git", "github", "docker", "kubernetes", "aws", "azure", "gcp",
    "linux", "rest api", "api", "excel", "power bi", "tableau",
    "data analysis", "data visualization", "statistics",
    "communication", "problem solving", "data structures", "algorithms",
    "oops", "object-oriented programming", "streamlit", "scipy",
    "opencv", "computer vision", "transformers", "llm",
    "generative ai", "prompt engineering", "testing", "pytest",
    "agile", "project management", "leadership", "teamwork", "research",
    "cybersecurity", "networking", "critical thinking",
    "time management", "powerpoint", "word", "business analysis",
    "financial analysis", "salesforce", "react.js", "next.js",
    "express.js", "spring boot", "php", "ruby", "go", "rust",
    "redis", "firebase", "supabase", "graphql",
]

ALIASES = {
    "natural language processing": "nlp",
    "react.js": "react",
    "object-oriented programming": "oops",
}


# =========================================================
# PERSONALIZED ROADMAP CONTENT
# =========================================================

ROADMAPS = {
    "python": {
        "priority": "High",
        "why": "Python is widely used in automation, backend development, data analysis, and AI.",
        "topics": [
            "Data types and control flow",
            "Functions, modules, and collections",
            "Object-oriented programming",
            "File handling and exceptions",
            "Working with APIs and virtual environments",
        ],
        "practice": [
            "Complete five short Python exercises",
            "Build a small automation tool",
            "Add tests and document a Python mini-project",
        ],
    },
    "sql": {
        "priority": "High",
        "why": "SQL helps you query, combine, and summarize information in relational databases.",
        "topics": [
            "SELECT, WHERE, and ORDER BY",
            "GROUP BY and aggregate functions",
            "INNER JOIN and LEFT JOIN",
            "Subqueries and common table expressions",
            "Database design and indexes",
        ],
        "practice": [
            "Solve ten SQL query exercises",
            "Write JOIN queries across related tables",
            "Analyze a dataset using SQL",
        ],
    },
    "machine learning": {
        "priority": "High",
        "why": "Machine learning work requires understanding data preparation, training, and model evaluation.",
        "topics": [
            "Supervised and unsupervised learning",
            "Regression and classification",
            "Train, validation, and test splits",
            "Feature preprocessing",
            "Precision, recall, F1, and cross-validation",
        ],
        "practice": [
            "Train a baseline classification model",
            "Compare two models using suitable metrics",
            "Document an end-to-end ML experiment",
        ],
    },
    "data analysis": {
        "priority": "High",
        "why": "Data analysis helps turn raw data into reliable findings and useful decisions.",
        "topics": [
            "Data cleaning",
            "Pandas DataFrames",
            "Missing values and outliers",
            "Exploratory data analysis",
            "Charts and communicating insights",
        ],
        "practice": [
            "Clean a CSV dataset",
            "Record five findings from exploratory analysis",
            "Create a short report with charts",
        ],
    },
    "pandas": {
        "priority": "High",
        "why": "Pandas is a key Python library for cleaning and analyzing tabular data.",
        "topics": [
            "Series and DataFrames",
            "Reading and writing CSV files",
            "Filtering, sorting, and grouping",
            "Missing data",
            "Merging and reshaping datasets",
        ],
        "practice": [
            "Clean a messy CSV file",
            "Summarize a dataset by categories",
            "Publish a notebook explaining your findings",
        ],
    },
    "numpy": {
        "priority": "Medium",
        "why": "NumPy provides efficient numerical and array operations used throughout scientific Python.",
        "topics": [
            "Array creation and shapes",
            "Indexing and slicing",
            "Vectorized operations",
            "Broadcasting",
            "Basic matrix operations",
        ],
        "practice": [
            "Practice array calculations",
            "Compare loops with vectorized operations",
            "Solve a small numerical task",
        ],
    },
    "algorithms": {
        "priority": "High",
        "why": "Algorithms help solve problems efficiently and commonly appear in technical interviews.",
        "topics": [
            "Searching and sorting",
            "Two pointers and sliding window",
            "Binary search",
            "Recursion and backtracking",
            "Greedy algorithms and introductory dynamic programming",
        ],
        "practice": [
            "Solve five easy algorithm problems",
            "Attempt three medium problems",
            "Explain time and space complexity",
        ],
    },
    "data structures": {
        "priority": "High",
        "why": "Data structures organize information and are fundamental to efficient programming.",
        "topics": [
            "Arrays and strings",
            "Stacks and queues",
            "Hash maps and sets",
            "Linked lists",
            "Trees and graphs",
        ],
        "practice": [
            "Implement a stack and queue",
            "Solve array and hash-map problems",
            "Practice a tree traversal problem",
        ],
    },
    "nlp": {
        "priority": "High",
        "why": "NLP is useful for text classification, document search, and language-based applications.",
        "topics": [
            "Text cleaning and tokenization",
            "Bag-of-words and TF-IDF",
            "Text classification",
            "Embeddings and cosine similarity",
            "Transformer fundamentals",
        ],
        "practice": [
            "Build a text classification project",
            "Create a document similarity tool",
            "Evaluate and document your results",
        ],
    },
    "deep learning": {
        "priority": "High",
        "why": "Deep learning is useful for applications involving neural networks, images, and text.",
        "topics": [
            "Neurons and neural network layers",
            "Activation and loss functions",
            "Backpropagation",
            "Optimizers",
            "Training and validation",
        ],
        "practice": [
            "Train a small neural network",
            "Plot training and validation metrics",
            "Document your model evaluation",
        ],
    },
    "scikit-learn": {
        "priority": "High",
        "why": "Scikit-learn provides practical tools for training and evaluating machine-learning models.",
        "topics": [
            "Estimators and pipelines",
            "Train-test splitting",
            "Preprocessing",
            "Classification and regression",
            "Model evaluation",
        ],
        "practice": [
            "Build a pipeline for a dataset",
            "Compare two estimators",
            "Write an evaluation summary",
        ],
    },
    "git": {
        "priority": "Medium",
        "why": "Git enables version control, experimentation, and collaborative development.",
        "topics": [
            "Repositories and commits",
            "Branches",
            "Merging",
            "Resolving conflicts",
            "Pull-request workflows",
        ],
        "practice": [
            "Create and merge a branch",
            "Practice reverting a change",
            "Open a pull request with a clear description",
        ],
    },
    "github": {
        "priority": "Medium",
        "why": "GitHub helps showcase projects, track issues, and collaborate on software.",
        "topics": [
            "Repository organization",
            "Writing README files",
            "Issues and project boards",
            "Pull requests",
            "Releases and contribution guidelines",
        ],
        "practice": [
            "Improve a project README",
            "Create an issue and work on a branch",
            "Document setup and testing instructions",
        ],
    },
    "docker": {
        "priority": "Medium",
        "why": "Docker packages applications and dependencies into reproducible environments.",
        "topics": [
            "Images and containers",
            "Dockerfile instructions",
            "Ports and environment variables",
            "Volumes",
            "Docker Compose basics",
        ],
        "practice": [
            "Containerize a small application",
            "Build and run the image locally",
            "Document startup and configuration",
        ],
    },
    "rest api": {
        "priority": "High",
        "why": "REST APIs let applications exchange data through predictable HTTP endpoints.",
        "topics": [
            "HTTP methods and status codes",
            "JSON request and response design",
            "Input validation and errors",
            "Authentication basics",
            "API testing and documentation",
        ],
        "practice": [
            "Build three CRUD endpoints",
            "Test successful and unsuccessful requests",
            "Document the endpoints with examples",
        ],
    },
    "api": {
        "priority": "Medium",
        "why": "API knowledge helps integrate services and build reliable application boundaries.",
        "topics": [
            "HTTP requests and responses",
            "JSON",
            "Authentication",
            "Rate limits and errors",
            "API testing",
        ],
        "practice": [
            "Call a public API",
            "Handle errors and timeouts",
            "Write an integration guide",
        ],
    },
    "react": {
        "priority": "High",
        "why": "React is widely used to build interactive, component-based web interfaces.",
        "topics": [
            "Components and props",
            "State and events",
            "Hooks",
            "Forms and validation",
            "API requests and loading states",
        ],
        "practice": [
            "Build a multi-component interface",
            "Add a form and validation",
            "Connect the UI to an API",
        ],
    },
    "javascript": {
        "priority": "High",
        "why": "JavaScript powers browser interactions and many full-stack applications.",
        "topics": [
            "Variables and functions",
            "Arrays and objects",
            "Promises and async/await",
            "DOM events",
            "Modules and error handling",
        ],
        "practice": [
            "Complete JavaScript exercises",
            "Fetch data from an API",
            "Build an interactive web page",
        ],
    },
    "html": {
        "priority": "Medium",
        "why": "HTML provides the structure and semantics of web pages.",
        "topics": [
            "Semantic elements",
            "Forms and inputs",
            "Accessible labels",
            "Document structure",
            "Metadata",
        ],
        "practice": [
            "Build a semantic page",
            "Create an accessible form",
            "Check form labels and structure",
        ],
    },
    "css": {
        "priority": "Medium",
        "why": "CSS controls layout, responsive behavior, and visual presentation.",
        "topics": [
            "The box model",
            "Flexbox and Grid",
            "Responsive design",
            "Typography and spacing",
            "Focus states and accessibility",
        ],
        "practice": [
            "Build a responsive card layout",
            "Test desktop and mobile widths",
            "Review contrast and keyboard focus",
        ],
    },
    "communication": {
        "priority": "Medium",
        "why": "Clear communication helps explain decisions and collaborate effectively.",
        "topics": [
            "Concise written updates",
            "Explaining technical ideas",
            "Asking clarifying questions",
            "Giving and receiving feedback",
        ],
        "practice": [
            "Write a one-page project summary",
            "Explain a project in two minutes",
            "Ask someone to review your explanation",
        ],
    },
    "problem solving": {
        "priority": "High",
        "why": "Problem-solving helps turn unclear requirements into structured, testable solutions.",
        "topics": [
            "Clarifying requirements",
            "Breaking problems into steps",
            "Edge cases",
            "Trade-off analysis",
            "Testing and iteration",
        ],
        "practice": [
            "Solve a problem and explain your approach",
            "List edge cases before coding",
            "Compare two possible solutions",
        ],
    },
}


# =========================================================
# TEXT AND SKILL UTILITIES
# =========================================================

def clean_text(text: str) -> str:
    text = (text or "").lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def contains_skill(text: str, skill: str) -> bool:
    text = clean_text(text)
    skill = clean_text(skill)

    if not text or not skill:
        return False

    # Boundaries prevent "java" from matching "javascript".
    pattern = rf"(?<![a-z0-9]){re.escape(skill)}(?![a-z0-9])"
    return bool(re.search(pattern, text))


def extract_skills(text: str) -> List[str]:
    found = set()

    for skill in SKILLS:
        if contains_skill(text, skill):
            found.add(ALIASES.get(skill, skill))

    return sorted(found)


def find_skill_evidence(text: str, skill: str) -> str:
    if not (text or "").strip():
        return ""

    sentences = re.split(r"(?<=[.!?])\s+|\n+", text)

    for sentence in sentences:
        if contains_skill(sentence, skill):
            return sentence.strip()[:500]

        for alias, canonical in ALIASES.items():
            if canonical == skill and contains_skill(sentence, alias):
                return sentence.strip()[:500]

    return ""


def get_skill_evidence(
    resume_text: str,
    skills: List[str],
) -> Dict[str, str]:
    return {
        skill: (
            find_skill_evidence(resume_text, skill)
            or "The skill keyword was detected, but a clear evidence excerpt could not be extracted."
        )
        for skill in skills
    }


# =========================================================
# TF-IDF MATCHING
# =========================================================

def calculate_similarity(resume_text: str, job_text: str) -> float:
    """Return TF-IDF cosine similarity as a value from 0 to 1."""

    documents = [
        clean_text(resume_text),
        clean_text(job_text),
    ]

    if not all(documents):
        return 0.0

    try:
        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
        )
        matrix = vectorizer.fit_transform(documents)

        return float(
            cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
        )
    except ValueError:
        return 0.0


# =========================================================
# SEMANTIC MATCHING
# =========================================================

@lru_cache(maxsize=1)
def load_semantic_model():
    """Load and cache the sentence-embedding model."""

    from sentence_transformers import SentenceTransformer

    return SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2"
    )


def calculate_semantic_similarity(
    resume_text: str,
    job_text: str,
) -> Optional[float]:
    """
    Return embedding cosine similarity as a percentage.
    None means the model could not be loaded or used.
    This is not a calibrated hiring probability.
    """

    resume_text = clean_text(resume_text)
    job_text = clean_text(job_text)

    if not resume_text or not job_text:
        return 0.0

    try:
        model = load_semantic_model()

        embeddings = model.encode(
            [resume_text[:12000], job_text[:12000]],
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

        cosine = float(
            cosine_similarity(
                embeddings[0:1],
                embeddings[1:2],
            )[0][0]
        )

        return round(
            max(0.0, min(100.0, cosine * 100.0)),
            2,
        )
    except Exception:
        # TF-IDF and skill-gap analysis still work if this fails.
        return None


def analyze_match(resume_text: str, job_description: str) -> dict:
    """
    Compare a resume and job description using semantic similarity.
    Keep skill-gap detection for the personalized learning roadmap.
    """
    resume_text = (resume_text or "").strip()
    job_description = (job_description or "").strip()

    if not resume_text or not job_description:
        return {
            "success": False,
            "message": "Please provide both resume text and a job description.",
            "resume_skills": [],
            "job_skills": [],
            "matched_skills": [],
            "missing_skills": [],
            "match_percentage": None,
            "semantic_similarity": None,
            "roadmap": [],
        }

    resume_skills = extract_skills(resume_text)
    job_skills = extract_skills(job_description)

    # Calculate the main score using semantic similarity.
    semantic_score = calculate_semantic_similarity(
        resume_text,
        job_description,
    )

    matched_skills = sorted(set(resume_skills) & set(job_skills))
    missing_skills = sorted(set(job_skills) - set(resume_skills))

    return {
        "success": True,
        "message": (
            "Semantic analysis completed successfully."
            if semantic_score is not None
            else "Skill analysis completed, but semantic matching is unavailable."
        ),
        "resume_skills": sorted(set(resume_skills)),
        "job_skills": sorted(set(job_skills)),
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "match_percentage": semantic_score,
        "semantic_similarity": semantic_score,
        "roadmap": generate_roadmap(missing_skills),
    }



def generate_roadmap(missing_skills: list[str]) -> list[dict]:
    """
    Build a learning roadmap from the skills missing
    for the selected job.
    """
    roadmap = []

    for index, skill in enumerate(missing_skills, start=1):
        resource = ROADMAPS.get(skill.lower().strip())

        if resource:
            topics = resource.get("topics", [])
            practice = resource.get("practice", [])

            roadmap.append({
                "step": index,
                "skill": skill,
                "topic": "; ".join(topics) if topics else resource.get("why", ""),
                "duration": resource.get("duration", "1–2 weeks (estimated)"),
                "resources": practice,
            })
        else:
            roadmap.append({
                "step": index,
                "skill": skill,
                "topic": f"Learn the fundamentals of {skill}",
                "duration": "1–2 weeks (estimated)",
                "resources": [
                    f"Study beginner materials for {skill}",
                    f"Build a small practice project using {skill}",
                ],
            })

    return roadmap