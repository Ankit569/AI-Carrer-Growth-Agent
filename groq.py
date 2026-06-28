import os
import json
import re
from groq import Groq


class GroqClient:
    """
    Thin wrapper around the Groq API.
    Sends a prompt and returns a parsed JSON dict (since all our
    agents ask the model to "return JSON only").

    Drop-in replacement for GeminiClient — same generate(prompt) -> dict interface.
    """

    def __init__(self, model_name: str = "llama-3.3-70b-versatile"):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError(
                "Missing Groq API key. Set GROQ_API_KEY as an environment "
                "variable (e.g. in a .env file or Streamlit secrets)."
            )

        self.client = Groq(api_key=api_key)
        self.model_name = model_name

    def generate(self, prompt: str) -> dict:
        try:
            result = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=0.3,
            )
            raw_text = result.choices[0].message.content.strip()
        except Exception as e:
            return {"error": f"Groq API call failed: {e}"}

        # Strip markdown code fences if the model added them anyway
        cleaned = re.sub(
            r"^```(?:json)?\s*|\s*```$", "", raw_text.strip(), flags=re.MULTILINE
        ).strip()

        try:
            return json.loads(cleaned)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", cleaned, flags=re.DOTALL)
            if match:
                try:
                    return json.loads(match.group(0))
                except json.JSONDecodeError:
                    pass
            return {
                "error": "Failed to parse Groq response as JSON",
                "raw_response": raw_text,
            }