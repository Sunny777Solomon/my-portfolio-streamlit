# app.py
import streamlit as st
from PIL import Image
import os
import importlib

from utils import link_button, github_link_button

st.set_page_config(page_title="Sunny Solomon | Portfolio", page_icon="🌙", layout="wide")

# ---------- Helpers ----------
def local_asset(path, fallback="https://via.placeholder.com/200"):
    return path if os.path.exists(path) else fallback

# ---------- Sidebar ----------
with st.sidebar:
    prof = local_asset("assets/profile.jpg")
    st.image(prof, width=220)
    st.title("Sunny Solomon")
    st.write("Data Science · UI/UX · Music")
    st.write("Hyderabad, India")
    st.write("📧 sunnysolomon20@gmail.com")
    link_button("https://www.linkedin.com/in/sunny-solomon/", "LinkedIn")
    link_button("https://github.com/Sunny777Solomon", "GitHub")
    st.markdown("---")
    st.markdown("**Quick Links**")
    link_button("#about", "About")
    link_button("#projects", "Projects")
    link_button("#demo", "ML Demo")
    link_button("#contact", "Contact")

# ---------- Main landing (ABOUT first) ----------
st.markdown("<a id='about'></a>", unsafe_allow_html=True)
col1, col2 = st.columns([2,1])
with col1:
    st.title("👋 Hi, I'm Sunny Solomon")
    st.subheader("Data Science & UI/UX Enthusiast | Creative Thinker | Problem Solver")
    st.write(
        """
I’m a Life Sciences graduate who blends creativity with analytical thinking. I’ve worked at **Synchrony Financial** and **Concentrix (Google Operations)**, where I developed strong communication, problem-solving, and attention-to-detail.

I build ML models, design UI/UX prototypes, and enjoy performing music in my free time. My current focus is on **interpretable ML**, **data visualization**, and **user-centered design**.
"""
    )
    st.markdown("**Highlights**")
    st.write("- Closed high-volume transactions in a pilot team at Synchrony Financial.\n- Supported YouTube TV customers at Concentrix (Google).\n- Built machine learning demos and UI prototypes; comfortable with Python, Adobe XD, and data visualization.")

    st.markdown("**Education**")
    st.write("B.Sc. in Biotechnology, Genetics & Chemistry — Bhavans Vivekananda Degree College")

    st.markdown("**Skills**")
    st.write("Python | Pandas | scikit-learn | Matplotlib | Adobe XD | UI/UX Design | MS Excel | Statistics | Data Visualization")

    # Resume download (add the PDF to assets/)
    if os.path.exists("assets/Sunny_Solomon_Resume.pdf"):
        with open("assets/Sunny_Solomon_Resume.pdf", "rb") as f:
            st.download_button("📄 Download Resume", f, file_name="Sunny_Solomon_Resume.pdf")
    else:
        st.info("Upload `assets/Sunny_Solomon_Resume.pdf` to enable resume download")

with col2:
    hero = local_asset("assets/hero.png")
    st.image(hero, use_column_width=True)

st.markdown("---")

# ---------- Projects Section ----------
st.markdown("<a id='projects'></a>", unsafe_allow_html=True)
st.header("🧩 Projects & Case Studies")

proj1_col, proj2_col = st.columns(2)
with proj1_col:
    st.subheader("Breast Cancer Risk Prediction")
    p1_img = local_asset("assets/project1.png")
    st.image(p1_img, use_column_width=True)
    st.write("Predictive model for 10-year risk estimation. Includes data preprocessing, model training, and visualization. (Demo available)")
    github_link_button("Sunny777Solomon", "Breast-cancer-Risk-Prediction-streamlit", "Open Repo")
    link_button("#demo", "Open Demo")

with proj2_col:
    st.subheader("Solo Leveling — Habit Tracker (UI/UX)")
    p2_img = local_asset("assets/project2.png")
    st.image(p2_img, use_column_width=True)
    st.write("Dark-theme habit tracker concept with level-up mechanics, created in Adobe XD. Includes user flows and prototypes.")
    # replace with your real Behance link if you have one:
    link_button("https://www.behance.net/", "View Design")

st.markdown("---")

# ---------- ML Demo Section (calls bc_app if present) ----------
st.markdown("<a id='demo'></a>", unsafe_allow_html=True)
st.header("🧪 Interactive ML Demo")
st.write("Try a lightweight demo of the breast cancer classifier. (Your full app can be integrated here.)")

# attempt to import bc_app and call run() if it exists
try:
    bc_app = importlib.import_module("bc_app")
    if hasattr(bc_app, "run"):
        bc_app.run()
    else:
        st.warning("Found bc_app module but no run() function. Please wrap your app in def run(): ...")
except Exception:
    st.info("No `bc_app.py` found in repo. To integrate your ready BC Streamlit app, create `bc_app.py` and expose a `run()` function. Or deploy the BC demo separately and link to it.")

st.markdown("---")

# ---------- Contact ----------
st.markdown("<a id='contact'></a>", unsafe_allow_html=True)
st.header("📫 Get in touch")
col1, col2, col3 = st.columns([1,1,1])
with col1:
    link_button("https://www.linkedin.com/in/sunny-solomon/", "LinkedIn")
with col2:
    link_button("https://github.com/Sunny777Solomon", "GitHub")
with col3:
    st.markdown("[📧 Email me](mailto:sunnysolomon20@gmail.com)")

st.markdown("---")
st.caption("© 2025 Sunny Solomon | Built with Streamlit")
