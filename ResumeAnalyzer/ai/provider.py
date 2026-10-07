"""
OpenAI API provider.

Keeps all OpenAI API communication in one place.
"""

import os

from openai import OpenAI


class OpenAIProvider:
    """Small wrapper around the OpenAI Responses API."""

    def __init__(self, model="gpt-6-luna"):
        self.model = model

        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY environment variable was not found."
            )

        self.client = OpenAI(
            api_key=api_key
        )

    def analyze(self, prompt):
        """
        Send a prompt to OpenAI and return the text response.
        """

        response = self.client.responses.create(
            model=self.model,
            input=prompt,
        )

        return response.output_text


def create_provider():
    """Create the default OpenAI provider."""

    return OpenAIProvider()


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print("Testing OpenAI connection...")

    try:
        provider = create_provider()

        result = provider.analyze(
            "Reply with exactly: Resume Analyzer AI is online."
        )

        print("\nAI RESPONSE:")
        print(result)

    except Exception as error:

        print("\nAI CONNECTION FAILED:")
        print(error)


if __name__ == "__main__":
    import os

    key = os.getenv("OPENAI_API_KEY")

    print("API key found:", key is not None)
    print("API key length:", len(key) if key else 0)

    if key:
        print("API key starts with:", key[:7])
        print("API key ends with:", key[-4:])

    print("\nTesting OpenAI connection...")

    try:
        provider = create_provider()

        result = provider.analyze(
            "Reply with exactly: Resume Analyzer AI is online."
        )

        print("\nAI RESPONSE:")
        print(result)

    except Exception as error:
        print("\nAI CONNECTION FAILED:")
        print(error)