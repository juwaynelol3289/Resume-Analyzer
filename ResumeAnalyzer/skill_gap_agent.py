"""
Skill Gap Agent.

Compares a candidate's resume skills with the skills needed
for a target job.

Categories:
- Already have
- Mentioned but weak
- Missing

The agent also prioritizes missing skills so the candidate
knows what to focus on first.

Important guardrail:
Never claim that a candidate has a skill unless the resume
actually supports that conclusion.
"""

from skills import detect_skills


def normalize_skill(skill):
    """Normalize a skill name for comparisons."""

    return skill.strip().lower()


def get_resume_skills(resume_text):
    """
    Detect skills explicitly present in the resume.
    """

    if not resume_text or not resume_text.strip():
        return []

    return detect_skills(resume_text)


def get_target_skills(
    required_skills,
    preferred_skills=None,
):
    """
    Combine required and preferred job skills.
    """

    preferred_skills = preferred_skills or []

    all_skills = []

    for skill in required_skills + preferred_skills:
        if skill not in all_skills:
            all_skills.append(skill)

    return all_skills


def classify_skills(
    resume_skills,
    required_skills,
    preferred_skills=None,
):
    """
    Classify target skills.

    Already have:
        Skill is clearly detected in the resume.

    Mentioned but weak:
        Skill appears in the resume but is not strongly
        supported by the available evidence.

    Missing:
        Skill does not appear in the resume.
    """

    preferred_skills = preferred_skills or []

    resume_lookup = {
        normalize_skill(skill): skill
        for skill in resume_skills
    }

    already_have = []
    mentioned_but_weak = []
    missing = []

    # Required skills
    for skill in required_skills:

        normalized = normalize_skill(skill)

        if normalized in resume_lookup:
            already_have.append(
                resume_lookup[normalized]
            )
        else:
            missing.append(skill)

    # Preferred skills
    for skill in preferred_skills:

        normalized = normalize_skill(skill)

        if normalized in resume_lookup:
            # Preferred skills detected in the resume are
            # treated as present, but their strength can be
            # evaluated later by the AI layer.
            already_have.append(
                resume_lookup[normalized]
            )
        else:
            missing.append(skill)

    # Remove duplicates while preserving order.
    already_have = list(
        dict.fromkeys(already_have)
    )

    missing = list(
        dict.fromkeys(missing)
    )

    return {
        "already_have": already_have,
        "mentioned_but_weak": mentioned_but_weak,
        "missing": missing,
    }


def identify_weak_skills(
    resume_text,
    resume_skills,
    target_skills,
):
    """
    Identify skills that are mentioned in the resume but
    have little supporting evidence.

    This is a conservative deterministic check.

    A skill is considered potentially weak when it appears
    only once in the resume.
    """

    resume_lower = resume_text.lower()

    weak_skills = []

    for skill in resume_skills:

        occurrences = resume_lower.count(
            skill.lower()
        )

        if occurrences <= 1 and skill in target_skills:
            weak_skills.append(skill)

    return weak_skills


def prioritize_missing_skills(
    missing_skills,
    required_skills,
    preferred_skills=None,
):
    """
    Prioritize skill gaps.

    Required skills receive higher priority than
    preferred skills.
    """

    preferred_skills = preferred_skills or []

    required_lookup = {
        normalize_skill(skill)
        for skill in required_skills
    }

    preferred_lookup = {
        normalize_skill(skill)
        for skill in preferred_skills
    }

    priority_gaps = []

    for skill in missing_skills:

        normalized = normalize_skill(skill)

        if normalized in required_lookup:
            priority = "high"
            reason = (
                "Required for the target role."
            )

        elif normalized in preferred_lookup:
            priority = "medium"
            reason = (
                "Preferred for the target role."
            )

        else:
            priority = "low"
            reason = (
                "Relevant skill gap."
            )

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

    return priority_gaps


def generate_learning_plan(priority_gaps):
    """
    Generate a simple learning priority list.

    This does not claim how long a skill will take to learn.
    """

    learning_plan = []

    for index, gap in enumerate(
        priority_gaps,
        start=1,
    ):
        learning_plan.append(
            {
                "rank": index,
                "skill": gap["skill"],
                "priority": gap["priority"],
                "reason": gap["reason"],
            }
        )

    return learning_plan


def analyze_skill_gaps(
    resume_text,
    required_skills,
    preferred_skills=None,
):
    """
    Perform a complete skill-gap analysis.
    """

    if not resume_text or not resume_text.strip():
        raise ValueError(
            "Resume text cannot be empty."
        )

    preferred_skills = preferred_skills or []

    resume_skills = get_resume_skills(
        resume_text
    )

    target_skills = get_target_skills(
        required_skills,
        preferred_skills,
    )

    classification = classify_skills(
        resume_skills,
        required_skills,
        preferred_skills,
    )

    weak_skills = identify_weak_skills(
        resume_text,
        resume_skills,
        target_skills,
    )

    # Move detected-but-weak skills into the weak category.
    for skill in weak_skills:

        if skill in classification["already_have"]:
            classification["already_have"].remove(
                skill
            )

        if skill not in classification[
            "mentioned_but_weak"
        ]:
            classification[
                "mentioned_but_weak"
            ].append(skill)

    priority_gaps = prioritize_missing_skills(
        classification["missing"],
        required_skills,
        preferred_skills,
    )

    learning_plan = generate_learning_plan(
        priority_gaps
    )

    return {
        "already_have": classification[
            "already_have"
        ],

        "mentioned_but_weak": classification[
            "mentioned_but_weak"
        ],

        "missing": classification[
            "missing"
        ],

        "priority_gaps": priority_gaps,

        "learning_plan": learning_plan,

        "guardrail": (
            "Only skills supported by the resume are "
            "classified as already having them. "
            "Missing skills are not assumed to exist."
        ),
    }


# ---------------------------------------------------------
# Direct test
# ---------------------------------------------------------

if __name__ == "__main__":

    example_resume = """
    Software Developer with 3 years of experience.

    Developed web applications using Python and Django.

    Built REST APIs and worked with SQL databases.

    Used Docker for development.

    Skills:
    Python
    Django
    SQL
    Docker
    Git
    """

    required = [
        "Python",
        "Django",
        "SQL",
        "AWS",
        "Kubernetes",
    ]

    preferred = [
        "Docker",
        "React",
    ]

    result = analyze_skill_gaps(
        example_resume,
        required,
        preferred,
    )

    print("\nSKILL GAP ANALYSIS")
    print("-" * 40)

    print("\nAlready Have:")
    for skill in result["already_have"]:
        print(f"✅ {skill}")

    print("\nMentioned But Weak:")
    for skill in result["mentioned_but_weak"]:
        print(f"🟡 {skill}")

    print("\nMissing:")
    for skill in result["missing"]:
        print(f"🔴 {skill}")

    print("\nPriority Gaps:")
    for gap in result["priority_gaps"]:
        print(
            f"{gap['priority'].upper()}: "
            f"{gap['skill']} — {gap['reason']}"
        )

    print("\nLearning Plan:")
    for item in result["learning_plan"]:
        print(
            f"{item['rank']}. "
            f"{item['skill']}"
        )