"""
Central configuration for Resume Analyzer.

Keep adjustable project settings here instead of scattering
them throughout the application.
"""

from pathlib import Path


# =========================================================
# PROJECT
# =========================================================

APP_NAME = "Resume Analyzer"
APP_VERSION = "1.0.0"


# =========================================================
# DIRECTORIES
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

UI_DIR = BASE_DIR / "ui"


# =========================================================
# FILE SETTINGS
# =========================================================

SUPPORTED_FILE_EXTENSIONS = {
    ".txt",
    ".pdf",
    ".docx",
}

MAX_FILE_SIZE_MB = 10


# =========================================================
# RESUME LENGTH
# =========================================================

MIN_RECOMMENDED_WORDS = 150

MAX_RECOMMENDED_WORDS = 1600

IDEAL_MIN_WORDS = 250

IDEAL_MAX_WORDS = 1200


# =========================================================
# SECTION WEIGHTS
# =========================================================

SECTION_WEIGHTS = {
    "Contact Information": 15,
    "Summary": 10,
    "Education": 10,
    "Experience": 20,
    "Skills": 15,
    "Projects": 15,
    "Certifications": 5,
}


# =========================================================
# RESUME SCORING
# =========================================================

# Maximum points available from each scoring category.

SECTION_SCORE_MAX = sum(
    SECTION_WEIGHTS.values()
)

SKILL_SCORE_MAX = 15

CONTENT_SCORE_MAX = 15


# Total raw points before normalization to 100.

TOTAL_SCORE = (
    SECTION_SCORE_MAX
    + SKILL_SCORE_MAX
    + CONTENT_SCORE_MAX
)


# =========================================================
# SKILL SCORING
# =========================================================

SKILL_SCORE_THRESHOLDS = [
    # (minimum skills, points)

    (15, 15),
    (10, 12),
    (7, 9),
    (4, 6),
    (1, 3),
    (0, 0),
]


# =========================================================
# JOB MATCHING
# =========================================================

# How much each matching component contributes
# to the overall job-match percentage.

JOB_SKILL_WEIGHT = 0.70

JOB_KEYWORD_WEIGHT = 0.30


# Match levels used by the UI.

JOB_MATCH_LEVELS = {
    "low": 50,
    "medium": 75,
    "high": 100,
}


# =========================================================
# RECOMMENDATION SETTINGS
# =========================================================

MAX_RECOMMENDATIONS = 10

MAX_MISSING_SKILLS_DISPLAYED = 8


# =========================================================
# UI SETTINGS
# =========================================================

WINDOW_WIDTH = 1100

WINDOW_HEIGHT = 700

MIN_WINDOW_WIDTH = 850

MIN_WINDOW_HEIGHT = 600

WINDOW_TITLE = f"{APP_NAME} v{APP_VERSION}"


# =========================================================
# UI COLORS
# =========================================================

COLORS = {
    "background": "#111827",
    "surface": "#1F2937",
    "surface_light": "#374151",

    "text": "#F9FAFB",
    "text_muted": "#9CA3AF",

    "accent": "#6366F1",

    "success": "#22C55E",
    "warning": "#F59E0B",
    "danger": "#EF4444",
}


# =========================================================
# FONT SETTINGS
# =========================================================

FONT_FAMILY = "Segoe UI"

FONT_SIZE_SMALL = 10

FONT_SIZE_NORMAL = 12

FONT_SIZE_LARGE = 16

FONT_SIZE_TITLE = 24


# =========================================================
# APPLICATION BEHAVIOR
# =========================================================

DEFAULT_DARK_MODE = True

REMEMBER_LAST_FILE = False


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def get_supported_extensions() -> tuple:
    """Return supported file extensions as a tuple."""

    return tuple(
        sorted(SUPPORTED_FILE_EXTENSIONS)
    )


def get_max_file_size_bytes() -> int:
    """Convert the maximum file size from MB to bytes."""

    return MAX_FILE_SIZE_MB * 1024 * 1024


def get_total_score() -> int:
    """Return the maximum possible raw resume score."""

    return TOTAL_SCORE


# =========================================================
# CONFIGURATION VALIDATION
# =========================================================

def validate_config() -> None:
    """Validate important configuration values."""

    if MAX_FILE_SIZE_MB <= 0:
        raise ValueError(
            "MAX_FILE_SIZE_MB must be greater than 0."
        )

    if MIN_RECOMMENDED_WORDS < 0:
        raise ValueError(
            "MIN_RECOMMENDED_WORDS cannot be negative."
        )

    if MAX_RECOMMENDED_WORDS <= MIN_RECOMMENDED_WORDS:
        raise ValueError(
            "MAX_RECOMMENDED_WORDS must be greater than "
            "MIN_RECOMMENDED_WORDS."
        )

    if IDEAL_MIN_WORDS < MIN_RECOMMENDED_WORDS:
        raise ValueError(
            "IDEAL_MIN_WORDS cannot be below "
            "MIN_RECOMMENDED_WORDS."
        )

    if IDEAL_MAX_WORDS > MAX_RECOMMENDED_WORDS:
        raise ValueError(
            "IDEAL_MAX_WORDS cannot exceed "
            "MAX_RECOMMENDED_WORDS."
        )

    if abs(
        JOB_SKILL_WEIGHT
        + JOB_KEYWORD_WEIGHT
        - 1.0
    ) > 0.001:
        raise ValueError(
            "JOB_SKILL_WEIGHT + JOB_KEYWORD_WEIGHT "
            "must equal 1.0."
        )

    if WINDOW_WIDTH <= 0:
        raise ValueError(
            "WINDOW_WIDTH must be greater than 0."
        )

    if WINDOW_HEIGHT <= 0:
        raise ValueError(
            "WINDOW_HEIGHT must be greater than 0."
        )

    if MIN_WINDOW_WIDTH <= 0:
        raise ValueError(
            "MIN_WINDOW_WIDTH must be greater than 0."
        )

    if MIN_WINDOW_HEIGHT <= 0:
        raise ValueError(
            "MIN_WINDOW_HEIGHT must be greater than 0."
        )


# =========================================================
# VALIDATE CONFIGURATION
# =========================================================

validate_config()


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print("=" * 50)
    print(APP_NAME)
    print("=" * 50)

    print(f"Version: {APP_VERSION}")

    print(
        f"Base directory: {BASE_DIR}"
    )

    print(
        f"Supported files: "
        f"{', '.join(get_supported_extensions())}"
    )

    print(
        f"Maximum file size: "
        f"{MAX_FILE_SIZE_MB} MB"
    )

    print(
        f"Section score: "
        f"{SECTION_SCORE_MAX}"
    )

    print(
        f"Skill score: "
        f"{SKILL_SCORE_MAX}"
    )

    print(
        f"Content score: "
        f"{CONTENT_SCORE_MAX}"
    )

    print(
        f"Maximum raw score: "
        f"{get_total_score()}"
    )

    print(
        f"Job skill weight: "
        f"{JOB_SKILL_WEIGHT * 100:.0f}%"
    )

    print(
        f"Job keyword weight: "
        f"{JOB_KEYWORD_WEIGHT * 100:.0f}%"
    )

    print("\n✅ Configuration is valid!")