# app.py
import streamlit as st
import os
import importlib
from PIL import Image
import datetime

# ---------------- Page config ----------------
st.set_page_config(
    page_title="Sunny Solomon — Portfolio",
    page_icon="🌙",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ---------------- CSS: Dark theme + animations ----------------
st.markdown(
    """
    <style>
    /* Page background - subtle gradient */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #071226 0%, #05050a 40%, #030305 100%);
        color: #e6eef8;
        font-family: "Inter", sans-serif;
    }

    /* Center container width */
    .main > div {
        max-width: 980px;
        margin: 0 auto;
    }

    /* Top nav */
    .nav {
        display:flex;
        justify-content:center;
        gap:10px;
        margin-bottom: 18px;
        margin-top: 10px;
    }
    .nav button {
        background: transparent;
        border: 1px solid rgba(60,130,255,0.12);
        color: #dff0ff;
        padding: 8px 14px;
        border-radius: 999px;
        font-weight: 600;
        cursor: pointer;
        transition: all .18s ease;
        box-shadow: 0 6px 18px rgba(3,8,26,0.6);
    }
    .nav button:hover {
        transform: translateY(-3px);
        background: linear-gradient(90deg, rgba(10,32,86,0.6), rgba(8,16,40,0.4));
        box-shadow: 0 10px 30px rgba(15,55,140,0.25);
        border-color: rgba(60,150,255,0.26);
    }
    .nav .active {
        background: linear-gradient(90deg,#062046, #0f2346);
        border: 1px solid rgba(60,140,255,0.35);
        box-shadow: 0 10px 30px rgba(10,40,100,0.45);
    }

    /* Hero */
    .hero {
        display:flex;
        gap:28px;
        align-items:center;
        margin-bottom: 18px;
    }
    .hero-left {
        flex:1;
    }
    .hero-right {
        width:180px;
        height:180px;
        border-radius: 16px;
        overflow:hidden;
        box-shadow: 0 12px 40px rgba(10,30,80,0.6);
        border: 1px solid rgba(255,255,255,0.03);
        animation: floaty 6s ease-in-out infinite;
    }
    @keyframes floaty {
        0% { transform: translateY(0px) }
        50% { transform: translateY(-8px) }
        100% { transform: translateY(0px) }
    }

    /* Hero text */
    .h1 {
        font-size:28px;
        font-weight:800;
        color: #e7f5ff;
        margin-bottom:6px;
    }
    .h2 {
        font-size:15px;
        color:#bcd9ff;
        margin-bottom:14px;
    }
    .lead {
        color:#a9cbe8;
        line-height:1.55;
        margin-bottom:12px;
    }

    /* Card style for sections */
    .card {
        background: linear-gradient(180deg, rgba(9,18,34,0.55), rgba(6,10,20,0.44));
        border-radius: 12px;
        padding: 18px;
        border: 1px solid rgba(255,255,255,0.03);
        margin-bottom: 14px;
        box-shadow: 0 6px 20px rgba(2,8,20,0.6);
    }

    /* Project cards grid */
    .projects {
        display:grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap:14px;
        margin-top:8px;
    }

    /* small link button */
    .linkbtn {
        display:inline-block;
        background: linear-gradient(90deg,#0b5cff,#2ea0ff);
        color: white;
        padding:8px 12px;
        border-radius: 999px;
        text-decoration:none;
        font-weight:700;
        margin-right:8px;
    }

    /* Small subtle fade in */
    .fade-in {
        animation: fadeUp .85s ease both;
    }
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(8px) }
        to { opacity: 1; transform: translateY(0px) }
    }

    /* footer */
    footer {opacity:0.8; color:#9fbbe6; margin-top:18px;}
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------- Helpers ----------------
def local_asset(path, fallback="https://via.placeholder.com/400x400.png?text=Sunny"):
    return path if os.path.exists(path) else fallback

def nav_button(label, key):
    """
    Render a top nav styled button and manage page state.
    """
    active = st.session_state.get("page", "home") == key
    classes = "active" if active else ""
    # Use HTML button so we can style centrally
    st.markdown(
        f"""<button class="{classes}" onclick="(function(){{document.dispatchEvent(new CustomEvent('nav', {{detail: '{key}'}}));}})()">{label}</button>""",
        unsafe_allow_html=True,
    )

# JS listener to bridge clicks to Streamlit (since we use HTML buttons)
# This snippet will post message to Streamlit via Streamlit's setComponentValue hack using location.hash
st.markdown(
    """
    <script>
    const handler = (e) => {
        // update location hash with page token
        location.hash = 'nav-' + e.detail;
    }
    document.addEventListener('nav', handler);

    // watch hash change and dispatch custom event for Streamlit to pick
    window.addEventListener('hashchange', () => {
        const v = location.hash.replace('#nav-','');
        if (typeof window.streamlitWebview !== 'undefined') {
            // legacy
        }
        // create a hidden input to pass to Streamlit on rerun
        const el = document.getElementById('streamlit_nav_input');
        if (el) {
            el.value = v;
            el.dispatchEvent(new Event('change'));
        } else {
            const input = document.createElement('input');
            input.id = 'streamlit_nav_input';
            input.value = v;
            input.style.display = 'none';
            input.onchange = function() { /* noop */ };
            document.body.appendChild(input);
        }
    }, false);
    </script>
    """,
    unsafe_allow_html=True,
)

# hidden input capturing hash - will be created on first hashchange by above script
st.markdown(
    """
    <input id="streamlit_nav_input" style="display:none" />
    <script>
    const el = document.getElementById('streamlit_nav_input');
    if (el) {
      el.addEventListener('change', (e) => {
         // trigger a Streamlit rerun by changing window.location.hash (already done)
      });
    }
    </script>
    """,
    unsafe_allow_html=True,
)

# sync hash into session_state if present
hash_val = st.experimental_get_query_params().get("nav", [None])[0]
# fallback to location hash via js -> but Streamlit can't directly read location.hash reliably,
# so we'll also allow user to click Streamlit buttons as backup.

# Initialize page
if "page" not in st.session_state:
    st.session_state["page"] = "home"

# If URL hash was set in previous interactions, keep it (best-effort)
# (Note: Streamlit can't read window.hash directly on server side reliably; users can still use nav.)
# Provide Streamlit-level top nav also (for keyboard / accessibility)
def set_page(p):
    st.session_state["page"] = p

# ---------------- Top Navigation (visual) ----------------
st.markdown("<div class='nav fade-in'>", unsafe_allow_html=True)
# We'll place HTML buttons (clicking them sets location.hash which the script picks up)
nav_items = [
    ("Home", "home"),
    ("About", "about"),
    ("Projects", "projects"),
    ("Skills", "skills"),
    ("Courses", "courses"),
    ("Education", "education"),
    ("Experience", "experience"),
    ("Contact", "contact"),
]
for label, key in nav_items:
    # Render as HTML button (styled) - we also render a hidden Streamlit button as fallback for state
    nav_button(label, key)
    # accessible fallback
    st.button(label, key=f"btn_{key}", on_click=set_page, args=(key,), help=f"Open {label}")
st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='card fade-in'>", unsafe_allow_html=True)

# ---------------- Home / Hero ----------------
if st.session_state["page"] == "home":
    # hero layout
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown('<div class="hero-left">', unsafe_allow_html=True)
        st.markdown('<div class="h1">Hey — I’m <span style="color:#BEE3FF">Sunny Solomon</span> 👋</div>', unsafe_allow_html=True)
        st.markdown('<div class="h2">Data Science · UI/UX · Music — I build interpretable ML & user-centered experiences.</div>', unsafe_allow_html=True)
        st.markdown('<div class="lead">Welcome! This interactive portfolio lets you explore my projects, skills, courses, and professional journey. Click any section above or use the buttons below to explore.</div>', unsafe_allow_html=True)

        # quick action buttons
        st.markdown(
            '<a class="linkbtn" href="#about" onclick="location.hash=\'nav-about\'">About</a>'
            '<a class="linkbtn" href="#projects" onclick="location.hash=\'nav-projects\'">Projects</a>'
            '<a class="linkbtn" href="#demo" onclick="location.hash=\'nav-projects\'">Live Demo</a>',
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
    with c2:
        # show profile image if available
        profile = local_asset("assets/profile.jpg")
        st.markdown(f'<div class="hero-right"><img src="{profile}" style="width:100%; height:100%; object-fit:cover;" /></div>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # short cards
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="card"><strong>Current Focus</strong><div style="margin-top:8px;color:#bcdcff">Interpretable ML • Survival Analysis • Data Viz • UI/UX</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="card"><strong>Location</strong><div style="margin-top:8px;color:#bcdcff">Hyderabad, India</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="card"><strong>Contact</strong><div style="margin-top:8px;color:#bcdcff">sunnysolomon20@gmail.com</div></div>', unsafe_allow_html=True)

    # small footer CTA
    st.markdown('<div style="text-align:center;margin-top:12px;color:#9fc6ff">Scroll or use the nav buttons above to explore the portfolio.</div>', unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- About ----------------
if st.session_state["page"] == "about":
    st.markdown("<div class='card fade-in'>", unsafe_allow_html=True)
    st.header("About — Sunny Solomon")
    st.write(
        """
I’m Sunny Solomon — a Data Science and UI/UX enthusiast from Hyderabad, India.

With a background in Life Sciences and a growing passion for AI, Machine Learning, and Data Visualization, I’m focused on transforming complex data into clear, actionable insights that drive impact.

I enjoy blending analytical thinking with creativity, designing meaningful interfaces, and building intelligent, user-centered solutions. Currently, I’m expanding my skills in machine learning, generative AI, and forecasting analytics, while continuously exploring ways to make data more human and intuitive.

Outside of work, I’m a musician at heart — a guitarist, keyboard player, and singer who finds rhythm in every detail. I also love football, gaming, and working out, which keep me motivated and balanced.

My goal is to keep learning, innovating, and creating — whether through data, design, or music.
"""
    )
    st.markdown("**Quick facts**")
    st.write("- B.Sc. Biotechnology, Genetics & Chemistry — Bhavans Vivekananda Degree College")
    st.write(f"- Age: 22 (Born April 26, 2002)")  # adjust if needed
    # Resume download
    if os.path.exists("assets/Sunny_Solomon_Resume.pdf"):
        with open("assets/Sunny_Solomon_Resume.pdf", "rb") as f:
            st.download_button("📄 Download Resume", f, file_name="Sunny_Solomon_Resume.pdf")
    else:
        st.info("Upload `assets/Sunny_Solomon_Resume.pdf` to enable resume download")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Projects ----------------
if st.session_state["page"] == "projects":
    st.markdown("<div class='card fade-in'>", unsafe_allow_html=True)
    st.header("Projects & Case Studies")
    st.write("Below are featured projects. Click each project to expand and see the details, tools, and links.")
    st.markdown('<div class="projects">', unsafe_allow_html=True)

    # Project: Breast Cancer Risk Prediction (expanded view)
    with st.expander("Breast Cancer Risk Prediction — Survival Analysis & Machine Learning", expanded=True):
        st.markdown("**Affiliation:** Associated with Boston Institute of Analytics")
        st.write(
            """
**Project summary:**  
This project aims to develop a predictive model that estimates the 10-year mortality risk for breast cancer patients using clinical and demographic data. 
It combines survival analysis (Kaplan-Meier, Cox PH) with machine learning algorithms (Random Forest, XGBoost, Logistic Regression) to enhance prediction accuracy.

**Workflow:**  
- Data preprocessing & feature engineering  
- Survival analysis (Kaplan-Meier plots, Cox proportional hazards)  
- Train & compare ML models (RandomForest, XGBoost, LogisticRegression)  
- Evaluate using C-index, ROC-AUC, calibration plots  
- Deliverables: survival curves, hazard visualization, comparative analysis, and an optional user-friendly interface for risk prediction
"""
        )
        st.markdown("**Key Deliverables**")
        st.write(
            """
- Data cleaning & preprocessing pipeline  
- Survival curves & hazard visualization  
- Comparative analysis (statistical vs. ML)  
- User-friendly demo for patient input & risk prediction
"""
        )
        st.markdown("**Tools & Technologies**")
        st.write("Python (Pandas, NumPy, Matplotlib, scikit-learn, lifelines), Jupyter Notebook, Data Visualization libraries")
        # repo link
        st.markdown('<a class="linkbtn" href="https://github.com/Sunny777Solomon/Breast-cancer-Risk-Prediction-streamlit" target="_blank">Open Repo</a>', unsafe_allow_html=True)
        st.markdown('<a class="linkbtn" href="#demo" onclick="location.hash=\'nav-projects\'">Open Demo</a>', unsafe_allow_html=True)

    # Add other project cards (example)
    with st.expander("Solo Leveling — Habit Tracker (UI/UX)", expanded=False):
        st.write(
            """
Dark-theme habit tracker concept with level-up mechanics and quest-based UX. Designed in Adobe XD.
- Deliverables: high-fidelity prototypes, user flows, interaction spec.
- Tools: Adobe XD, Figma, basic Kivy prototype (mobile).
"""
        )
        st.markdown('<a class="linkbtn" href="https://www.behance.net/" target="_blank">View Design</a>', unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Skills ----------------
if st.session_state["page"] == "skills":
    st.markdown("<div class='card fade-in'>", unsafe_allow_html=True)
    st.header("Skills")
    st.write("A snapshot of technical and soft skills I bring to the table.")
    tech, design, soft = st.columns(3)
    with tech:
        st.subheader("Technical")
        st.write("- Python\n- Pandas\n- NumPy\n- scikit-learn\n- XGBoost\n- lifelines (survival analysis)\n- Matplotlib / Seaborn\n- SQL")
    with design:
        st.subheader("Design")
        st.write("- UI/UX prototyping (Adobe XD, Figma)\n- Design systems\n- User flows & wireframing")
    with soft:
        st.subheader("Other")
        st.write("- Communication\n- Problem solving\n- Cross-functional collaboration\n- Presentation skills")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Courses / Certifications ----------------
if st.session_state["page"] == "courses":
    st.markdown("<div class='card fade-in'>", unsafe_allow_html=True)
    st.header("Courses & Certifications")
    st.write("Courses completed (list your certificates here):")
    st.write(
        """
- Survival Analysis & Time-to-Event Modeling — [Boston Institute of Analytics]  
- UI/UX Design Course — Adobe XD (completed)  
- Python for Data Science — (course name / provider)  
- (Add any Coursera / Udemy / edX certs here)
"""
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Education ----------------
if st.session_state["page"] == "education":
    st.markdown("<div class='card fade-in'>", unsafe_allow_html=True)
    st.header("Education")
    st.write("Formal education and relevant academic details.")
    st.write("- **B.Sc. Biotechnology, Genetics & Chemistry** — Bhavans Vivekananda Degree College (Year)") 
    st.write("- **Sri Chaitanya Junior College** (2017–2019)")
    st.write("- **Buds and Flowers High School**")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Experience ----------------
if st.session_state["page"] == "experience":
    st.markdown("<div class='card fade-in'>", unsafe_allow_html=True)
    st.header("Experience")
    st.subheader("Synchrony Financial — Junior Associate (Sep 2022 – May 2023)")
    st.write("- Part of a pilot team that handled high-volume transactions.\n- Worked with international clients and resolved escalations.\n- Gained experience in process-driven operations and communication.")
    st.subheader("Concentrix (Google Operations) — CSR (Jul 2023 – Oct 2023)")
    st.write("- Supported YouTube TV customers with technical and non-technical issues.\n- Maintained high CSAT through efficient troubleshooting.")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Contact / Socials / Demo integration ----------------
if st.session_state["page"] == "contact":
    st.markdown("<div class='card fade-in'>", unsafe_allow_html=True)
    st.header("Contact & Links")
    st.write("Let's connect — I'm open to collaborations, freelance work, and opportunities.")
    c1, c2, c3 = st.columns([1,1,1])
    with c1:
        st.markdown('<a class="linkbtn" href="https://www.linkedin.com/in/sunny-solomon/" target="_blank">LinkedIn</a>', unsafe_allow_html=True)
    with c2:
        st.markdown('<a class="linkbtn" href="https://github.com/Sunny777Solomon" target="_blank">GitHub</a>', unsafe_allow_html=True)
    with c3:
        st.markdown('<a class="linkbtn" href="mailto:sunnysolomon20@gmail.com" target="_blank">Email</a>', unsafe_allow_html=True)

    st.markdown("<hr/>", unsafe_allow_html=True)
    st.write("Live demo integration:")
    # attempt to import bc_app and call run() if it exists
    try:
        bc_app = importlib.import_module("bc_app")
        if hasattr(bc_app, "run"):
            st.markdown("Found `bc_app` — launching demo below.")
            bc_app.run()
        else:
            st.warning("Found bc_app module but no run() function. Please wrap your BC app into def run():")
    except Exception:
        st.info("If you want the live Breast Cancer demo embedded here, add `bc_app.py` to this repo exposing `def run()` (I can generate a wrapper).")

    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- Footer ----------------
st.markdown(
    f"""
    <div style="text-align:center;margin-top:18px;color:#7fb0e7">
      © {datetime.datetime.now().year} Sunny Solomon — Built with Streamlit
    </div>
    """,
    unsafe_allow_html=True,
)
