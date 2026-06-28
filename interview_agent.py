import os
import json
from groq import Groq

class InterviewAgent:
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        self.model_name = "llama-3.3-70b-versatile"  # fast + strong Groq model

    def generate_qa_prep(self, job_role: str, level: str) -> dict:
        if not self.client:
            return {
                "prep_materials": [
                    {
                        "question": f"Explain your experience with core tools required for a {job_role} role.",
                        "type": "Technical",
                        "model_answer": f"I have built projects using the stack common to {job_role}, ensuring data flow efficiency and standard code conventions.",
                        "tips": "Highlight specific frameworks, project sizes, and challenges you overcame."
                    },
                    {
                        "question": "Tell me about a time you faced a technical roadblock and how you resolved it.",
                        "type": "Behavioral",
                        "model_answer": "In my project, I encountered a latency issue. I systematically logged execution times, isolated the slow DB query, created index patterns, and reduced load times by 40%.",
                        "tips": "Use the STAR method: Situation, Task, Action, Result."
                    }
                ]
            }

        prompt = f"""
        Generate 5 interview preparation questions for a "{job_role}" position at the "{level}" level.
        Mix technical questions (relevant to the role's stack) and behavioral questions.
        Provide model answers and preparation tips for each.

        Return a valid JSON object matching this structure:
        {{
            "prep_materials": [
                {{
                    "question": "The question text",
                    "type": "Technical or Behavioral",
                    "model_answer": "A detailed high-quality model answer",
                    "tips": "Tips on how the candidate should structure their answer"
                }}
            ]
        }}
        Do not include markdown tags. Return only JSON.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            return {
                "prep_materials": [
                    {
                        "question": f"[API Offline Fallback] Explain your experience with core tools required for a {job_role} role.",
                        "type": "Technical",
                        "model_answer": f"I have built projects using the stack common to {job_role}, ensuring data flow efficiency and standard code conventions.",
                        "tips": "Highlight specific frameworks, project sizes, and challenges you overcame."
                    },
                    {
                        "question": "[API Offline Fallback] Tell me about a time you faced a technical roadblock and how you resolved it.",
                        "type": "Behavioral",
                        "model_answer": "In my project, I encountered a latency issue. I systematically logged execution times, isolated the slow DB query, created index patterns, and reduced load times by 40%.",
                        "tips": "Use the STAR method: Situation, Task, Action, Result."
                    }
                ],
                "api_warning": True
            }

    def conduct_mock_interview(self, history: list, user_message: str, job_role: str, level: str) -> dict:
        if not self.client:
            return {
                "feedback": "Nice job answering! (API key not available for full evaluation)",
                "next_question": "Can you explain how you handle version control and code deployment?",
                "is_concluded": False,
                "assessment": None
            }

        history_str = ""
        for h in history:
            role = "Interviewer" if h["role"] == "assistant" else "Candidate"
            content = h["content"]
            history_str += f"{role}: {content}\n"

        prompt = f"""
        You are an experienced technical recruiter conducting a mock interview for the role of "{job_role}" ({level} level).
        Here is the history of the interview conversation so far:
        {history_str}

        The candidate just responded with:
        Candidate: "{user_message}"

        Perform the following steps:
        1. Evaluate the candidate's last answer. Give brief, constructive feedback.
        2. Decide if you have asked enough questions (aim for 3-4 rounds).
           - If NOT concluded: output the next relevant interview question. Set "is_concluded" to false.
           - If CONCLUDED: summarize their overall performance, provide strengths, areas of improvement, a numeric score (0 to 100), and set "is_concluded" to true, with "next_question" as "CONCLUDED".

        Return a valid JSON object matching this structure:
        {{
            "feedback": "Brief feedback about their latest answer.",
            "next_question": "The next interview question text OR 'CONCLUDED'",
            "is_concluded": false,
            "assessment": {{
                "score": 85,
                "strengths": ["strength1", "strength2"],
                "improvements": ["improvement1", "improvement2"]
            }}
        }}
        If is_concluded is false, "assessment" can be null.
        Do not include markdown tags. Return only JSON.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )
            return json.loads(response.choices[0].message.content)
        except Exception as e:
            rounds = len(history) // 2
            if rounds >= 2:
                return {
                    "feedback": "[API Offline Fallback] Good details provided in your answers.",
                    "next_question": "CONCLUDED",
                    "is_concluded": True,
                    "assessment": {
                        "score": 82,
                        "strengths": ["Clear response layout", "Logical troubleshooting explanation"],
                        "improvements": ["Elaborate more on optimization outcomes", "Mention architectural design decisions"]
                    }
                }
            else:
                return {
                    "feedback": "[API Offline Fallback] Understood. Let's proceed.",
                    "next_question": "Can you explain how you handle version control, testing, and CI/CD pipelines in your code?",
                    "is_concluded": False,
                    "assessment": None
                }
