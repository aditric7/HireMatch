import streamlit as st
from pypdf import PdfReader
from matcher import analyze_match
import html


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="HireMatch",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# SESSION STATE - SIDEBAR NAVIGATION
# ============================================================

if "page" not in st.session_state:
    st.session_state.page = "Home"


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background: #f7f9fd;
}

.block-container {
    max-width: 1180px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}


/* ==========================================================
   SIDEBAR
   ========================================================== */

section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e8ebf2;
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.5rem;
}

.sidebar-logo {
    font-size: 21px;
    font-weight: 800;
    color: #172554;
    margin-bottom: 3px;
}

.sidebar-subtitle {
    font-size: 12px;
    color: #8a91a5;
    margin-bottom: 20px;
}

.sidebar-security {
    margin-top: 90px;
    background: #f6f8fc;
    border-radius: 9px;
    padding: 11px;
    font-size: 11px;
    line-height: 1.5;
    color: #7d8498;
}


/* Sidebar buttons */

section[data-testid="stSidebar"] .stButton {
    margin-bottom: 4px;
}

section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: #687086 !important;
    border: none !important;
    box-shadow: none !important;
    text-align: left !important;
    justify-content: flex-start !important;
    padding: 9px 12px !important;
    height: 38px !important;
    font-size: 13px !important;
    font-weight: 600 !important;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: #f2f1ff !important;
    color: #5946df !important;
}

.sidebar-active-button {
    background: #eef0ff !important;
    color: #5946df !important;
}


/* ==========================================================
   HERO
   ========================================================== */

.hero-wrapper {
    text-align: center;
    padding: 8px 10px 20px 10px;
}

.hero-icon {
    font-size: 48px;
    margin-bottom: 3px;
}

.hero-title {
    font-size: 39px;
    line-height: 1.05;
    font-weight: 850;
    color: #172554;
    letter-spacing: -1.2px;
}

.hero-title span {
    color: #6548e8;
}

.hero-subtitle {
    font-size: 17px;
    font-weight: 650;
    color: #1e2b50;
    margin-top: 7px;
}

.hero-description {
    max-width: 700px;
    margin: 9px auto 0 auto;
    color: #778097;
    font-size: 13px;
    line-height: 1.6;
}


/* ==========================================================
   PRIVACY
   ========================================================== */

.privacy-box {
    background: #f0efff;
    border: 1px solid #dedaff;
    border-radius: 9px;
    padding: 11px 14px;
    color: #5a50a0;
    font-size: 12px;
    margin-bottom: 22px;
}


/* ==========================================================
   SECTION TITLES
   ========================================================== */

.section-heading {
    font-size: 20px;
    font-weight: 800;
    color: #172554;
    margin-top: 10px;
    margin-bottom: 12px;
}


/* ==========================================================
   CARDS
   ========================================================== */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #ffffff;
    border: 1px solid #e2e7f0;
    border-radius: 13px;
    box-shadow: 0 3px 13px rgba(30, 41, 80, 0.05);
}


/* ==========================================================
   INPUT LABELS
   ========================================================== */

.input-title {
    font-size: 16px;
    font-weight: 800;
    color: #1d2b50;
}

.input-description {
    font-size: 12px;
    color: #8a92a5;
    line-height: 1.5;
    margin-top: 3px;
    margin-bottom: 11px;
}


/* ==========================================================
   FILE UPLOADER
   ========================================================== */

[data-testid="stFileUploader"] {
    background: #fafdff;
    border: 1px dashed #b9c8ea;
    border-radius: 9px;
}

[data-testid="stFileUploader"] * {
    font-size: 12px;
}


/* ==========================================================
   TEXT AREAS
   ========================================================== */

textarea {
    background: #ffffff !important;
    color: #26314d !important;
    border: 1px solid #dce2ec !important;
    border-radius: 9px !important;
    font-size: 12px !important;
}

textarea::placeholder {
    color: #a2a9b8 !important;
}


/* ==========================================================
   ANALYZE BUTTON
   ========================================================== */

.stButton > button {
    background: linear-gradient(
        90deg,
        #5b49df,
        #7553eb
    ) !important;

    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    height: 45px;
    font-size: 13px !important;
    font-weight: 750 !important;

    box-shadow:
        0 4px 12px rgba(91, 73, 223, 0.22);
}

.stButton > button:hover {
    background: linear-gradient(
        90deg,
        #503ed0,
        #6745db
    ) !important;
}


/* ==========================================================
   METRICS
   ========================================================== */

[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e2e7f0;
    border-radius: 11px;
    padding: 13px;
}

[data-testid="stMetricLabel"] {
    color: #70798e !important;
    font-size: 11px !important;
}

[data-testid="stMetricValue"] {
    color: #172554 !important;
    font-size: 27px !important;
    font-weight: 800 !important;
}


/* ==========================================================
   PROGRESS
   ========================================================== */

[data-testid="stProgressBar"] > div {
    background: #e5e9f1;
    border-radius: 20px;
}

[data-testid="stProgressBar"] > div > div {
    background: #6650e5;
    border-radius: 20px;
}


/* ==========================================================
   EXPANDERS
   ========================================================== */

[data-testid="stExpander"] {
    background: #ffffff;
    border: 1px solid #e1e6ef;
    border-radius: 9px;
    margin-bottom: 7px;
}

[data-testid="stExpander"] summary {
    font-size: 13px;
    font-weight: 700;
    color: #253253;
}


/* ==========================================================
   RESUME PREVIEW - FIXED
   ========================================================== */

.resume-preview {
    background: #ffffff !important;
    color: #26314d !important;
    border: 1px solid #dce3ee;
    border-radius: 9px;
    padding: 16px;
    font-size: 13px !important;
    line-height: 1.7;
    white-space: pre-wrap;
    word-wrap: break-word;
    max-height: 430px;
    overflow-y: auto;
    font-family: Arial, sans-serif;
    text-align: left;
}

.resume-preview,
.resume-preview * {
    color: #26314d !important;
    background: transparent !important;
}


/* ==========================================================
   ROADMAP
   ========================================================== */

.roadmap-title {
    font-size: 16px;
    font-weight: 800;
    color: #18336a;
}

.priority-high {
    display: inline-block;
    background: #ffe8ed;
    color: #d92f52;
    border-radius: 20px;
    padding: 5px 10px;
    font-size: 11px;
    font-weight: 700;
    margin: 7px 0 10px 0;
}

.roadmap-label {
    font-size: 12px;
    font-weight: 800;
    color: #263657;
}

.roadmap-text {
    font-size: 12px;
    color: #68748c;
    line-height: 1.55;
}


/* ==========================================================
   EQUAL WEEK CARDS - FIXED
   ========================================================== */

.week-card {
    background: #ffffff;
    border: 1px solid #dfe7f2;
    border-radius: 11px;
    min-height: 118px;
    height: 118px;
    padding: 14px;
    box-sizing: border-box;
}

.week-number {
    font-size: 13px;
    font-weight: 800;
    color: #4f46c9;
    margin-bottom: 7px;
}

.week-title {
    font-size: 12px;
    font-weight: 800;
    color: #24355c;
    margin-bottom: 5px;
}

.week-description {
    font-size: 11px;
    line-height: 1.45;
    color: #6e7890;
}


/* ==========================================================
   INFO / SUCCESS BOXES
   ========================================================== */

.stAlert {
    font-size: 12px !important;
}


/* ==========================================================
   OTHER PAGES
   ========================================================== */

.info-page-title {
    font-size: 30px;
    font-weight: 850;
    color: #172554;
    margin-bottom: 7px;
}

.info-page-subtitle {
    font-size: 13px;
    color: #778097;
    margin-bottom: 25px;
}

.info-card {
    background: #ffffff;
    border: 1px solid #e1e6ef;
    border-radius: 13px;
    padding: 20px;
    min-height: 145px;
    box-shadow: 0 3px 13px rgba(30, 41, 80, 0.05);
}

.info-card-title {
    font-size: 15px;
    font-weight: 800;
    color: #20315b;
    margin-bottom: 8px;
}

.info-card-text {
    font-size: 12px;
    color: #68748c;
    line-height: 1.65;
}


/* ==========================================================
   FOOTER
   ========================================================== */

.footer {
    text-align: center;
    color: #9aa2b2;
    font-size: 11px;
    padding-top: 22px;
}


/* ==========================================================
   HOME PAGE TEXT VISIBILITY FIX
   ========================================================== */

.home-matching-heading {
    color: #172554 !important;
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 12px;
}

.home-missing-heading {
    color: #172554 !important;
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 12px;
}

.home-job-skills-heading {
    color: #172554 !important;
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 12px;
}

.home-disclaimer {
    color: #68748c !important;
    font-size: 12px;
    line-height: 1.6;
}

.stAlert p,
.stAlert div,
.stAlert span {
    color: #26314d !important;
}

[data-testid="stExpander"] .stMarkdown,
[data-testid="stExpander"] .stMarkdown p,
[data-testid="stExpander"] .stMarkdown span {
    color: #26314d !important;
}

.roadmap-intro {
    color: #68748c !important;
    font-size: 13px;
    line-height: 1.6;
}

.roadmap-heading {
    color: #172554 !important;
    font-size: 20px;
    font-weight: 800;
}


/* ==========================================================
   FINAL ROADMAP TEXT VISIBILITY FIX
   ========================================================== */

.home-disclaimer,
.home-disclaimer * {
    color: #68748c !important;
}

.roadmap-heading,
.roadmap-heading * {
    color: #172554 !important;
}

.week-card,
.week-card * {
    color: #26314d !important;
}

.week-number,
.week-number * {
    color: #4f46c9 !important;
}

.week-title,
.week-title * {
    color: #24355c !important;
}

.week-description,
.week-description * {
    color: #6e7890 !important;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown(
        '<div class="sidebar-logo">🎯 HireMatch</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="sidebar-subtitle">'
        'Resume Intelligence & Job Matching'
        '</div>',
        unsafe_allow_html=True
    )

    # Home
    if st.button(
        "⌂  Home",
        use_container_width=True
    ):
        st.session_state.page = "Home"

    # How It Works
    if st.button(
        "◉  How It Works",
        use_container_width=True
    ):
        st.session_state.page = "How It Works"

    # Features
    if st.button(
        "⚙  Features",
        use_container_width=True
    ):
        st.session_state.page = "Features"

    # About
    if st.button(
        "ⓘ  About",
        use_container_width=True
    ):
        st.session_state.page = "About"

    st.markdown(
        '<div class="sidebar-security">'
        '🔒 &nbsp; Your data stays local<br>'
        '&nbsp;&nbsp;&nbsp;&nbsp;and private.'
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# HOW IT WORKS PAGE
# ============================================================

if st.session_state.page == "How It Works":

    st.markdown(
        '<div class="info-page-title">'
        'How It Works'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="info-page-subtitle">'
        'HireMatch analyzes your resume against a target job '
        'description in a simple five-step process.'
        '</div>',
        unsafe_allow_html=True
    )

    c1, c2 = st.columns(2, gap="large")

    with c1:

        st.markdown(
            """
            <div class="info-card">
                <div class="info-card-title">
                    01 &nbsp; 📄 Upload Resume
                </div>
                <div class="info-card-text">
                    Upload your resume as a PDF. HireMatch extracts
                    the text locally so it can be analyzed.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        st.markdown(
            """
            <div class="info-card">
                <div class="info-card-title">
                    03 &nbsp; 🔎 NLP Analysis
                </div>
                <div class="info-card-text">
                    TF-IDF and cosine similarity are used to calculate
                    how closely the resume text matches the job description.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        st.markdown(
            """
            <div class="info-card">
                <div class="info-card-title">
                    05 &nbsp; 🎯 Preparation Roadmap
                </div>
                <div class="info-card-text">
                    Missing skills are converted into a personalized
                    learning roadmap containing topics and practice suggestions.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:

        st.markdown(
            """
            <div class="info-card">
                <div class="info-card-title">
                    02 &nbsp; 💼 Add Job Description
                </div>
                <div class="info-card-text">
                    Paste the job description for the role you want
                    to compare against your resume.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        st.markdown(
            """
            <div class="info-card">
                <div class="info-card-title">
                    04 &nbsp; 🔎 Skill Gap Analysis
                </div>
                <div class="info-card-text">
                    HireMatch identifies matching skills, missing skills
                    and evidence for skills already present in your resume.
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="footer">'
        '🎯 HireMatch • NLP-Based Resume Matching'
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# FEATURES PAGE
# ============================================================

elif st.session_state.page == "Features":

    st.markdown(
        '<div class="info-page-title">'
        'Features'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="info-page-subtitle">'
        'Core capabilities included in the HireMatch system.'
        '</div>',
        unsafe_allow_html=True
    )

    feature_data = [
        (
            "📄",
            "PDF Resume Extraction",
            "Upload a PDF resume and automatically extract its text."
        ),
        (
            "🔎",
            "NLP Resume Matching",
            "Use TF-IDF and cosine similarity to calculate text similarity."
        ),
        (
            "🎯",
            "Skill Gap Analysis",
            "Identify skills that match the target role and skills that are missing."
        ),
        (
            "🧾",
            "Resume Evidence",
            "Show evidence from the resume for detected matching skills."
        ),
        (
            "📚",
            "Personalized Roadmap",
            "Generate job-specific learning topics and practical preparation suggestions."
        ),
        (
            "🔒",
            "Local Processing",
            "Resume content remains within the application and is not sent to an external AI API."
        ),
    ]

    feature_cols = st.columns(
        2,
        gap="large"
    )

    for index, (
        icon,
        title,
        description
    ) in enumerate(feature_data):

        with feature_cols[index % 2]:

            st.markdown(
                f"""
                <div class="info-card">
                    <div class="info-card-title">
                        {icon} &nbsp; {title}
                    </div>
                    <div class="info-card-text">
                        {description}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

            st.write("")

    st.markdown(
        '<div class="footer">'
        '🎯 HireMatch • Built with Python, Streamlit & NLP'
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# ABOUT PAGE
# ============================================================

elif st.session_state.page == "About":

    st.markdown(
        '<div class="info-page-title">'
        'About HireMatch'
        '</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="info-page-subtitle">'
        'An NLP-based resume and job description matching system.'
        '</div>',
        unsafe_allow_html=True
    )

    # ========================================================
    # WHAT IS HIREMATCH?
    # ========================================================

    with st.container(border=True):

        st.markdown(
            """
            <div style="
                color: #20315b;
                font-size: 15px;
                font-weight: 800;
                margin-bottom: 10px;
            ">
                🎯 &nbsp; What is HireMatch?
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style="
                color: #68748c;
                font-size: 13px;
                line-height: 1.7;
            ">
                HireMatch is a resume–job description matching system
                designed to help students and job seekers understand
                how closely their resume aligns with a target role.
                <br><br>
                Instead of only providing a similarity percentage,
                HireMatch also identifies matching skills, missing skills,
                evidence from the resume and a personalized preparation
                roadmap.
            </div>
            """,
            unsafe_allow_html=True
        )

    st.write("")

    # ========================================================
    # TECHNOLOGIES + PROJECT PURPOSE
    # ========================================================

    about_col1, about_col2 = st.columns(
        2,
        gap="large"
    )

    # --------------------------------------------------------
    # TECHNOLOGIES
    # --------------------------------------------------------

    with about_col1:

        with st.container(border=True):

            st.markdown(
                """
                <div style="
                    color: #20315b;
                    font-size: 15px;
                    font-weight: 800;
                    margin-bottom: 10px;
                ">
                    🛠 &nbsp; Technologies
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div style="
                    color: #68748c;
                    font-size: 13px;
                    line-height: 1.8;
                ">
                    • Python<br>
                    • Streamlit<br>
                    • Natural Language Processing<br>
                    • TF-IDF<br>
                    • Cosine Similarity<br>
                    • Scikit-learn<br>
                    • PyPDF
                </div>
                """,
                unsafe_allow_html=True
            )

    # --------------------------------------------------------
    # PROJECT PURPOSE
    # --------------------------------------------------------

    with about_col2:

        with st.container(border=True):

            st.markdown(
                """
                <div style="
                    color: #20315b;
                    font-size: 15px;
                    font-weight: 800;
                    margin-bottom: 10px;
                ">
                    🎓 &nbsp; Project Purpose
                </div>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div style="
                    color: #68748c;
                    font-size: 13px;
                    line-height: 1.7;
                ">
                    HireMatch demonstrates how traditional NLP techniques
                    can be combined with rule-based skill analysis to create
                    a practical resume intelligence application.
                </div>
                """,
                unsafe_allow_html=True
            )


# ============================================================
# HOME PAGE
# ============================================================

else:

    # ========================================================
    # HERO
    # ========================================================

    st.markdown(
        '<div class="hero-wrapper">'
        '<div class="hero-icon">🎯</div>'
        '<div class="hero-title">'
        'Hire<span>Match</span>'
        '</div>'
        '<div class="hero-subtitle">'
        'Resume Intelligence & Job Matching'
        '</div>'
        '<div class="hero-description">'
        'Upload your resume and paste the target job description '
        'to get a match score, skill gap analysis and a '
        'personalized preparation roadmap.'
        '</div>'
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # PRIVACY
    # ========================================================

    st.markdown(
        '<div class="privacy-box">'
        '🔒 &nbsp; <b>Your resume stays within this application</b> '
        'and is not sent to an external AI API.'
        '</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # INPUT SECTION
    # ========================================================

    st.markdown(
        '<div class="section-heading">'
        '📄 &nbsp; Resume & Target Job'
        '</div>',
        unsafe_allow_html=True
    )

    resume_col, job_col = st.columns(
        2,
        gap="large"
    )


    # ========================================================
    # RESUME
    # ========================================================

    with resume_col:

        with st.container(border=True):

            st.markdown(
                '<div class="input-title">📄 &nbsp; Resume</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="input-description">'
                'Upload your resume as a PDF or paste the text manually.'
                '</div>',
                unsafe_allow_html=True
            )

            uploaded_resume = st.file_uploader(
                "Upload Resume PDF",
                type=["pdf"]
            )

            resume_text = ""

            if uploaded_resume is not None:

                try:

                    reader = PdfReader(
                        uploaded_resume
                    )

                    for page in reader.pages:

                        page_text = page.extract_text()

                        if page_text:
                            resume_text += page_text + "\n"

                    if resume_text.strip():

                        st.success(
                            "✅ Resume uploaded and text extracted successfully!"
                        )

                        with st.expander(
                            "👀 Preview extracted resume text"
                        ):

                            safe_resume_text = html.escape(
                                resume_text
                            )

                            st.markdown(
                                f"""
                                <div class="resume-preview">
                                {safe_resume_text}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                    else:

                        st.error(
                            "Could not extract text from this PDF."
                        )

                except Exception as error:

                    st.error(
                        f"Could not read the PDF: {error}"
                    )

            manual_resume = st.text_area(
                "Paste your resume text manually",
                height=145,
                placeholder="Paste your resume text here..."
            )

            if manual_resume.strip():

                resume_text = manual_resume


    # ========================================================
    # JOB DESCRIPTION
    # ========================================================

    with job_col:

        with st.container(border=True):

            st.markdown(
                '<div class="input-title">'
                '💼 &nbsp; Target Job Description'
                '</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="input-description">'
                'Paste the job description you want to compare against your resume.'
                '</div>',
                unsafe_allow_html=True
            )

            job_text = st.text_area(
                "Job Description",
                height=285,
                placeholder="Paste the target job description here..."
            )


    # ========================================================
    # ANALYZE BUTTON
    # ========================================================

    st.write("")

    analyze_button = st.button(
        "🔍  Analyze Match",
        type="primary",
        use_container_width=True
    )


    # ========================================================
    # ANALYSIS
    # ========================================================

    if analyze_button:

        if not resume_text.strip():

            st.warning(
                "Please upload a PDF resume or paste your resume text."
            )

        elif not job_text.strip():

            st.warning(
                "Please provide the target job description."
            )

        else:

            result = analyze_match(
                resume_text,
                job_text
            )

            score = max(
                0,
                min(
                    100,
                    result["match_percentage"]
                )
            )


            # ==================================================
            # MATCH RESULT
            # ==================================================

            st.divider()

            st.markdown(
                '<div class="section-heading">'
                '📊 &nbsp; Match Result'
                '</div>',
                unsafe_allow_html=True
            )

            score_col, matching_col, missing_col = st.columns(
                [1, 1, 1],
                gap="medium"
            )

            with score_col:

                st.metric(
                    "Resume Match",
                    f"{score:.1f}%"
                )

                st.progress(
                    score / 100
                )

            with matching_col:

                st.metric(
                    "✅ Matching Skills",
                    len(result["matching_skills"])
                )

            with missing_col:

                st.metric(
                    "❌ Missing Skills",
                    len(result["missing_skills"])
                )


            # ==================================================
            # SKILL GAP ANALYSIS
            # ==================================================

            st.markdown(
                '<div class="section-heading">'
                '🔎 &nbsp; Skill Gap Analysis'
                '</div>',
                unsafe_allow_html=True
            )


            # ==================================================
            # MATCHING SKILLS
            # ==================================================

            st.markdown(
                '<div class="home-matching-heading">'
                '🟢 Matching Skills & Resume Evidence'
                '</div>',
                unsafe_allow_html=True
            )

            matching_skills = result["matching_skills"]

            if matching_skills:

                skill_cols = st.columns(
                    4,
                    gap="small"
                )

                for index, skill in enumerate(
                    matching_skills
                ):

                    with skill_cols[
                        index % 4
                    ]:

                        evidence = result.get(
                            "skill_evidence",
                            {}
                        ).get(
                            skill,
                            ""
                        )

                        with st.expander(
                            f"✓ {skill.title()}"
                        ):

                            st.caption(
                                "Resume evidence"
                            )

                            st.write(
                                evidence
                            )

            else:

                st.info(
                    "No matching skills were detected."
                )


            # ==================================================
            # MISSING SKILLS
            # ==================================================

            st.markdown(
                '<div class="home-missing-heading">'
                '🔴 Missing Skills'
                '</div>',
                unsafe_allow_html=True
            )

            if result["missing_skills"]:

                missing_cols = st.columns(
                    2,
                    gap="small"
                )

                for index, skill in enumerate(
                    result["missing_skills"]
                ):

                    with missing_cols[
                        index % 2
                    ]:

                        st.error(
                            f"❌ **{skill.title()}** — "
                            "Not found in your resume."
                        )

            else:

                st.success(
                    "🎉 No missing skills were detected!"
                )


            # ==================================================
            # DETECTED JOB SKILLS
            # ==================================================

            st.markdown(
                '<div class="home-job-skills-heading">'
                '🔑 Skills Detected in Job Description'
                '</div>',
                unsafe_allow_html=True
            )

            if result["job_skills"]:

                st.info(
                    "  •  ".join(
                        skill.title()
                        for skill in result["job_skills"]
                    )
                )

            else:

                st.write(
                    "No skills from the built-in "
                    "skill dictionary were detected."
                )


            # ==================================================
            # ROADMAP
            # ==================================================

            st.divider()

            st.markdown(
                '<div class="section-heading">'
                '🎯 &nbsp; Personalized Preparation Roadmap'
                '</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="roadmap-intro">'
                'This roadmap is generated from the skills '
                'missing from your resume but required by '
                'the target job description.'
                '</div>',
                unsafe_allow_html=True
            )

            roadmap = result.get(
                "roadmap",
                {}
            )

            if roadmap:

                roadmap_cols = st.columns(
                    2,
                    gap="large"
                )

                for index, (
                    skill,
                    details
                ) in enumerate(
                    roadmap.items()
                ):

                    with roadmap_cols[
                        index % 2
                    ]:

                        with st.container(
                            border=True
                        ):

                            st.markdown(
                                f'<div class="roadmap-title">'
                                f'📚 &nbsp; {skill.title()}'
                                f'</div>',
                                unsafe_allow_html=True
                            )

                            st.markdown(
                                '<div class="priority-high">'
                                '🔴 &nbsp; Priority: High'
                                '</div>',
                                unsafe_allow_html=True
                            )

                            st.markdown(
                                '<div class="roadmap-label">'
                                'Why this skill matters:'
                                '</div>',
                                unsafe_allow_html=True
                            )

                            st.markdown(
                                f'<div class="roadmap-text">'
                                f'{details["why"]}'
                                f'</div>',
                                unsafe_allow_html=True
                            )

                            st.write("")

                            st.markdown(
                                '<div class="roadmap-label">'
                                '📖 &nbsp; Topics to focus on:'
                                '</div>',
                                unsafe_allow_html=True
                            )

                            for topic in details[
                                "topics"
                            ]:

                                st.markdown(
                                    f'<div class="roadmap-text">'
                                    f'• {topic}'
                                    f'</div>',
                                    unsafe_allow_html=True
                                )

                            st.write("")

                            st.markdown(
                                '<div class="roadmap-label">'
                                '💻 &nbsp; Suggested practice:'
                                '</div>',
                                unsafe_allow_html=True
                            )

                            for practice in details[
                                "practice"
                            ]:

                                st.markdown(
                                    f'<div class="roadmap-text">'
                                    f'• {practice}'
                                    f'</div>',
                                    unsafe_allow_html=True
                                )


                # ==============================================
                # EQUAL FOUR-WEEK SEQUENCE
                # ==============================================



                st.markdown(
                    '<div class="roadmap-heading">'
                    '📅 Suggested Preparation Sequence'
                    '</div>',
                    unsafe_allow_html=True
                )

                week1, week2, week3, week4 = st.columns(
                    4,
                    gap="small"
                )

                with week1:

                    st.markdown(
                        """
                        <div class="week-card">
                            <div class="week-number">
                                ① Week 1
                            </div>
                            <div class="week-title">
                                Learn fundamentals
                            </div>
                            <div class="week-description">
                                Learn the fundamentals of the first skill.
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with week2:

                    st.markdown(
                        """
                        <div class="week-card">
                            <div class="week-number">
                                ② Week 2
                            </div>
                            <div class="week-title">
                                Practice
                            </div>
                            <div class="week-description">
                                Practice problems and hands-on exercises.
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with week3:

                    st.markdown(
                        """
                        <div class="week-card">
                            <div class="week-number">
                                ③ Week 3
                            </div>
                            <div class="week-title">
                                Learn the next skill
                            </div>
                            <div class="week-description">
                                Learn and practice the second skill.
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with week4:

                    st.markdown(
                        """
                        <div class="week-card">
                            <div class="week-number">
                                ④ Week 4
                            </div>
                            <div class="week-title">
                                Build & revise
                            </div>
                            <div class="week-description">
                                Build a small project and revise interview concepts.
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            else:

                st.success(
                    "🎉 Your resume already covers the "
                    "detected skills required by this job!"
                )


            # ==================================================
            # DISCLAIMER
            # ==================================================

            st.divider()

            st.markdown(
                '<div class="home-disclaimer">'
                'The percentage is a TF-IDF text-similarity score, '
                'not a hiring prediction. Skill matching is based '
                'on a predefined beginner-friendly skill dictionary. '
                'The preparation roadmap is generated from predefined '
                'learning recommendations for detected skill gaps.'
                '</div>',
                unsafe_allow_html=True
            )


    # ========================================================
    # FOOTER
    # ========================================================

    st.markdown(
        '<div class="footer">'
        '🎯 HireMatch • Built with Python, Streamlit & NLP'
        '</div>',
        unsafe_allow_html=True
    )