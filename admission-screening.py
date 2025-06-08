import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import io

# WAEC/NECO Grade to Point Mapping
grade_points = {
    'A1': 10, 'B2': 9, 'B3': 8,
    'C4': 7, 'C5': 6, 'C6': 5,
    'D7': 0, 'E8': 0, 'F9': 0
}

st.title("University Screening Score Calculator")

st.subheader("Candidate Information")
name = st.text_input("Full Name")
jamb_number = st.text_input("JAMB Registration Number")
course = st.text_input("Course of Interest")

st.subheader("JAMB Scores (English is compulsory)")
jamb_subjects = []
jamb_scores = []

# English is compulsory
english_score = st.number_input("English", min_value=0, max_value=100, value=0)
jamb_subjects.append("English")
jamb_scores.append(english_score)

# Other 3 subjects
for i in range(3):
    subject = st.text_input(f"Subject {i+2} Name")
    score = st.number_input(f"{subject} Score", min_value=0, max_value=100, value=0, key=f"jamb{i}")
    jamb_subjects.append(subject)
    jamb_scores.append(score)

total_jamb = sum(jamb_scores)
jamb_percentage = round(total_jamb / 8, 2)

st.write(f"JAMB Total: {total_jamb} / 400")
st.write(f"JAMB Screening Score: {jamb_percentage}%")

if total_jamb < 195:
    st.error("You must score at least 195 in JAMB to be eligible for screening.")
else:
    st.subheader("WAEC/NECO Results (5 Relevant Subjects)")

    waec_subjects = []
    waec_grades = []
    waec_points = []

    for i in range(5):
        subject = st.text_input(f"WAEC/NECO Subject {i+1}")
        grade = st.selectbox(f"Grade for {subject}", list(grade_points.keys()), key=f"grade{i}")
        point = grade_points[grade]

        waec_subjects.append(subject)
        waec_grades.append(grade)
        waec_points.append(point)

    total_waec = sum(waec_points)
    waec_percentage = round(total_waec, 2)

    st.write(f"WAEC/NECO Total Points: {total_waec} / 50")
    st.write(f"WAEC/NECO Score: {waec_percentage}%")

    aggregate_score = round(jamb_percentage + waec_percentage, 2)
    st.subheader(f"Aggregate Score: {aggregate_score}%")

    if aggregate_score >= 50:
        success_message = f"🎉 Congratulations, {name} with JAMB number {jamb_number} is qualified to register into Lagos State University with the aggregate score of {aggregate_score}%."
        st.success(success_message)

        # PDF generation using reportlab
        buffer = io.BytesIO()
        pdf = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        y = height - 50
        pdf.setFont("Helvetica-Bold", 16)
        pdf.drawCentredString(width / 2, y, "Lagos State University Screening Result")

        y -= 40
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, y, f"Name: {name}")
        y -= 20
        pdf.drawString(50, y, f"JAMB Number: {jamb_number}")
        y -= 20
        pdf.drawString(50, y, f"Course of Interest: {course}")

        y -= 30
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y, "JAMB Scores:")
        pdf.setFont("Helvetica", 12)
        for subj, score in zip(jamb_subjects, jamb_scores):
            y -= 20
            pdf.drawString(70, y, f"{subj}: {score}")
        y -= 20
        pdf.drawString(70, y, f"JAMB Score (%): {jamb_percentage}")

        y -= 30
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y, "WAEC/NECO Grades:")
        pdf.setFont("Helvetica", 12)
        for subj, grade, point in zip(waec_subjects, waec_grades, waec_points):
            y -= 20
            pdf.drawString(70, y, f"{subj}: {grade} ({point} points)")
        y -= 20
        pdf.drawString(70, y, f"WAEC Score (%): {waec_percentage}")

        y -= 30
        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y, f"Aggregate Score: {aggregate_score}%")

        pdf.save()
        buffer.seek(0)

        st.download_button(
            label="📄 Download Result as PDF",
            data=buffer,
            file_name="screening_result.pdf",
            mime="application/pdf"
        )
    else:
        st.error("Sorry, you are not qualified for admission as your aggregate score is below 50%.")