import streamlit as st
from io import BytesIO
from pypdf import PdfReader
from docx import Document
from matcher import analyze_match
from auth_db import (
    init_db,
    create_user,
    authenticate_user,
    get_profile,
    update_profile,
    save_analysis,
    get_history,
)
from ats_checker import analyze_ats

# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="HireMatch | AI Career Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Create the local database tables if they do not exist yet.
init_db()

if "user" not in st.session_state:
    st.session_state["user"] = None


# --------------------------------------------------
# Custom styling
# --------------------------------------------------

st.markdown(
    """
    <style>
    .stApp {
        background-color: #0b1020;
        color: #f3f4f6;
    }

    [data-testid="stSidebar"] {
        background-color: #11182b;
        border-right: 1px solid #26314a;
    }

    .hero {
        padding: 28px;
        border: 1px solid #344264;
        border-radius: 20px;
        background: linear-gradient(
            135deg,
            #182444 0%,
            #11182b 65%,
            #19243b 100%
        );
        margin-bottom: 24px;
    }

    .hero h1 {
        font-size: 2.7rem;
        color: #ffffff;
        margin-bottom: 8px;
    }

    .hero p {
        color: #c5cde0;
        font-size: 1.05rem;
        line-height: 1.7;
        max-width: 780px;
    }

    /* Polished authentication surface */
    div[data-testid="stTabs"] button[role="tab"] {
        font-weight: 650;
        padding: 12px 18px;
    }
    div[data-testid="stForm"] {
        background: linear-gradient(145deg, rgba(24,36,68,.82), rgba(17,24,43,.96));
        border: 1px solid #344264;
        border-radius: 18px;
        padding: 24px 24px 18px 24px;
    }
    div[data-testid="stTextInput"] label {
        color: #e4e9f7;
        font-weight: 600;
    }
    div[data-testid="stTextInput"] input {
        background: #0d1426;
        border: 1px solid #394766;
        border-radius: 10px;
        min-height: 44px;
    }
    div[data-testid="stTextInput"] input:focus {
        border-color: #8b7cff;
        box-shadow: 0 0 0 1px #8b7cff;
    }

    .section-card {
        padding: 20px;
        border: 1px solid #2c3854;
        border-radius: 16px;
        background-color: #11182b;
        margin-bottom: 18px;
    }

    .muted {
        color: #a9b4cc;
    }

    div.stButton > button[kind="primary"] {
        background-color: #7c6cff;
        border: none;
        color: white;
        border-radius: 10px;
        min-height: 48px;
        font-weight: 600;
    }

    div.stButton > button[kind="primary"]:hover {
        background-color: #6655ef;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Login and registration gate
# --------------------------------------------------

if st.session_state.get("user") is None:
    st.markdown(
        """
        <div class="hero">
            <h1>🎯 Welcome to HireMatch</h1>
            <p>Your next opportunity starts with a stronger application. Sign in to
            compare your resume with a role, discover skill gaps, build a learning
            roadmap, and review your ATS readiness in one workspace.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    auth_left, auth_main, auth_right = st.columns([1, 2.2, 1])
    with auth_main:
        st.markdown("### Your career workspace")
        st.caption("Secure access to your profile, match results, and saved analysis history.")
        login_tab, register_tab = st.tabs(["Sign in", "Create account"])

        with login_tab:
            with st.form("login_form"):
                login_email = st.text_input("Email address", key="login_email")
                login_password = st.text_input(
                    "Password", type="password", key="login_password"
                )
                login_submitted = st.form_submit_button(
                    "Sign in", type="primary", use_container_width=True
                )

            if login_submitted:
                user = authenticate_user(login_email.strip(), login_password)
                if user:
                    st.session_state["user"] = user
                    st.session_state["current_page"] = "Home"
                    st.rerun()
                else:
                    st.error("Email or password was not recognized.")
                    st.caption(
                        "Accounts are stored in the database used by this running instance. "
                        "If you registered before a redeploy/restart, the deployment may be "
                        "using a fresh temporary database. Use persistent storage for accounts "
                        "or create the account again on this instance."
                    )

        with register_tab:
            with st.form("register_form"):
                register_name = st.text_input("Full name", key="register_name")
                register_email = st.text_input("Email address", key="register_email")
                register_password = st.text_input(
                    "Password (at least 8 characters)",
                    type="password",
                    key="register_password",
                )
                confirm_password = st.text_input(
                    "Confirm password", type="password", key="confirm_password"
                )
                register_submitted = st.form_submit_button(
                    "Create account", type="primary", use_container_width=True
                )

            if register_submitted:
                if register_password != confirm_password:
                    st.error("The passwords do not match.")
                else:
                    created, message = create_user(
                        register_email.strip(), register_password, register_name.strip()
                    )
                    if created:
                        user = authenticate_user(
                            register_email.strip(), register_password
                        )
                        if user:
                            st.session_state["user"] = user
                            st.session_state["current_page"] = "Home"
                            st.success("Account created. You are now signed in.")
                            st.rerun()
                        else:
                            st.success(message)
                    else:
                        st.error(message)

    st.caption(
        "Your account stores profile details and analysis summaries. "
        "Avoid uploading sensitive personal information you do not need to analyze."
    )
    st.stop()


# --------------------------------------------------
# Sidebar Navigation
# --------------------------------------------------

with st.sidebar:
    st.markdown("## 🎯 HireMatch")
    st.caption("Your AI-powered career companion")
    st.divider()

    st.markdown("### Navigation")

    if st.button("🏠 Home", use_container_width=True):
        st.session_state["current_page"] = "Home"

    if st.button("🧩 Skill Match", use_container_width=True):
        st.session_state["current_page"] = "Skill Match"

    if st.button("🗺️ Learning Roadmap", use_container_width=True):
        st.session_state["current_page"] = "Learning Roadmap"

    if st.button("⚙️ How It Works", use_container_width=True):
        st.session_state["current_page"] = "How It Works"

    if st.button("✨ Features", use_container_width=True):
        st.session_state["current_page"] = "Features"

    if st.button("💜 About", use_container_width=True):
        st.session_state["current_page"] = "About"

    st.divider()
    st.markdown("### Your account")
    signed_in_user = st.session_state.get("user") or {}
    st.caption(signed_in_user.get("full_name") or signed_in_user.get("email", "Signed in"))

    if st.button("👤 My Profile", use_container_width=True):
        st.session_state["current_page"] = "My Profile"

    if st.button("🕘 Analysis History", use_container_width=True):
        st.session_state["current_page"] = "Analysis History"

    if st.button("🧾 ATS Checker", use_container_width=True):
        st.session_state["current_page"] = "ATS Checker"

    if st.button("🚪 Sign out", use_container_width=True):
        st.session_state["user"] = None
        st.session_state.pop("hirematch_result", None)
        st.session_state.pop("hirematch_ats_result", None)
        st.session_state["current_page"] = "Home"
        st.rerun()

    st.divider()
    st.caption("HireMatch • Career development assistant")

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Home"



# --------------------------------------------------
# Page Routing: Informational Pages
# --------------------------------------------------

current_page = st.session_state["current_page"]


# --------------------------------------------------
# MY PROFILE PAGE
# --------------------------------------------------

if current_page == "My Profile":
    st.markdown("## 👤 My Profile")
    st.caption("Keep your career details together in one place.")

    current_user = st.session_state.get("user") or {}
    user_id = current_user.get("id", current_user.get("user_id"))
    profile = get_profile(user_id) if user_id is not None else None
    profile = profile or current_user

    with st.form("profile_form"):
        full_name = st.text_input(
            "Full name", value=profile.get("full_name", "") or ""
        )
        headline = st.text_input(
            "Professional headline",
            value=profile.get("headline", "") or "",
            placeholder="e.g. B.Tech student | Aspiring ML Engineer",
        )
        education = st.text_input(
            "Education", value=profile.get("education", "") or "",
            placeholder="e.g. B.Tech in Computer Science",
        )
        target_role = st.text_input(
            "Target role", value=profile.get("target_role", "") or "",
            placeholder="e.g. Machine Learning Intern",
        )
        skills = st.text_input(
            "Skills (comma-separated)",
            value=profile.get("skills", "") or "",
            placeholder="Python, SQL, machine learning",
        )
        experience_level = st.selectbox(
            "Experience level",
            ["Student", "Entry level", "Internship", "Experienced", "Career switcher"],
            index=(
                ["Student", "Entry level", "Internship", "Experienced", "Career switcher"].index(
                    profile.get("experience_level")
                )
                if profile.get("experience_level") in [
                    "Student", "Entry level", "Internship", "Experienced", "Career switcher"
                ] else 0
            ),
        )
        bio = st.text_area(
            "About you",
            value=profile.get("bio", "") or "",
            placeholder="Briefly describe your interests, projects, and career goals.",
        )
        profile_submitted = st.form_submit_button(
            "Save profile", type="primary", use_container_width=True
        )

    if profile_submitted:
        if user_id is None:
            st.error("Could not identify your account. Please sign in again.")
        else:
            update_profile(
                user_id, full_name.strip(), headline.strip(), education.strip(),
                target_role.strip(), skills.strip(), experience_level, bio.strip()
            )
            refreshed = get_profile(user_id)
            if refreshed:
                st.session_state["user"] = refreshed
            st.success("Your profile has been saved.")

    st.info("Only enter professional details you are comfortable storing in this app.")
    st.stop()


# --------------------------------------------------
# ANALYSIS HISTORY PAGE
# --------------------------------------------------

elif current_page == "Analysis History":
    st.markdown("## 🕘 Analysis History")
    st.caption("Your latest saved analysis summaries.")

    current_user = st.session_state.get("user") or {}
    user_id = current_user.get("id", current_user.get("user_id"))
    history = get_history(user_id, limit=30) if user_id is not None else []

    if not history:
        st.info("No saved analyses yet. Run an analysis from Home to see it here.")
    else:
        for item in history:
            with st.container(border=True):
                st.markdown(
                    f"**{item.get('job_title') or 'Target role'}**"
                )
                date_value = item.get("created_at", "")
                st.caption(f"Saved: {date_value}")
                col1, col2 = st.columns(2)
                semantic_score = item.get("semantic_score")
                ats_score = item.get("ats_score")
                col1.metric(
                    "Semantic match",
                    f"{float(semantic_score):.1f}%"
                    if semantic_score is not None else "Unavailable",
                )
                col2.metric(
                    "ATS readiness",
                    f"{float(ats_score):.0f}/100"
                    if ats_score is not None else "Unavailable",
                )
                st.write("Matched skills:", item.get("matched_skills") or "None recorded")
                st.write("Skills to develop:", item.get("missing_skills") or "None recorded")

    st.caption("The history stores summary data, not the original resume text.")
    st.stop()


# --------------------------------------------------
# ATS CHECKER PAGE
# --------------------------------------------------

elif current_page == "ATS Checker":
    st.markdown("## 🧾 ATS Resume Checker")
    st.caption("Run a basic formatting and content checklist on resume text.")

    ats_resume_text = st.text_area(
        "Paste resume text",
        height=280,
        key="ats_resume_input",
        placeholder="Paste selectable text from your resume here...",
    )

    if st.button("Check ATS readiness", type="primary", use_container_width=True):
        if not ats_resume_text.strip():
            st.warning("Paste resume text before running the checker.")
        else:
            st.session_state["standalone_ats_result"] = analyze_ats(ats_resume_text)

    standalone_result = st.session_state.get("standalone_ats_result")
    if standalone_result:
        ats_score = standalone_result.get("score", standalone_result.get("ats_score"))
        checks = standalone_result.get("checks", [])
        if ats_score is not None:
            score_value = float(ats_score)
            score_col, status_col, checks_col = st.columns([1, 1.4, 1])
            with score_col:
                st.metric("ATS readiness", f"{score_value:.0f}/100")
                st.progress(max(0.0, min(1.0, score_value / 100)))
            with status_col:
                if score_value >= 80:
                    st.success("Strong checklist coverage")
                    st.caption("Keep tailoring your resume to each role.")
                elif score_value >= 60:
                    st.info("Good start — some improvements needed")
                    st.caption("Prioritize the failed high-value checks.")
                else:
                    st.warning("Needs improvement")
                    st.caption("Start with contact details and core sections.")
            with checks_col:
                st.metric("Checks passed", f"{standalone_result.get('passed_count', 0)} / {standalone_result.get('total_checks', len(checks))}")
                st.caption("Points are weighted by checklist importance.")

        st.markdown("#### Checklist breakdown")
        if checks:
            import pandas as pd
            table_rows = [{
                "Check": item.get("label", "Resume check"),
                "Result": "Pass" if item.get("passed") else "Needs attention",
                "Weight": f"{item.get('points', 0)} pts",
                "Recommendation / evidence": item.get("feedback", ""),
            } for item in checks]
            st.dataframe(
                pd.DataFrame(table_rows),
                hide_index=True,
                use_container_width=True,
                column_config={
                    "Check": st.column_config.TextColumn("Check", width="medium"),
                    "Result": st.column_config.TextColumn("Result", width="small"),
                    "Weight": st.column_config.TextColumn("Weight", width="small"),
                    "Recommendation / evidence": st.column_config.TextColumn("Recommendation / evidence", width="large"),
                },
            )
            with st.expander("Show only items to improve"):
                failed = [item for item in checks if not item.get("passed")]
                if failed:
                    for item in failed:
                        st.markdown(f"**{item.get('label')}** · {item.get('points', 0)} weighted points")
                        st.write(item.get("feedback", ""))
                else:
                    st.success("All checks in this checklist passed.")

        st.caption(
            standalone_result.get(
                "disclaimer",
                "This is a basic heuristic checklist, not a guarantee that an ATS will accept or rank a resume."
            )
        )

    st.stop()


# --------------------------------------------------
# ABOUT PAGE
# --------------------------------------------------

if current_page == "About":

    st.markdown("## 💜 About HireMatch")
    st.caption("Understand your skills. Discover your next steps.")

    st.markdown(
        """
        <div style="
            padding: 30px;
            border-radius: 18px;
            background: linear-gradient(135deg, #211b3b, #172b43);
            border: 1px solid #49416e;
            margin: 12px 0 24px 0;
        ">
            <h1 style="margin: 0; color: #ffffff;">
                Your career journey, <span style="color: #b9a2ff;">
                made clearer.</span>
            </h1>
            <p style="font-size: 16px; color: #d6d6e7; line-height: 1.8;">
                HireMatch is a resume and job-description analysis
                assistant designed to help you understand how your
                current skills align with a target role and where
                you could focus your learning next.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🎯 Why HireMatch?")
    st.write(
        "Job descriptions can be difficult to interpret, and it is "
        "not always obvious which skills you already demonstrate or "
        "which ones you may want to develop. HireMatch brings that "
        "information together in one place."
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### 🧭 Find direction")
        st.write(
            "Compare the skills mentioned in your resume with those "
            "listed in a target job description."
        )

    with col2:
        st.markdown("#### 🌱 Plan your growth")
        st.write(
            "Use identified skill gaps to explore topics, learning "
            "resources, and practical next steps."
        )

    st.divider()
    st.markdown("### 💡 Our approach")

    st.markdown("""
    - **Clarity:** present relevant skill information in an understandable format.
    - **Practical learning:** turn skill gaps into actionable learning goals.
    - **User control:** let you provide resume text and choose the job you want to explore.
    - **Continuous improvement:** support your career preparation as your skills grow.
    """)

    st.info(
        "Important: A match score is an estimate based on the "
        "application's matching method. It is not a hiring decision "
        "or a guarantee of interview selection."
    )

    st.markdown("### 🚀 Your next step")
    st.write(
        "Start with a resume and a job description. Review the "
        "comparison, then use your results to plan what to learn next."
    )

    if st.button("Go to Home", use_container_width=False):
        st.session_state["current_page"] = "Home"
        st.rerun()

    st.stop()


# --------------------------------------------------
# FEATURES PAGE
# --------------------------------------------------

elif current_page == "Features":

    st.markdown("## ✨ Explore HireMatch Features")
    st.caption("Everything in one place to support your job preparation.")

    st.markdown(
        """
        <div style="
            padding: 22px;
            border-radius: 16px;
            background: linear-gradient(135deg, #211b3b, #172b43);
            border: 1px solid #49416e;
            margin-bottom: 22px;
        ">
            <h2 style="color: white; margin-top: 0;">
                From resume to learning plan
            </h2>
            <p style="color: #d6d6e7; line-height: 1.7;">
                Explore your current skills, understand a role's
                requirements, and identify possible areas for growth.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    feature_col1, feature_col2 = st.columns(2, gap="large")

    with feature_col1:
        with st.container(border=True):
            st.markdown("### 📄 Resume input")
            st.write(
                "Upload a supported PDF or DOCX resume, or paste "
                "your resume text manually."
            )
            st.caption("Purpose: provide the skills and experience to analyze.")

        with st.container(border=True):
            st.markdown("### 🎯 Skill matching")
            st.write(
                "Compare skills found in your resume with skills "
                "identified in the target job description."
            )
            st.caption("Purpose: understand your current alignment with a role.")

        with st.container(border=True):
            st.markdown("### ✅ Matched skills")
            st.write(
                "Review skills that appear in both your resume and "
                "the target job description."
            )
            st.caption("Purpose: recognize relevant experience you already show.")

    with feature_col2:
        with st.container(border=True):
            st.markdown("### 🧩 Skill gaps")
            st.write(
                "Identify job-related skills mentioned in the "
                "description that were not detected in your resume."
            )
            st.caption(
                "Tip: a missing skill may be absent from your resume "
                "or simply not recognized by the current matcher."
            )

        with st.container(border=True):
            st.markdown("### 🗺️ Learning roadmap")
            st.write(
                "Explore suggested topics, resources, and practice "
                "activities associated with skills you want to develop."
            )
            st.caption("Purpose: turn a skill gap into a learning goal.")

        with st.container(border=True):
            st.markdown("### 📊 Match overview")
            st.write(
                "Review the application's match percentage alongside "
                "the individual matched and missing skills."
            )
            st.caption(
                "The percentage is an indicator, not a prediction "
                "of hiring success."
            )

    st.divider()
    st.markdown("### 🔄 A simple workflow")

    step1, step2, step3 = st.columns(3)

    with step1:
        st.markdown("#### 01 · Add")
        st.write("Provide your resume and the job description.")

    with step2:
        st.markdown("#### 02 · Compare")
        st.write("Run the analysis and review the detected skills.")

    with step3:
        st.markdown("#### 03 · Improve")
        st.write("Explore learning suggestions and practice relevant skills.")

    st.warning(
        "Feature availability depends on the current implementation. "
        "For example, scanned PDFs may require OCR support, and the "
        "roadmap depends on the application's configured skill data."
    )

    if st.button("Go to Home", use_container_width=False):
        st.session_state["current_page"] = "Home"
        st.rerun()

    st.stop()


# --------------------------------------------------
# HOW IT WORKS PAGE
# --------------------------------------------------

elif current_page == "How It Works":

    st.markdown("## ⚙️ How HireMatch Works")
    st.caption("A step-by-step guide from job description to learning goals.")

    st.markdown(
        """
        <div style="
            padding: 24px;
            border-radius: 16px;
            background: linear-gradient(135deg, #211b3b, #172b43);
            border: 1px solid #49416e;
            margin: 12px 0 24px 0;
        ">
            <h2 style="color: white; margin-top: 0;">
                A clearer way to prepare for your target role
            </h2>
            <p style="color: #d6d6e7; line-height: 1.8;">
                HireMatch takes the resume and job description you provide,
                compares their skills using the configured matching logic,
                and presents the resulting comparison and learning suggestions.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🪜 Follow these steps")

    with st.container(border=True):
        st.markdown("#### 1. 📄 Add your resume")
        st.write(
            "Upload a PDF or DOCX file, or paste your resume text. "
            "Include relevant projects, technical skills, education, "
            "and experience."
        )

    with st.container(border=True):
        st.markdown("#### 2. 💼 Add the target job description")
        st.write(
            "Paste the job posting's responsibilities, required skills, "
            "and preferred qualifications. More complete descriptions "
            "can provide more useful comparison context."
        )

    with st.container(border=True):
        st.markdown("#### 3. 🔍 Run the analysis")
        st.write(
            "Select the analysis button. The application processes "
            "the provided text and identifies skills according to its "
            "current matching rules."
        )

    with st.container(border=True):
        st.markdown("#### 4. 📊 Review your results")
        st.write(
            "Check the displayed match percentage, matched skills, "
            "and skills from the job description that were not detected "
            "in your resume."
        )

    with st.container(border=True):
        st.markdown("#### 5. 🗺️ Explore your learning roadmap")
        st.write(
            "Review the suggested topics and learning resources for "
            "skills you want to strengthen. Choose a manageable topic "
            "and practice it through a small project or exercise."
        )

    st.divider()
    st.markdown("### 🧠 How should you interpret the results?")

    result_col1, result_col2 = st.columns(2)

    with result_col1:
        st.markdown("#### ✅ Matched skills")
        st.write(
            "These are skills detected in both inputs. Check that "
            "your resume includes clear evidence of how you used them."
        )

    with result_col2:
        st.markdown("#### 🧩 Missing skills")
        st.write(
            "These are skills detected in the job description but not "
            "detected in your resume. If you have the skills, consider "
            "describing your experience more clearly; otherwise, use "
            "them to guide your learning."
        )

    st.info(
        "The results depend on the text you provide and the matching "
        "logic implemented in the app. A high score does not guarantee "
        "a job, and a low score does not automatically mean you are "
        "unqualified."
    )

    if st.button("Go to Home", use_container_width=False):
        st.session_state["current_page"] = "Home"
        st.rerun()

    st.stop()


# --------------------------------------------------
# Hero section
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">
        <h1> 🎯Find your fit. Build your future.</h1>
        <p>
            Discover how your skills align with a job, identify learning
            gaps, and create a practical roadmap toward your career goals.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# Introduction
# --------------------------------------------------

st.subheader("Let's find your next opportunity")

st.markdown(
    """
    <p class="muted">
        Add your resume and a target job description to get your
        skill-match analysis and personalized learning recommendations.
    </p>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# User inputs
# --------------------------------------------------

resume_col, job_col = st.columns(2, gap="large")

with resume_col:
    st.markdown("### 📄 Your resume")

    uploaded_resume = st.file_uploader(
        "Upload your resume (PDF or Word)",
        type=["pdf", "docx"],
        key="resume_file",
    )

    if uploaded_resume is not None:
        try:
            file_bytes = uploaded_resume.getvalue()

            if uploaded_resume.name.lower().endswith(".pdf"):
                pdf_reader = PdfReader(BytesIO(file_bytes))
                extracted_text = "\n".join(
                    page.extract_text() or ""
                    for page in pdf_reader.pages
                )
            else:
                document = Document(BytesIO(file_bytes))
                extracted_text = "\n".join(
                    paragraph.text
                    for paragraph in document.paragraphs
                )

            if extracted_text.strip():
                if st.session_state.get("resume_input") != extracted_text:
                    st.session_state["resume_input"] = extracted_text
                st.success("Resume text extracted successfully.")
            else:
                st.warning(
                    "No selectable text found. This PDF may be scanned "
                    "and require OCR."
                )

        except Exception as exc:
            st.error(f"Could not read the uploaded file: {exc}")

    resume_text = st.text_area(
        "Resume text",
        height=300,
        placeholder=(
            "Upload your resume above or paste your resume text here...\n\n"
            "Example:\n"
            "BTech student with experience in Python, SQL, "
            "Git, and basic machine learning."
        ),
        help="Upload a PDF or DOCX, or paste your resume text manually.",
        key="resume_input",
        label_visibility="collapsed",
    )

    st.caption("Tip: Include your projects, technical skills, and experience.")

with job_col:
    st.markdown("### 💼 Target job")

    job_description = st.text_area(
        "Job description",
        height=300,
        placeholder=(
            "Paste the job description here...\n\n"
            "Example:\n"
            "We are looking for a candidate skilled in Python, SQL, "
            "machine learning, and data analysis."
        ),
        help="Paste the responsibilities and required skills from the job listing.",
        key="job_input",
        label_visibility="collapsed",
    )

    st.caption("Tip: Include the job's required and preferred skills.")


# --------------------------------------------------
# Analyze button
# --------------------------------------------------

st.markdown("")

left_space, button_col, right_space = st.columns([1, 2, 1])

with button_col:
    analyze_clicked = st.button(
        "✨ Analyze My Match",
        type="primary",
        use_container_width=True,
    )


# --------------------------------------------------
# Input validation and analysis
# --------------------------------------------------

if analyze_clicked:
    if not resume_text.strip():
        st.warning("Please enter your resume text before continuing.")

    elif not job_description.strip():
        st.warning("Please enter a job description before continuing.")

    else:
        with st.spinner("Analyzing your skills..."):
            try:
                result = analyze_match(
                    resume_text=resume_text,
                    job_description=job_description,
                )

                st.session_state["hirematch_result"] = result

                if result.get("success", False):
                    ats_result = analyze_ats(resume_text)
                    st.session_state["hirematch_ats_result"] = ats_result

                    current_user = st.session_state.get("user") or {}
                    user_id = current_user.get("id", current_user.get("user_id"))
                    if user_id is not None:
                        try:
                            first_line = next(
                                (line.strip() for line in job_description.splitlines() if line.strip()),
                                "Target role",
                            )
                            save_analysis(
                                user_id=user_id,
                                job_title=first_line[:100],
                                semantic_score=result.get("semantic_similarity"),
                                ats_score=ats_result.get("score", ats_result.get("ats_score")),
                                matched_skills=result.get("matched_skills", []),
                                missing_skills=result.get("missing_skills", []),
                            )
                        except Exception:
                            # Keep the live analysis usable if history saving fails.
                            pass

            except Exception as exc:
                st.error(
                    "HireMatch could not complete the analysis. "
                    "Check that matcher.py is configured correctly."
                )
                st.exception(exc)

# --------------------------------------------------
# Analysis results
# --------------------------------------------------

if "hirematch_result" in st.session_state:
    result = st.session_state["hirematch_result"]

    st.divider()
    st.header("📊 Your HireMatch Results")

    if not result.get("success", False):
        st.warning(result.get("message", "Analysis could not be completed."))

    else:
        
        # Semantic match score
        score = result.get("semantic_similarity")

        st.markdown("### Your job compatibility")

        score_col, summary_col = st.columns([1, 2], gap="large")

        with score_col:
            if score is not None:
                score = float(score)

                st.metric(
                    label="Semantic Match",
                    value=f"{score:.1f}%",
                )
                st.progress(max(0.0, min(1.0, score / 100)))
            else:
                st.metric(
                    label="Semantic Match",
                    value="Unavailable",
                )

        with summary_col:
            st.markdown("#### What your score means")

            if score is None:
                st.warning(
                    "Semantic matching is currently unavailable. "
                    "Please try again after checking the model and connection."
                )
            elif score >= 80:
                st.success(
                    "The model found strong textual similarity. Review "
                    "the skill gaps and verify the details yourself."
                )
            elif score >= 50:
                st.info(
                    "The model found some textual similarity. Focus on "
                    "the relevant missing skills and experience."
                )
            else:
                st.warning(
                    "The model found lower textual similarity. Check "
                    "whether your resume describes relevant experience "
                    "and projects clearly."
                )

            st.caption(
                "Semantic similarity measures textual similarity. It is "
                "not a hiring probability or a guarantee of suitability."
            )

        st.divider()

        # ATS readiness checklist
        ats_result = st.session_state.get("hirematch_ats_result")
        if ats_result:
            st.markdown("### 🧾 ATS resume readiness")
            ats_score = ats_result.get("score", ats_result.get("ats_score"))
            if ats_score is not None:
                ats_col, ats_summary_col = st.columns([1, 2], gap="large")
                with ats_col:
                    st.metric("ATS checklist score", f"{float(ats_score):.0f}/100")
                    st.progress(max(0.0, min(1.0, float(ats_score) / 100)))
                with ats_summary_col:
                    st.write(
                        f"{ats_result.get('passed_count', 0)} of "
                        f"{ats_result.get('total_checks', len(ats_result.get('checks', [])))} "
                        "basic resume checks passed."
                    )
                    st.caption(
                        ats_result.get(
                            "disclaimer",
                            "This heuristic checklist is not a guarantee of ATS compatibility or hiring success."
                        )
                    )

            with st.expander("Review ATS checklist details"):
                for check in ats_result.get("checks", []):
                    label = check.get("label", "Resume check")
                    feedback = check.get("feedback", "")
                    points = check.get("points", 0)
                    if check.get("passed"):
                        st.success(f"✓ {label} (+{points} points) — {feedback}")
                    else:
                        st.warning(f"• {label} — {feedback}")

        st.divider()

        # Skill summary
        st.markdown("### 🧩 Skill breakdown")

        matched = result.get("matched_skills", [])
        missing = result.get("missing_skills", [])
        required = result.get("job_skills", [])

        metric1, metric2, metric3 = st.columns(3)

        metric1.metric("Skills Required", len(required))
        metric2.metric("Skills Matched", len(matched))
        metric3.metric("Skills to Learn", len(missing))

        matched_col, missing_col = st.columns(2, gap="large")

        with matched_col:
            st.markdown("#### ✅ Matched skills")

            if matched:
                for skill in matched:
                    st.markdown(f"- 🟢 **{skill.title()}**")
            else:
                st.write("No matching skills were detected yet.")

        with missing_col:
            st.markdown("#### 🎯 Skills to develop")

            if missing:
                for skill in missing:
                    st.markdown(f"- 🟠 **{skill.title()}**")
            else:
                st.success(
                    "No missing skills were detected among the "
                    "supported skills in this analysis."
                )

        with st.expander("View all detected skills"):
            st.markdown("**Skills found in your resume**")
            st.write(
                ", ".join(result.get("resume_skills", []))
                or "No supported skills detected."
            )

            st.markdown("**Skills found in the job description**")
            st.write(
                ", ".join(required)
                or "No supported skills detected."
            )

        st.divider()

        # Personalized learning roadmap
        st.markdown("### 🗺️ Your personalized learning roadmap")

        roadmap = result.get("roadmap", [])

        if missing and roadmap:
            st.write(
                "These learning steps are based on the missing skills "
                "identified in your selected job description."
            )

            for item in roadmap:
                with st.container(border=True):
                    st.markdown(
                        f"#### Step {item.get('step', '?')}: "
                        f"{item.get('skill', 'Skill').title()}"
                    )

                    st.write(item.get("topic", "Review this skill's fundamentals."))

                    st.caption(
                        f"Estimated learning time: "
                        f"{item.get('duration', 'Varies by learner')}"
                    )

                    resources = item.get("resources", [])

                    if resources:
                        st.markdown("**Learning resources**")

                        for resource in resources:
                            if isinstance(resource, dict):
                                resource_title = resource.get(
                                    "title", "Learning resource"
                                )
                                resource_url = resource.get("url", "")

                                if resource_url.startswith(
                                    ("https://", "http://")
                                ):
                                    st.markdown(
                                        f"- [{resource_title}]({resource_url})"
                                    )
                                else:
                                    st.markdown(f"- {resource_title}")

                            elif isinstance(resource, str):
                                if resource.startswith(
                                    ("https://", "http://")
                                ):
                                    st.markdown(
                                        f"- [Open learning resource]({resource})"
                                    )
                                else:
                                    st.markdown(f"- {resource}")

                    else:
                        st.caption(
                            "Add a verified learning resource for this "
                            "skill to the ROADMAPS dictionary in matcher.py."
                        )

        elif not missing:
            st.success(
                "No learning gaps were detected among the supported skills. "
                "Consider practicing interview questions and building "
                "projects relevant to this role."
            )

        else:
            st.info(
                "A roadmap could not be generated for these skills yet. "
                "Check the ROADMAPS dictionary in matcher.py."
            )

        st.divider()

        # Next steps
        st.markdown("### 🚀 Recommended next steps")

        st.markdown(
            """
            1. Prioritize the missing skills most frequently requested
               in your target roles.
            2. Practice each skill with a small hands-on project.
            3. Add genuine project experience to your resume as you build it.
            4. Re-run the analysis after updating your resume.
            """
        )

        # Reset results and start a fresh analysis
        if st.button("🔄 Start a New Analysis"):
            st.session_state.pop("hirematch_result", None)
            st.session_state.pop("hirematch_ats_result", None)
            st.rerun()


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    "HireMatch | AI-assisted career planning · "
    "Use results as guidance, not as a hiring guarantee."
)
