"""
Resume Improvement Agent.

Identifies weak resume content and generates improvement
suggestions without inventing experience, skills, or achievements.

The actual rewriting can later be connected to the AI system.
This module provides deterministic analysis and structured
inputs for the future AI Rewrite Agent.
"""

import re


WEAK_ACTION_WORDS = {
    "worked": "Developed or contributed to",
    "helped": "Contributed to",
    "did": "Completed",
    "made": "Created",
    "used": "Utilized",
    "responsible for": "Managed",
    "was responsible for": "Managed",
    "assisted": "Supported",
}


VAGUE_PHRASES = [
    "worked on",
    "helped with",
    "did some",
    "responsible for",
    "was responsible for",
    "involved in",
    "worked with",
]


ACHIEVEMENT_INDICATORS = [
    "%",
    "increased",
    "decreased",
    "reduced",
    "improved",
    "saved",
    "generated",
    "grew",
    "achieved",
    "delivered",
    "launched",
    "completed",
]


def extract_bullet_points(resume_text):
    """
    Extract bullet points from a resume.
    """

    if not resume_text:
        return []

    bullets = []

    for line in resume_text.splitlines():
        line = line.strip()

        if not line:
            continue

        if re.match(r"^[-•*]\s+", line):
            bullet = re.sub(
                r"^[-•*]\s+",
                "",
                line,
            ).strip()

            if bullet:
                bullets.append(bullet)

    return bullets


def detect_weak_bullet_points(resume_text):
    """
    Identify bullet points that may need stronger wording.

    A bullet is considered potentially weak when it:
    - Uses vague action phrases
    - Is too short
    - Does not describe an outcome
    - Starts with weak wording
    """

    bullets = extract_bullet_points(resume_text)

    weak_bullets = []

    for bullet in bullets:
        lower = bullet.lower()

        reasons = []

        # Check vague phrases.
        for phrase in VAGUE_PHRASES:
            if lower.startswith(phrase):
                reasons.append(
                    "Uses vague wording."
                )
                break

        # Check very short bullets.
        if len(bullet.split()) < 6:
            reasons.append(
                "Contains very little detail."
            )

        # Check achievement evidence.
        has_achievement = any(
            indicator in lower
            for indicator in ACHIEVEMENT_INDICATORS
        )

        if not has_achievement:
            reasons.append(
                "Does not clearly show measurable impact."
            )

        if reasons:
            weak_bullets.append(
                {
                    "original": bullet,
                    "reasons": reasons,
                }
            )

    return weak_bullets


def suggest_bullet_structure(bullet):
    """
    Suggest a stronger structure for a resume bullet.

    The structure is:

    Action + Task + Technology/Method + Result
    """

    return (
        "Try structuring this bullet as: "
        "Action + Task + Technology/Method + Result."
    )


def analyze_bullet_points(resume_text):
    """
    Analyze resume bullets and provide improvement guidance.
    """

    weak_bullets = detect_weak_bullet_points(
        resume_text
    )

    results = []

    for item in weak_bullets:
        results.append(
            {
                "original": item["original"],
                "reasons": item["reasons"],
                "suggestion": suggest_bullet_structure(
                    item["original"]
                ),
            }
        )

    return results


def analyze_summary(resume_text):
    """
    Analyze the resume summary.

    This does not rewrite the summary yet.
    It identifies areas that could be improved.
    """

    lines = resume_text.splitlines()

    summary_lines = []

    in_summary = False

    for line in lines:
        stripped = line.strip()

        if stripped.lower() in {
            "summary",
            "professional summary",
            "profile",
        }:
            in_summary = True
            continue

        if in_summary:
            if stripped.upper() in {
                "EDUCATION",
                "EXPERIENCE",
                "SKILLS",
                "PROJECTS",
                "CERTIFICATIONS",
            }:
                break

            if stripped:
                summary_lines.append(stripped)

    if not summary_lines:
        return {
            "present": False,
            "issues": [
                "No professional summary was detected."
            ],
            "suggestion": (
                "Consider adding a concise professional "
                "summary tailored to the target role."
            ),
        }

    summary = " ".join(summary_lines)

    issues = []

    if len(summary.split()) < 25:
        issues.append(
            "Summary may be too short."
        )

    if len(summary.split()) > 100:
        issues.append(
            "Summary may be too long."
        )

    if not any(
        word in summary.lower()
        for word in [
            "experience",
            "developer",
            "engineer",
            "analyst",
            "designer",
            "manager",
            "specialist",
        ]
    ):
        issues.append(
            "Summary may not clearly communicate the candidate's role."
        )

    return {
        "present": True,
        "text": summary,
        "issues": issues,
        "suggestion": (
            "Highlight the candidate's role, strongest relevant "
            "skills, experience, and value to the target position."
        ),
    }


def suggest_wording_improvements(resume_text):
    """
    Identify common weak wording and suggest stronger alternatives.

    This does NOT automatically rewrite the candidate's content.
    """

    suggestions = []

    for weak_phrase, stronger_phrase in WEAK_ACTION_WORDS.items():

        if weak_phrase in resume_text.lower():

            suggestions.append(
                {
                    "original_phrase": weak_phrase,
                    "suggested_phrase": stronger_phrase,
                }
            )

    return suggestions


def analyze_resume_for_improvement(resume_text):
    """
    Perform a complete deterministic resume improvement analysis.
    """

    if not resume_text or not resume_text.strip():
        raise ValueError(
            "Resume text cannot be empty."
        )

    bullet_analysis = analyze_bullet_points(
        resume_text
    )

    summary_analysis = analyze_summary(
        resume_text
    )

    wording_analysis = suggest_wording_improvements(
        resume_text
    )

    return {
        "weak_bullets": bullet_analysis,
        "summary": summary_analysis,
        "wording_improvements": wording_analysis,
        "guardrail": (
            "Suggestions must only use information already "
            "present in the resume. Do not invent experience, "
            "skills, achievements, metrics, or responsibilities."
        ),
    }


# ---------------------------------------------------------
# Direct test
# ---------------------------------------------------------

if __name__ == "__main__":

    example_resume = """
    ALEX JOHNSON

    SUMMARY

    Software Developer with experience building web applications.

    EXPERIENCE

    Software Developer
    TechNova Solutions

    - Worked on web applications using Python and Django.
    - Helped with database development.
    - Fixed bugs.
    - Built REST APIs for internal tools.
    """

    result = analyze_resume_for_improvement(
        example_resume
    )

    print("\nRESUME IMPROVEMENT ANALYSIS")
    print("-" * 40)

    print("\nWeak Bullets:")

    for bullet in result["weak_bullets"]:
        print(f"\nOriginal: {bullet['original']}")
        print("Reasons:")

        for reason in bullet["reasons"]:
            print(f"- {reason}")

        print(f"Suggestion: {bullet['suggestion']}")

    print("\nSummary:")
    print(result["summary"])

    print("\nWording Improvements:")

    for item in result["wording_improvements"]:
        print(
            f"- {item['original_phrase']} "
            f"→ {item['suggested_phrase']}"
        )

    print("\nGuardrail:")
    print(result["guardrail"])