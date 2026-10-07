"""
Skill detection system for Resume Analyzer.

The skill database is stored in data/skills.json so new
skills can be added without modifying this Python file.
"""

import json
import re
from pathlib import Path


# ---------------------------------------------------------
# DATABASE LOCATION
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

SKILLS_FILE = BASE_DIR / "data" / "skills.json"


# ---------------------------------------------------------
# LOAD SKILLS
# ---------------------------------------------------------

def load_skills() -> dict:
    """Load the skill database from JSON."""

    if not SKILLS_FILE.exists():
        raise FileNotFoundError(
            f"Skill database not found: {SKILLS_FILE}"
        )

    try:
        with open(
            SKILLS_FILE,
            "r",
            encoding="utf-8",
        ) as file:
            data = json.load(file)

    except json.JSONDecodeError as e:
        raise ValueError(
            f"Invalid skills.json: {e}"
        )

    if not isinstance(data, dict):
        raise ValueError(
            "skills.json must contain a JSON object."
        )

    return data


# Load once when the module starts.
SKILLS = load_skills()


# ---------------------------------------------------------
# TEXT MATCHING
# ---------------------------------------------------------

def _contains_skill(
    text: str,
    keyword: str,
) -> bool:
    """
    Check whether a skill keyword appears in text.
    """

    keyword = keyword.lower().strip()

    if not keyword:
        return False

    # Special characters such as +, #, / and .
    # are escaped so they are treated literally.
    pattern = rf"(?<!\w){re.escape(keyword)}(?!\w)"

    return re.search(
        pattern,
        text,
        re.IGNORECASE,
    ) is not None


# ---------------------------------------------------------
# SKILL DETECTION
# ---------------------------------------------------------

def detect_skills(text: str) -> dict:
    """
    Detect skills in resume text.

    Returns:

        {
            "Programming Languages": [
                "Python",
                "JavaScript"
            ],

            "Web Development": [
                "Django",
                "React"
            ]
        }
    """

    if not text:
        return {}

    detected = {}

    for category, skills in SKILLS.items():

        found = []

        for skill_name, keywords in skills.items():

            for keyword in keywords:

                if _contains_skill(
                    text,
                    keyword,
                ):
                    found.append(skill_name)
                    break

        if found:
            detected[category] = found

    return detected


# ---------------------------------------------------------
# FLAT SKILL LIST
# ---------------------------------------------------------

def get_all_skills(text: str) -> list:
    """Return every detected skill as one list."""

    detected = detect_skills(text)

    return [
        skill
        for skills in detected.values()
        for skill in skills
    ]


# ---------------------------------------------------------
# SKILL COUNT
# ---------------------------------------------------------

def count_skills(text: str) -> int:
    """Return the number of detected skills."""

    return len(
        get_all_skills(text)
    )


# ---------------------------------------------------------
# SKILL SUMMARY
# ---------------------------------------------------------

def get_skill_summary(text: str) -> dict:
    """Return statistics about detected skills."""

    detected = detect_skills(text)

    return {
        "total": count_skills(text),
        "categories": len(detected),
        "by_category": detected,
    }


# ---------------------------------------------------------
# TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    sample_resume = """
    John Doe

    Python Developer

    Skills:
    Python, Django, JavaScript, React, SQL,
    PostgreSQL, Git, Docker, AWS, Pandas, NumPy.

    Experienced in teamwork, communication,
    leadership and problem solving.
    """

    results = detect_skills(
        sample_resume
    )

    print("=" * 50)
    print("DETECTED SKILLS")
    print("=" * 50)

    for category, skills in results.items():

        print(f"\n{category}:")

        for skill in skills:
            print(f"  ✓ {skill}")

    print("\n" + "=" * 50)

    print(
        f"TOTAL SKILLS: "
        f"{count_skills(sample_resume)}"
    )

    print("=" * 50)