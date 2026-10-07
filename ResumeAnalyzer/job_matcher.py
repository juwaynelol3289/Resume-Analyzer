"""
Job Description and Resume Matching Engine.

Compares a resume against a job description and identifies:
- Required skills
- Preferred skills
- Experience requirements
- Important keywords
- Matched skills
- Missing skills
- Priority gaps
- Overall match percentage

This module is deterministic and does not use AI.
"""

import re

from config import (
    JOB_SKILL_WEIGHT,
    JOB_KEYWORD_WEIGHT,
    MAX_MISSING_SKILLS_DISPLAYED,
)

from skills import detect_skills


# Common job-related keywords that can be useful when matching
COMMON_JOB_KEYWORDS = [
    "api",
    "rest",
    "rest api",
    "backend",
    "frontend",
    "full stack",
    "software development",
    "web development",
    "database",
    "sql",
    "testing",
    "debugging",
    "version control",
    "agile",
    "scrum",
    "cloud",
    "automation",
    "deployment",
    "devops",
    "data analysis",
    "machine learning",
    "communication",
    "leadership",
    "teamwork",
    "problem solving",
]


def normalize_text(text):
    """
    Normalize text for easier matching.
    """

    if not text:
        return ""

    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_job_keywords(job_description):
    """
    Extract important keywords from a job description.

    Returns a list of keywords found in the job description.
    """

    normalized = normalize_text(job_description)

    found_keywords = []

    for keyword in COMMON_JOB_KEYWORDS:
        if keyword in normalized:
            found_keywords.append(keyword)

    return found_keywords


def extract_experience_requirements(job_description):
    """
    Extract basic experience requirements from a job description.

    Examples:
    - 3+ years
    - 2 years of experience
    - minimum 5 years
    """

    if not job_description:
        return []

    patterns = [
        r"\b\d+\+?\s+years?\s+(?:of\s+)?experience\b",
        r"\bminimum\s+\d+\s+years?\b",
        r"\bat\s+least\s+\d+\s+years?\b",
    ]

    requirements = []

    for pattern in patterns:
        matches = re.findall(
            pattern,
            job_description,
            flags=re.IGNORECASE,
        )

        for match in matches:
            cleaned = match.strip()

            if cleaned not in requirements:
                requirements.append(cleaned)

    return requirements


def extract_required_and_preferred_sections(job_description):
    """
    Try to separate skills mentioned as required from skills
    mentioned as preferred or nice-to-have.

    This is a deterministic heuristic, not an AI judgment.
    """

    if not job_description:
        return "", ""

    lines = job_description.splitlines()

    required_lines = []
    preferred_lines = []

    current_section = "required"

    for line in lines:
        stripped = line.strip()

        if not stripped:
            continue

        lower = stripped.lower()

        if any(
            phrase in lower
            for phrase in [
                "preferred",
                "nice to have",
                "nice-to-have",
                "bonus",
                "desired",
                "plus",
            ]
        ):
            current_section = "preferred"
            continue

        if any(
            phrase in lower
            for phrase in [
                "required",
                "requirements",
                "must have",
                "must-have",
                "qualifications",
            ]
        ):
            current_section = "required"
            continue

        if current_section == "preferred":
            preferred_lines.append(stripped)
        else:
            required_lines.append(stripped)

    return (
        "\n".join(required_lines),
        "\n".join(preferred_lines),
    )


def extract_required_skills(job_description):
    """
    Detect skills from the job description that appear in
    required/qualification sections.
    """

    required_text, _ = extract_required_and_preferred_sections(
        job_description
    )

    if not required_text.strip():
        required_text = job_description

    return detect_skills(required_text)


def extract_preferred_skills(job_description):
    """
    Detect skills from preferred/nice-to-have sections.
    """

    _, preferred_text = extract_required_and_preferred_sections(
        job_description
    )

    if not preferred_text.strip():
        return []

    return detect_skills(preferred_text)


def match_skills(resume_text, job_description):
    """
    Compare skills in the resume against skills in the job description.

    Returns:
        matched_skills
        missing_skills
        required_skills
        preferred_skills
    """

    resume_skills = set(detect_skills(resume_text))

    required_skills = set(
        extract_required_skills(job_description)
    )

    preferred_skills = set(
        extract_preferred_skills(job_description)
    )

    all_job_skills = required_skills | preferred_skills

    matched_skills = sorted(
        resume_skills & all_job_skills
    )

    missing_skills = sorted(
        all_job_skills - resume_skills
    )

    return {
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "required_skills": sorted(required_skills),
        "preferred_skills": sorted(preferred_skills),
    }


def match_keywords(resume_text, job_description):
    """
    Compare important job keywords against the resume.
    """

    resume_normalized = normalize_text(resume_text)
    job_keywords = extract_job_keywords(job_description)

    matched_keywords = []
    missing_keywords = []

    for keyword in job_keywords:
        if keyword in resume_normalized:
            matched_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)

    return {
        "matched_keywords": sorted(matched_keywords),
        "missing_keywords": sorted(missing_keywords),
        "total_keywords": len(job_keywords),
    }


def calculate_skill_match(skill_data):
    """
    Calculate the percentage of job skills matched.
    """

    required_skills = skill_data["required_skills"]
    preferred_skills = skill_data["preferred_skills"]
    matched_skills = skill_data["matched_skills"]

    all_job_skills = set(
        required_skills + preferred_skills
    )

    if not all_job_skills:
        return 0

    return round(
        len(set(matched_skills))
        / len(all_job_skills)
        * 100
    )


def calculate_keyword_match(keyword_data):
    """
    Calculate the percentage of important keywords matched.
    """

    total_keywords = keyword_data["total_keywords"]

    if total_keywords == 0:
        return 0

    return round(
        len(keyword_data["matched_keywords"])
        / total_keywords
        * 100
    )


def calculate_overall_match(skill_match, keyword_match):
    """
    Calculate the overall resume-to-job match.

    Skills are weighted more heavily than keywords.
    """

    score = (
        skill_match * JOB_SKILL_WEIGHT
        + keyword_match * JOB_KEYWORD_WEIGHT
    )

    return round(score)


def prioritize_gaps(skill_data, job_description):
    """
    Prioritize missing skills.

    Required skills are considered higher priority than
    preferred skills.
    """

    required_skills = set(
        skill_data["required_skills"]
    )

    preferred_skills = set(
        skill_data["preferred_skills"]
    )

    missing_skills = set(
        skill_data["missing_skills"]
    )

    priority_gaps = []

    for skill in missing_skills:

        if skill in required_skills:
            priority = "high"
            reason = (
                "Required skill mentioned in the job description."
            )
        elif skill in preferred_skills:
            priority = "medium"
            reason = (
                "Preferred skill mentioned in the job description."
            )
        else:
            priority = "low"
            reason = "Relevant skill gap."

        priority_gaps.append(
            {
                "skill": skill,
                "priority": priority,
                "reason": reason,
            }
        )

    priority_order = {
        "high": 0,
        "medium": 1,
        "low": 2,
    }

    priority_gaps.sort(
        key=lambda item: (
            priority_order[item["priority"]],
            item["skill"].lower(),
        )
    )

    return priority_gaps[
        :MAX_MISSING_SKILLS_DISPLAYED
    ]


def explain_match(
    overall_match,
    skill_match,
    keyword_match,
    skill_data,
):
    """
    Generate a simple deterministic explanation of the match.
    """

    if overall_match >= 85:
        level = "Strong match"
    elif overall_match >= 70:
        level = "Good match"
    elif overall_match >= 50:
        level = "Moderate match"
    else:
        level = "Low match"

    missing_required = [
        skill
        for skill in skill_data["missing_skills"]
        if skill in skill_data["required_skills"]
    ]

    if missing_required:
        return (
            f"{level} for this role, but there are important "
            f"missing required skills: "
            f"{', '.join(missing_required[:5])}."
        )

    if skill_match >= keyword_match:
        return (
            f"{level}. The resume has good skill alignment "
            "with the job description."
        )

    return (
        f"{level}, but the resume could improve its "
        "keyword alignment with the job description."
    )


def match_resume_to_job(resume_text, job_description):
    """
    Perform a complete resume-to-job comparison.

    Returns a structured dictionary suitable for the UI
    and future AI orchestration.
    """

    if not resume_text or not resume_text.strip():
        raise ValueError("Resume text cannot be empty.")

    if not job_description or not job_description.strip():
        raise ValueError(
            "Job description cannot be empty."
        )

    skill_data = match_skills(
        resume_text,
        job_description,
    )

    keyword_data = match_keywords(
        resume_text,
        job_description,
    )

    skill_match = calculate_skill_match(
        skill_data
    )

    keyword_match = calculate_keyword_match(
        keyword_data
    )

    overall_match = calculate_overall_match(
        skill_match,
        keyword_match,
    )

    experience_requirements = (
        extract_experience_requirements(
            job_description
        )
    )

    priority_gaps = prioritize_gaps(
        skill_data,
        job_description,
    )

    explanation = explain_match(
        overall_match,
        skill_match,
        keyword_match,
        skill_data,
    )

    return {
        "overall_match": overall_match,

        "skill_match": skill_match,

        "keyword_match": keyword_match,

        "matched_skills": skill_data[
            "matched_skills"
        ],

        "missing_skills": skill_data[
            "missing_skills"
        ],

        "required_skills": skill_data[
            "required_skills"
        ],

        "preferred_skills": skill_data[
            "preferred_skills"
        ],

        "matched_keywords": keyword_data[
            "matched_keywords"
        ],

        "missing_keywords": keyword_data[
            "missing_keywords"
        ],

        "experience_requirements": (
            experience_requirements
        ),

        "priority_gaps": priority_gaps,

        "explanation": explanation,
    }


# ---------------------------------------------------------
# Direct test
# ---------------------------------------------------------

if __name__ == "__main__":

    example_resume = """
    Software Developer with 3 years of experience.
    Python, Django, SQL, PostgreSQL, Git, Docker.
    Built REST APIs and web applications.
    """

    example_job = """
    Software Developer

    Required:
    Python
    Django
    SQL
    AWS
    3+ years of experience

    Preferred:
    Docker
    Kubernetes

    Experience with REST APIs and Git is preferred.
    """

    result = match_resume_to_job(
        example_resume,
        example_job,
    )

    print("\nJOB MATCH RESULTS")
    print("-" * 40)

    for key, value in result.items():
        print(f"{key}: {value}")