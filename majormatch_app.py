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

# Step 3: Recommend Majors
st.header("🎯 Step 3: Your Recommended Majors")

def score_major(interests, completed):
    # Define sample majors and their requirements
    majors = {
        "Accounting": {
            "required_courses": ["ACCT 2004", "ACCT 2013", "ECON 2003", "BLAW 2033"],
            "interest_weights": {"numbers": 0.4, "business": 0.4, "tech": 0.2}
        },
        "Psychology": {
            "required_courses": ["PSY 2003", "STAT 2163", "ENGL 1013"],
            "interest_weights": {"people": 0.6, "creative": 0.2, "tech": 0.2}
        },
        "Computer Science": {
            "required_courses": ["COMS 2003", "MATH 2914", "ENGL 1013"],
            "interest_weights": {"tech": 0.6, "numbers": 0.3, "creative": 0.1}
        },
        "Marketing": {
            "required_courses": ["MKT 3043", "BUAD 2003", "ENGL 2053"],
            "interest_weights": {"business": 0.5, "creative": 0.3, "people": 0.2}
        },
        "English": {
            "required_courses": ["ENGL 1013", "ENGL 1023", "ENGL 2053"],
            "interest_weights": {"creative": 0.6, "people": 0.3, "tech": 0.1}
        }
    }

    results = []
    for major, data in majors.items():
        required = data["required_courses"]
        matched = [course for course in required if course in completed]
        completion_score = len(matched) / len(required)

        interest_score = sum(interests[k] * v for k, v in data["interest_weights"].items()) / 10

        total_score = round((completion_score * 0.6 + interest_score * 0.4) * 100, 1)
        results.append((major, total_score, len(matched), len(required)))

    return sorted(results, key=lambda x: x[1], reverse=True)

if transcript_df is not None:
    ranked = score_major(interests, completed_courses)
    for major, score, matched, total in ranked[:3]:
        st.markdown(f"**{major}** — Fit Score: {score}%  ")
        st.markdown(f"_Completed {matched} of {total} key courses_\n")
else:
    st.info("Upload a transcript to see major recommendations.")
