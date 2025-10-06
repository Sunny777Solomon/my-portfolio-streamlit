import streamlit as st
import os
from dataclasses import dataclass
from typing import List, Optional
import datetime

# ============================================================================
# PAGE CONFIGURATION
# ============================================================================
st.set_page_config(
    page_title="Sunny Solomon — Portfolio",
    page_icon="🌙",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ============================================================================
# DATA MODELS
# ============================================================================
@dataclass
class Project:
    title: str
    subtitle: str
    description: str
    deliverables: List[str]
    tools: List[str]
    links: dict
    tags: List[str]
    image: Optional[str] = None

# ============================================================================
# STYLING
# ============================================================================
def load_css():
    st.markdown("""
    <style>
    /* ========== Base Styles ========== */
    .stApp {
        background: radial-gradient(circle at 10% 20%, #071226 0%, #05050a 40%, #030305 100%);
        color: #e6eef8;
        font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    .main > div {
        max-width: 980px;
        margin: 0 auto;
        padding: 20px;
    }

    /* ========== Navigation ========== */
    div[data-testid="column"] button {
        width: 100%;
        border-radius: 999px;
        font-weight: 600;
        transition: all 0.18s ease;
        border: 1px solid rgba(60,130,255,0.12);
        background: transparent;
        color: #dff0ff;
    }

    div[data-testid="column"] button:hover {
        transform: translateY(-2px);
        background: linear-gradient(90deg, rgba(10,32,86,0.6), rgba(8,16,40,0.4));
        box-shadow: 0 10px 30px rgba(15,55,140,0.25);
        border-color: rgba(60,150,255,0.26);
    }

    /* ========== Cards ========== */
    .card {
        background: linear-gradient(180deg, rgba(9,18,34,0.55), rgba(6,10,20,0.44));
        border-radius: 12px;
        padding: 24px;
        border: 1px solid rgba(255,255,255,0.03);
        margin-bottom: 16px;
        box-shadow: 0 6px 20px rgba(2,8,20,0.6);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(10, 40, 100, 0.4);
    }

    /* ========== Hero Section ========== */
    .hero-container {
        display: flex;
        gap: 32px;
        align-items: center;
        margin-bottom: 32px;
        padding: 24px;
        background: linear-gradient(180deg, rgba(9,18,34,0.55), rgba(6,10,20,0.44));
        border-radius: 16px;
        border: 1px solid rgba(255,255,255,0.03);
    }

    .hero-image {
        width: 180px;
        height: 180px;
        border-radius: 16px;
        overflow: hidden;
        box-shadow: 0 12px 40px rgba(10,30,80,0.6);
        border: 2px solid rgba(190,227,255,0.2);
        animation: floaty 6s ease-in-out infinite;
        flex-shrink: 0;
    }

    @keyframes floaty {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-8px); }
    }

    .hero-title {
        font-size: 32px;
        font-weight: 800;
        color: #e7f5ff;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        font-size: 16px;
        color: #bcd9ff;
        margin-bottom: 16px;
    }

    .hero-description {
        color: #a9cbe8;
        line-height: 1.6;
        margin-bottom: 20px;
    }

    /* ========== Buttons ========== */
    .action-btn {
        display: inline-block;
        background: linear-gradient(90deg, #0b5cff, #2ea0ff);
        color: white;
        padding: 10px 20px;
        border-radius: 999px;
        text-decoration: none;
        font-weight: 700;
        margin-right: 10px;
        margin-top: 8px;
        transition: all 0.2s ease;
    }

    .action-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(11,92,255,0.4);
        text-decoration: none;
        color: white;
    }

    /* ========== Project Tags ========== */
    .project-tag {
        background: rgba(11,92,255,0.2);
        color: #5db4ff;
        padding: 6px 12px;
        border-radius: 12px;
        font-size: 12px;
        margin-right: 8px;
        margin-bottom: 8px;
        display: inline-block;
        border: 1px solid rgba(11,92,255,0.3);
    }

    /* ========== Tech Stack ========== */
    .tech-item {
        background: rgba(60,130,255,0.15);
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        margin: 4px;
        border: 1px solid rgba(60,130,255,0.2);
        transition: all 0.2s ease;
    }

    .tech-item:hover {
        background: rgba(60,130,255,0.25);
        transform: translateY(-2px);
    }

    /* ========== Info Cards ========== */
    .info-card {
        background: linear-gradient(135deg, rgba(11,92,255,0.1), rgba(46,160,255,0.05));
        padding: 20px;
        border-radius: 12px;
        border: 1px solid rgba(60,130,255,0.2);
        text-align: center;
    }

    .info-card strong {
        color: #5db4ff;
        font-size: 14px;
        display: block;
        margin-bottom: 8px;
    }

    .info-card-content {
        color: #bcdcff;
        font-size: 15px;
    }

    /* ========== Expander Styling ========== */
    .streamlit-expanderHeader {
        background: linear-gradient(90deg, rgba(11,92,255,0.1), rgba(46,160,255,0.05));
        border-radius: 8px;
        border: 1px solid rgba(60,130,255,0.2);
        font-weight: 600;
        color: #e7f5ff;
    }

    /* ========== Section Headers ========== */
    h1, h2, h3 {
        color: #e7f5ff;
    }

    /* ========== Mobile Responsive ========== */
    @media (max-width: 768px) {
        .hero-container {
            flex-direction: column;
            text-align: center;
        }

        .hero-image {
            width: 140px;
            height: 140px;
        }

        .hero-title {
            font-size: 24px;
        }

        .hero-subtitle {
            font-size: 14px;
        }

        div[data-testid="column"] {
            min-width: 100% !important;
        }
    }

    /* ========== Animations ========== */
    .fade-in {
        animation: fadeUp 0.85s ease both;
    }

    @keyframes fadeUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* ========== Hide Streamlit Branding ========== */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================
@st.cache_data
def local_asset(path, fallback="https://via.placeholder.com/400x400.png?text=Profile"):
    """Check if local asset exists, return fallback if not"""
    return path if os.path.exists(path) else fallback

# ============================================================================
# COMPONENT FUNCTIONS
# ============================================================================
def render_navigation():
    """Render navigation bar"""
    st.markdown("<div style='margin-bottom: 20px;'>", unsafe_allow_html=True)
    
    nav_items = [
        ("🏠", "home"),
        ("👤", "about"),
        ("🚀", "projects"),
        ("💡", "skills"),
        ("📚", "courses"),
        ("🎓", "education"),
        ("💼", "experience"),
        ("📬", "contact"),
    ]
    
    cols = st.columns(len(nav_items))
    for idx, (icon, key) in enumerate(nav_items):
        with cols[idx]:
            button_type = "primary" if st.session_state.get("page") == key else "secondary"
            if st.button(icon, key=f"nav_{key}", use_container_width=True, type=button_type):
                st.session_state["page"] = key
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_project_card(project: Project, expanded: bool = False):
    """Render an individual project card"""
    with st.expander(f"🚀 {project.title}", expanded=expanded):
        st.markdown(f"**{project.subtitle}**")
        
        # Tags
        if project.tags:
            tags_html = "".join([f'<span class="project-tag">{tag}</span>' for tag in project.tags])
            st.markdown(tags_html, unsafe_allow_html=True)
        
        st.write(project.description)
        
        # Deliverables
        if project.deliverables:
            st.markdown("**📦 Key Deliverables**")
            for item in project.deliverables:
                st.markdown(f"- {item}")
        
        # Tools
        if project.tools:
            st.markdown("**🛠️ Tech Stack**")
            tool_cols = st.columns(min(4, len(project.tools)))
            for idx, tool in enumerate(project.tools):
                with tool_cols[idx % len(tool_cols)]:
                    st.markdown(f'<div class="tech-item">{tool}</div>', unsafe_allow_html=True)
        
        # Links
        if project.links:
            st.markdown("**🔗 Links**")
            link_html = "".join([
                f'<a href="{url}" target="_blank" class="action-btn">{label}</a>'
                for label, url in project.links.items()
            ])
            st.markdown(link_html, unsafe_allow_html=True)

# ============================================================================
# PAGE CONTENT
# ============================================================================
def render_home():
    """Home page content"""
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    
    # Hero Section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        <div class="hero-title">Hey — I'm <span style="color:#BEE3FF">Sunny Solomon</span> 👋</div>
        <div class="hero-subtitle">Data Science · UI/UX · Music</div>
        <div class="hero-description">
        I build interpretable ML models and user-centered experiences. Welcome to my interactive 
        portfolio where you can explore my projects, skills, and professional journey.
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <a href="#" class="action-btn" onclick="return false;">View Projects</a>
        <a href="#" class="action-btn" onclick="return false;">Contact Me</a>
        """, unsafe_allow_html=True)
    
    with col2:
        profile_path = local_asset("assets/profile.jpg")
        st.markdown(f'<div class="hero-image"><img src="{profile_path}" style="width:100%;height:100%;object-fit:cover;"></div>', unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Info Cards
    st.markdown("<div style='margin-top: 24px;'>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="info-card">
            <strong>Current Focus</strong>
            <div class="info-card-content">Interpretable ML<br>Survival Analysis<br>Data Viz</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="info-card">
            <strong>Location</strong>
            <div class="info-card-content">Hyderabad, India</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="info-card">
            <strong>Contact</strong>
            <div class="info-card-content">sunnysolomon20<br>@gmail.com</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_about():
    """About page content"""
    st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
    st.header("About — Sunny Solomon")
    
    st.write("""
I'm Sunny Solomon — a Data Science and UI/UX enthusiast from Hyderabad, India.

With a background in Life Sciences and a growing passion for AI, Machine Learning, and Data Visualization, 
I'm focused on transforming complex data into clear, actionable insights that drive impact.

I enjoy blending analytical thinking with creativity, designing meaningful interfaces, and building 
intelligent, user-centered solutions. Currently, I'm expanding my skills in machine learning, generative 
AI, and forecasting analytics, while continuously exploring ways to make data more human and intuitive.

**Outside of work:**  
I'm a musician at heart — a guitarist, keyboard player, and singer who finds rhythm in every detail. 
I also love football, gaming, and working out, which keep me motivated and balanced.

**My goal:**  
To keep learning, innovating, and creating — whether through data, design, or music.
""")
    
    st.markdown("---")
    st.markdown("**Quick Facts**")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("🎓 B.Sc. Biotechnology, Genetics & Chemistry")
        st.write("📍 Hyderabad, Telangana, India")
        st.write("🎂 Born April 26, 2002")
    
    with col2:
        st.write("🎸 Musician (Guitar, Keyboard, Vocals)")
        st.write("⚽ Football Enthusiast")
        st.write("🎮 Gamer & Fitness Buff")
    
    # Resume Download
    if os.path.exists("assets/Sunny_Solomon_Resume.pdf"):
        with open("assets/Sunny_Solomon_Resume.pdf", "rb") as f:
            st.download_button(
                "📄 Download Resume",
                f,
                file_name="Sunny_Solomon_Resume.pdf",
                mime="application/pdf",
                use_container_width=True
            )
    else:
        st.info("📄 Resume available upon request")
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_projects():
    """Projects page content"""
    st.markdown('<div class="fade-in">', unsafe_allow_html=True)
    st.header("Projects & Case Studies")
    st.write("Explore my featured work across data science, machine learning, and UI/UX design.")
    
    projects = [
        Project(
            title="Breast Cancer Risk Prediction",
            subtitle="Survival Analysis & Machine Learning",
            description="""
            A comprehensive predictive model estimating 10-year mortality risk for breast cancer patients 
            using clinical and demographic data. This project combines survival analysis techniques 
            (Kaplan-Meier, Cox PH) with modern machine learning algorithms to enhance prediction accuracy.
            """,
            deliverables=[
                "Data preprocessing & feature engineering pipeline",
                "Survival curves & hazard visualization (Kaplan-Meier plots)",
                "Comparative analysis of statistical vs. ML approaches",
                "Interactive risk prediction interface with patient input"
            ],
            tools=["Python", "Pandas", "NumPy", "scikit-learn", "XGBoost", "lifelines", "Matplotlib"],
            links={
                "GitHub": "https://github.com/Sunny777Solomon/Breast-cancer-Risk-Prediction-streamlit",
                "Live Demo": "#demo"
            },
            tags=["Healthcare", "Machine Learning", "Survival Analysis", "Python", "Data Science"]
        ),
        Project(
            title="Solo Leveling — Habit Tracker",
            subtitle="UI/UX Design & Gamification",
            description="""
            A dark-themed habit tracker application concept inspired by RPG mechanics. Features level-up 
            systems, quest-based achievements, and immersive user experience design. Built with modern 
            design principles and gamification psychology.
            """,
            deliverables=[
                "High-fidelity interactive prototypes",
                "User flows & journey mapping",
                "Interaction specifications & micro-animations",
                "Design system documentation"
            ],
            tools=["Adobe XD", "Figma", "Kivy", "Python"],
            links={
                "Behance": "https://www.behance.net/",
                "Prototype": "#"
            },
            tags=["UI/UX", "Mobile Design", "Gamification", "Prototyping"]
        ),
    ]
    
    for idx, project in enumerate(projects):
        render_project_card(project, expanded=(idx == 0))
        st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_skills():
    """Skills page content"""
    st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
    st.header("Skills & Expertise")
    st.write("A comprehensive overview of technical and soft skills I bring to every project.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("💻 Technical")
        st.markdown("""
        - **Languages:** Python, SQL
        - **Data Science:** Pandas, NumPy, scikit-learn
        - **ML/AI:** XGBoost, TensorFlow basics
        - **Survival Analysis:** lifelines
        - **Visualization:** Matplotlib, Seaborn, Plotly
        - **Tools:** Jupyter, Git, Streamlit
        """)
    
    with col2:
        st.subheader("🎨 Design")
        st.markdown("""
        - **UI/UX Design:** Adobe XD, Figma
        - **Prototyping:** Interactive mockups
        - **Design Systems:** Component libraries
        - **User Research:** Journey mapping
        - **Wireframing:** Low to high fidelity
        - **Visual Design:** Typography, color theory
        """)
    
    with col3:
        st.subheader("🤝 Soft Skills")
        st.markdown("""
        - **Communication:** Clear & effective
        - **Problem Solving:** Analytical thinking
        - **Collaboration:** Cross-functional teams
        - **Presentation:** Data storytelling
        - **Adaptability:** Quick learner
        - **Leadership:** Team coordination
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_courses():
    """Courses page content"""
    st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
    st.header("Courses & Certifications")
    st.write("Continuous learning through structured courses and professional development.")
    
    courses = [
        {
            "name": "Survival Analysis & Time-to-Event Modeling",
            "provider": "Boston Institute of Analytics",
            "status": "Completed",
            "year": "2024"
        },
        {
            "name": "UI/UX Design Fundamentals",
            "provider": "Adobe XD",
            "status": "Completed",
            "year": "2023"
        },
        {
            "name": "Python for Data Science",
            "provider": "Online Course",
            "status": "Completed",
            "year": "2023"
        },
        {
            "name": "Machine Learning Specialization",
            "provider": "In Progress",
            "status": "Ongoing",
            "year": "2024"
        }
    ]
    
    for course in courses:
        with st.expander(f"📚 {course['name']}"):
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**Provider:** {course['provider']}")
                st.write(f"**Status:** {course['status']}")
            with col2:
                st.write(f"**Year:** {course['year']}")
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_education():
    """Education page content"""
    st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
    st.header("Education")
    st.write("Academic background and formal qualifications.")
    
    education = [
        {
            "degree": "B.Sc. Biotechnology, Genetics & Chemistry",
            "institution": "Bhavans Vivekananda Degree College",
            "period": "2019 - 2022",
            "details": "Focus on life sciences with strong foundation in scientific methodology"
        },
        {
            "degree": "Intermediate (12th Grade)",
            "institution": "Sri Chaitanya Junior College",
            "period": "2017 - 2019",
            "details": "Science stream with emphasis on Biology and Chemistry"
        },
        {
            "degree": "Secondary Education (10th Grade)",
            "institution": "Buds and Flowers High School",
            "period": "Till 2017",
            "details": "Strong academic foundation"
        }
    ]
    
    for edu in education:
        st.markdown(f"### 🎓 {edu['degree']}")
        st.write(f"**{edu['institution']}** | *{edu['period']}*")
        st.write(edu['details'])
        st.markdown("---")
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_experience():
    """Experience page content"""
    st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
    st.header("Professional Experience")
    st.write("Work history and professional achievements.")
    
    experiences = [
        {
            "title": "Junior Associate",
            "company": "Synchrony Financial",
            "period": "Sep 2022 – May 2023",
            "responsibilities": [
                "Part of a pilot team handling high-volume financial transactions",
                "Worked with international clients on complex account management",
                "Resolved escalations efficiently with focus on customer satisfaction",
                "Gained expertise in process-driven operations and compliance"
            ]
        },
        {
            "title": "Customer Service Representative",
            "company": "Concentrix (Google Operations)",
            "period": "Jul 2023 – Oct 2023",
            "responsibilities": [
                "Provided technical and non-technical support for YouTube TV customers",
                "Maintained high CSAT scores through efficient troubleshooting",
                "Handled complex customer inquiries with professionalism",
                "Collaborated with cross-functional teams for issue resolution"
            ]
        }
    ]
    
    for exp in experiences:
        st.markdown(f"### 💼 {exp['title']}")
        st.write(f"**{exp['company']}** | *{exp['period']}*")
        for resp in exp['responsibilities']:
            st.write(f"- {resp}")
        st.markdown("---")
    
    st.markdown("</div>", unsafe_allow_html=True)

def render_contact():
    """Contact page content"""
    st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
    st.header("Let's Connect")
    st.write("I'm open to collaborations, freelance opportunities, and exciting projects. Reach out!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <a href="https://www.linkedin.com/in/sunny-solomon/" target="_blank" class="action-btn" style="display:block;text-align:center;margin-bottom:12px">
        LinkedIn
        </a>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <a href="https://github.com/Sunny777Solomon" target="_blank" class="action-btn" style="display:block;text-align:center;margin-bottom:12px">
        GitHub
        </a>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <a href="mailto:sunnysolomon20@gmail.com" class="action-btn" style="display:block;text-align:center;margin-bottom:12px">
        Email
        </a>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Contact Form
    st.subheader("📬 Send a Message")
    with st.form("contact_form"):
        name = st.text_input("Your Name")
        email = st.text_input("Your Email")
        subject = st.text_input("Subject")
        message = st.text_area("Message", height=150)
        
        submitted = st.form_submit_button("Send Message", use_container_width=True)
        
        if submitted:
            if name and email and message:
                st.success("✅ Thank you! I'll get back to you soon.")
                st.balloons()
            else:
                st.error("Please fill in all required fields.")
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Demo Integration Section
    st.markdown('<div class="card fade-in">', unsafe_allow_html=True)
    st.subheader("🔬 Live Demo: Breast Cancer Risk Prediction")
    st.write("Try the interactive demo of my breast cancer risk prediction model.")
    
    try:
        import bc_app
        if hasattr(bc_app, "run"):
            st.info("Loading interactive demo...")
            bc_app.run()
        else:
            st.warning("Demo module found but run() function not available.")
    except ImportError:
        st.info("""
        **Demo Integration Instructions:**
        
        To add the live Breast Cancer Risk Prediction demo:
        1. Create a file named `bc_app.py` in the same directory
        2. Add a `def run():` function that contains your Streamlit app code
        3. The demo will automatically load in this section
        
        Or visit the standalone demo at: 
        [GitHub Repository](https://github.com/Sunny777Solomon/Breast-cancer-Risk-Prediction-streamlit)
        """)
    
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================================
# MAIN APPLICATION
# ============================================================================
def main():
    # Load custom CSS
    load_css()
    
    # Initialize session state
    if "page" not in st.session_state:
        st.session_state["page"] = "home"
    
    # Render navigation
    render_navigation()
    
    # Route to appropriate page
    current_page = st.session_state["page"]
    
    if current_page == "home":
        render_home()
    elif current_page == "about":
        render_about()
    elif current_page == "projects":
        render_projects()
    elif current_page == "skills":
        render_skills()
    elif current_page == "courses":
        render_courses()
    elif current_page == "education":
        render_education()
    elif current_page == "experience":
        render_experience()
    elif current_page == "contact":
        render_contact()
    
    # Footer
    st.markdown("---")
    st.markdown(f"""
    <div style="text-align:center;color:#7fb0e7;padding:20px 0;">
        © {datetime.datetime.now().year} Sunny Solomon — Built with ❤️ using Streamlit
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
