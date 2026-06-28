
# 🚀 AI Career Growth Agent

The **AI Career Growth Agent** is a Streamlit-based intelligence platform designed to guide students and fresh graduates transitioning into the tech workforce. By leveraging the **Groq API** and local datasets, the system provides automated, personalized, and interactive career consultation tools.

## 🌟 Key Features

1. **📄 Resume Analysis Agent**: Extracts tech skills, identifies strengths and structural weaknesses, computes an ATS matching score, and suggests improvements.
2. **🎯 Career Recommendation**: Matches student degree, experience level, existing skill set, and core interest topics to recommend 3 concrete matching job roles with explicit reasoning.
3. **🔍 Skill Gap Analyzer**: Compares current skills against standard requirements (loaded dynamically from local CSV databases or LLM synthesis) and displays visual radar charts of skill alignment.
4. **🎤 Interview Prep Agent**: Generates study cards for technical and behavioral questions and runs an interactive, back-and-forth **Mock Interview Simulator** chatbot that scores responses in real-time.
5. **🗺️ Career Roadmap Agent**: Maps gap skills to a month-by-month study curriculum complete with learning milestones, mini-projects, and reference links.

## 🛠️ Technology Stack
- **Frontend / Interface**: Streamlit (with custom premium glassmorphism styling)
- **Data Visualization**: Plotly (Radar charts and gauges)
- **Language Models**: 
  - **Groq API** (using `llama-3.3-70b-versatile` via `groq` SDK) for resume analysis, career recommendations, gap analysis, mock interviews, and roadmaps.
- **Data Storage**: Local CSV configuration sets
- **Document Loading**: `pypdf` and `python-docx` for document ingestion

## 📂 Project Structure
```text
AI-Career-Growth-Agent/
│
├── app.py                 # Main Streamlit UI & State controller
│
├── agents/
│   ├── resume_agent.py    # Extracts skills & scores ATS
│   ├── skill_agent.py     # Handles recommendations & gaps
│   ├── interview_agent.py # Generates QA & drives interview bot
│   └── roadmap_agent.py   # Synthesizes monthly timeline curriculums
│
├── data/
│   ├── job_roles.csv      # Baseline job roles -> required skills
│   └── skills.csv         # Autocomplete skills index
│
├── utils/
│   ├── pdf_reader.py      # PDF and DOCX text extractor
│   └── text_processor.py  # Regex text cleanups & mail/phone extractors
│
├── requirements.txt       # Dependencies
└── README.md              # Documentation
```

## ⚙️ Setup and Run Instructions

### 1. Pre-requisites
Make sure Python 3.10+ is installed on your system.

### 2. Configure environment
Ensure you have your API key set in your environment. You can configure it by creating a `.env` file in the root directory:

```env
GROQ_API_KEY="your_groq_api_key_here"
```

Alternatively, you can set it in your terminal environment:
- On Windows (PowerShell):
  ```powershell
  $env:GROQ_API_KEY="your_groq_api_key_here"
  ```
- On Linux/macOS:
  ```bash
  export GROQ_API_KEY="your_groq_api_key_here"
  ```

### 3. Run the App
Launch the Streamlit app locally:
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.
```
