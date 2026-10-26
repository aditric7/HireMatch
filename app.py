import streamlit as st
from io import BytesIO
from pypdf import PdfReader
from docx import Document
from matcher import analyze_match

# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="HireMatch | AI Career Assistant",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)


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
    st.caption("HireMatch • Career development assistant")

if "current_page" not in st.session_state:
    st.session_state["current_page"] = "Home"



# --------------------------------------------------
# Page Routing: Informational Pages
# --------------------------------------------------

current_page = st.session_state["current_page"]


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
        # Match score
        score = result.get("match_percentage", 0)

        st.markdown("### Your job compatibility")

        score_col, summary_col = st.columns([1, 2], gap="large")

        with score_col:
            st.metric(
                label="Skill Match",
                value=f"{score}%",
            )
            st.progress(score / 100)

        with summary_col:
            st.markdown("#### What your score means")

            if score >= 80:
                st.success(
                    "Strong skill alignment! Review the remaining gaps "
                    "and prepare examples from your projects."
                )
            elif score >= 50:
                st.info(
                    "You have a useful foundation. Focus on the missing "
                    "skills most relevant to this role."
                )
            else:
                st.warning(
                    "There are several skill gaps to explore. Use the "
                    "roadmap below to plan your next learning steps."
                )

            st.caption(
                "This score compares detected skills only. It does not "
                "measure your full qualifications or guarantee hiring."
            )

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
            st.rerun()


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.divider()

st.caption(
    "HireMatch | AI-assisted career planning · "
    "Use results as guidance, not as a hiring guarantee."
)
