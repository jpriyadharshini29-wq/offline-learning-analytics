import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import base64

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="Offline Learning Analytics", layout="wide")

# -------------------------------------------------
# BACKGROUND HANDLER
# -------------------------------------------------
def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# -------------------------------------------------
# GLOBAL BIG FONT STYLES 🚀
# -------------------------------------------------
st.markdown("""
<style>

/* GLOBAL TEXT */
html, body, [class*="css"] {
    font-size: 22px !important;
}

/* HEADINGS */
h1 { font-size: 44px !important; }
h2 { font-size: 38px !important; }
h3 { font-size: 32px !important; }

/* SIDEBAR */
section[data-testid="stSidebar"] * {
    font-size: 22px !important;
}

/* METRICS */
div[data-testid="stMetricValue"] {
    font-size: 38px !important;
    font-weight: 700;
}
div[data-testid="stMetricLabel"] {
    font-size: 22px !important;
}

/* TABLES */
.dataframe th, .dataframe td {
    font-size: 20px !important;
}

/* INPUTS */
label, .stSelectbox, .stTextInput, .stRadio {
    font-size: 22px !important;
}

/* ALERTS */
.stAlert {
    font-size: 22px !important;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
@st.cache_data
def load_data():
    return (
        pd.read_csv("data/students.csv"),
        pd.read_csv("data/exam_marks.csv"),
        pd.read_csv("data/teachers.csv"),
        pd.read_csv("data/syllabus_class_10.csv"),
    )

students_df, marks_df, teachers_df, syllabus_df = load_data()

# -------------------------------------------------
# RISK LOGIC
# -------------------------------------------------
def calculate_risk(row):
    if row["attendance_percentage"] < 60:
        return "HIGH", "Low attendance"
    elif row["attendance_percentage"] < 75:
        return "MEDIUM", "Irregular attendance"
    else:
        return "LOW", "Stable"

students_df[["risk", "reason"]] = students_df.apply(
    lambda r: pd.Series(calculate_risk(r)), axis=1
)

# -------------------------------------------------
# SESSION STATE
# -------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "role" not in st.session_state:
    st.session_state.role = None

# -------------------------------------------------
# BACKGROUND SWITCH
# -------------------------------------------------
if not st.session_state.logged_in:
    set_background("school_bg.jpg")
else:
    set_background("dashboard_bg.jpg")

# -------------------------------------------------
# LOGIN PAGE
# -------------------------------------------------
def login_page():
    st.title("🔐 Login")
    role = st.selectbox("Login as", ["Student", "Teacher"])
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login") and username and password:
        st.session_state.logged_in = True
        st.session_state.role = role
        st.rerun()

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
def sidebar():
    with st.sidebar:
        st.markdown("## Dashboard")
        page = st.radio("Navigation", ["Home", "Students", "Alerts", "Syllabus"])
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.role = None
            st.rerun()
    return page

# -------------------------------------------------
# STUDENT DASHBOARD
# -------------------------------------------------
def student_dashboard(page):
    st.header("🎓 Student Dashboard")

    name = st.selectbox("Select Student", students_df["name"])
    s = students_df[students_df["name"] == name].iloc[0]
    marks = marks_df[marks_df["student_id"] == s["student_id"]]

    if page == "Home":
        c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
        c1.metric("Attendance %", s["attendance_percentage"])
        c2.metric("Assignments", s["assignments_completed"])
        c3.metric("Projects", s["projects_completed"])

        with c4:
            fig, ax = plt.subplots(figsize=(2.2, 2.2))
            ax.pie(
                [s["attendance_percentage"], 100 - s["attendance_percentage"]],
                labels=["P", "A"],
                autopct="%1.0f%%",
                textprops={"fontsize": 14},
            )
            ax.axis("equal")
            st.pyplot(fig, use_container_width=False)

    elif page == "Students":
        st.dataframe(marks, use_container_width=True)

    elif page == "Alerts":
        st.info(f"{s['risk']} RISK — {s['reason']}")

    elif page == "Syllabus":
        subject = st.selectbox("Subject", syllabus_df["subject"].unique())
        st.dataframe(syllabus_df[syllabus_df["subject"] == subject])

# -------------------------------------------------
# TEACHER DASHBOARD
# -------------------------------------------------
def teacher_dashboard(page):
    st.header("🧑‍🏫 Teacher Dashboard")

    t = st.selectbox("Select Teacher", teachers_df["name"])
    teacher = teachers_df[teachers_df["name"] == t].iloc[0]

    if page == "Home":
        c1, c2, c3 = st.columns(3)
        c1.metric("Subject", teacher["subject"])
        c2.metric("Experience", teacher["experience_years"])
        c3.metric("Class", teacher["assigned_class"])

    elif page == "Students":
        st.dataframe(students_df, use_container_width=True)

    elif page == "Alerts":
        alerts = marks_df[marks_df["exam_marks"] < 40]
        st.dataframe(alerts)

    elif page == "Syllabus":
        st.dataframe(syllabus_df)

# -------------------------------------------------
# MAIN
# -------------------------------------------------
def main():
    if not st.session_state.logged_in:
        login_page()
    else:
        page = sidebar()
        if st.session_state.role == "Student":
            student_dashboard(page)
        else:
            teacher_dashboard(page)

main()
