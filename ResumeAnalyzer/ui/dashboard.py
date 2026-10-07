"""
Resume Analyzer Career Intelligence Dashboard.

Displays:
- Traditional resume analysis
- Career Intelligence report
- Job Match analysis
- ATS compatibility
- Skill gaps
- Resume improvement suggestions
- AI-powered resume analysis
"""

import tkinter as tk
from tkinter import messagebox

from config import (
    COLORS,
    FONT_FAMILY,
    FONT_SIZE_NORMAL,
    FONT_SIZE_SMALL,
    FONT_SIZE_TITLE,
)

from ui.widgets import (
    Card,
    SectionTitle,
    PrimaryButton,
    SecondaryButton,
    ScoreCard,
    StatCard,
    ProgressBar,
    SkillTag,
    RecommendationCard,
    ScrollableFrame,
)

from career_agent import CareerIntelligenceAgent
from ai.ai_worker import AIWorker


class ResumeDashboard(tk.Frame):
    """Main dashboard for displaying resume and career analysis."""

    def __init__(
        self,
        parent,
        analysis_data,
        resume_text,
        on_new_resume,
    ):
        super().__init__(
            parent,
            bg=COLORS["background"],
        )

        self.analysis_data = analysis_data
        self.resume_text = resume_text
        self.on_new_resume = on_new_resume

        self.job_description = ""
        self.career_report = None

        self.ai_worker = None
        self.ai_card = None
        self.ai_loading_label = None

        self.build_dashboard()

    # =========================================================
    # DASHBOARD
    # =========================================================

    def build_dashboard(self):
        """Build the complete dashboard."""

        self._build_header()

        self.scrollable = ScrollableFrame(self)

        self.scrollable.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10),
        )

        self.content = self.scrollable.content

        self._build_career_intelligence()
        self._build_job_description()
        self._build_score_section()
        self._build_statistics()
        self._build_score_breakdown()
        self._build_sections()
        self._build_skills()
        self._build_recommendations()

        self._run_initial_career_analysis()
        self.show_ai_analysis()

    # =========================================================
    # HEADER
    # =========================================================

    def _build_header(self):
        """Build dashboard header."""

        header = tk.Frame(
            self,
            bg=COLORS["surface"],
            height=70,
        )

        header.pack(
            fill="x",
            padx=10,
            pady=10,
        )

        header.pack_propagate(False)

        title = tk.Label(
            header,
            text="🧠 Career Intelligence Dashboard",
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=(
                FONT_FAMILY,
                FONT_SIZE_TITLE,
                "bold",
            ),
        )

        title.pack(
            side="left",
            padx=20,
        )

        new_button = PrimaryButton(
            header,
            text="📄 New Resume",
            command=self.on_new_resume,
        )

        new_button.pack(
            side="right",
            padx=20,
        )

    # =========================================================
    # CAREER INTELLIGENCE
    # =========================================================

    def _build_career_intelligence(self):
        """Build the main Career Intelligence summary."""

        self.career_card = Card(self.content)

        self.career_card.pack(
            fill="x",
            padx=20,
            pady=10,
        )

        SectionTitle(
            self.career_card,
            "🧠 Career Intelligence",
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 10),
        )

        self.career_summary_frame = tk.Frame(
            self.career_card,
            bg=COLORS["surface"],
        )

        self.career_summary_frame.pack(
            fill="x",
            padx=15,
            pady=(0, 15),
        )

        self.career_summary_frame.columnconfigure(
            (0, 1, 2),
            weight=1,
        )

        self.resume_quality_label = self._create_metric(
            self.career_summary_frame,
            "📊 Resume Quality",
            0,
        )

        self.ats_score_label = self._create_metric(
            self.career_summary_frame,
            "🛡️ ATS Compatibility",
            1,
        )

        self.job_match_label = self._create_metric(
            self.career_summary_frame,
            "⭐ Job Match",
            2,
        )

    def _create_metric(
        self,
        parent,
        title,
        column,
    ):
        """Create a metric card inside the Career Intelligence section."""

        frame = tk.Frame(
            parent,
            bg=COLORS["surface_light"],
        )

        frame.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=5,
            pady=5,
        )

        tk.Label(
            frame,
            text=title,
            bg=COLORS["surface_light"],
            fg=COLORS["text_muted"],
            font=(
                FONT_FAMILY,
                FONT_SIZE_SMALL,
                "bold",
            ),
        ).pack(
            pady=(12, 3),
        )

        value_label = tk.Label(
            frame,
            text="--",
            bg=COLORS["surface_light"],
            fg=COLORS["text"],
            font=(
                FONT_FAMILY,
                FONT_SIZE_TITLE,
                "bold",
            ),
        )

        value_label.pack(
            pady=(0, 12),
        )

        return value_label

    def _update_career_summary(self):
        """Update Career Intelligence summary metrics."""

        if not self.career_report:
            return

        summary = self.career_report.get(
            "summary",
            {},
        )

        resume_quality = summary.get(
            "resume_quality",
            self.analysis_data.get("score", 0),
        )

        ats_score = summary.get(
            "ats_compatibility",
            0,
        )

        job_match = summary.get(
            "job_match",
            None,
        )

        self.resume_quality_label.config(
            text=f"{resume_quality}/100",
        )

        self.ats_score_label.config(
            text=f"{ats_score}/100",
        )

        if job_match is None:
            self.job_match_label.config(
                text="No JD",
                fg=COLORS["text_muted"],
            )
        else:
            self.job_match_label.config(
                text=f"{job_match}%",
                fg=COLORS["text"],
            )

    def _run_initial_career_analysis(self):
        """Run Career Intelligence without a job description."""

        try:
            agent = CareerIntelligenceAgent(
                self.resume_text,
                "",
            )

            self.career_report = agent.run()

            self._update_career_summary()
            self._display_career_details()

        except Exception as error:
            self._display_career_error(error)

    # =========================================================
    # JOB DESCRIPTION
    # =========================================================

    def _build_job_description(self):
        """Build the job description input section."""

        card = Card(self.content)

        card.pack(
            fill="x",
            padx=20,
            pady=10,
        )

        SectionTitle(
            card,
            "💼 Target Job Description",
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 5),
        )

        tk.Label(
            card,
            text=(
                "Paste a job description below to unlock "
                "Job Match, keyword analysis, and skill gaps."
            ),
            bg=COLORS["surface"],
            fg=COLORS["text_muted"],
            font=(
                FONT_FAMILY,
                FONT_SIZE_SMALL,
            ),
            anchor="w",
            justify="left",
        ).pack(
            fill="x",
            padx=15,
            pady=(0, 8),
        )

        self.job_text = tk.Text(
            card,
            height=8,
            bg=COLORS["background"],
            fg=COLORS["text"],
            insertbackground=COLORS["text"],
            selectbackground=COLORS["accent"],
            relief="flat",
            bd=0,
            wrap="word",
            font=(
                FONT_FAMILY,
                FONT_SIZE_NORMAL,
            ),
        )

        self.job_text.pack(
            fill="x",
            padx=15,
            pady=5,
        )

        button_frame = tk.Frame(
            card,
            bg=COLORS["surface"],
        )

        button_frame.pack(
            fill="x",
            padx=15,
            pady=(8, 15),
        )

        SecondaryButton(
            button_frame,
            text="🔍 Analyze Job Match",
            command=self.analyze_job_description,
        ).pack(
            side="left",
        )

        self.job_status_label = tk.Label(
            button_frame,
            text="No job description loaded.",
            bg=COLORS["surface"],
            fg=COLORS["text_muted"],
            font=(
                FONT_FAMILY,
                FONT_SIZE_SMALL,
            ),
        )

        self.job_status_label.pack(
            side="left",
            padx=15,
        )

    def analyze_job_description(self):
        """Analyze the current resume against the entered job description."""

        job_description = self.job_text.get(
            "1.0",
            "end",
        ).strip()

        if not job_description:
            messagebox.showwarning(
                "Job Description",
                "Please paste a job description first.",
            )
            return

        try:
            self.job_description = job_description

            self.job_status_label.config(
                text="🔄 Analyzing...",
                fg=COLORS["warning"],
            )

            self.update_idletasks()

            agent = CareerIntelligenceAgent(
                self.resume_text,
                self.job_description,
            )

            self.career_report = agent.run()

            self._update_career_summary()
            self._display_career_details()

            self.job_status_label.config(
                text="✅ Job analysis complete.",
                fg=COLORS["success"],
            )

        except Exception as error:

            self.job_status_label.config(
                text="⚠️ Analysis failed.",
                fg=COLORS["danger"],
            )

            messagebox.showerror(
                "Job Analysis Error",
                str(error),
            )

    # =========================================================
    # CAREER DETAILS
    # =========================================================

    def _display_career_details(self):
        """Display the current Career Intelligence details."""

        if hasattr(
            self,
            "career_details_frame",
        ):
            self.career_details_frame.destroy()

        self.career_details_frame = tk.Frame(
            self.content,
            bg=COLORS["background"],
        )

        self.career_details_frame.pack(
            fill="x",
            padx=20,
            pady=10,
            before=self._get_first_regular_section(),
        )

        self._build_priority_section(
            self.career_details_frame
        )

        self._build_job_match_section(
            self.career_details_frame
        )

        self._build_ats_section(
            self.career_details_frame
        )

        self._build_skill_gap_section(
            self.career_details_frame
        )

        self._build_rewrite_section(
            self.career_details_frame
        )

    def _get_first_regular_section(self):
        """
        Return the first existing dashboard section.

        Used so Career Intelligence details stay near the top.
        """

        for child in self.content.winfo_children():

            if child is self.career_card:
                continue

            if child.winfo_manager():
                return child

        return None

    def _build_priority_section(self, parent):
        """Display top priorities."""

        priorities = self.career_report.get(
            "top_priorities",
            [],
        )

        card = Card(parent)

        card.pack(
            fill="x",
            pady=5,
        )

        SectionTitle(
            card,
            "🔥 Top Priorities",
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 10),
        )

        if not priorities:

            tk.Label(
                card,
                text="No major priorities detected.",
                bg=COLORS["surface"],
                fg=COLORS["text_muted"],
                font=(
                    FONT_FAMILY,
                    FONT_SIZE_NORMAL,
                ),
            ).pack(
                padx=15,
                pady=10,
            )

            return

        for index, priority in enumerate(
            priorities[:8],
            start=1,
        ):

            priority_name = priority.get(
                "priority",
                "medium",
            )

            color = {
                "high": COLORS["danger"],
                "medium": COLORS["warning"],
                "low": COLORS["success"],
            }.get(
                priority_name,
                COLORS["text"],
            )

            row = tk.Frame(
                card,
                bg=COLORS["surface"],
            )

            row.pack(
                fill="x",
                padx=15,
                pady=4,
            )

            tk.Label(
                row,
                text=f"{index}.",
                bg=COLORS["surface"],
                fg=color,
                font=(
                    FONT_FAMILY,
                    FONT_SIZE_NORMAL,
                    "bold",
                ),
                width=4,
                anchor="w",
            ).pack(
                side="left",
            )

            tk.Label(
                row,
                text=priority.get(
                    "message",
                    "",
                ),
                bg=COLORS["surface"],
                fg=COLORS["text"],
                font=(
                    FONT_FAMILY,
                    FONT_SIZE_NORMAL,
                ),
                justify="left",
                anchor="w",
                wraplength=800,
            ).pack(
                side="left",
                fill="x",
                expand=True,
            )

    def _build_job_match_section(self, parent):
        """Display Job Match Agent results."""

        job_match = self.career_report.get(
            "job_match",
            None,
        )

        if not job_match:
            return

        card = Card(parent)

        card.pack(
            fill="x",
            pady=5,
        )

        SectionTitle(
            card,
            "⭐ Job Match Agent",
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 10),
        )

        overall = job_match.get(
            "overall_match",
            0,
        )

        tk.Label(
            card,
            text=f"{overall}%",
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=(
                FONT_FAMILY,
                FONT_SIZE_TITLE,
                "bold",
            ),
        ).pack(
            anchor="w",
            padx=15,
        )

        ProgressBar(
            card,
            overall,
        ).pack(
            fill="x",
            padx=15,
            pady=(5, 12),
        )

        self._display_skill_list(
            card,
            "✅ Matched Skills",
            job_match.get(
                "matched_skills",
                [],
            ),
            COLORS["success"],
        )

        self._display_skill_list(
            card,
            "🔴 Missing Skills",
            job_match.get(
                "missing_skills",
                [],
            ),
            COLORS["danger"],
        )

        self._display_skill_list(
            card,
            "🔑 Matched Keywords",
            job_match.get(
                "matched_keywords",
                [],
            ),
            COLORS["success"],
        )

        self._display_skill_list(
            card,
            "⚠️ Missing Keywords",
            job_match.get(
                "missing_keywords",
                [],
            ),
            COLORS["warning"],
        )

        explanation = job_match.get(
            "explanation",
            "",
        )

        if explanation:

            tk.Label(
                card,
                text=explanation,
                bg=COLORS["surface"],
                fg=COLORS["text_muted"],
                font=(
                    FONT_FAMILY,
                    FONT_SIZE_NORMAL,
                ),
                justify="left",
                anchor="w",
                wraplength=850,
            ).pack(
                fill="x",
                padx=15,
                pady=(8, 15),
            )

    def _build_ats_section(self, parent):
        """Display ATS Agent results."""

        ats = self.career_report.get(
            "ats_analysis",
            {},
        )

        card = Card(parent)

        card.pack(
            fill="x",
            pady=5,
        )

        SectionTitle(
            card,
            "🛡️ ATS Compatibility",
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 10),
        )

        score = ats.get(
            "ats_score",
            0,
        )

        tk.Label(
            card,
            text=f"{score}/100",
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=(
                FONT_FAMILY,
                FONT_SIZE_TITLE,
                "bold",
            ),
        ).pack(
            anchor="w",
            padx=15,
        )

        ProgressBar(
            card,
            score,
        ).pack(
            fill="x",
            padx=15,
            pady=(5, 12),
        )

        keyword_data = ats.get(
            "keyword_coverage",
            {},
        )

        section_data = ats.get(
            "sections",
            {},
        )

        contact_data = ats.get(
            "contact_information",
            {},
        )

        formatting_data = ats.get(
            "formatting",
            {},
        )

        title_data = ats.get(
            "job_title_alignment",
            {},
        )

        self._display_ats_metric(
            card,
            "🔑 Keyword Coverage",
            keyword_data.get("score", 0),
        )

        self._display_ats_metric(
            card,
            "📑 Section Coverage",
            section_data.get("score", 0),
        )

        self._display_ats_metric(
            card,
            "📞 Contact Information",
            contact_data.get("score", 0),
        )

        self._display_ats_metric(
            card,
            "🎨 Formatting",
            formatting_data.get("score", 0),
        )

        if title_data.get("job_title"):

            self._display_ats_metric(
                card,
                "🎯 Job Title Alignment",
                title_data.get("score", 0),
            )

        issues = formatting_data.get(
            "issues",
            [],
        )

        if issues:

            self._display_text_list(
                card,
                "⚠️ Formatting Issues",
                issues,
            )

    def _display_ats_metric(
        self,
        parent,
        title,
        score,
    ):
        """Display an ATS metric."""

        row = tk.Frame(
            parent,
            bg=COLORS["surface"],
        )

        row.pack(
            fill="x",
            padx=15,
            pady=4,
        )

        tk.Label(
            row,
            text=title,
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=(
                FONT_FAMILY,
                FONT_SIZE_NORMAL,
            ),
        ).pack(
            side="left",
        )

        tk.Label(
            row,
            text=f"{score}%",
            bg=COLORS["surface"],
            fg=COLORS["text_muted"],
            font=(
                FONT_FAMILY,
                FONT_SIZE_NORMAL,
                "bold",
            ),
        ).pack(
            side="right",
        )

        ProgressBar(
            parent,
            score,
        ).pack(
            fill="x",
            padx=15,
            pady=(0, 5),
        )

    def _build_skill_gap_section(self, parent):
        """Display Skill Gap Agent results."""

        skill_gaps = self.career_report.get(
            "skill_gap_analysis",
            None,
        )

        if not skill_gaps:
            return

        card = Card(parent)

        card.pack(
            fill="x",
            pady=5,
        )

        SectionTitle(
            card,
            "🛠️ Skill Gap Agent",
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 10),
        )

        self._display_skill_list(
            card,
            "✅ Already Have",
            skill_gaps.get(
                "already_have",
                [],
            ),
            COLORS["success"],
        )

        self._display_skill_list(
            card,
            "🟡 Mentioned But Weak",
            skill_gaps.get(
                "mentioned_but_weak",
                [],
            ),
            COLORS["warning"],
        )

        self._display_skill_list(
            card,
            "🔴 Missing",
            skill_gaps.get(
                "missing",
                [],
            ),
            COLORS["danger"],
        )

        learning_plan = skill_gaps.get(
            "learning_plan",
            [],
        )

        if learning_plan:

            SectionTitle(
                card,
                "📚 Suggested Learning Priority",
            ).pack(
                anchor="w",
                padx=15,
                pady=(12, 8),
            )

            for item in learning_plan[:8]:

                tk.Label(
                    card,
                    text=(
                        f"{item.get('rank', '?')}. "
                        f"{item.get('skill', '')} "
                        f"— {item.get('reason', '')}"
                    ),
                    bg=COLORS["surface"],
                    fg=COLORS["text"],
                    font=(
                        FONT_FAMILY,
                        FONT_SIZE_NORMAL,
                    ),
                    justify="left",
                    anchor="w",
                    wraplength=850,
                ).pack(
                    fill="x",
                    padx=20,
                    pady=3,
                )

    def _build_rewrite_section(self, parent):
        """Display Resume Improvement Agent results."""

        rewrite = self.career_report.get(
            "rewrite_analysis",
            {},
        )

        card = Card(parent)

        card.pack(
            fill="x",
            pady=5,
        )

        SectionTitle(
            card,
            "✍️ Resume Improvement Agent",
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 10),
        )

        summary = rewrite.get(
            "summary",
            {},
        )

        if summary:

            summary_text = summary.get(
                "suggestion",
                "",
            )

            if summary_text:

                tk.Label(
                    card,
                    text=(
                        "📝 Summary:\n"
                        + summary_text
                    ),
                    bg=COLORS["surface"],
                    fg=COLORS["text"],
                    font=(
                        FONT_FAMILY,
                        FONT_SIZE_NORMAL,
                    ),
                    justify="left",
                    anchor="w",
                    wraplength=850,
                ).pack(
                    fill="x",
                    padx=15,
                    pady=8,
                )

        weak_bullets = rewrite.get(
            "weak_bullets",
            [],
        )

        if weak_bullets:

            SectionTitle(
                card,
                "⚠️ Weak Bullet Points",
            ).pack(
                anchor="w",
                padx=15,
                pady=(10, 8),
            )

            for bullet in weak_bullets[:8]:

                original = bullet.get(
                    "original",
                    "",
                )

                reasons = bullet.get(
                    "reasons",
                    [],
                )

                suggestion = bullet.get(
                    "suggestion",
                    "",
                )

                text = (
                    f"• {original}\n\n"
                    f"Why: {', '.join(reasons)}\n"
                    f"Suggestion: {suggestion}"
                )

                tk.Label(
                    card,
                    text=text,
                    bg=COLORS["surface"],
                    fg=COLORS["text"],
                    font=(
                        FONT_FAMILY,
                        FONT_SIZE_NORMAL,
                    ),
                    justify="left",
                    anchor="w",
                    wraplength=850,
                ).pack(
                    fill="x",
                    padx=20,
                    pady=6,
                )

        wording = rewrite.get(
            "wording_improvements",
            [],
        )

        if wording:

            SectionTitle(
                card,
                "📝 Wording Improvements",
            ).pack(
                anchor="w",
                padx=15,
                pady=(10, 8),
            )

            for item in wording[:8]:

                tk.Label(
                    card,
                    text=(
                        f"'{item.get('original_phrase', '')}' "
                        f"→ "
                        f"'{item.get('suggested_phrase', '')}'"
                    ),
                    bg=COLORS["surface"],
                    fg=COLORS["text"],
                    font=(
                        FONT_FAMILY,
                        FONT_SIZE_NORMAL,
                    ),
                    anchor="w",
                ).pack(
                    fill="x",
                    padx=20,
                    pady=3,
                )

    def _display_skill_list(
        self,
        parent,
        title,
        items,
        text_color,
    ):
        """Display a compact skill/keyword list."""

        SectionTitle(
            parent,
            title,
        ).pack(
            anchor="w",
            padx=15,
            pady=(8, 5),
        )

        if not items:

            tk.Label(
                parent,
                text="None detected.",
                bg=COLORS["surface"],
                fg=COLORS["text_muted"],
                font=(
                    FONT_FAMILY,
                    FONT_SIZE_SMALL,
                ),
            ).pack(
                anchor="w",
                padx=20,
                pady=3,
            )

            return

        frame = tk.Frame(
            parent,
            bg=COLORS["surface"],
        )

        frame.pack(
            fill="x",
            padx=15,
            pady=(0, 8),
        )

        for item in items:

            tk.Label(
                frame,
                text=f"  {item}  ",
                bg=COLORS["surface_light"],
                fg=text_color,
                font=(
                    FONT_FAMILY,
                    FONT_SIZE_SMALL,
                    "bold",
                ),
                padx=5,
                pady=4,
            ).pack(
                side="left",
                padx=3,
                pady=3,
            )

    def _display_text_list(
        self,
        parent,
        title,
        items,
    ):
        """Display a simple text list."""

        SectionTitle(
            parent,
            title,
        ).pack(
            anchor="w",
            padx=15,
            pady=(10, 5),
        )

        for item in items:

            tk.Label(
                parent,
                text=f"• {item}",
                bg=COLORS["surface"],
                fg=COLORS["text"],
                font=(
                    FONT_FAMILY,
                    FONT_SIZE_NORMAL,
                ),
                justify="left",
                anchor="w",
                wraplength=850,
            ).pack(
                fill="x",
                padx=20,
                pady=3,
            )

    def _display_career_error(self, error):
        """Display a Career Intelligence error."""

        tk.Label(
            self.career_card,
            text=(
                "⚠️ Career Intelligence analysis failed.\n\n"
                f"{error}"
            ),
            bg=COLORS["surface"],
            fg=COLORS["danger"],
            font=(
                FONT_FAMILY,
                FONT_SIZE_NORMAL,
            ),
            justify="left",
            anchor="w",
        ).pack(
            fill="x",
            padx=15,
            pady=(0, 15),
        )

    # =========================================================
    # ORIGINAL RESUME SCORE
    # =========================================================

    def _build_score_section(self):
        """Display the overall resume score."""

        score = self.analysis_data.get(
            "score",
            0,
        )

        card = Card(self.content)

        card.pack(
            fill="x",
            padx=20,
            pady=10,
        )

        ScoreCard(
            card,
            score,
        ).pack(
            fill="x",
            padx=15,
            pady=15,
        )

    # =========================================================
    # STATISTICS
    # =========================================================

    def _build_statistics(self):
        """Display resume statistics."""

        stats_frame = tk.Frame(
            self.content,
            bg=COLORS["background"],
        )

        stats_frame.pack(
            fill="x",
            padx=20,
            pady=10,
        )

        stats_frame.columnconfigure(
            (0, 1, 2),
            weight=1,
        )

        word_count = self.analysis_data.get(
            "word_count",
            0,
        )

        skill_count = self.analysis_data.get(
            "skill_count",
            0,
        )

        sections = self.analysis_data.get(
            "sections",
            {},
        )

        section_count = sum(
            1
            for value in sections.values()
            if value
        )

        StatCard(
            stats_frame,
            "📝 Words",
            str(word_count),
        ).grid(
            row=0,
            column=0,
            sticky="ew",
            padx=5,
        )

        StatCard(
            stats_frame,
            "🛠️ Skills",
            str(skill_count),
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=5,
        )

        StatCard(
            stats_frame,
            "📚 Sections",
            str(section_count),
        ).grid(
            row=0,
            column=2,
            sticky="ew",
            padx=5,
        )

    # =========================================================
    # SCORE BREAKDOWN
    # =========================================================

    def _build_score_breakdown(self):
        """Display score breakdown."""

        details = self.analysis_data.get(
            "score_details",
            {},
        )

        card = Card(self.content)

        card.pack(
            fill="x",
            padx=20,
            pady=10,
        )

        SectionTitle(
            card,
            "📊 Score Breakdown",
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 10),
        )

        for name, values in details.items():

            score = values.get(
                "score",
                0,
            )

            maximum = values.get(
                "maximum",
                1,
            )

            percentage = (
                score / maximum * 100
                if maximum
                else 0
            )

            row = tk.Frame(
                card,
                bg=COLORS["surface"],
            )

            row.pack(
                fill="x",
                padx=15,
                pady=6,
            )

            tk.Label(
                row,
                text=name.title(),
                bg=COLORS["surface"],
                fg=COLORS["text"],
                font=(
                    FONT_FAMILY,
                    FONT_SIZE_NORMAL,
                ),
            ).pack(
                side="left",
            )

            tk.Label(
                row,
                text=f"{score}/{maximum}",
                bg=COLORS["surface"],
                fg=COLORS["text_muted"],
                font=(
                    FONT_FAMILY,
                    FONT_SIZE_SMALL,
                ),
            ).pack(
                side="right",
            )

            ProgressBar(
                card,
                percentage,
            ).pack(
                fill="x",
                padx=15,
                pady=(0, 8),
            )

    # =========================================================
    # SECTIONS
    # =========================================================

    def _build_sections(self):
        """Display detected resume sections."""

        sections = self.analysis_data.get(
            "sections",
            {},
        )

        card = Card(self.content)

        card.pack(
            fill="x",
            padx=20,
            pady=10,
        )

        SectionTitle(
            card,
            "📑 Resume Sections",
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 10),
        )

        for name, present in sections.items():

            status = (
                "✓ Found"
                if present
                else "✗ Missing"
            )

            color = (
                COLORS["success"]
                if present
                else COLORS["danger"]
            )

            row = tk.Frame(
                card,
                bg=COLORS["surface"],
            )

            row.pack(
                fill="x",
                padx=15,
                pady=4,
            )

            tk.Label(
                row,
                text=name,
                bg=COLORS["surface"],
                fg=COLORS["text"],
                font=(
                    FONT_FAMILY,
                    FONT_SIZE_NORMAL,
                ),
            ).pack(
                side="left",
            )

            tk.Label(
                row,
                text=status,
                bg=COLORS["surface"],
                fg=color,
                font=(
                    FONT_FAMILY,
                    FONT_SIZE_NORMAL,
                    "bold",
                ),
            ).pack(
                side="right",
            )

    # =========================================================
    # SKILLS
    # =========================================================

    def _build_skills(self):
        """Display detected skills."""

        skills = self.analysis_data.get(
            "skills",
            {},
        )

        card = Card(self.content)

        card.pack(
            fill="x",
            padx=20,
            pady=10,
        )

        SectionTitle(
            card,
            "🛠️ Detected Skills",
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 10),
        )

        if not skills:

            tk.Label(
                card,
                text="No skills detected.",
                bg=COLORS["surface"],
                fg=COLORS["text_muted"],
                font=(
                    FONT_FAMILY,
                    FONT_SIZE_NORMAL,
                ),
            ).pack(
                padx=15,
                pady=10,
            )

            return

        for category, skill_list in skills.items():

            tk.Label(
                card,
                text=category,
                bg=COLORS["surface"],
                fg=COLORS["text"],
                font=(
                    FONT_FAMILY,
                    FONT_SIZE_NORMAL,
                    "bold",
                ),
            ).pack(
                anchor="w",
                padx=15,
                pady=(8, 4),
            )

            skills_frame = tk.Frame(
                card,
                bg=COLORS["surface"],
            )

            skills_frame.pack(
                fill="x",
                padx=15,
                pady=(0, 8),
            )

            for skill in skill_list:

                SkillTag(
                    skills_frame,
                    skill,
                ).pack(
                    side="left",
                    padx=3,
                    pady=3,
                )

    # =========================================================
    # RECOMMENDATIONS
    # =========================================================

    def _build_recommendations(self):
        """Display traditional recommendations."""

        recommendations = self.analysis_data.get(
            "recommendations",
            [],
        )

        card = Card(self.content)

        card.pack(
            fill="x",
            padx=20,
            pady=10,
        )

        SectionTitle(
            card,
            "💡 Recommendations",
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 10),
        )

        if not recommendations:

            tk.Label(
                card,
                text="No recommendations.",
                bg=COLORS["surface"],
                fg=COLORS["text_muted"],
                font=(
                    FONT_FAMILY,
                    FONT_SIZE_NORMAL,
                ),
            ).pack(
                padx=15,
                pady=10,
            )

            return

        for recommendation in recommendations:

            RecommendationCard(
                card,
                recommendation.get(
                    "message",
                    "",
                ),
                recommendation.get(
                    "priority",
                    "medium",
                ),
                recommendation.get(
                    "category",
                    "General",
                ),
            ).pack(
                fill="x",
                padx=15,
                pady=5,
            )

    # =========================================================
    # AI ANALYSIS
    # =========================================================

    def show_ai_analysis(self):
        """Start AI-powered analysis in the background."""

        self.ai_card = Card(self.content)

        self.ai_card.pack(
            fill="x",
            padx=20,
            pady=10,
        )

        SectionTitle(
            self.ai_card,
            "🤖 AI Resume Analysis",
        ).pack(
            anchor="w",
            padx=15,
            pady=(15, 10),
        )

        self.ai_loading_label = tk.Label(
            self.ai_card,
            text=(
                "🤖 AI is analyzing your resume...\n\n"
                "You can continue using the application."
            ),
            bg=COLORS["surface"],
            fg=COLORS["text_muted"],
            font=(
                FONT_FAMILY,
                FONT_SIZE_NORMAL,
            ),
            justify="center",
        )

        self.ai_loading_label.pack(
            padx=15,
            pady=20,
        )

        self.ai_worker = AIWorker(
            self.resume_text
        )

        self.ai_worker.start()

        self.after(
            100,
            self._check_ai_worker,
        )

    def _check_ai_worker(self):
        """Check whether the background AI worker finished."""

        if self.ai_worker is None:
            return

        if not self.ai_worker.is_finished():

            self.after(
                100,
                self._check_ai_worker,
            )

            return

        if self.ai_worker.error is not None:

            self.ai_loading_label.config(
                text=(
                    "⚠️ AI analysis failed.\n\n"
                    f"{self.ai_worker.error}"
                ),
                fg=COLORS["danger"],
                justify="left",
            )

            return

        result = self.ai_worker.result

        self.ai_loading_label.destroy()

        self._display_ai_result(
            self.ai_card,
            result,
        )

    def _display_ai_result(
        self,
        card,
        data,
    ):
        """Display structured AI analysis."""

        text_sections = [
            (
                "🧠 Overall Impression",
                data.get(
                    "overall_impression",
                    "",
                ),
            ),
            (
                "✍️ Writing",
                data.get(
                    "writing",
                    "",
                ),
            ),
            (
                "💼 Experience",
                data.get(
                    "experience",
                    "",
                ),
            ),
            (
                "🛠️ Skills",
                data.get(
                    "skills",
                    "",
                ),
            ),
            (
                "📝 Summary",
                data.get(
                    "summary",
                    "",
                ),
            ),
        ]

        for title, content in text_sections:

            SectionTitle(
                card,
                title,
            ).pack(
                anchor="w",
                padx=15,
                pady=(10, 5),
            )

            tk.Label(
                card,
                text=content,
                bg=COLORS["surface"],
                fg=COLORS["text"],
                font=(
                    FONT_FAMILY,
                    FONT_SIZE_NORMAL,
                ),
                justify="left",
                anchor="w",
                wraplength=900,
            ).pack(
                fill="x",
                padx=15,
                pady=(0, 10),
            )

        self._add_ai_list(
            card,
            "💪 Strengths",
            data.get(
                "strengths",
                [],
            ),
        )

        self._add_ai_list(
            card,
            "⚠️ Weaknesses",
            data.get(
                "weaknesses",
                [],
            ),
        )

        self._add_ai_list(
            card,
            "✅ Action Items",
            data.get(
                "action_items",
                [],
            ),
        )

    def _add_ai_list(
        self,
        parent,
        title,
        items,
    ):
        """Display a list of AI-generated items."""

        SectionTitle(
            parent,
            title,
        ).pack(
            anchor="w",
            padx=15,
            pady=(10, 5),
        )

        if not items:

            tk.Label(
                parent,
                text="None.",
                bg=COLORS["surface"],
                fg=COLORS["text_muted"],
                font=(
                    FONT_FAMILY,
                    FONT_SIZE_NORMAL,
                ),
            ).pack(
                fill="x",
                padx=25,
                pady=3,
            )

            return

        for item in items:

            tk.Label(
                parent,
                text=f"• {item}",
                bg=COLORS["surface"],
                fg=COLORS["text"],
                font=(
                    FONT_FAMILY,
                    FONT_SIZE_NORMAL,
                ),
                justify="left",
                anchor="w",
                wraplength=900,
            ).pack(
                fill="x",
                padx=25,
                pady=3,
            )


# =============================================================
# DIRECT TEST
# =============================================================

if __name__ == "__main__":

    fake_analysis = {
        "score": 82,

        "score_details": {
            "sections": {
                "score": 70,
                "maximum": 90,
            },
            "skills": {
                "score": 12,
                "maximum": 15,
            },
            "content": {
                "score": 14,
                "maximum": 15,
            },
        },

        "word_count": 420,

        "sections": {
            "Contact Information": True,
            "Summary": True,
            "Education": True,
            "Experience": True,
            "Skills": True,
            "Projects": True,
            "Certifications": False,
        },

        "skills": {
            "Programming Languages": [
                "Python",
                "JavaScript",
            ],
            "Web Development": [
                "Django",
            ],
            "Databases": [
                "SQL",
            ],
        },

        "skill_count": 4,

        "recommendations": [
            {
                "message": "Add measurable achievements.",
                "priority": "high",
                "category": "Content",
            },
        ],
    }

    fake_resume = """
    Alex Johnson

    Software Developer

    SUMMARY

    Python developer interested in web applications.

    EXPERIENCE

    Software Developer

    - Built Python applications.
    - Worked on web applications.

    SKILLS

    Python, Django, SQL
    """

    root = tk.Tk()

    root.title(
        "Resume Analyzer - Career Intelligence"
    )

    root.geometry(
        "1100x700"
    )

    dashboard = ResumeDashboard(
        root,
        fake_analysis,
        fake_resume,
        root.destroy,
    )

    dashboard.pack(
        fill="both",
        expand=True,
    )

    root.mainloop()