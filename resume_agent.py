# agents/resume_agent.py

# pyrefly: ignore [missing-import]
from core.groq import GroqClient
# pyrefly: ignore [missing-import]
from utils.ats_score import calculate_ats_score


class ResumeAgent:
    """
    AI Resume Analysis Agent
    Extracts skills, strengths, weaknesses and career insights
    """

    def __init__(self):
        self.model_name = "gemini-1.5-flash"
        self.ai = GroqClient()


    def analyze_resume(self, text: str) -> dict:
        """
        Analyze resume content using Gemini AI
        """

        if not text.strip():
            return {
                "candidate_profile": {},
                "detected_skills": [],
                "strengths": [],
                "weaknesses": [],
                "ats_score": 100,
                "missing_skills": [],
                "recommendations": [
                    "Please upload a valid resume"
                ]
            }


        prompt = f"""
You are an expert technical recruiter.

Analyze this resume and return JSON only.

Resume:
{text}

Reference skill list to check against (mark any of these found in the resume):
Python, SQL, Java, C++, JavaScript, React, FastAPI, Flask, Django,
PyTorch, TensorFlow, Scikit-learn, Keras, Pandas, NumPy,
LangChain, LangGraph, LlamaIndex, CrewAI, AutoGen,
RAG, Vector Databases, FAISS, ChromaDB, Pinecone,
Prompt Engineering, Fine-tuning, LoRA, PEFT,
Power BI, Tableau, Excel,
Docker, Kubernetes, AWS, GCP, Azure,
Git, GitHub, CI/CD, REST APIs, MCP (Model Context Protocol),
NLP, Computer Vision, MLOps

Return:

{{
"candidate_profile": {{
"name":"",
"education":"",
"experience":""
}},

"detected_skills":[],
"strengths":[],
"weaknesses":[],
"missing_skills":[],
"recommendations":[]
}}

Rules:
- "detected_skills": list every skill from the reference list (or close variants) found anywhere in the resume text.
- "missing_skills": list important skills from the reference list NOT found in the resume, relevant to AI/Software/Data roles.
- "strengths" and "weaknesses": short bullet phrases, not empty unless resume is truly blank.
- "recommendations": 3-5 actionable suggestions to improve the resume for AI Engineering roles.
- Output valid JSON only. No markdown, no commentary, no code fences.

Focus on AI, Software Engineering and Data roles.
"""


        response = self.ai.generate(prompt)
        print("DEBUG RAW RESPONSE",response)


        ats = calculate_ats_score(
            response.get("detected_skills", [])
        )


        response["ats_score"] = ats


        return response