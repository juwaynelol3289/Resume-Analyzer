"""
Main Tkinter application for Resume Analyzer.
"""

import tkinter as tk
from tkinter import filedialog, messagebox

from config import (
    COLORS,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH,
    MIN_WINDOW_HEIGHT,
    FONT_FAMILY,
    FONT_SIZE_TITLE,
    FONT_SIZE_NORMAL,
)

from parser import parse_resume
from analyzer import analyze_resume

from ui.dashboard import ResumeDashboard


class ResumeAnalyzerApp(tk.Tk):
    """Main Resume Analyzer application."""

    def __init__(self):
        super().__init__()

        self.title("Resume Analyzer")

        self.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
        )

        self.minsize(
            MIN_WINDOW_WIDTH,
            MIN_WINDOW_HEIGHT
        )

        self.configure(
            bg=COLORS["background"]
        )

        self.current_file = None
        self.current_resume_text = None
        self.current_analysis = None

        self.show_home()

    # =========================================================
    # HOME SCREEN
    # =========================================================

    def show_home(self):
        """Display the home screen."""

        for widget in self.winfo_children():
            widget.destroy()

        container = tk.Frame(
            self,
            bg=COLORS["background"]
        )

        container.pack(
            fill="both",
            expand=True
        )

        title = tk.Label(
            container,
            text="📄 Resume Analyzer",
            bg=COLORS["background"],
            fg=COLORS["text"],
            font=(
                FONT_FAMILY,
                30,
                "bold"
            )
        )

        title.pack(
            pady=(120, 10)
        )

        subtitle = tk.Label(
            container,
            text=(
                "Analyze your resume with traditional "
                "scoring and AI-powered feedback."
            ),
            bg=COLORS["background"],
            fg=COLORS["text_muted"],
            font=(
                FONT_FAMILY,
                FONT_SIZE_NORMAL
            )
        )

        subtitle.pack(
            pady=(0, 30)
        )

        choose_button = tk.Button(
            container,
            text="📂 Choose Resume",
            command=self.choose_resume,
            bg=COLORS["accent"],
            fg=COLORS["text"],
            activebackground=COLORS["accent"],
            activeforeground=COLORS["text"],
            relief="flat",
            padx=30,
            pady=15,
            font=(
                FONT_FAMILY,
                FONT_SIZE_NORMAL,
                "bold"
            ),
            cursor="hand2"
        )

        choose_button.pack()

        supported = tk.Label(
            container,
            text="Supported formats: TXT • PDF • DOCX",
            bg=COLORS["background"],
            fg=COLORS["text_muted"],
            font=(
                FONT_FAMILY,
                FONT_SIZE_NORMAL
            )
        )

        supported.pack(
            pady=20
        )

    # =========================================================
    # FILE SELECTION
    # =========================================================

    def choose_resume(self):
        """Open the resume file picker."""

        file_path = filedialog.askopenfilename(
            title="Choose Resume",
            filetypes=[
                (
                    "Resume files",
                    "*.txt *.pdf *.docx"
                ),
                (
                    "Text files",
                    "*.txt"
                ),
                (
                    "PDF files",
                    "*.pdf"
                ),
                (
                    "Word documents",
                    "*.docx"
                ),
                (
                    "All files",
                    "*.*"
                )
            ]
        )

        if not file_path:
            return

        self.load_resume(
            file_path
        )

    # =========================================================
    # LOAD RESUME
    # =========================================================

    def load_resume(self, file_path):
        """Parse and analyze a selected resume."""

        try:

            self.current_file = file_path

            # Parse resume
            resume_text = parse_resume(
                file_path
            )

            if not resume_text.strip():

                raise ValueError(
                    "The selected resume contains no readable text."
                )

            self.current_resume_text = resume_text

            # Traditional analysis
            analysis = analyze_resume(
                resume_text
            )

            self.current_analysis = analysis

            self.show_dashboard()

        except Exception as error:

            messagebox.showerror(
                "Resume Analyzer Error",
                str(error)
            )

    # =========================================================
    # DASHBOARD
    # =========================================================

    def show_dashboard(self):
        """Display the analysis dashboard."""

        for widget in self.winfo_children():
            widget.destroy()

        dashboard = ResumeDashboard(
            self,
            self.current_analysis,
            self.current_resume_text,
            self.show_home
        )

        dashboard.pack(
            fill="both",
            expand=True
        )


# =============================================================
# DIRECT TEST
# =============================================================

if __name__ == "__main__":

    app = ResumeAnalyzerApp()

    app.mainloop()