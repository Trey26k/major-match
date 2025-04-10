import streamlit as st
import pandas as pd

st.set_page_config(page_title="MajorMatch", layout="centered")
st.title("🎓 MajorMatch - Find Your Best-Fit College Major")

st.markdown("""
This prototype analyzes your transcript and interests to suggest majors you might succeed in.
""")

# Step 1: Upload transcript
st.header("📄 Step 1: Upload Your Transcript")
transcript_file = st.file_uploader("Upload your transcript (CSV or Excel)", type=["csv", "xlsx"])

transcript_df = None
completed_courses = []
if transcript_file:
    if transcript_file.name.endswith(".csv"):
        transcript_df = pd.read_csv(transcript_file)
    else:
        transcript_df = pd.read_excel(transcript_file)

    completed_courses = transcript_df['Course'].tolist()

    st.subheader("📊 Transcript Preview")
    st.dataframe(transcript_df.head())

# Step 2: Interest Survey
st.header("🧠 Step 2: Tell Us About Your Interests")

interests = {
    "numbers": st.slider("I enjoy working with numbers and solving problems", 0, 10, 5),
    "people": st.slider("I enjoy working with people and helping others", 0, 10, 5),
    "creative": st.slider("I enjoy creative writing, arts, or design", 0, 10, 5),
    "business": st.slider("I'm interested in business, finance, or management", 0, 10, 5),
    "tech": st.slider("I enjoy working with computers, tech, or data", 0, 10, 5),
}

desired_income = st.slider("Desired annual income ($)", 30000, 150000, 60000, step=5000)

# Step 3: Manually defined course catalogs
catalog_data = {
    # ... (same catalog_data as before, omitted for brevity)
}

income_estimates = {
    "Accounting": 70000,
    "Business Management": 65000,
    "Psychology": 50000,
    "English Education": 48000,
    "Political Science": 55000
}

career_data = {
    "Accounting": {
        "jobs": ["Auditor", "Tax Analyst", "Corporate Accountant"],
        "companies": ["Deloitte", "EY", "Walmart Finance"],
    },
    "Business Management": {
        "jobs": ["Operations Manager", "Project Coordinator", "Business Analyst"],
        "companies": ["J.B. Hunt", "Amazon", "Accenture"],
    },
    "Psychology": {
        "jobs": ["Behavioral Health Technician", "Research Assistant", "HR Specialist"],
        "companies": ["Arkansas Behavioral Health", "UAMS", "State Agencies"],
    },
    "English Education": {
        "jobs": ["High School English Teacher", "Curriculum Designer", "ESL Instructor"],
        "companies": ["Public Schools", "K12 Inc.", "Edmentum"],
    },
    "Political Science": {
        "jobs": ["Policy Analyst", "Legislative Assistant", "Public Relations Associate"],
        "companies": ["State Legislature", "NGOs", "Law Firms"],
    }
}

def wildcard_match(course_pattern, completed):
    if course_pattern.endswith("XXXX"):
        prefix = course_pattern.split()[0]
        return any(course.startswith(prefix) for course in completed)
    elif course_pattern.endswith("1XXX"):
        prefix = course_pattern.split()[0] + " 1"
        return any(course.startswith(prefix) for course in completed)
    else:
        return course_pattern in completed

# Matching logic
st.header("🎯 Step 3: Your Recommended Majors")

def get_interest_score(major_name):
    major_name = major_name.lower()
    if "accounting" in major_name:
        return (interests["numbers"] * 0.4 + interests["business"] * 0.4 + interests["tech"] * 0.2) / 10
    elif "psychology" in major_name:
        return (interests["people"] * 0.6 + interests["creative"] * 0.2 + interests["tech"] * 0.2) / 10
    elif "business" in major_name:
        return (interests["business"] * 0.5 + interests["numbers"] * 0.3 + interests["people"] * 0.2) / 10
    elif "english" in major_name:
        return (interests["creative"] * 0.6 + interests["people"] * 0.3 + interests["tech"] * 0.1) / 10
    elif "political" in major_name:
        return (interests["people"] * 0.5 + interests["creative"] * 0.3 + interests["numbers"] * 0.2) / 10
    else:
        return sum(interests.values()) / 50

def score_majors(catalog, completed):
    results = []
    for major, requirements in catalog.items():
        matched = [req for req in requirements if wildcard_match(req, completed)]
        completion_score = len(matched) / len(requirements) if requirements else 0
        interest_score = get_interest_score(major)
        income_gap = abs(income_estimates.get(major, 60000) - desired_income)
        results.append((major, completion_score, interest_score, income_gap, matched, requirements))

    top_completion = sorted(results, key=lambda x: x[1], reverse=True)[:3]
    return sorted(top_completion, key=lambda x: x[2], reverse=True)

if transcript_df is not None:
    ranked = score_majors(catalog_data, completed_courses)
    for major, comp_score, interest_score, income_gap, matched, requirements in ranked:
        st.markdown(f"### 🎓 {major}")
        st.markdown(f"**Progress:** {len(matched)} / {len(requirements)} courses completed ({round(100 * len(matched) / len(requirements))}%)")
        st.markdown(f"**Interest Fit:** {round(interest_score * 100)}%")
        st.markdown(f"**Estimated Salary:** ${income_estimates.get(major, 'N/A'):,}")

        with st.expander("💼 Career Opportunities"):
            st.markdown("**Example Job Titles:**")
            st.write(", ".join(career_data.get(major, {}).get("jobs", [])))
            st.markdown("**Employers Hiring This Major:**")
            st.write(", ".join(career_data.get(major, {}).get("companies", [])))

        with st.expander("📚 Courses Left to Complete"):
            remaining = [r for r in requirements if not wildcard_match(r, completed_courses)]
            for course in remaining:
                st.markdown(f"- {course}")

        st.markdown("---")
else:
    st.info("Upload a transcript to see major recommendations.")
