"""
ATS Compatibility Agent.

Analyzes a resume for common Applicant Tracking System
(ATS) compatibility factors.

Checks:
- Keyword coverage
- Resume structure
- Important sections
- Contact information
- Job-title alignment
- Formatting issues
"""

import re

from analyzer import detect_sections, detect_contact_info
from job_matcher import extract_job_keywords


EXPECTED_SECTIONS = [
    "Contact Information",
    "Summary",
    "Education",
    "Experience",
    "Skills",
    "Projects",
    "Certifications",
]


def calculate_keyword_coverage(resume_text, job_description=""):
    """
    Calculate how many important job-description keywords
    appear in the resume.

    If no job description is provided, keyword coverage
    cannot be calculated meaningfully.
    """

    if not job_description:
        return {
            "score": 0,
            "matched_keywords": [],
            "missing_keywords": [],
        }

    resume_lower = resume_text.lower()

    job_keywords = extract_job_keywords(
        job_description
    )

    if not job_keywords:
        return {
            "score": 100,
            "matched_keywords": [],
            "missing_keywords": [],
        }

    matched_keywords = []
    missing_keywords = []

    for keyword in job_keywords:
        if keyword.lower() in resume_lower:
            matched_keywords.append(keyword)
        else:
            missing_keywords.append(keyword)

    score = round(
        len(matched_keywords)
        / len(job_keywords)
        * 100
    )

    return {
        "score": score,
        "matched_keywords": matched_keywords,
        "missing_keywords": missing_keywords,
    }


def check_required_sections(resume_text):
    """
    Check which standard resume sections are present.
    """

    sections = detect_sections(resume_text)

    present_sections = []
    missing_sections = []

    for section in EXPECTED_SECTIONS:
        if sections.get(section):
            present_sections.append(section)
        else:
            missing_sections.append(section)

    score = round(
        len(present_sections)
        / len(EXPECTED_SECTIONS)
        * 100
    )

    return {
        "score": score,
        "present_sections": present_sections,
        "missing_sections": missing_sections,
    }


def check_contact_information(resume_text):
    """
    Check whether basic contact information exists.
    """

    contact = detect_contact_info(resume_text)

    fields = [
        "email",
        "phone",
        "location",
    ]

    found = []
    missing = []

    for field in fields:
        value = contact.get(field)

        if value:
            found.append(field)
        else:
            missing.append(field)

    if not fields:
        score = 100
    else:
        score = round(
            len(found) / len(fields) * 100
        )

    return {
        "score": score,
        "found": found,
        "missing": missing,
    }


def check_formatting(resume_text):
    """
    Perform basic ATS-friendly formatting checks.

    These checks focus on plain-text compatibility rather
    than visual design.
    """

    issues = []

    lines = resume_text.splitlines()

    if len(resume_text.strip()) == 0:
        issues.append(
            "Resume contains no readable text."
        )

    if len(resume_text) > 30000:
        issues.append(
            "Resume is unusually long and may be difficult "
            "for some ATS systems to process."
        )

    if "\t" in resume_text:
        issues.append(
            "Resume contains tab characters. "
            "Consistent spacing is safer for ATS parsing."
        )

    special_character_count = len(
        re.findall(
            r"[^\w\s.,:;()'\"&/@%+\-]",
            resume_text,
            flags=re.UNICODE,
        )
    )

    if special_character_count > 50:
        issues.append(
            "Resume contains many unusual special characters. "
            "Simpler formatting may improve ATS compatibility."
        )

    score = max(
        0,
        100 - len(issues) * 20
    )

    return {
        "score": score,
        "issues": issues,
    }


def check_job_title_alignment(
    resume_text,
    job_description="",
):
    """
    Check whether the resume contains the likely job title
    from the job description.

    This uses a simple heuristic and does not attempt to
    infer a title when one cannot be identified.
    """

    if not job_description:
        return {
            "score": 0,
            "job_title": None,
            "aligned": False,
        }

    job_lines = [
        line.strip()
        for line in job_description.splitlines()
        if line.strip()
    ]

    if not job_lines:
        return {
            "score": 0,
            "job_title": None,
            "aligned": False,
        }

    # Usually the first non-empty line is the job title.
    job_title = job_lines[0]

    resume_lower = resume_text.lower()
    title_lower = job_title.lower()

    # Exact title match.
    if title_lower in resume_lower:
        return {
            "score": 100,
            "job_title": job_title,
            "aligned": True,
        }

    # Check individual meaningful title words.
    title_words = [
        word
        for word in re.findall(
            r"\b[a-zA-Z]{3,}\b",
            title_lower,
        )
    ]

    if not title_words:
        return {
            "score": 0,
            "job_title": job_title,
            "aligned": False,
        }

    matched_words = [
        word
        for word in title_words
        if word in resume_lower
    ]

    score = round(
        len(matched_words)
        / len(title_words)
        * 100
    )

    return {
        "score": score,
        "job_title": job_title,
        "aligned": score >= 50,
    }


def calculate_ats_score(
    keyword_score,
    section_score,
    contact_score,
    formatting_score,
    title_score,
):
    """
    Calculate the overall ATS compatibility score.

    Weighting:
    - Keywords: 30%
    - Sections: 25%
    - Contact information: 15%
    - Formatting: 20%
    - Job-title alignment: 10%
    """

    # If there is no job description, title and keyword
    # scores are unavailable.
    if keyword_score == 0 and title_score == 0:
        score = (
            section_score * 0.35
            + contact_score * 0.20
            + formatting_score * 0.45
        )
    else:
        score = (
            keyword_score * 0.30
            + section_score * 0.25
            + contact_score * 0.15
            + formatting_score * 0.20
            + title_score * 0.10
        )

    return round(score)


def generate_ats_recommendations(
    keyword_data,
    section_data,
    contact_data,
    formatting_data,
    title_data,
):
    """
    Generate actionable ATS recommendations.
    """

    recommendations = []

    if keyword_data["missing_keywords"]:
        recommendations.append(
            {
                "priority": "high",
                "message": (
                    "Improve keyword coverage by naturally "
                    "including relevant terms from the job description."
                ),
            }
        )

    if section_data["missing_sections"]:
        recommendations.append(
            {
                "priority": "medium",
                "message": (
                    "Consider adding missing standard sections: "
                    + ", ".join(
                        section_data["missing_sections"]
                    )
                    + "."
                ),
            }
        )

    if contact_data["missing"]:
        recommendations.append(
            {
                "priority": "high",
                "message": (
                    "Add missing contact information: "
                    + ", ".join(
                        contact_data["missing"]
                    )
                    + "."
                ),
            }
        )

    for issue in formatting_data["issues"]:
        recommendations.append(
            {
                "priority": "medium",
                "message": issue,
            }
        )

    if title_data["job_title"] and not title_data["aligned"]:
        recommendations.append(
            {
                "priority": "medium",
                "message": (
                    "Consider aligning the resume's job title "
                    "with the target role when accurate."
                ),
            }
        )

    return recommendations


def analyze_ats(
    resume_text,
    job_description="",
):
    """
    Perform a complete ATS compatibility analysis.

    Returns a structured result that can later be
    consumed by the Career Intelligence Agent.
    """

    if not resume_text or not resume_text.strip():
        raise ValueError(
            "Resume text cannot be empty."
        )

    keyword_data = calculate_keyword_coverage(
        resume_text,
        job_description,
    )

    section_data = check_required_sections(
        resume_text
    )

    contact_data = check_contact_information(
        resume_text
    )

    formatting_data = check_formatting(
        resume_text
    )

    title_data = check_job_title_alignment(
        resume_text,
        job_description,
    )

    ats_score = calculate_ats_score(
        keyword_data["score"],
        section_data["score"],
        contact_data["score"],
        formatting_data["score"],
        title_data["score"],
    )

    recommendations = generate_ats_recommendations(
        keyword_data,
        section_data,
        contact_data,
        formatting_data,
        title_data,
    )

    return {
        "ats_score": ats_score,

        "keyword_coverage": keyword_data,

        "sections": section_data,

        "contact_information": contact_data,

        "formatting": formatting_data,

        "job_title_alignment": title_data,

        "recommendations": recommendations,
    }


# ---------------------------------------------------------
# Direct test
# ---------------------------------------------------------

if __name__ == "__main__":

    example_resume = """
    ALEX JOHNSON

    Software Developer

    Email: alex.johnson@example.com
    Phone: +1 555-123-4567
    Location: New York, NY

    SUMMARY

    Software Developer with 3 years of experience
    building web applications.

    EDUCATION

    Bachelor of Science in Computer Science

    EXPERIENCE

    Software Developer
    TechNova Solutions

    - Developed web applications using Python and Django.
    - Built REST APIs for internal tools.

    SKILLS

    Python, Django, SQL, Git, Docker

    PROJECTS

    Task Management Web Application

    CERTIFICATIONS

    Python Programming Certificate
    """

    example_job = """
    Backend Developer

    Required:
    Python
    Django
    SQL
    AWS

    Preferred:
    Docker

    3+ years of experience.

    REST APIs and Git experience preferred.
    """

    result = analyze_ats(
        example_resume,
        example_job,
    )

    print("\nATS ANALYSIS")
    print("-" * 40)

    for key, value in result.items():
        print(f"{key}: {value}")