import os
import json
from groq import Groq

class RoadmapAgent:
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        self.model_name = "llama-3.3-70b-versatile"

    def generate_roadmap(self, user_skills: list, target_role: str, gap_skills: list, duration_months: int = 3) -> dict:
        """
        Generates a personalized month-by-month learning plan to bridge the skill gap.
        Returns structured JSON with milestones, action items, projects, and resources.
        """
        user_skills_str = ", ".join(user_skills) if user_skills else "None listed"
        gap_skills_str = ", ".join(gap_skills) if gap_skills else "General role fundamentals"

        if not self.client:
            # Fallback mock roadmap generator
            roadmap = []
            for i in range(1, duration_months + 1):
                roadmap.append({
                    "period": f"Month {i}",
                    "milestone": f"Acquire core competencies in subset of gap skills",
                    "topics": [gap_skills[0] if gap_skills else "Core Programming", "Fundamentals"],
                    "action_items": ["Read documentation", "Build mini project"],
                    "resources": [
                        {"name": "FreeCodeCamp", "url": "https://www.freecodecamp.org"},
                        {"name": "Roadmap.sh", "url": "https://roadmap.sh"}
                    ]
                })
            return {"roadmap": roadmap}

        prompt = f"""
        Design a highly tailored month-by-month learning roadmap for a student aiming to become a "{target_role}".
        - Duration: {duration_months} months
        - User's existing skills: {user_skills_str}
        - Key skills to learn (gaps): {gap_skills_str}

        Return a valid JSON object matching this structure:
        {{
            "roadmap": [
                {{
                    "period": "Month 1: [Custom Title]",
                    "milestone": "Key milestone goal for this month.",
                    "topics": ["Topic 1", "Topic 2", ...],
                    "action_items": [
                        "Specific action item / exercise.",
                        "Concrete project task."
                    ],
                    "resources": [
                        {{
                            "name": "Resource Name (e.g. YouTube, official docs, Coursera)",
                            "url": "URL or search suggestion description"
                        }}
                    ]
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
            # Fallback mock roadmap generator on error
            roadmap = []
            gaps = gap_skills if gap_skills else ["Standard Tech Foundation"]
            for i in range(1, duration_months + 1):
                # Pick a subset of skills to learn
                skill_slice = gaps[(i-1) % len(gaps): i % len(gaps) + 1]
                roadmap.append({
                    "period": f"Month {i}: Master {', '.join(skill_slice)}",
                    "milestone": f"Complete hands-on projects and theoretical study of {', '.join(skill_slice)}.",
                    "topics": skill_slice + ["Core Concepts", "Best Practices"],
                    "action_items": [
                        f"Study syntax and basic architecture of {skill_slice[0]}.",
                        f"Implement a small-scale sample application using {skill_slice[0]}.",
                        "Optimize code execution speed and commit to version control."
                    ],
                    "resources": [
                        {"name": "Official Documentation", "url": f"https://www.google.com/search?q={skill_slice[0]}+documentation"},
                        {"name": "FreeCodeCamp Interactive Course", "url": "https://www.freecodecamp.org"}
                    ]
                })
            return {"roadmap": roadmap, "api_warning": True}