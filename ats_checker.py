
import re


def analyze_ats(resume_text):
    """Run basic, explainable ATS-style resume checks."""
    text = (resume_text or "").strip()
    lower = text.lower()

    checks = []

    def add_check(label, points, passed, success, improvement):
        checks.append({
            "label": label,
            "points": points,
            "passed": bool(passed),
            "feedback": success if passed else improvement,
        })

    # Contact information
    has_email = bool(
        re.search(
            r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
            text,
            re.IGNORECASE,
        )
    )
    add_check(
        "Email address", 10, has_email,
        "An email address was detected.",
        "Add a professional email address.",
    )

    has_phone = bool(
        re.search(
            r"(?<!\w)(?:\+?\d[\d\s().-]{7,}\d)(?!\w)",
            text,
        )
    )
    add_check(
        "Phone number", 10, has_phone,
        "A possible phone number was detected.",
        "Add a contact phone number if appropriate.",
    )

    # Common resume sections
    headings = {
        "Education": [
            "education", "academic background", "qualifications",
        ],
        "Skills": [
            "skills", "technical skills", "core competencies",
        ],
        "Experience": [
            "experience", "work experience", "internship",
            "professional experience",
        ],
        "Projects": [
            "projects", "academic projects", "personal projects",
        ],
    }

    section_points = {
        "Education": 15,
        "Skills": 15,
        "Experience": 15,
        "Projects": 10,
    }

    for section, keywords in headings.items():
        found = any(
            re.search(
                rf"(?im)^\s*(?:{re.escape(keyword)})\s*:?\s*$",
                text,
            )
            for keyword in keywords
        )

        add_check(
            f"{section} section",
            section_points[section],
            found,
            f"A recognizable {section.lower()} heading was detected.",
            f"Consider adding a clearly labelled {section.lower()} section.",
        )

    # Evidence of measurable impact
    has_numbers = bool(
        re.search(
            r"\b\d+(?:\.\d+)?\s*(?:%|percent|users|customers|"
            r"projects|hours|days|weeks|months|years|records)\b",
            lower,
        )
    )
    add_check(
        "Measurable achievements", 10, has_numbers,
        "A possible quantified achievement was detected.",
        "Where accurate, describe outcomes with numbers or measurable results.",
    )

    # Common action verbs used in project and experience descriptions
    action_verbs = (
        "built", "developed", "designed", "implemented",
        "created", "improved", "analyzed", "automated",
        "managed", "led", "tested", "deployed",
        "optimized", "delivered", "organized",
    )

    has_action_verb = any(
        re.search(rf"\b{verb}\b", lower)
        for verb in action_verbs
    )

    add_check(
        "Action-oriented descriptions", 10, has_action_verb,
        "An action verb was detected.",
        "Describe your actual contributions with clear action verbs.",
    )

    # Check whether enough text was extracted for useful analysis.
    readable = len(text.split()) >= 50
    add_check(
        "Readable resume text", 5, readable,
        "There is enough extracted text for a basic check.",
        "Provide more resume text or check whether the document was extracted correctly.",
    )

    score = sum(
        item["points"] for item in checks if item["passed"]
    )

    return {
        "score": score,
        "checks": checks,
        "passed_count": sum(item["passed"] for item in checks),
        "total_checks": len(checks),
        "disclaimer": (
            "This is a basic checklist, not a real ATS simulation. "
            "It checks extracted text and cannot reliably assess visual "
            "formatting, parsing by a specific employer's system, or hiring outcomes."
        ),
    }
