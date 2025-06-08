import streamlit as st
import base64

# Grade-to-point mapping
grade_points = {
    'A1': 10, 'B2': 9, 'B3': 8,
    'C4': 7, 'C5': 6, 'C6': 5,
    'D7': 0, 'E8': 0, 'F9': 0
}

st.title("University Screening Score Calculator")

# Candidate Info
st.subheader("Candidate Information")
name = st.text_input("Full Name")
jamb_number = st.text_input("JAMB Registration Number")
course = st.text_input("Course of Interest")

# JAMB Input
st.subheader("JAMB Scores (English is compulsory)")
jamb_subjects = []
jamb_scores = []

english_score = st.number_input("English", min_value=0, max_value=100, value=0)
jamb_subjects.append("English")
jamb_scores.append(english_score)

for i in range(3):
    subj = st.text_input(f"Subject {i+2} Name")
    score = st.number_input(f"{subj} Score", min_value=0, max_value=100, value=0, key=f"jamb{i}")
    jamb_subjects.append(subj)
    jamb_scores.append(score)

total_jamb = sum(jamb_scores)
jamb_percentage = round(total_jamb / 8, 2)

st.write(f"JAMB Total: {total_jamb} / 400")
st.write(f"JAMB Screening Score: {jamb_percentage}%")

if total_jamb < 195:
    st.error("You must score at least 195 in JAMB to be eligible for screening.")
else:
    st.subheader("WAEC/NECO Results (5 Subjects)")
    waec_subjects = []
    waec_grades = []
    waec_points = []

    for i in range(5):
        subj = st.text_input(f"WAEC/NECO Subject {i+1}")
        grade = st.selectbox(f"Grade for {subj}", list(grade_points.keys()), key=f"waec{i}")
        point = grade_points[grade]
        waec_subjects.append(subj)
        waec_grades.append(grade)
        waec_points.append(point)

    total_waec = sum(waec_points)
    waec_percentage = round(total_waec, 2)

    st.write(f"WAEC/NECO Total Points: {total_waec} / 50")
    st.write(f"WAEC/NECO Score: {waec_percentage}%")

    aggregate_score = round(jamb_percentage + waec_percentage, 2)
    st.subheader(f"Aggregate Score: {aggregate_score}%")

    if aggregate_score >= 50:
        st.success(f"🎉 Congratulations, {name} with JAMB number {jamb_number} is qualified to register into Lagos State University with the aggregate score of {aggregate_score}%.")

        # HTML result string with inline print button and styling
        html_result = f"""
        <html>
        <head>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; }}
            h2 {{ color: darkgreen; }}
            ul {{ padding-left: 20px; }}
            button.print-btn {{
                background-color: #4CAF50;
                color: white;
                padding: 10px 20px;
                margin-bottom: 20px;
                border: none;
                cursor: pointer;
                font-size: 16px;
                border-radius: 5px;
            }}
        </style>
        </head>
        <body>
        <button class="print-btn" onclick="window.print()">🖨️ Print Result</button>
        <h2>Lagos State University Screening Result</h2>
        <p><strong>Name:</strong> {name}</p>
        <p><strong>JAMB Number:</strong> {jamb_number}</p>
        <p><strong>Course of Interest:</strong> {course}</p>
        <hr>
        <h3>JAMB Scores</h3>
        <ul>
        {''.join([f'<li>{subj}: {score}</li>' for subj, score in zip(jamb_subjects, jamb_scores)])}
        </ul>
        <p><strong>JAMB Screening Score:</strong> {jamb_percentage}%</p>

        <h3>WAEC/NECO Grades</h3>
        <ul>
        {''.join([f'<li>{subj}: {grade} ({grade_points[grade]} points)</li>' for subj, grade in zip(waec_subjects, waec_grades)])}
        </ul>
        <p><strong>WAEC Score:</strong> {waec_percentage}%</p>

        <h3>Aggregate Score: {aggregate_score}%</h3>
        <h3 style='color:green;'>Congratulations, you are qualified for admission!</h3>
        </body>
        </html>
        """

        # Show preview in Streamlit
        st.components.v1.html(html_result, height=600, scrolling=True)

        # Offer HTML as downloadable file
        b64 = base64.b64encode(html_result.encode()).decode()
        href = f'<a href="data:text/html;base64,{b64}" download="screening_result.html">📥 Download Result as HTML</a>'
        st.markdown(href, unsafe_allow_html=True)

    else:
        st.error("Sorry, your aggregate score is below 50%. You are not qualified.")
