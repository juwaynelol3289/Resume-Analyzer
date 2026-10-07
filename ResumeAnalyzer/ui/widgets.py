"""
Reusable Tkinter widgets for Resume Analyzer.

This module contains UI components that can be reused
throughout the application.
"""

import tkinter as tk
from tkinter import ttk

from config import (
    COLORS,
    FONT_FAMILY,
    FONT_SIZE_SMALL,
    FONT_SIZE_NORMAL,
    FONT_SIZE_LARGE,
    FONT_SIZE_TITLE,
)


# =========================================================
# STYLE HELPERS
# =========================================================

def create_font(size, weight="normal"):
    """Create a consistent application font."""

    return (
        FONT_FAMILY,
        size,
        weight,
    )


# =========================================================
# CARD
# =========================================================

class Card(tk.Frame):
    """Reusable dark-themed card container."""

    def __init__(
        self,
        parent,
        padding=20,
        **kwargs,
    ):
        super().__init__(
            parent,
            bg=COLORS["surface"],
            **kwargs,
        )

        self.configure(
            highlightthickness=0,
            bd=0,
        )

        self.inner = tk.Frame(
            self,
            bg=COLORS["surface"],
        )

        self.inner.pack(
            fill="both",
            expand=True,
            padx=padding,
            pady=padding,
        )


# =========================================================
# SECTION TITLE
# =========================================================

class SectionTitle(tk.Label):
    """Large title used above dashboard sections."""

    def __init__(
        self,
        parent,
        text,
        **kwargs,
    ):
        super().__init__(
            parent,
            text=text,
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=create_font(
                FONT_SIZE_LARGE,
                "bold",
            ),
            anchor="w",
            **kwargs,
        )


# =========================================================
# PRIMARY BUTTON
# =========================================================

class PrimaryButton(tk.Button):
    """Main application button."""

    def __init__(
        self,
        parent,
        text,
        command=None,
        **kwargs,
    ):
        super().__init__(
            parent,
            text=text,
            command=command,
            bg=COLORS["accent"],
            fg=COLORS["text"],
            activebackground=COLORS["accent"],
            activeforeground=COLORS["text"],
            font=create_font(
                FONT_SIZE_NORMAL,
                "bold",
            ),
            relief="flat",
            bd=0,
            padx=18,
            pady=10,
            cursor="hand2",
            **kwargs,
        )


# =========================================================
# SECONDARY BUTTON
# =========================================================

class SecondaryButton(tk.Button):
    """Secondary application button."""

    def __init__(
        self,
        parent,
        text,
        command=None,
        **kwargs,
    ):
        super().__init__(
            parent,
            text=text,
            command=command,
            bg=COLORS["surface_light"],
            fg=COLORS["text"],
            activebackground=COLORS["surface_light"],
            activeforeground=COLORS["text"],
            font=create_font(
                FONT_SIZE_NORMAL,
                "bold",
            ),
            relief="flat",
            bd=0,
            padx=18,
            pady=10,
            cursor="hand2",
            **kwargs,
        )


# =========================================================
# SCORE CARD
# =========================================================

class ScoreCard(Card):
    """Card displaying a large resume score."""

    def __init__(
        self,
        parent,
        score=0,
        title="Resume Score",
        **kwargs,
    ):
        super().__init__(
            parent,
            **kwargs,
        )

        title_label = tk.Label(
            self.inner,
            text=title,
            bg=COLORS["surface"],
            fg=COLORS["text_muted"],
            font=create_font(
                FONT_SIZE_NORMAL,
                "bold",
            ),
        )

        title_label.pack(
            anchor="w",
        )

        self.score_label = tk.Label(
            self.inner,
            text=f"{score}/100",
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=create_font(
                FONT_SIZE_TITLE,
                "bold",
            ),
        )

        self.score_label.pack(
            anchor="w",
            pady=(8, 0),
        )

    def set_score(self, score):
        """Update the displayed score."""

        self.score_label.config(
            text=f"{score}/100"
        )


# =========================================================
# STAT CARD
# =========================================================

class StatCard(Card):
    """Small card displaying a statistic."""

    def __init__(
        self,
        parent,
        title,
        value,
        **kwargs,
    ):
        super().__init__(
            parent,
            padding=15,
            **kwargs,
        )

        tk.Label(
            self.inner,
            text=title,
            bg=COLORS["surface"],
            fg=COLORS["text_muted"],
            font=create_font(
                FONT_SIZE_SMALL,
            ),
        ).pack(
            anchor="w",
        )

        self.value_label = tk.Label(
            self.inner,
            text=str(value),
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=create_font(
                FONT_SIZE_LARGE,
                "bold",
            ),
        )

        self.value_label.pack(
            anchor="w",
            pady=(5, 0),
        )

    def set_value(self, value):
        """Update the statistic."""

        self.value_label.config(
            text=str(value)
        )


# =========================================================
# PROGRESS BAR
# =========================================================

class ProgressBar(tk.Frame):
    """Custom progress bar."""

    def __init__(
        self,
        parent,
        value=0,
        height=10,
        **kwargs,
    ):
        super().__init__(
            parent,
            bg=COLORS["surface"],
            **kwargs,
        )

        self.height = height
        self.value = 0

        self.canvas = tk.Canvas(
            self,
            height=height,
            bg=COLORS["surface_light"],
            highlightthickness=0,
            bd=0,
        )

        self.canvas.pack(
            fill="x",
            expand=True,
        )

        self.set_value(value)

        self.bind(
            "<Configure>",
            lambda event: self.draw(),
        )

    def set_value(self, value):
        """Set progress value from 0 to 100."""

        self.value = max(
            0,
            min(100, float(value)),
        )

        self.draw()

    def draw(self):
        """Redraw the progress bar."""

        self.canvas.delete("all")

        width = self.canvas.winfo_width()

        if width <= 1:
            return

        progress_width = (
            width * self.value / 100
        )

        self.canvas.create_rectangle(
            0,
            0,
            progress_width,
            self.height,
            fill=COLORS["accent"],
            outline="",
        )


# =========================================================
# SKILL TAG
# =========================================================

class SkillTag(tk.Label):
    """Small label used for displaying a skill."""

    def __init__(
        self,
        parent,
        text,
        **kwargs,
    ):
        super().__init__(
            parent,
            text=f"  {text}  ",
            bg=COLORS["surface_light"],
            fg=COLORS["text"],
            font=create_font(
                FONT_SIZE_SMALL,
                "bold",
            ),
            padx=4,
            pady=4,
            **kwargs,
        )


# =========================================================
# STATUS ROW
# =========================================================

class StatusRow(tk.Frame):
    """Displays a section with a check or cross."""

    def __init__(
        self,
        parent,
        title,
        status=False,
        **kwargs,
    ):
        super().__init__(
            parent,
            bg=COLORS["surface"],
            **kwargs,
        )

        self.status = status

        self.icon_label = tk.Label(
            self,
            bg=COLORS["surface"],
            font=create_font(
                FONT_SIZE_NORMAL,
                "bold",
            ),
        )

        self.icon_label.pack(
            side="left",
            padx=(0, 8),
        )

        self.title_label = tk.Label(
            self,
            text=title,
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=create_font(
                FONT_SIZE_NORMAL,
            ),
        )

        self.title_label.pack(
            side="left",
        )

        self.update_status(status)

    def update_status(self, status):
        """Update the row status."""

        self.status = status

        if status:
            self.icon_label.config(
                text="✓",
                fg=COLORS["success"],
            )
        else:
            self.icon_label.config(
                text="✕",
                fg=COLORS["danger"],
            )


# =========================================================
# RECOMMENDATION CARD
# =========================================================

class RecommendationCard(Card):
    """Displays a single recommendation."""

    def __init__(
        self,
        parent,
        message,
        priority="medium",
        category="General",
        **kwargs,
    ):
        super().__init__(
            parent,
            padding=15,
            **kwargs,
        )

        priority_colors = {
            "high": COLORS["danger"],
            "medium": COLORS["warning"],
            "low": COLORS["success"],
        }

        priority_color = priority_colors.get(
            priority.lower(),
            COLORS["text_muted"],
        )

        header = tk.Frame(
            self.inner,
            bg=COLORS["surface"],
        )

        header.pack(
            fill="x",
        )

        tk.Label(
            header,
            text=category,
            bg=COLORS["surface"],
            fg=COLORS["text_muted"],
            font=create_font(
                FONT_SIZE_SMALL,
                "bold",
            ),
        ).pack(
            side="left",
        )

        tk.Label(
            header,
            text=priority.upper(),
            bg=COLORS["surface"],
            fg=priority_color,
            font=create_font(
                FONT_SIZE_SMALL,
                "bold",
            ),
        ).pack(
            side="right",
        )

        tk.Label(
            self.inner,
            text=message,
            bg=COLORS["surface"],
            fg=COLORS["text"],
            font=create_font(
                FONT_SIZE_NORMAL,
            ),
            justify="left",
            anchor="w",
            wraplength=500,
        ).pack(
            fill="x",
            pady=(8, 0),
        )


# =========================================================
# SCROLLABLE FRAME
# =========================================================

class ScrollableFrame(tk.Frame):
    """
    A vertically scrollable frame.

    Useful for long recommendation lists,
    skill lists, and analysis results.
    """

    def __init__(
        self,
        parent,
        **kwargs,
    ):
        super().__init__(
            parent,
            bg=COLORS["background"],
            **kwargs,
        )

        self.canvas = tk.Canvas(
            self,
            bg=COLORS["background"],
            highlightthickness=0,
            bd=0,
        )

        self.scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.canvas.yview,
        )

        self.content = tk.Frame(
            self.canvas,
            bg=COLORS["background"],
        )

        self.window_id = (
            self.canvas.create_window(
                (0, 0),
                window=self.content,
                anchor="nw",
            )
        )

        self.canvas.configure(
            yscrollcommand=self.scrollbar.set,
        )

        self.canvas.pack(
            side="left",
            fill="both",
            expand=True,
        )

        self.scrollbar.pack(
            side="right",
            fill="y",
        )

        self.content.bind(
            "<Configure>",
            self._update_scroll_region,
        )

        self.canvas.bind(
            "<Configure>",
            self._resize_content,
        )

    def _update_scroll_region(self, event=None):
        """Update the canvas scroll region."""

        self.canvas.configure(
            scrollregion=self.canvas.bbox("all")
        )

    def _resize_content(self, event):
        """Keep content width equal to canvas width."""

        self.canvas.itemconfigure(
            self.window_id,
            width=event.width,
        )