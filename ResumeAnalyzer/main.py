"""
Entry point for Resume Analyzer.
"""

from ui.app import ResumeAnalyzerApp


def main():
    """Launch the Resume Analyzer application."""

    app = ResumeAnalyzerApp()
    app.mainloop()


if __name__ == "__main__":
    main()