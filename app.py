import streamlit as st
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
import plotly.graph_objects as go
import os

# Import utility modules
from utils.pdf_reader import extract_text
from utils.text_processor import extract_email, extract_phone, clean_text

# Import backend agents
from agents.resume_agent import ResumeAgent
from agents.skill_agent import SkillAgent
from agents.interview_agent import InterviewAgent
from agents.roadmap_agent import RoadmapAgent

# Initialize agents
resume_agent = ResumeAgent()
skill_agent = SkillAgent()
interview_agent = InterviewAgent()
roadmap_agent = RoadmapAgent()

# Set page configuration
st.set_page_config(
    page_title="AI Career Growth Agent",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Custom CSS Styling for Glassmorphism and Elegant Colors
custom_css = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap');

/* Global Font Settings & Pitch Black Background */
html, body, [class*="css"], .stApp, [data-testid="stAppViewContainer"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #f8fafc;
    background-color: #000000 !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', sans-serif;
    font-weight: 600;
}

/* Sidebar Custom Styling - Pure Black */
section[data-testid="stSidebar"] {
    background-color: #050505 !important;
    border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
}

/* Custom Card Container (High Contrast Dark Slate) */
.premium-card {
    background: rgba(18, 18, 18, 0.8) !important;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.8);
}

.premium-card h3 {
    margin-top: 0px;
    color: #818cf8;
}

/* Custom Badges */
.skill-badge {
    display: inline-block;
    padding: 6px 12px;
    margin: 4px;
    background: rgba(99, 102, 241, 0.15);
    color: #818cf8;
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
}

.missing-badge {
    display: inline-block;
    padding: 6px 12px;
    margin: 4px;
    background: rgba(239, 68, 68, 0.1);
    color: #f87171;
    border: 1px solid rgba(239, 68, 68, 0.25);
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
}

.matching-badge {
    display: inline-block;
    padding: 6px 12px;
    margin: 4px;
    background: rgba(16, 185, 129, 0.1);
    color: #34d399;
    border: 1px solid rgba(16, 185, 129, 0.25);
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
}

/* Gradient text utility */
.gradient-text {
    background: linear-gradient(90deg, #818cf8, #a855f7);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-weight: 700;
}

/* Styled Timeline container */
.timeline-card {
    border-left: 3px solid #818cf8;
    padding-left: 20px;
    margin-left: 10px;
    margin-bottom: 25px;
    position: relative;
}

.timeline-dot {
    height: 12px;
    width: 12px;
    background-color: #818cf8;
    border-radius: 50%;
    position: absolute;
    left: -8px;
    top: 5px;
    box-shadow: 0 0 8px #818cf8;
}

/* Premium Black Button with Neon Indigo Glow and Hover Scaling */
div.stButton > button {
    background: #000000 !important;
    color: #ffffff !important;
    border-radius: 12px !important;
    border: 1.5px solid #818cf8 !important;
    font-weight: 600 !important;
    padding: 10px 24px !important;
    transition: all 0.3s ease-in-out !important;
    box-shadow: 0 0 15px rgba(129, 140, 248, 0.2) !important;
}

div.stButton > button:hover {
    background: linear-gradient(135deg, #818cf8 0%, #6366f1 100%) !important;
    color: #000000 !important;
    border: 1.5px solid #818cf8 !important;
    box-shadow: 0 0 25px rgba(129, 140, 248, 0.6) !important;
    transform: translateY(-2px) !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.markdown("""
<div style="
text-align:center;
padding:20px;
">
<h1 class="gradient-text">
🤖 AI Career Growth Agent
</h1>

<p style="color:#94a3b8;font-size:18px;">
AI-powered Resume Analysis • Skill Intelligence • Career Planning
</p>

</div>
""", unsafe_allow_html=True)
# Helper to load autocomplete options
@st.cache_data
def get_autocomplete_options():
    skills_file = os.path.join("data", "skills.csv")
    roles_file = os.path.join("data", "job_roles.csv")
    
    skills = []
    roles = []
    
    if os.path.exists(skills_file):
        try:
            df = pd.read_csv(skills_file)
            skills = df["Skill"].tolist()
        except:
            pass
    if os.path.exists(roles_file):
        try:
            df = pd.read_csv(roles_file)
            roles = df["Role"].tolist()
        except:
            pass
    return skills, roles

skills_list, roles_list = get_autocomplete_options()

# Sidebar Setup
st.sidebar.markdown(
    "<h1 style='text-align: center; margin-bottom: 0px;'>🚀 Career Growth</h1>"
    "<p style='text-align: center; color: #818cf8; font-size: 14px; margin-top: 0px;'>Personalized AI Agents</p>",
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Select Feature Agent",
    [
        "📄 Resume Analysis Agent",
        "🎯 Career Recommendation",
        "🔍 Skill Gap Analyzer",
        "🎤 Interview Prep Agent",
        "🗺️ Career Roadmap Agent"
    ]
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div style='font-size: 12px; color: #64748b; text-align: center;'>"
    "Powered by Groq API<br>Standard Model: llama-3.3-70b-versatile"
    "</div>",
    unsafe_allow_html=True
)

# ----------------- PAGE 1: RESUME ANALYSIS AGENT -----------------
if page == "📄 Resume Analysis Agent":
    st.markdown("<h1>📄 Resume Analysis Agent</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 16px; color: #94a3b8;'>Upload your resume (PDF or DOCX) to get a full analysis: skills breakdown, strengths, weaknesses, and a numeric ATS match score.</p>", unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload Resume Document", type=["pdf", "docx"])
    
    if uploaded_file is not None:
        with st.spinner("Extracting content and running AI Resume screening..."):
            # Extract Text
            try:
                raw_text = extract_text(uploaded_file, uploaded_file.name)
                # Extract simple contact tags
                email = extract_email(raw_text)
                phone = extract_phone(raw_text)
                
                # Analyze with Agent
                analysis = resume_agent.analyze_resume(raw_text)
                
                # Setup columns for visualizations
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
                    st.subheader("Candidate Information")
                    st.write(f"**Filename:** {uploaded_file.name}")
                    st.write(f"**Email:** {email}")
                    st.write(f"**Phone:** {phone}")
                    
                    # Create Gauge Chart for ATS Score
                    ats_score = analysis.get("ats_score", 0)
                    fig = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = ats_score,
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "ATS Score", 'font': {'size': 20, 'family': 'Outfit'}},
                        gauge = {
                            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#475569"},
                            'bar': {'color': "#6366f1"},
                            'bgcolor': "rgba(30, 41, 59, 0.5)",
                            'borderwidth': 2,
                            'bordercolor': "#475569",
                            'steps': [
                                {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.2)'},
                                {'range': [50, 75], 'color': 'rgba(245, 158, 11, 0.2)'},
                                {'range': [75, 100], 'color': 'rgba(16, 185, 129, 0.2)'}
                            ]
                        }
                    ))
                    fig.update_layout(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)',
                        font={'color': "#f8fafc"},
                        height=250,
                        margin=dict(l=10, r=10, t=40, b=10)
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    st.markdown("</div>", unsafe_allow_html=True)

                with col2:
                    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
                    st.subheader("Skills Categorization")
                    
                    st.write("**Detected Skills:**")
                    detected_skills = analysis.get("detected_skills", [])
                    if detected_skills:
                        badge_html = "".join([f"<span class='matching-badge'>✓ {s}</span>" for s in detected_skills])
                        st.markdown(badge_html, unsafe_allow_html=True)
                    else:
                        st.write("*No distinct skills detected.*")
                    
                    st.write("<br>**Industry Skill Gaps (Standard recommendations):**", unsafe_allow_html=True)
                    missing_skills = analysis.get("missing_skills", [])
                    if missing_skills:
                        badge_html = "".join([f"<span class='missing-badge'>✗ {s}</span>" for s in missing_skills])
                        st.markdown(badge_html, unsafe_allow_html=True)
                    else:
                        st.write("*No major skill gaps identified.*")
                    st.markdown("</div>", unsafe_allow_html=True)

                # Extended Feedback Sections
                st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
                st.subheader("Detailed Evaluation & Strengths")
                st.markdown("**Core Strengths:**")
                for strength in analysis.get("strengths", []):
                    st.write(f"- {strength}")
                
                st.markdown("<br>**Areas of Weakness:**", unsafe_allow_html=True)
                for weakness in analysis.get("weaknesses", []):
                    st.write(f"- {weakness}")
                
                st.markdown("<br>**Actionable Recommendations:**", unsafe_allow_html=True)
                for rec in analysis.get("recommendations", []):
                    st.write(f"💡 {rec}")
                st.markdown("</div>", unsafe_allow_html=True)
                
            except Exception as e:
                st.error(f"Error analyzing document: {e}")

# ----------------- PAGE 2: CAREER RECOMMENDATION -----------------
elif page == "🎯 Career Recommendation":
    st.markdown("<h1>🎯 Career Recommendation Agent</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 16px; color: #94a3b8;'>Enter details about your academic and vocational background to get tailored professional role suggestions.</p>", unsafe_allow_html=True)

    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        degree = st.text_input("Highest Degree / Major", placeholder="e.g. Bachelor of Computer Applications")
        user_skills = st.multiselect("Your Current Skills", options=skills_list if skills_list else ["Python", "SQL", "HTML/CSS"])
    with col2:
        experience = st.text_input("Years/Type of Experience", placeholder="e.g. 1 year internship / Fresher")
        interests = st.text_area("Your Core Interests & Goals", placeholder="e.g. I want to build AI systems, work in web backend, or analyze data patterns.")
        
    submit = st.button("Generate Career Suggestions")
    st.markdown("</div>", unsafe_allow_html=True)

    if submit:
        if not degree or not user_skills:
            st.warning("Please fill in your Degree and select at least one skill to generate recommendations.")
        else:
            with st.spinner("Analyzing candidate profile and cross-referencing market demands..."):
                recommendations = skill_agent.recommend_roles(degree, user_skills, experience, interests)
                
                st.markdown("<h3>Recommended Career Paths</h3>", unsafe_allow_html=True)
                for index, item in enumerate(recommendations.get("roles", [])):
                    st.markdown(f"""
                    <div class='premium-card'>
                        <h4 style='color: #818cf8; margin-top: 0px;'>{index + 1}. {item.get('role')}</h4>
                        <p style='color: #cbd5e1; font-size: 15px;'>{item.get('reason')}</p>
                    </div>
                    """, unsafe_allow_html=True)

# ----------------- PAGE 3: SKILL GAP ANALYZER -----------------
elif page == "🔍 Skill Gap Analyzer":
    st.markdown("<h1>🔍 Skill Gap Analyzer Agent</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 16px; color: #94a3b8;'>Compare your skills against a target job role to visualize your profile match and discover specific gap items.</p>", unsafe_allow_html=True)

    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        target_role = st.selectbox("Select Target Role", options=roles_list if roles_list else ["AI Engineer", "Machine Learning Engineer", "Backend Developer"])
    with col2:
        user_skills = st.multiselect("Enter Your Current Skills", options=skills_list if skills_list else ["Python", "SQL"])
        
    submit = st.button("Analyze Gaps")
    st.markdown("</div>", unsafe_allow_html=True)

    if submit:
        with st.spinner("Calculating skill overlap score..."):
            gap_data = skill_agent.analyze_skill_gap(user_skills, target_role)
            
            col_graph, col_stats = st.columns([1, 1])
            
            with col_graph:
                st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
                st.subheader("Profile Overlap Radar")
                
                required = gap_data["required_skills"]
                user_has = [1 if r in gap_data["matching_skills"] else 0 for r in required]
                ideal = [1 for _ in required]
                
                # Plotly Radar Chart
                fig = go.Figure()
                fig.add_trace(go.Scatterpolar(
                    r=user_has,
                    theta=required,
                    fill='toself',
                    name='Your Skills',
                    line_color='#6366f1'
                ))
                fig.add_trace(go.Scatterpolar(
                    r=ideal,
                    theta=required,
                    fill='toself',
                    name='Job Requirement',
                    line_color='rgba(255,255,255,0.2)'
                ))
                
                fig.update_layout(
                    polar=dict(
                        radialaxis=dict(visible=False, range=[0, 1]),
                        angularaxis=dict(color="#f8fafc", gridcolor="rgba(255,255,255,0.1)")
                    ),
                    showlegend=True,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font={'color': "#f8fafc"},
                    margin=dict(l=30, r=30, t=30, b=30),
                    height=300
                )
                st.plotly_chart(fig, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)
                
            with col_stats:
                st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
                st.subheader("Match Breakdown")
                st.markdown(f"Job Description: *{gap_data['role_description']}*")
                st.markdown(f"**Match Score: {gap_data['match_score']}%**")
                
                st.write("**Matching Skills:**")
                if gap_data["matching_skills"]:
                    st.markdown("".join([f"<span class='matching-badge'>{s}</span>" for s in gap_data["matching_skills"]]), unsafe_allow_html=True)
                else:
                    st.write("*None*")
                    
                st.write("<br>**Missing Skills / Gaps:**", unsafe_allow_html=True)
                if gap_data["missing_skills"]:
                    st.markdown("".join([f"<span class='missing-badge'>{s}</span>" for s in gap_data["missing_skills"]]), unsafe_allow_html=True)
                else:
                    st.write("*Profile 100% matched!*")
                st.markdown("</div>", unsafe_allow_html=True)
                
            # Suggested learning list
            st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
            st.subheader("Actionable Learning Suggestions")
            for item in gap_data["learning_focus"]:
                st.markdown(f"- {item}")
            st.markdown("</div>", unsafe_allow_html=True)

            # Save gaps in session state for roadmap page convenience
            st.session_state["gap_skills"] = gap_data["missing_skills"]
            st.session_state["user_skills"] = user_skills
            st.session_state["target_role"] = target_role

# ----------------- PAGE 4: INTERVIEW PREPARATION -----------------
elif page == "🎤 Interview Prep Agent":
    st.markdown("<h1>🎤 Interview Preparation Agent</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 16px; color: #94a3b8;'>Study tailored questions and test yourself with our interactive AI interview simulation panel.</p>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["📚 Study Q&A Preparation", "💬 Interactive Mock Interview"])
    
    with tab1:
        st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            prep_role = st.selectbox("Select Target Job Role", options=roles_list if roles_list else ["AI Engineer", "Data Analyst"], key="prep_role")
        with col2:
            prep_level = st.selectbox("Experience Level", options=["Junior", "Mid", "Senior"], key="prep_level")
        submit_prep = st.button("Generate Prep Material")
        st.markdown("</div>", unsafe_allow_html=True)
        
        if submit_prep:
            with st.spinner("Generating typical interview questions..."):
                materials = interview_agent.generate_qa_prep(prep_role, prep_level)
                
                for idx, qa in enumerate(materials.get("prep_materials", [])):
                    with st.expander(f"Question {idx + 1} ({qa.get('type')}): {qa.get('question')}"):
                        st.markdown(f"**Model Answer:**\n{qa.get('model_answer')}")
                        st.markdown(f"**Recruiter Tip:**\n*{qa.get('tips')}*")
                        
    with tab2:
        st.subheader("Live Recruiter Chatbot")
        st.write("Start an interactive chat-based interview simulator. The interviewer will ask a question, you provide an answer, and the AI evaluates your response before asking the next question.")
        
        # Setup session states for mock interview
        if "chat_history" not in st.session_state:
            st.session_state["chat_history"] = []
        if "interview_active" not in st.session_state:
            st.session_state["interview_active"] = False
        if "current_question_num" not in st.session_state:
            st.session_state["current_question_num"] = 0
        if "assessment_report" not in st.session_state:
            st.session_state["assessment_report"] = None
        if "active_interview_role" not in st.session_state:
            st.session_state["active_interview_role"] = ""
        if "active_interview_level" not in st.session_state:
            st.session_state["active_interview_level"] = ""

        if not st.session_state["interview_active"]:
            st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
            col_a, col_b = st.columns(2)
            with col_a:
                role_input = st.selectbox("Select Role to Mock", options=roles_list if roles_list else ["AI Engineer"], key="mock_role")
            with col_b:
                level_input = st.selectbox("Select Level to Mock", options=["Junior", "Mid", "Senior"], key="mock_level")
            
            if st.button("Start Interview Session"):
                st.session_state["chat_history"] = [
                    {"role": "assistant", "content": f"Hello! Welcome to your mock technical interview for the {role_input} ({level_input}) role. I will be your AI interviewer today. Let's start with the first question: Can you describe a recent project you built, and what tools or technologies you chose for it?"}
                ]
                st.session_state["interview_active"] = True
                st.session_state["current_question_num"] = 1
                st.session_state["assessment_report"] = None
                st.session_state["active_interview_role"] = role_input
                st.session_state["active_interview_level"] = level_input
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"**Current Interview:** {st.session_state['active_interview_role']} ({st.session_state['active_interview_level']})")
            
            # Display Chat Messages
            for chat in st.session_state["chat_history"]:
                role = "assistant" if chat["role"] == "assistant" else "user"
                with st.chat_message(role):
                    st.write(chat["content"])
            
            # Render evaluation scorecard if concluded
            if st.session_state["assessment_report"]:
                st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
                report = st.session_state["assessment_report"]
                st.markdown(f"<h3>Interview Concluded! Overall Score: {report.get('score', 0)}/100</h3>", unsafe_allow_html=True)
                
                col_st, col_im = st.columns(2)
                with col_st:
                    st.markdown("**Key Strengths:**")
                    for stg in report.get("strengths", []):
                        st.write(f"✓ {stg}")
                with col_im:
                    st.markdown("**Key Focus Improvements:**")
                    for imp in report.get("improvements", []):
                        st.write(f"💡 {imp}")
                
                st.markdown("</div>", unsafe_allow_html=True)
                if st.button("Reset Interview"):
                    st.session_state["interview_active"] = False
                    st.session_state["chat_history"] = []
                    st.session_state["current_question_num"] = 0
                    st.session_state["assessment_report"] = None
                    st.rerun()
            else:
                user_ans = st.chat_input("Type your response here...")
                if user_ans:
                    # Append user message
                    st.session_state["chat_history"].append({"role": "user", "content": user_ans})
                    
                    with st.spinner("Interviewer is evaluating and formulating next question..."):
                        # Get AI response
                        result = interview_agent.conduct_mock_interview(
                            history=st.session_state["chat_history"][:-1],
                            user_message=user_ans,
                            job_role=st.session_state["active_interview_role"],
                            level=st.session_state["active_interview_level"]
                        )
                        
                        # Add feedback and next question to chat history
                        feedback = result.get("feedback", "")
                        next_q = result.get("next_question", "")
                        
                        assistant_response = f"**Feedback:** {feedback}\n\n**Next Question:** {next_q}"
                        if result.get("is_concluded") or next_q == "CONCLUDED":
                            assistant_response = f"**Feedback:** {feedback}\n\n**Interview Concluded.** Generating final report card..."
                            st.session_state["assessment_report"] = result.get("assessment", {})
                            
                        st.session_state["chat_history"].append({"role": "assistant", "content": assistant_response})
                        st.session_state["current_question_num"] += 1
                        st.rerun()

# ----------------- PAGE 5: CAREER ROADMAP GENERATOR -----------------
elif page == "🗺️ Career Roadmap Agent":
    st.markdown("<h1>🗺️ Career Roadmap Agent</h1>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 16px; color: #94a3b8;'>Receive a month-by-month structured curriculum complete with milestones, project suggestions, and reference URLs to bridge your skill gap.</p>", unsafe_allow_html=True)

    # Pull defaults from session state if available from skill gap page
    default_role = st.session_state.get("target_role", "")
    default_gaps = st.session_state.get("gap_skills", [])
    default_skills = st.session_state.get("user_skills", [])
    default_gaps = [g for g in default_gaps if g in skills_list] if skills_list else []
    

    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        target_role = st.text_input("Target Role", value=default_role if default_role else "Machine Learning Engineer")
        user_skills_input = st.multiselect("Your Current Skills", options=skills_list if skills_list else ["Python"], default=default_skills)
    with col2:
        gap_skills_input = st.multiselect("Gap Skills to Cover", options=skills_list if skills_list else ["TensorFlow", "Docker"], default=default_gaps)
    with col3:
        duration = st.slider("Duration (Months)", min_value=1, max_value=6, value=3)
        
    submit = st.button("Generate Roadmap Plan")
    st.markdown("</div>", unsafe_allow_html=True)

    if submit:
        if not target_role:
            st.warning("Please specify a target role.")
        else:
            with st.spinner("Synthesizing learning path roadmap with milestones..."):
                roadmap_data = roadmap_agent.generate_roadmap(
                    user_skills=user_skills_input,
                    target_role=target_role,
                    gap_skills=gap_skills_input,
                    duration_months=duration
                )
                
                st.markdown("<h3>Study Timeline & Schedule</h3>", unsafe_allow_html=True)
                
                for idx, month in enumerate(roadmap_data.get("roadmap", [])):
                    st.markdown(f"""
                    <div class='timeline-card'>
                        <div class='timeline-dot'></div>
                        <h4 style='color: #818cf8; margin-top: 0px;'>{month.get('period')}</h4>
                        <p style='color: #94a3b8; font-weight: 500;'>Milestone: {month.get('milestone')}</p>
                        <div style='margin-bottom: 10px;'>
                    """, unsafe_allow_html=True)
                    
                    st.write("**Topics to Master:**")
                    topic_html = "".join([f"<span class='skill-badge'>{t}</span>" for t in month.get("topics", [])])
                    st.markdown(topic_html, unsafe_allow_html=True)
                    
                    st.write("<br>**Milestone Tasks & Action Items:**", unsafe_allow_html=True)
                    for action in month.get("action_items", []):
                        st.write(f"- {action}")
                        
                    st.write("<br>**Suggested Learning References:**", unsafe_allow_html=True)
                    for res in month.get("resources", []):
                        name = res.get("name")
                        url = res.get("url")
                        st.markdown(f"- [{name}]({url})")
                        
                    st.markdown("</div></div>", unsafe_allow_html=True)
