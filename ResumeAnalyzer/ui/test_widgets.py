import tkinter as tk

from ui.widgets import (
    ScoreCard,
    StatCard,
    SkillTag,
    StatusRow,
    RecommendationCard,
)


root = tk.Tk()

root.title("Resume Analyzer - Widget Test")
root.geometry("700x600")

root.configure(
    bg="#111827"
)


# Score
score = ScoreCard(
    root,
    score=87,
)

score.pack(
    fill="x",
    padx=20,
    pady=10,
)


# Statistic
stats = StatCard(
    root,
    title="Skills Found",
    value=14,
)

stats.pack(
    fill="x",
    padx=20,
    pady=10,
)


# Skill
SkillTag(
    root,
    "Python",
).pack(
    padx=20,
    pady=5,
)


# Status
StatusRow(
    root,
    "Education",
    True,
).pack(
    fill="x",
    padx=20,
    pady=5,
)


# Recommendation
RecommendationCard(
    root,
    "Consider adding a Projects section.",
    priority="medium",
    category="Structure",
).pack(
    fill="x",
    padx=20,
    pady=10,
)


root.mainloop()