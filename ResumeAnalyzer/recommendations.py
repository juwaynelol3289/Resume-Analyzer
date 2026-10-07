"""
Recommendation engine for Resume Analyzer.

Generates actionable recommendations from resume analysis
and optional job-match information.

The engine supports both:
    1. The newer analysis-dictionary interface.
    2. The older keyword-argument interface.

The engine always attempts to provide useful recommendations.
"""

from config import (
    MAX_RECOMMENDATIONS,
    MAX_MISSING_SKILLS_DISPLAYED,
)


# =============================================================
# PRIORITY
# =============================================================

PRIORITY_ORDER = {
    "high": 0,
    "medium": 1,
    "low": 2,
}


# =============================================================
# RECOMMENDATION CREATION
# =============================================================

def create_recommendation(
    message,
    priority="medium",
    category="General",
):
    """Create a standard recommendation."""

    return {
        "message": message,
        "priority": priority,
        "category": category,
    }


# =============================================================
# STRUCTURE ANALYSIS
# =============================================================

def analyze_structure(analysis):
    """Analyze resume sections."""

    recommendations = []

    sections = analysis.get(
        "sections",
        {},
    )

    if not sections:

        recommendations.append(
            create_recommendation(
                "Make sure your resume includes clear sections "
                "for your summary, education, experience, skills, "
                "projects, and certifications where relevant.",
                "medium",
                "Structure",
            )
        )

        return recommendations

    for section, present in sections.items():

        if not present:

            recommendations.append(
                create_recommendation(
                    f"Add a {section} section to make your "
                    "resume more complete.",
                    "high",
                    "Structure",
                )
            )

    # Strong structure still gets useful advice.
    if all(sections.values()):

        recommendations.append(
            create_recommendation(
                "Your resume contains the major expected sections. "
                "Keep this structure consistent and easy to scan.",
                "low",
                "Structure",
            )
        )

    return recommendations


# =============================================================
# CONTACT ANALYSIS
# =============================================================

def analyze_contact(analysis):
    """Analyze contact information."""

    recommendations = []

    contact = analysis.get(
        "contact",
        {},
    )

    if not contact:

        recommendations.append(
            create_recommendation(
                "Make sure your resume includes clear contact "
                "information such as your name, email address, "
                "and phone number.",
                "high",
                "Contact",
            )
        )

        return recommendations

    missing = []

    if not contact.get("name"):
        missing.append("name")

    if not contact.get("email"):
        missing.append("email address")

    if not contact.get("phone"):
        missing.append("phone number")

    if missing:

        recommendations.append(
            create_recommendation(
                "Add missing contact information: "
                + ", ".join(missing)
                + ".",
                "high",
                "Contact",
            )
        )

    else:

        recommendations.append(
            create_recommendation(
                "Your contact information is complete. "
                "Keep it easy to find near the top of the resume.",
                "low",
                "Contact",
            )
        )

    return recommendations


# =============================================================
# SKILL ANALYSIS
# =============================================================

def analyze_skills(analysis):
    """Analyze the resume's skills."""

    recommendations = []

    skill_count = analysis.get(
        "skill_count",
        0,
    )

    skills = analysis.get(
        "skills",
        {},
    )

    if skill_count == 0:

        recommendations.append(
            create_recommendation(
                "Add a dedicated skills section containing "
                "relevant technical and professional skills.",
                "high",
                "Skills",
            )
        )

        return recommendations

    if skill_count < 4:

        recommendations.append(
            create_recommendation(
                "Consider adding more relevant skills that "
                "you genuinely have experience with.",
                "medium",
                "Skills",
            )
        )

    elif skill_count < 8:

        recommendations.append(
            create_recommendation(
                "Your skills section has a reasonable foundation. "
                "Consider adding other relevant skills from your "
                "actual experience.",
                "low",
                "Skills",
            )
        )

    else:

        recommendations.append(
            create_recommendation(
                "Your resume contains a strong range of skills. "
                "Prioritize the skills most relevant to your "
                "target roles.",
                "low",
                "Skills",
            )
        )

    if skills:

        recommendations.append(
            create_recommendation(
                "Keep your skills section focused on skills "
                "you can confidently demonstrate through your "
                "education, projects, or experience.",
                "low",
                "Skills",
            )
        )

    return recommendations


# =============================================================
# LENGTH ANALYSIS
# =============================================================

def analyze_length(analysis):
    """Analyze resume length."""

    recommendations = []

    word_count = analysis.get(
        "word_count",
        0,
    )

    if word_count == 0:

        recommendations.append(
            create_recommendation(
                "Add meaningful resume content before "
                "optimizing its length.",
                "high",
                "Content",
            )
        )

    elif word_count < 150:

        recommendations.append(
            create_recommendation(
                "Your resume is quite short. Add relevant "
                "education, experience, projects, or achievements "
                "where appropriate.",
                "medium",
                "Content",
            )
        )

    elif word_count > 1200:

        recommendations.append(
            create_recommendation(
                "Your resume is quite long. Remove repetitive "
                "or less relevant information and prioritize "
                "your strongest experience.",
                "medium",
                "Content",
            )
        )

    else:

        recommendations.append(
            create_recommendation(
                "Your resume length is reasonable. Keep future "
                "edits focused on relevant information.",
                "low",
                "Content",
            )
        )

    return recommendations


# =============================================================
# EXPERIENCE ANALYSIS
# =============================================================

def analyze_experience(analysis):
    """Analyze experience information."""

    recommendations = []

    experience = analysis.get(
        "experience",
        {},
    )

    sections = analysis.get(
        "sections",
        {},
    )

    if not sections.get(
        "Experience",
        False,
    ):

        recommendations.append(
            create_recommendation(
                "Add an experience section if you have relevant "
                "work, internship, volunteer, or practical "
                "experience.",
                "medium",
                "Experience",
            )
        )

        return recommendations

    if not experience:

        recommendations.append(
            create_recommendation(
                "Make your experience descriptions specific "
                "and focused on what you accomplished.",
                "medium",
                "Experience",
            )
        )

    else:

        recommendations.append(
            create_recommendation(
                "Strengthen experience bullets by describing "
                "your actions, results, and measurable impact "
                "where possible.",
                "medium",
                "Experience",
            )
        )

    return recommendations


# =============================================================
# JOB MATCH ANALYSIS
# =============================================================

def analyze_job_match(job_match):
    """Generate recommendations from job matching."""

    recommendations = []

    if not job_match:
        return recommendations

    overall_match = job_match.get(
        "overall_match",
        0,
    )

    missing_skills = job_match.get(
        "missing_skills",
        [],
    )

    missing_keywords = job_match.get(
        "missing_keywords",
        [],
    )

    if overall_match < 50:

        recommendations.append(
            create_recommendation(
                "Your resume has a low match with this job. "
                "Review the missing skills and keywords and "
                "only add items you genuinely possess.",
                "high",
                "Job Match",
            )
        )

    elif overall_match < 75:

        recommendations.append(
            create_recommendation(
                "Your resume has a moderate match with this job. "
                "Focus on the highest-priority missing skills "
                "and relevant keywords you genuinely have.",
                "medium",
                "Job Match",
            )
        )

    else:

        recommendations.append(
            create_recommendation(
                "Your resume matches this job well. "
                "Keep the strongest matching skills and "
                "keywords prominent.",
                "low",
                "Job Match",
            )
        )

    if missing_skills:

        displayed_skills = missing_skills[
            :MAX_MISSING_SKILLS_DISPLAYED
        ]

        recommendations.append(
            create_recommendation(
                "Review these missing skills: "
                + ", ".join(displayed_skills)
                + ". Only add skills you actually possess.",
                "high",
                "Skill Gap",
            )
        )

    if missing_keywords:

        recommendations.append(
            create_recommendation(
                "Review the job description for important "
                "missing keywords such as: "
                + ", ".join(missing_keywords[:8])
                + ". Use them naturally when truthful.",
                "medium",
                "ATS",
            )
        )

    return recommendations


# =============================================================
# SORTING
# =============================================================

def sort_recommendations(recommendations):
    """Sort recommendations by priority."""

    return sorted(
        recommendations,
        key=lambda recommendation: (
            PRIORITY_ORDER.get(
                recommendation.get(
                    "priority",
                    "medium",
                ),
                1,
            )
        ),
    )


# =============================================================
# DUPLICATE REMOVAL
# =============================================================

def remove_duplicates(recommendations):
    """Remove duplicate recommendation messages."""

    unique = []
    seen = set()

    for recommendation in recommendations:

        message = recommendation.get(
            "message",
            "",
        ).strip().lower()

        if not message:
            continue

        if message in seen:
            continue

        seen.add(message)

        unique.append(
            recommendation
        )

    return unique


# =============================================================
# FALLBACK RECOMMENDATIONS
# =============================================================

def create_fallback_recommendations():
    """
    Recommendations used when no obvious weaknesses
    were detected.
    """

    return [

        create_recommendation(
            "Add measurable achievements to your strongest "
            "experience or project bullets whenever possible.",
            "medium",
            "Impact",
        ),

        create_recommendation(
            "Tailor your resume to each target job by "
            "highlighting the most relevant skills and "
            "experience.",
            "medium",
            "Job Targeting",
        ),

        create_recommendation(
            "Keep your resume concise and remove information "
            "that does not support your target role.",
            "low",
            "Content",
        ),

        create_recommendation(
            "Review your resume regularly and update it with "
            "new projects, skills, certifications, and "
            "achievements.",
            "low",
            "Maintenance",
        ),

    ]


# =============================================================
# RESUME RECOMMENDATIONS
# =============================================================

def generate_resume_recommendations(
    analysis=None,
    sections=None,
    contact=None,
    skills=None,
    word_count=0,
    experience=None,
    **kwargs,
):
    """
    Generate recommendations from resume analysis.

    Supports both:

        generate_resume_recommendations(analysis)

    and the older style:

        generate_resume_recommendations(
            sections=...,
            contact=...,
            skills=...,
            word_count=...,
            experience=...
        )
    """

    # =========================================================
    # NEW INTERFACE
    # =========================================================

    if analysis is not None:

        if not isinstance(
            analysis,
            dict,
        ):
            analysis = {}

    # =========================================================
    # OLD INTERFACE
    # =========================================================

    else:

        analysis = {
            "sections": sections or {},
            "contact": contact or {},
            "skills": skills or {},

            "skill_count": (
                sum(
                    len(skill_list)
                    for skill_list in (
                        skills or {}
                    ).values()
                    if isinstance(
                        skill_list,
                        list,
                    )
                )
                if isinstance(
                    skills,
                    dict,
                )
                else 0
            ),

            "word_count": word_count or 0,

            "experience": experience or {},
        }

    recommendations = []

    # =========================================================
    # RUN ANALYZERS
    # =========================================================

    recommendations.extend(
        analyze_structure(
            analysis
        )
    )

    recommendations.extend(
        analyze_contact(
            analysis
        )
    )

    recommendations.extend(
        analyze_skills(
            analysis
        )
    )

    recommendations.extend(
        analyze_length(
            analysis
        )
    )

    recommendations.extend(
        analyze_experience(
            analysis
        )
    )

    # =========================================================
    # CLEAN
    # =========================================================

    recommendations = remove_duplicates(
        recommendations
    )

    recommendations = sort_recommendations(
        recommendations
    )

    # =========================================================
    # NEVER RETURN AN EMPTY LIST
    # =========================================================

    if not recommendations:

        recommendations = (
            create_fallback_recommendations()
        )

    return recommendations[
        :MAX_RECOMMENDATIONS
    ]


# =============================================================
# JOB RECOMMENDATIONS
# =============================================================

def generate_job_recommendations(
    analysis,
    job_match=None,
):
    """
    Generate recommendations using resume analysis
    and optional job-match information.
    """

    recommendations = (
        generate_resume_recommendations(
            analysis
        )
    )

    if job_match:

        recommendations.extend(
            analyze_job_match(
                job_match
            )
        )

    recommendations = remove_duplicates(
        recommendations
    )

    recommendations = sort_recommendations(
        recommendations
    )

    if not recommendations:

        recommendations = (
            create_fallback_recommendations()
        )

    return recommendations[
        :MAX_RECOMMENDATIONS
    ]