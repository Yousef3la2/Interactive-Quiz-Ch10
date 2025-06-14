import fitz
import re
import streamlit as st
import random
from collections import defaultdict

# قراءة الأسئلة من PDF
pdf_path = "Chapter10.pdf"
doc = fitz.open(pdf_path)
text = ""
for page in doc:
    text += page.get_text()
doc.close()

# استخراج الأسئلة والإجابات
pattern = re.compile(
    r"(\d+\.\s+.*?(?:A\..*?\n).*?B\..*?\n.*?C\..*?\n.*?D\..*?\n).*?Correct Answer:\s*([ABCD])",
    re.DOTALL
)
matches = pattern.findall(text)

questions = []

for block, correct in matches:
    lines = block.strip().splitlines()
    if not lines or len(lines) < 5:
        continue

    question_text = lines[0].strip()
    options = {}
    for line in lines[1:]:
        if line.strip()[:2] in ["A.", "B.", "C.", "D."]:
            letter = line.strip()[0]
            text = line.strip()[2:].strip()
            options[letter] = text

    questions.append({
        "question": question_text,
        "options": options,
        "correct": correct
    })

# ترتيب الأسئلة عشوائي
if "shuffled_questions" not in st.session_state:
    st.session_state.shuffled_questions = random.sample(questions, len(questions))
    st.session_state.current_q = 0
    st.session_state.correct_count = 0
    st.session_state.user_answers = {}
    st.session_state.submitted = False

q_index = st.session_state.current_q
q = st.session_state.shuffled_questions[q_index]

# إعداد واجهة Streamlit
st.set_page_config(page_title="Chapter 10 Quiz", layout="centered")
st.title("🧠 Chapter 10 Interactive Quiz")

# عرض الحالة في الأعلى
st.info(f"Question {q_index + 1} of {len(st.session_state.shuffled_questions)}")
st.success(f"Correct Answers: {st.session_state.correct_count}")

# عرض السؤال الحالي
st.markdown(f"**{q_index + 1}. {q['question']}**")

# عرض الاختيارات
selected_letter = st.radio("Select your answer:", list(q['options'].keys()), format_func=lambda x: f"{x}) {q['options'][x]}", key=f"choice_{q_index}")

# زرار السبمت
if st.button("Submit Answer") and not st.session_state.submitted:
    st.session_state.user_answers[q_index] = selected_letter
    if selected_letter == q['correct']:
        st.success("✅ Correct!")
        st.session_state.correct_count += 1
    else:
        st.error("❌ Incorrect.")
        st.info(f"Correct answer: {q['correct']}) {q['options'][q['correct']]}")
    st.session_state.submitted = True

# زر التالي بعد السبمت فقط
if st.session_state.submitted:
    if st.button("Next Question"):
        st.session_state.current_q += 1
        st.session_state.submitted = False
        if st.session_state.current_q >= len(st.session_state.shuffled_questions):
            st.success("🎉 You've completed all questions! Restarting from beginning.")
            st.session_state.shuffled_questions = random.sample(questions, len(questions))
            st.session_state.current_q = 0
            st.session_state.correct_count = 0
            st.session_state.user_answers = {}