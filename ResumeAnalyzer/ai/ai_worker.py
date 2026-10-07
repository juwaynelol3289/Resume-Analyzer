"""
Background AI worker for Resume Analyzer.

Runs AI analysis in a separate thread so the Tkinter
interface remains responsive while OpenAI is processing.
"""

import threading

from ai.ai_analyzer import analyze_resume_with_ai


class AIWorker:
    """Run AI resume analysis in a background thread."""

    def __init__(self, resume_text):
        self.resume_text = resume_text

        self.result = None
        self.error = None

        self.thread = None

    def start(self):
        """Start the AI analysis in the background."""

        if self.thread is not None and self.thread.is_alive():
            return

        self.thread = threading.Thread(
            target=self._run,
            daemon=True
        )

        self.thread.start()

    def _run(self):
        """Perform the AI analysis."""

        try:
            self.result = analyze_resume_with_ai(
                self.resume_text
            )

        except Exception as error:
            self.error = error

    def is_finished(self):
        """Return True when the worker has finished."""

        return (
            self.thread is not None
            and not self.thread.is_alive()
        )