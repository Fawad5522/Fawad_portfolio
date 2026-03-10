# =========================
# Fawad Ahmad Portfolio App
# =========================
import streamlit as st
from pathlib import Path
import zipfile
import requests
from PIL import Image

# -------------------------
# 1) PAGE SETTINGS
# -------------------------
st.set_page_config(
    page_title="Fawad Ahmad Portfolio",
    page_icon="📊",
    layout="wide",
)

# -------------------------
# 2) BASIC DATA
# -------------------------
BASE_DIR = Path(__file__).parent

FILES = {
    "profile_image": "portfolio image.jpeg",
    "resume_pdf": "fawad-data-analyst.pdf",
    "internship_certificate": "Fawad Ahmad Data Science Certificate.pdf",
    "recommendation_letter": "Fawad Ahmad Data Science Recommendation.pdf",
    "fyp_zip": "FawadFyp.zip",
    "societies_zip": "Edwardes Societies pics.zip",
}

PROFILE = {
    "name": "Fawad Ahmad",
    "headline": "Aspiring Data Analyst | Python, SQL, Power BI",
    "short_intro": (
        "Motivated Computer Science graduate with a keen interest in "
        "Data Science, Python, Data Analysis, and Business Intelligence."
    ),
    "about": (
        "I am Fawad Ahmad, a BS Computer Science graduate from Edwardes College "
        "Peshawar affiliated with the University of Peshawar. I enjoy solving "
        "real-world problems through data analysis, dashboard development, and "
        "practical programming projects using Python, Power BI, SQL, and Excel. "
        "Alongside technical work, I have actively participated in college societies "
        "where I developed leadership, communication, teamwork, and event management skills."
    ),
    "college": "Edwardes College Peshawar",
    "degree": "BS Computer Science",
    "status": "Graduate",
    "email": "fadeejaan846@gmail.com",
    "phone": "03326085485",
    "linkedin": "https://www.linkedin.com/in/fawad-ahmad-86aa312b1",
    "github": "https://github.com/Fawad5522",
    "github_username": "Fawad5522",
}

FYP_INFO = {
    "title": "A Business Intelligence–Driven Analysis of Retail Sales Using Power BI",
    "summary": (
        "This project focuses on analyzing retail sales data using Business Intelligence "
        "techniques to uncover insights about product performance, customer behavior, "
        "regional sales trends, and time-based patterns. The work included data cleaning, "
        "star schema modeling, and interactive dashboard development in Power BI."
    ),
    "tools": ["Power BI", "Python", "Excel", "SQL Concepts", "Star Schema Modeling"],
    
    "methodology": [
        "Collect and understand retail sales data",
        "Clean and prepare the dataset",
        "Build star schema structure for analysis",
        "Create interactive dashboards in Power BI",
        "Analyze product, customer, category, and regional trends",
        "Present business insights for decision-making",
    ],
    
    "highlights": [
        "Product and category performance analysis",
        "Customer insights dashboard",
        "Regional analysis dashboard",
        "Sub-category comparison",
        "Temporal and operational trends",
        "Star schema design for structured BI analysis",
    ],
}

SKILLS = {
    "Technical Skills": [
        "Python",
        "C++",
        "Power BI",
        "SQL",
        "Excel",
        "Streamlit",
        "Frontend Web",
    ],
    "Research & Analytical Skills": [
        "Thesis Writing",
        "Literature Review",
        "Data Analysis",
        "Data Science",
        "Data Cleaning",
        "Dashboard Storytelling",
    ],
    "Soft Skills": [
        "Communication",
        "Teamwork",
        "Presentation",
        "Leadership",
        "Problem Solving",
    ],
}

SOCIETIES = {
    "Tech Tribe Society": {
        "role": "President",
        "description": (
            "Organized seminars on the realm of technology and cyber security awareness 101."
        ),
        "keywords": ["tech tribe", "cyber"],
    },
    "Pashto Society": {
        "role": "Deputy Chief / Joint Secretary",
        "description": (
            "Organized seminars on poetry, poets, writers, and annual culture day "
            "to promote culture and language."
        ),
        "keywords": ["pashto society", "culture"],
    },
    "Dramatic Society": {
        "role": "Actor",
        "description": (
            "Performed in The Saga of Khushal Khan Khattak, Macbeth, and Troy."
        ),
        "keywords": ["dramatic","Dramatic", "macbeth", "troy", "khusahal", "khushal"],
    },
    "English Literary Society": {
        "role": "Creative Strategist / Deputy Coordinator",
        "description": (
            "Participated in movie discussions, open discussions on national heroes, "
            "writers, and poetry."
        ),
        "keywords": ["english literary","English Literary" ],
    },
}

# -------------------------
# 3) HELPER FUNCTIONS
# -------------------------
def file_path(filename: str) -> Path:
    """Return full path of a file in the same folder as app.py."""
    return BASE_DIR / filename


def extract_zip_if_needed(zip_file: Path, output_folder_name: str) -> Path | None:
    """
    Extract zip only once.
    If folder already exists, it reuses it.
    """
    output_dir = BASE_DIR / output_folder_name

    if not zip_file.exists():
        return None

    if not output_dir.exists():
        output_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zip_file, "r") as zf:
            zf.extractall(output_dir)

    return output_dir


def find_first_folder(root: Path | None, folder_name: str) -> Path | None:
    """Find the first folder with a matching name anywhere inside root."""
    if root is None or not root.exists():
        return None

    for item in root.rglob("*"):
        if item.is_dir() and item.name.lower() == folder_name.lower():
            return item
    return None


def find_first_file(root: Path | None, patterns: list[str]) -> Path | None:
    """Find first file matching any pattern."""
    if root is None or not root.exists():
        return None

    for pattern in patterns:
        matches = list(root.rglob(pattern))
        if matches:
            return matches[0]
    return None


def find_images(root: Path | None, keywords=None) -> list[Path]:
    """Find image files optionally filtered by keywords in filename."""
    if root is None or not root.exists():
        return []

    images = []
    for pattern in ["*.jpg", "*.jpeg", "*.png", "*.webp", "*.JPG", "*.JPEG", "*.PNG", "*.WEBP"]:
        images.extend(root.rglob(pattern))

    if keywords:
        filtered = []
        for img in images:
            name = img.name.lower()
            if any(keyword.lower() in name for keyword in keywords):
                filtered.append(img)
        images = filtered

    return sorted(images, key=lambda x: x.name.lower())


def show_download_button(path: Path | None, label: str, key: str):
    """Show download button if file exists."""
    if path and path.exists():
        with open(path, "rb") as f:
            st.download_button(
                label=label,
                data=f,
                file_name=path.name,
                mime="application/octet-stream",
                key=key,
                use_container_width=True,
            )
    else:
        st.warning(f"{label} file not found.")


@st.cache_data(show_spinner=False)
def get_github_repos(username: str):
    """
    Get public GitHub repos using GitHub API.
    This makes the Projects page dynamic.
    """
    url = f"https://api.github.com/users/{username}/repos?sort=updated&per_page=100"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        repos = response.json()

        # Remove forks so only your main repos show
        repos = [repo for repo in repos if not repo.get("fork", False)]

        # Sort by stars first, then updated repos
        repos.sort(
            key=lambda x: (x.get("stargazers_count", 0), x.get("updated_at", "")),
            reverse=True,
        )
        return repos
    except Exception:
        return []


def skill_chips(skill_list):
    """Show skills as small chips."""
    chips_html = ""
    for skill in skill_list:
        chips_html += f'<span class="skill-chip">{skill}</span>'
    st.markdown(chips_html, unsafe_allow_html=True)


def link_button_html(text, url):
    """Simple HTML button-like link."""
    return f'<a class="custom-link-btn" href="{url}" target="_blank">{text}</a>'


# -------------------------
# 4) LOAD FILES / EXTRACT ZIPS
# -------------------------
profile_img_path = file_path(FILES["profile_image"])
resume_pdf_path = file_path(FILES["resume_pdf"])
cert_pdf_path = file_path(FILES["internship_certificate"])
rec_pdf_path = file_path(FILES["recommendation_letter"])

fyp_extract_dir = extract_zip_if_needed(file_path(FILES["fyp_zip"]), "extracted_fyp")
societies_extract_dir = extract_zip_if_needed(file_path(FILES["societies_zip"]), "extracted_societies")

powerbi_folder = find_first_folder(fyp_extract_dir, "PowerBI")
thesis_pdf_path = find_first_file(fyp_extract_dir, ["*FAWADFYPLATEST.pdf", "*.pdf"])
pbix_file_path = find_first_file(fyp_extract_dir, ["*.pbix"])
star_schema_img = find_first_file(powerbi_folder, ["*Star Schema*.jpg", "*star*.jpg", "*schema*.jpg"])

dashboard_images = find_images(powerbi_folder)
if star_schema_img and star_schema_img in dashboard_images:
    dashboard_images.remove(star_schema_img)

society_images_all = find_images(societies_extract_dir)

# -------------------------
# 5) SIMPLE CUSTOM STYLING
# -------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(180deg, #07111f 0%, #0c1830 100%);
        color: #f5f7fa;
    }

    .hero-card, .info-card {
        background: rgba(255,255,255,0.06);
        padding: 1.2rem;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.08);
        box-shadow: 0 8px 24px rgba(0,0,0,0.15);
        margin-bottom: 1rem;
    }

    .section-title {
        font-size: 1.9rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 0.2rem;
    }

    .muted-text {
        color: #cfd8e3;
        font-size: 1rem;
    }

    .custom-link-btn {
        display: inline-block;
        padding: 0.65rem 1rem;
        margin: 0.25rem 0.35rem 0.25rem 0;
        background: #1e90ff;
        color: white !important;
        text-decoration: none;
        border-radius: 10px;
        font-weight: 600;
    }

    .skill-chip {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        margin: 0.25rem;
        background: rgba(30,144,255,0.18);
        color: #e8f3ff;
        border: 1px solid rgba(30,144,255,0.35);
        border-radius: 999px;
        font-size: 0.9rem;
    }

    .small-note {
        color: #b8c6d6;
        font-size: 0.9rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------
# 6) SIDEBAR
# -------------------------
st.sidebar.title("Fawad Ahmad")
st.sidebar.title("Portfolio Menu")
page = st.sidebar.radio(
    "Go to",
    [
        "Home",
        "About",
        "FYP & Thesis",
        "Experience & Achievements",
        "Leadership & Societies",
        "Skills",
        "Projects",
        "Contact",
    ],
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"**{PROFILE['name']}**")
st.sidebar.caption(PROFILE["headline"])
st.sidebar.markdown(f"[LinkedIn]({PROFILE['linkedin']})")
st.sidebar.markdown(f"[GitHub]({PROFILE['github']})")

# -------------------------
# 7) HOME PAGE
# -------------------------
if page == "Home":
    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        if profile_img_path.exists():
            st.image(str(profile_img_path), use_container_width=True)
        else:
            st.info("Profile image not found.")

    with col2:
        st.markdown('<div class="hero-card">', unsafe_allow_html=True)
        st.markdown(f"<div class='section-title'>{PROFILE['name']}</div>", unsafe_allow_html=True)
        st.markdown(f"### {PROFILE['headline']}")
        st.markdown(f"<p class='muted-text'>{PROFILE['short_intro']}</p>", unsafe_allow_html=True)

        st.markdown(
            link_button_html("LinkedIn", PROFILE["linkedin"])
            + link_button_html("GitHub", PROFILE["github"]),
            unsafe_allow_html=True,
        )

        st.markdown("</div>", unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Degree", "BSCS")
        c2.metric("Focus", "Data Science")
        c3.metric("BI Tool", "Power BI")
        c4.metric("Role", "Graduate")

        st.markdown("#### Quick Summary")
        st.write(
            "Computer Science graduate with interest in Data Science, Python, "
            "SQL, Excel, Streamlit, and Business Intelligence. Strong in "
            "leadership, communication, and practical project work."
        )

        show_download_button(resume_pdf_path, "📄 Download Resume", "resume_home")

    st.markdown("---")
    st.subheader("Featured Highlights")

    h1, h2, h3, h4 = st.columns(4)
    h1.info("🎓 BS Computer Science Graduate")
    h2.info("📊 Power BI FYP & Thesis")
    h3.info("🏢 Data Science Internship")
    h4.info("👥 Society Leadership Roles")

    st.markdown("---")
    st.subheader("Featured FYP")
    st.write(FYP_INFO["title"])
    st.caption(FYP_INFO["summary"])

    if dashboard_images:
        preview_cols = st.columns(3)
        for i, img_path in enumerate(dashboard_images[:3]):
            with preview_cols[i % 3]:
                st.image(str(img_path), caption=img_path.stem.replace("_", " ").title(), use_container_width=True)

# -------------------------
# 8) ABOUT PAGE
# -------------------------
elif page == "About":
    st.title("About Me")

    left, right = st.columns([2, 1], gap="large")

    with left:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.write(PROFILE["about"])
        st.markdown("</div>", unsafe_allow_html=True)

        st.subheader("Education")
        st.write(f"**College:** {PROFILE['college']}")
        st.write(f"**Degree:** {PROFILE['degree']}")
        st.write(f"**Status:** {PROFILE['status']}")

        st.subheader("Career Direction")
        st.write(
            "I am aiming for opportunities in Data Analysis, Data Science, "
            "Business Intelligence, and Python-based project development."
        )

    with right:
        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.markdown("### Profile Snapshot")
        st.write("• Motivated Computer Science graduate")
        st.write("• Interested in Data Science and Analytics")
        st.write("• Hands-on with Python and Power BI")
        st.write("• Strong communication and teamwork")
        st.markdown("</div>", unsafe_allow_html=True)

# -------------------------
# 9) FYP & THESIS PAGE
# -------------------------
elif page == "FYP & Thesis":
    st.title("FYP & Thesis")

    st.markdown(f"## {FYP_INFO['title']}")
    st.write(FYP_INFO["summary"])

    m1, m2, m3 = st.columns(3)
    m1.metric("Main Tool", "Power BI")
    m2.metric("Project Type", "Business Intelligence")
    m3.metric("Outputs", "Dashboards + Thesis")

    tab1, tab2, tab3, tab4 = st.tabs(["Overview", "Methodology", "Dashboards", "Downloads"])

    with tab1:
        st.subheader("Project Overview")
        st.write(
            "This project analyzes retail sales data to discover business insights "
            "related to products, customers, regions, categories, and trends over time."
        )

        st.subheader("Tools Used")
        skill_chips(FYP_INFO["tools"])

        st.subheader("Key Highlights")
        for item in FYP_INFO["highlights"]:
            st.write(f"• {item}")

    with tab2:
        st.subheader("Methodology")
        for step_no, step in enumerate(FYP_INFO["methodology"], start=1):
            st.write(f"{step_no}. {step}")

        if star_schema_img and star_schema_img.exists():
            st.subheader("Star Schema")
            st.image(str(star_schema_img), caption="Star Schema Design", use_container_width=True)

    with tab3:
        st.subheader("Power BI Dashboards")

        if dashboard_images:
            cols = st.columns(2)
            for i, img_path in enumerate(dashboard_images):
                with cols[i % 2]:
                    clean_title = img_path.stem.replace("_", " ").replace("-", " ").title()
                    st.image(str(img_path), caption=clean_title, use_container_width=True)
        else:
            st.info("No dashboard images found in the FYP zip.")

    with tab4:
        st.subheader("Project Files")
        show_download_button(thesis_pdf_path, "📘 Download Thesis PDF", "thesis_download")
        show_download_button(pbix_file_path, "📊 Download Power BI File (.pbix)", "pbix_download")
        show_download_button(resume_pdf_path, "📄 Download Resume", "resume_fyp")

# -------------------------
# 10) EXPERIENCE PAGE
# -------------------------
elif page == "Experience & Achievements":
    st.title("Experience & Achievements")

    st.subheader("Data Science Internship")
    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.write("**Company:** Arch Technologies")
    st.write("**Type:** Unpaid Internship / Training Program")
    st.write("**Duration:** 8 Weeks")
    st.write(
        "Completed a Data Science internship and training experience focused on "
        "professional growth, practical learning, responsibility, punctuality, "
        "team collaboration, and workplace discipline."
    )
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        show_download_button(cert_pdf_path, "🏅 Download Internship Certificate", "cert_download")
    with c2:
        show_download_button(rec_pdf_path, "✉️ Download Recommendation Letter", "rec_download")

    st.subheader("Other Achievement Highlights")
    st.write("• Completed BS Computer Science degree")
    st.write("• Built Power BI based FYP and thesis")
    st.write("• Participated actively in college societies")
    st.write("• Built practical projects using Python and C++")

# -------------------------
# 11) LEADERSHIP PAGE
# -------------------------
elif page == "Leadership & Societies":
    st.title("Leadership & Societies")
    st.write(
        "These activities reflect leadership, communication, teamwork, creativity, "
        "and active participation in campus life."
    )

    # Create one tab for each society
    tabs = st.tabs(list(SOCIETIES.keys()))

    for tab, (society_name, data) in zip(tabs, SOCIETIES.items()):
        with tab:
            st.subheader(society_name)
            st.write(f"**Role:** {data['role']}")
            st.write(data["description"])

            matched_images = find_images(societies_extract_dir, data["keywords"])

            if matched_images:
                cols = st.columns(2)
                for i, img_path in enumerate(matched_images):
                    with cols[i % 2]:
                        st.image(
                            str(img_path),
                            caption=img_path.stem,
                            use_container_width=True,
                        )
            else:
                st.info("No matching images found for this section.")

# -------------------------
# 12) SKILLS PAGE
# -------------------------
elif page == "Skills":
    st.title("Skills")

    for category, items in SKILLS.items():
        st.subheader(category)
        skill_chips(items)
        st.markdown("")

    st.subheader("Most Relevant Tools for My Career Goal")
    st.write("Python, Power BI, SQL, Excel, Streamlit")

# -------------------------
# 13) PROJECTS PAGE
# -------------------------
elif page == "Projects":
    st.title("Projects")
    st.write("Below are public repositories fetched from my GitHub profile.")

    repos = get_github_repos(PROFILE["github_username"])

    # Always show the GitHub profile link
    st.markdown(
        link_button_html("Open GitHub Profile", PROFILE["github"]),
        unsafe_allow_html=True,
    )

    if repos:
        for repo in repos[:8]:  # show top 8 repos
            st.markdown('<div class="info-card">', unsafe_allow_html=True)
            st.markdown(f"### {repo.get('name', 'Untitled Repo')}")
            st.write(repo.get("description") or "No description added yet.")
            st.write(f"**Language:** {repo.get('language') or 'Not specified'}")
            st.write(f"**Stars:** {repo.get('stargazers_count', 0)}")
            st.write(f"**Updated:** {repo.get('updated_at', '')[:10]}")
            st.markdown(
                link_button_html("Open Repository", repo.get("html_url", PROFILE["github"])),
                unsafe_allow_html=True,
            )
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning(
            "Could not fetch GitHub repositories right now. "
            "Check your internet connection or make sure the username is correct."
        )

# -------------------------
# 14) CONTACT PAGE
# -------------------------
elif page == "Contact":
    st.title("Contact")

    st.markdown('<div class="info-card">', unsafe_allow_html=True)
    st.write(f"**Name:** {PROFILE['name']}")
    st.write(f"**Email:** {PROFILE['email']}")
    st.write(f"**Phone:** {PROFILE['phone']}")
    st.write(f"**LinkedIn:** {PROFILE['linkedin']}")
    st.write(f"**GitHub:** {PROFILE['github']}")
    st.markdown("</div>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(link_button_html("LinkedIn", PROFILE["linkedin"]), unsafe_allow_html=True)
    with c2:
        st.markdown(link_button_html("GitHub", PROFILE["github"]), unsafe_allow_html=True)
    with c3:
        show_download_button(resume_pdf_path, "📄 Download Resume", "resume_contact")

    st.caption("You can edit any text, colors, or section order later according to your preference.")