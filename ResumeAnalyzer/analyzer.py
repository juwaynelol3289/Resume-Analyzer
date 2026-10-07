"""
Main resume analysis engine.

Uses skills.py to analyze a resume
and generate a structured report.
"""

import re

from skills import detect_skills, get_all_skills

from config import (
    SECTION_WEIGHTS,
    SKILL_SCORE_THRESHOLDS,
    SKILL_SCORE_MAX,
    CONTENT_SCORE_MAX,
)

from recommendations import generate_resume_recommendations


# ---------------------------------------------------------
# EXPECTED RESUME SECTIONS
# ---------------------------------------------------------

SECTIONS = {
    "Contact Information": [
        "contact",
        "phone",
        "email",
        "linkedin",
        "github",
    ],

    "Summary": [
        "summary",
        "professional summary",
        "profile",
        "objective",
        "career objective",
    ],

    "Education": [
        "education",
        "academic background",
        "qualifications",
    ],

    "Experience": [
        "experience",
        "work experience",
        "employment",
        "professional experience",
    ],

    "Skills": [
        "skills",
        "technical skills",
        "core skills",
        "competencies",
    ],

    "Projects": [
        "projects",
        "personal projects",
        "academic projects",
    ],

    "Certifications": [
        "certifications",
        "certificates",
        "licenses",
    ],
}


# ---------------------------------------------------------
# SECTION DETECTION
# ---------------------------------------------------------

def detect_sections(text: str) -> dict:
    """Detect common resume sections."""

    text_lower = text.lower()

    sections_found = {}

    for section, keywords in SECTIONS.items():
        sections_found[section] = any(
            re.search(
                rf"(?<!\w){re.escape(keyword)}(?!\w)",
                text_lower,
            )
            for keyword in keywords
        )

    return sections_found


# ---------------------------------------------------------
# CONTACT INFORMATION
# ---------------------------------------------------------

def detect_contact_info(text: str) -> dict:
    """Detect common contact information."""

    email = re.search(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        text,
    )

    phone = re.search(
        r"(?:\+?\d[\d\s().-]{7,}\d)",
        text,
    )

    linkedin = re.search(
        r"(linkedin\.com/in/[A-Za-z0-9_-]+)",
        text,
        re.IGNORECASE,
    )

    github = re.search(
        r"(github\.com/[A-Za-z0-9_-]+)",
        text,
        re.IGNORECASE,
    )

    return {
        "email": email is not None,
        "phone": phone is not None,
        "linkedin": linkedin is not None,
        "github": github is not None,
    }


# ---------------------------------------------------------
# WORD COUNT
# ---------------------------------------------------------

def get_word_count(text: str) -> int:
    """Return the approximate number of words."""

    return len(
        re.findall(
            r"\b[\w'-]+\b",
            text,
        )
    )


# ---------------------------------------------------------
# EXPERIENCE DETECTION
# ---------------------------------------------------------

def estimate_experience(text: str) -> dict:
    """Detect explicitly mentioned years of experience."""

    matches = re.findall(
        r"(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*experience",
        text.lower(),
    )

    years = [int(value) for value in matches]

    return {
        "mentioned": bool(years),
        "years": max(years) if years else 0,
    }


# ---------------------------------------------------------
# SECTION SCORE
# ---------------------------------------------------------

def calculate_section_score(sections: dict) -> tuple:
    """Calculate the resume section score."""

    score = sum(
        weight
        for section, weight in SECTION_WEIGHTS.items()
        if sections.get(section, False)
    )

    maximum = sum(
        SECTION_WEIGHTS.values()
    )

    return score, maximum


# ---------------------------------------------------------
# SKILL SCORE
# ---------------------------------------------------------

def calculate_skill_score(skill_count: int) -> tuple:
    """Calculate skill score using config.py thresholds."""

    for minimum_skills, points in SKILL_SCORE_THRESHOLDS:
        if skill_count >= minimum_skills:
            return points, SKILL_SCORE_MAX

    return 0, SKILL_SCORE_MAX


# ---------------------------------------------------------
# CONTENT SCORE
# ---------------------------------------------------------

def calculate_content_score(
    word_count: int,
    contact_info: dict,
    experience: dict,
) -> tuple:
    """Calculate basic content score."""

    score = 0

    # Resume length.
    if 250 <= word_count <= 1200:
        score += 6

    elif (
        150 <= word_count < 250
        or 1200 < word_count <= 1600
    ):
        score += 4

    elif word_count >= 100:
        score += 2

    # Contact information.
    if contact_info["email"]:
        score += 3

    if contact_info["phone"]:
        score += 2

    # Experience.
    if experience["mentioned"]:
        score += 2

    return min(
        score,
        CONTENT_SCORE_MAX,
    ), CONTENT_SCORE_MAX


# ---------------------------------------------------------
# MAIN ANALYZER
# ---------------------------------------------------------

def analyze_resume(text: str) -> dict:
    """
    Analyze a resume and return a complete report.
    """

    if not text or not text.strip():
        raise ValueError(
            "Resume text is empty."
        )

    # Analyze basic information.
    sections = detect_sections(text)

    contact_info = detect_contact_info(text)

    experience = estimate_experience(text)

    # Analyze skills.
    detected_skills = detect_skills(text)

    all_skills = get_all_skills(text)

    skill_count = len(all_skills)

    # Analyze content.
    word_count = get_word_count(text)

    # Calculate scores.
    section_score, section_max = (
        calculate_section_score(sections)
    )

    skill_score, skill_max = (
        calculate_skill_score(skill_count)
    )

    content_score, content_max = (
        calculate_content_score(
            word_count,
            contact_info,
            experience,
        )
    )

    # Raw score.
    total_score = (
        section_score
        + skill_score
        + content_score
    )

    maximum_score = (
        section_max
        + skill_max
        + content_max
    )

    # Normalize to 0-100.
    percentage = round(
        (total_score / maximum_score) * 100
    )

    # Generate recommendations through the
    # dedicated recommendation module.
    recommendations = (
        generate_resume_recommendations(
            sections=sections,
            contact_info=contact_info,
            skill_count=skill_count,
            word_count=word_count,
            experience=experience,
        )
    )

    return {
        "score": percentage,

        "score_details": {
            "sections": {
                "score": section_score,
                "maximum": section_max,
            },

            "skills": {
                "score": skill_score,
                "maximum": skill_max,
            },

            "content": {
                "score": content_score,
                "maximum": content_max,
            },
        },

        "word_count": word_count,

        "sections": sections,

        "contact": contact_info,

        "experience": experience,

        "skills": detected_skills,

        "skill_count": skill_count,

        "recommendations": recommendations,
    }


# ---------------------------------------------------------
# TERMINAL TEST
# ---------------------------------------------------------

if __name__ == "__main__":

    sample_resume = """
    John Doe
    john.doe@email.com
    +91 9876543210
    linkedin.com/in/johndoe
    github.com/johndoe

    Professional Summary
    Python developer with 3 years of experience building
    web applications.

    Education
    Bachelor of Computer Science

    Work Experience
    Python Developer - ABC Technologies
    Developed web applications using Python and Django.

    Skills
    Python, Django, JavaScript, React, SQL, PostgreSQL,
    Git, Docker, AWS, Pandas, NumPy.

    Projects
    Resume Analyzer
    Built a resume analysis application using Python.

    Certifications
    Python Programming Certificate
    """

    report = analyze_resume(sample_resume)

    print("\n" + "=" * 60)
    print("📄 RESUME ANALYSIS")
    print("=" * 60)

    print(
        f"\n⭐ Overall Score: "
        f"{report['score']}/100"
    )

    print(
        f"📝 Word Count: "
        f"{report['word_count']}"
    )

    print(
        f"🧠 Skills Found: "
        f"{report['skill_count']}"
    )

    print("\n📂 SECTIONS")

    for section, found in report["sections"].items():
        icon = "✅" if found else "❌"
        print(f"{icon} {section}")

    print("\n🧠 SKILLS")

    for category, skills in report["skills"].items():
        print(f"\n{category}:")
        print("  " + ", ".join(skills))

    print("\n📊 SCORE BREAKDOWN")

    for category, data in report["score_details"].items():
        print(
            f"{category.title()}: "
            f"{data['score']}/{data['maximum']}"
        )

    print("\n💡 RECOMMENDATIONS")

    if report["recommendations"]:
        for recommendation in report["recommendations"]:
            print(
                f"[{recommendation['priority'].upper()}] "
                f"{recommendation['message']}"
            )
    else:
        print("🎉 No major recommendations!")