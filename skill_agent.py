import os
import json
import pandas as pd
from groq import Groq

class SkillAgent:
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY")
        self.client = Groq(api_key=self.api_key) if self.api_key else None
        self.model_name = "llama-3.3-70b-versatile"
        self.csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "job_roles.csv")

    def recommend_roles(self, degree: str, skills: list, experience: str, interests: str) -> dict:
        """
        Recommends suitable career roles based on user input.
        Returns a dict containing a list of roles with matching explanations.
        """
        skills_str = ", ".join(skills) if isinstance(skills, list) else str(skills)

        if not self.client:
            # Fallback mock data
            return {
                "roles": [
                    {
                        "role": "Python Developer",
                        "reason": f"Your background with degree '{degree}' and skills in '{skills_str}' strongly matches Python web and scripting demands."
                    },
                    {
                        "role": "AI Engineer",
                        "reason": f"Your interest in '{interests}' and development experience aligns well with modern Generative AI application development."
                    },
                    {
                        "role": "Data Analyst",
                        "reason": "Analytical skillsets combined with Python allow for effective business intelligence reporting."
                    }
                ]
            }

        prompt = f"""
        Recommend 3 potential career roles for a user with the following profile:
        - Degree: {degree}
        - Current Skills: {skills_str}
        - Experience: {experience}
        - Interests/Goals: {interests}

        Return a valid JSON object matching the structure:
        {{
            "roles": [
                {{
                    "role": "Role Name",
                    "reason": "A clear description of why this role matches their profile, connecting their specific skills, degree, and interests."
                }}
            ]
        }}
        Do not include markdown blocks or extra commentary. Return only JSON.
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
                "roles": [
                    {
                        "role": "Python Developer",
                        "reason": f"[API Offline Fallback] Your background with degree '{degree}' and skills in '{skills_str}' strongly matches Python web and scripting demands."
                    },
                    {
                        "role": "AI Engineer",
                        "reason": f"[API Offline Fallback] Your interest in '{interests}' and development experience aligns well with modern Generative AI application development."
                    },
                    {
                        "role": "Data Analyst",
                        "reason": "[API Offline Fallback] Analytical skillsets combined with Python allow for effective business intelligence reporting."
                    }
                ],
                "api_warning": True
            }

    def analyze_skill_gap(self, user_skills: list, target_role: str) -> dict:
        """
        Compares user's skills with required skills for a target job role.
        Utilizes local CSV database first, falling back to Groq API.
        """
        # Lowercase list for comparison
        user_skills_clean = [s.strip().lower() for s in user_skills]

        # Check local database
        required_skills = []
        role_description = ""
        found_in_csv = False

        if os.path.exists(self.csv_path):
            try:
                df = pd.read_csv(self.csv_path)
                match = df[df["Role"].str.lower() == target_role.strip().lower()]
                if not match.empty:
                    skills_raw = match.iloc[0]["Required_Skills"]
                    required_skills = [s.strip() for s in skills_raw.split(",")]
                    role_description = match.iloc[0]["Description"]
                    found_in_csv = True
            except Exception as e:
                print(f"Error reading CSV: {e}")

        # If not found locally and Groq is available, query Groq
        if not found_in_csv and self.client:
            prompt = f"""
            Identify the typical key required technical skills for the job role: "{target_role}".
            List between 5 to 10 crucial skills.

            Return a valid JSON object matching this structure:
            {{
                "role_description": "Brief description of what this role does.",
                "required_skills": ["Skill 1", "Skill 2", "Skill 3", "Skill 4", "Skill 5", ...]
            }}
            Do not include markdown blocks. Return only JSON.
            """
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )
                data = json.loads(response.choices[0].message.content)
                required_skills = data.get("required_skills", [])
                role_description = data.get("role_description", "")
            except Exception as e:
                # Basic default fallback
                required_skills = ["Python", "SQL", "Git", "Problem Solving", "System Design"]
                role_description = "Standard software engineering role."
        elif not found_in_csv:
            # Fallback if no CSV and no API Key
            required_skills = ["Python", "SQL", "Git", "Problem Solving", "System Design"]
            role_description = "General Engineering Role (Mock data fallback)."

        # Calculate matches and gaps
        matching_skills = []
        missing_skills = []

        for req in required_skills:
            req_clean = req.lower().strip()
            # Check if user has it (direct match or substring)
            has_skill = False
            for user_s in user_skills_clean:
                if user_s in req_clean or req_clean in user_s:
                    has_skill = True
                    break
            if has_skill:
                matching_skills.append(req)
            else:
                missing_skills.append(req)

        # Match score calculation
        total = len(required_skills)
        match_score = int((len(matching_skills) / total) * 100) if total > 0 else 0

        # Ask Groq for structured recommendations/learning focus if API key is active
        learning_focus = []
        if self.client and missing_skills:
            prompt = f"""
            A student wants to become a "{target_role}".
            They have matching skills: {", ".join(matching_skills)}.
            They are missing skills: {", ".join(missing_skills)}.

            Suggest 3-4 specific technical learning focus areas or short projects to bridge this gap.
            Return a valid JSON object matching this structure:
            {{
                "learning_focus": ["Focus area 1 - project details", "Focus area 2 - resources", ...]
            }}
            Do not include markdown blocks. Return only JSON.
            """
            try:
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )
                data = json.loads(response.choices[0].message.content)
                learning_focus = data.get("learning_focus", [])
            except Exception:
                pass

        if not learning_focus:
            # Default fallback suggestions
            learning_focus = [
                f"Study fundamentals of {', '.join(missing_skills[:2])} via online tutorials.",
                f"Build a small portfolio project incorporating {missing_skills[0] if missing_skills else 'new tools'}.",
                "Practice relevant technical coding challenges on online assessment platforms."
            ]

        return {
            "job_role": target_role,
            "role_description": role_description,
            "required_skills": required_skills,
            "matching_skills": matching_skills,
            "missing_skills": missing_skills,
            "match_score": match_score,
            "learning_focus": learning_focus
        }