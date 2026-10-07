"""
AI-powered resume analysis.

Connects the existing resume analyzer to OpenAI
and converts the AI response into structured data.
"""

import json

from ai.provider import create_provider
from ai.prompts import (
    SYSTEM_PROMPT,
    build_resume_analysis_prompt,
)


class AIResumeAnalyzer:
    """Analyze resumes using OpenAI."""

    def __init__(self):
        self.provider = create_provider()

    def analyze(self, resume_text):
        """
        Analyze a resume and return structured data.
        """

        if not resume_text or not resume_text.strip():
            raise ValueError(
                "Resume text cannot be empty."
            )

        prompt = build_resume_analysis_prompt(
            resume_text
        )

        full_prompt = (
            SYSTEM_PROMPT
            + "\n\n"
            + prompt
        )

        response = self.provider.analyze(
            full_prompt
        )

        return self.parse_response(response)

    @staticmethod
    def parse_response(response):
        """
        Convert the AI's JSON response into a Python dictionary.
        """

        if not response:
            raise ValueError(
                "AI returned an empty response."
            )

        try:
            data = json.loads(response)

        except json.JSONDecodeError as error:
            raise ValueError(
                "AI returned invalid JSON."
            ) from error

        required_keys = {
            "overall_impression",
            "strengths",
            "weaknesses",
            "writing",
            "experience",
            "skills",
            "summary",
            "action_items",
        }

        missing_keys = (
            required_keys - data.keys()
        )

        if missing_keys:
            raise ValueError(
                "AI response is missing required fields: "
                + ", ".join(sorted(missing_keys))
            )

        return data


def analyze_resume_with_ai(resume_text):
    """
    Convenience function for AI resume analysis.
    """

    analyzer = AIResumeAnalyzer()

    return analyzer.analyze(
        resume_text
    )


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    sample_resume = """
    Alex Johnson

    Software Developer

    Email: alex@example.com
    Phone: 555-123-4567

    SUMMARY
    Python developer interested in building web applications.

    EDUCATION
    Bachelor of Computer Science

    EXPERIENCE
    Software Developer
    Built Python applications and worked with databases.
    Developed internal tools for the development team.

    SKILLS
    Python, Django, SQL, Git, JavaScript

    PROJECTS
    Created a web application using Django and PostgreSQL.
    """

    print("Starting AI resume analysis...\n")

    try:

        result = analyze_resume_with_ai(
            sample_resume
        )

        print("=" * 60)
        print("STRUCTURED AI RESUME ANALYSIS")
        print("=" * 60)

        print(
            json.dumps(
                result,
                indent=4,
            )
        )

    except Exception as error:

        print("AI ANALYSIS FAILED:")
        print(error)