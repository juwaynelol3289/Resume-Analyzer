"""
Career Intelligence Agent.

Main orchestrator for Resume Analyzer.

Connects:
- Resume Analyzer
- Job Match Agent
- ATS Agent
- Resume Rewrite Agent
- Skill Gap Agent

The orchestrator combines their structured results into
one Career Intelligence Report.

Important:
This module coordinates the deterministic agents.
It does not invent candidate information.
"""

from analyzer import analyze_resume

from job_matcher import match_resume_to_job

from ats_agent import analyze_ats

from rewrite_agent import analyze_resume_for_improvement

from skill_gap_agent import analyze_skill_gaps


class CareerIntelligenceAgent:
    """
    Main Career Intelligence orchestrator.

    Takes a resume and optional job description and runs
    the appropriate analysis agents.
    """

    def __init__(
        self,
        resume_text,
        job_description="",
    ):
        if not resume_text or not resume_text.strip():
            raise ValueError(
                "Resume text cannot be empty."
            )

        self.resume_text = resume_text
        self.job_description = (
            job_description or ""
        )

    def run_resume_analysis(self):
        """
        Run the existing deterministic resume analyzer.
        """

        return analyze_resume(
            self.resume_text
        )

    def run_job_match(self):
        """
        Run Job Match Agent when a job description
        is available.
        """

        if not self.job_description.strip():
            return None

        return match_resume_to_job(
            self.resume_text,
            self.job_description,
        )

    def run_ats_analysis(self):
        """
        Run ATS Agent.
        """

        return analyze_ats(
            self.resume_text,
            self.job_description,
        )

    def run_rewrite_analysis(self):
        """
        Run Resume Improvement Agent.
        """

        return analyze_resume_for_improvement(
            self.resume_text
        )

    def run_skill_gap_analysis(
        self,
        job_match_result,
    ):
        """
        Run Skill Gap Agent using the skills discovered
        by the Job Match Agent.
        """

        if not job_match_result:
            return None

        required_skills = job_match_result.get(
            "required_skills",
            [],
        )

        preferred_skills = job_match_result.get(
            "preferred_skills",
            [],
        )

        return analyze_skill_gaps(
            self.resume_text,
            required_skills,
            preferred_skills,
        )

    def build_summary(
        self,
        resume_result,
        job_match_result,
        ats_result,
    ):
        """
        Build a concise high-level summary of the
        candidate's current resume.
        """

        summary = {
            "resume_quality": resume_result.get(
                "score",
                0,
            ),
            "ats_compatibility": ats_result.get(
                "ats_score",
                0,
            ),
        }

        if job_match_result:
            summary["job_match"] = (
                job_match_result.get(
                    "overall_match",
                    0,
                )
            )
        else:
            summary["job_match"] = None

        return summary

    def build_priorities(
        self,
        resume_result,
        job_match_result,
        ats_result,
        rewrite_result,
        skill_gap_result,
    ):
        """
        Combine the most important issues from all
        available agents.

        Higher-priority issues appear first.
        """

        priorities = []

        # -------------------------------------------------
        # Job Match priorities
        # -------------------------------------------------

        if job_match_result:

            for gap in job_match_result.get(
                "priority_gaps",
                [],
            ):

                if gap.get("priority") == "high":

                    priorities.append(
                        {
                            "priority": "high",
                            "source": "Job Match",
                            "message": (
                                f"Address missing required "
                                f"skill: {gap.get('skill')}."
                            ),
                        }
                    )

        # -------------------------------------------------
        # ATS priorities
        # -------------------------------------------------

        for recommendation in ats_result.get(
            "recommendations",
            [],
        ):

            if recommendation.get(
                "priority"
            ) == "high":

                priorities.append(
                    {
                        "priority": "high",
                        "source": "ATS",
                        "message": recommendation.get(
                            "message",
                            "",
                        ),
                    }
                )

        # -------------------------------------------------
        # Rewrite priorities
        # -------------------------------------------------

        weak_bullets = rewrite_result.get(
            "weak_bullets",
            [],
        )

        if weak_bullets:

            priorities.append(
                {
                    "priority": "medium",
                    "source": "Rewrite",
                    "message": (
                        f"Improve {len(weak_bullets)} "
                        "weak resume bullet point(s)."
                    ),
                }
            )

        # -------------------------------------------------
        # Skill Gap priorities
        # -------------------------------------------------

        if skill_gap_result:

            for gap in skill_gap_result.get(
                "priority_gaps",
                [],
            ):

                if gap.get("priority") == "high":

                    priorities.append(
                        {
                            "priority": "high",
                            "source": "Skill Gap",
                            "message": (
                                f"Learn or address "
                                f"{gap.get('skill')}."
                            ),
                        }
                    )

        # -------------------------------------------------
        # Resume structure
        # -------------------------------------------------

        resume_score = resume_result.get(
            "score",
            0,
        )

        if resume_score < 70:

            priorities.append(
                {
                    "priority": "medium",
                    "source": "Resume Analyzer",
                    "message": (
                        "Improve the overall resume "
                        "structure and content quality."
                    ),
                }
            )

        # -------------------------------------------------
        # Sort priorities
        # -------------------------------------------------

        priority_order = {
            "high": 0,
            "medium": 1,
            "low": 2,
        }

        priorities.sort(
            key=lambda item: (
                priority_order.get(
                    item.get("priority"),
                    3,
                ),
                item.get(
                    "source",
                    "",
                ),
            )
        )

        # Remove duplicate messages.
        unique_priorities = []

        seen = set()

        for item in priorities:

            message = item.get(
                "message",
                "",
            )

            if message in seen:
                continue

            seen.add(message)
            unique_priorities.append(item)

        return unique_priorities

    def build_final_report(
        self,
        resume_result,
        job_match_result,
        ats_result,
        rewrite_result,
        skill_gap_result,
    ):
        """
        Build the final structured Career Intelligence
        report.
        """

        summary = self.build_summary(
            resume_result,
            job_match_result,
            ats_result,
        )

        priorities = self.build_priorities(
            resume_result,
            job_match_result,
            ats_result,
            rewrite_result,
            skill_gap_result,
        )

        return {
            "summary": summary,

            "resume_analysis": resume_result,

            "job_match": job_match_result,

            "ats_analysis": ats_result,

            "rewrite_analysis": rewrite_result,

            "skill_gap_analysis": skill_gap_result,

            "top_priorities": priorities,

            "guardrails": {
                "no_invented_experience": True,
                "no_invented_skills": True,
                "source_based_analysis": True,
            },
        }

    def run(self):
        """
        Run the complete Career Intelligence pipeline.

        Pipeline:

        Resume
           ↓
        Resume Analyzer
           ↓
        Job Match
           ↓
        ATS
           ↓
        Rewrite
           ↓
        Skill Gap
           ↓
        Final Career Intelligence Report
        """

        # -------------------------------------------------
        # 1. Resume Analysis
        # -------------------------------------------------

        resume_result = (
            self.run_resume_analysis()
        )

        # -------------------------------------------------
        # 2. Job Match
        # -------------------------------------------------

        job_match_result = (
            self.run_job_match()
        )

        # -------------------------------------------------
        # 3. ATS Analysis
        # -------------------------------------------------

        ats_result = (
            self.run_ats_analysis()
        )

        # -------------------------------------------------
        # 4. Resume Improvement
        # -------------------------------------------------

        rewrite_result = (
            self.run_rewrite_analysis()
        )

        # -------------------------------------------------
        # 5. Skill Gap
        # -------------------------------------------------

        skill_gap_result = (
            self.run_skill_gap_analysis(
                job_match_result
            )
        )

        # -------------------------------------------------
        # 6. Final Report
        # -------------------------------------------------

        return self.build_final_report(
            resume_result,
            job_match_result,
            ats_result,
            rewrite_result,
            skill_gap_result,
        )


def run_career_intelligence(
    resume_text,
    job_description="",
):
    """
    Convenience function for running the complete
    Career Intelligence Agent.
    """

    agent = CareerIntelligenceAgent(
        resume_text,
        job_description,
    )

    return agent.run()


# ---------------------------------------------------------
# Direct test
# ---------------------------------------------------------

if __name__ == "__main__":

    example_resume = """
    ALEX JOHNSON

    SOFTWARE DEVELOPER

    Email: alex.johnson@example.com
    Phone: +1 555-123-4567
    Location: New York, NY

    SUMMARY

    Software Developer with 3 years of experience
    building web applications using Python and Django.

    EDUCATION

    Bachelor of Science in Computer Science

    EXPERIENCE

    Software Developer
    TechNova Solutions

    - Worked on web applications using Python and Django.
    - Built REST APIs used by internal tools.
    - Improved database queries using SQL.

    SKILLS

    Python, Django, SQL, Git, Docker

    PROJECTS

    Task Management Web Application

    - Built a task management application using Django.

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
    Kubernetes

    3+ years of experience.

    Experience with REST APIs and Git.
    """

    report = run_career_intelligence(
        example_resume,
        example_job,
    )

    print("\n")
    print("=" * 60)
    print("CAREER INTELLIGENCE REPORT")
    print("=" * 60)

    print("\nSUMMARY")
    print("-" * 60)

    for key, value in report["summary"].items():
        print(
            f"{key}: {value}"
        )

    print("\nTOP PRIORITIES")
    print("-" * 60)

    for priority in report[
        "top_priorities"
    ]:

        print(
            f"[{priority['priority'].upper()}] "
            f"{priority['source']}: "
            f"{priority['message']}"
        )

    print("\nJOB MATCH")
    print("-" * 60)

    job_match = report["job_match"]

    if job_match:

        print(
            f"Overall Match: "
            f"{job_match['overall_match']}%"
        )

        print(
            "Matched Skills:",
            job_match["matched_skills"],
        )

        print(
            "Missing Skills:",
            job_match["missing_skills"],
        )

    print("\nATS")
    print("-" * 60)

    print(
        "ATS Score:",
        report["ats_analysis"]["ats_score"],
    )

    print("\nSKILL GAPS")
    print("-" * 60)

    skill_gaps = report[
        "skill_gap_analysis"
    ]

    if skill_gaps:

        print(
            "Already Have:",
            skill_gaps["already_have"],
        )

        print(
            "Mentioned But Weak:",
            skill_gaps["mentioned_but_weak"],
        )

        print(
            "Missing:",
            skill_gaps["missing"],
        )

    print("\n")
    print("=" * 60)
    print("CAREER INTELLIGENCE COMPLETE")
    print("=" * 60)