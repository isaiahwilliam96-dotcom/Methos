import streamlit as st
from openai import OpenAI
import os
import matplotlib.pyplot as plt
import base64
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import streamlit.components.v1 as components

st.set_page_config(layout="centered")

st.markdown("""
<style>

.stApp {
    background: linear-gradient(-45deg,#0f172a,#1e293b,#334155,#0f172a);
    background-size:400% 400%;
    animation:gradientBG 18s ease infinite;
    overflow:hidden;
}

@keyframes gradientBG {
0% {background-position:0% 50%;}
50% {background-position:100% 50%;}
100% {background-position:0% 50%;}
}

.math-symbol {
    position:fixed;
    color:rgba(255,255,255,0.08);
    font-size:40px;
    animation: float 20s linear infinite;
    pointer-events:none;
}

@keyframes float {
0% {transform:translateY(100vh) rotate(0deg);}
100% {transform:translateY(-10vh) rotate(360deg);}
}


/* -------- TEXT ANIMATION -------- */

@keyframes fadeSlide {
0% {opacity:0; transform:translateY(20px);}
100% {opacity:1; transform:translateY(0);}
}

@keyframes glow {
0% {text-shadow:0 0 5px #a5b4fc;}
50% {text-shadow:0 0 20px #818cf8;}
100% {text-shadow:0 0 5px #a5b4fc;}
}

.animated-title {
font-size:42px;
font-weight:700;
animation:fadeSlide 1.2s ease-out, glow 3s ease-in-out infinite;
}

.animated-subtitle {
font-size:18px;
animation:fadeSlide 1.5s ease forwards;
}

.animated-section {
animation:fadeSlide 1s ease-out;
}

</style>

<div class="math-symbol" style="left:5%;">π</div>
<div class="math-symbol" style="left:15%;animation-delay:3s;">∑</div>
<div class="math-symbol" style="left:25%;animation-delay:7s;">∫</div>
<div class="math-symbol" style="left:35%;animation-delay:2s;">√</div>
<div class="math-symbol" style="left:45%;animation-delay:5s;">x²</div>
<div class="math-symbol" style="left:55%;animation-delay:9s;">Δ</div>
<div class="math-symbol" style="left:65%;animation-delay:4s;">θ</div>
<div class="math-symbol" style="left:75%;animation-delay:6s;">λ</div>
<div class="math-symbol" style="left:85%;animation-delay:1s;">∞</div>

""", unsafe_allow_html=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# -----------------------
# Music Function
# -----------------------
def play_music(file):
    st.audio(file, start_time=0)

# -----------------------
# Global Styling
# -----------------------
    
# -----------------------
# Session State
# -----------------------
if "score" not in st.session_state:
    st.session_state.score = 0

if "hint_level" not in st.session_state:
    st.session_state.hint_level = 0

if "answer" not in st.session_state:
    st.session_state.answer = ""

if "current_problem" not in st.session_state:
    st.session_state.current_problem = ""

# -----------------------
# Sidebar
# -----------------------
st.sidebar.title("📊 Learning Dashboard")
st.sidebar.metric("Score", st.session_state.score)
st.sidebar.metric("Hints Used", st.session_state.hint_level)

mode = st.sidebar.selectbox(
    "Choose Mode",
    ["Practice Mode", "Exam Mode", "Fun Mode"]
)

with st.sidebar:
    st.header("🎵 Background Music")

    if st.session_state.hint_level >= 2:
        play_music("struggle.mp3")
    elif mode == "Exam Mode":
        play_music("calm.mp3")
    elif mode == "Practice Mode":
        play_music("focus.mp3")
    else:
        play_music("fun.mp3")

st.sidebar.markdown("### 🧠 My Mnemonics")

mnemonic_input = st.sidebar.text_area(
    "Add your memorising tricks:",
    placeholder="Example: Product rule = LIM → Left × dRight + Right × dLeft"
)

if "mnemonics" not in st.session_state:
    st.session_state.mnemonics = ""

if st.sidebar.button("Save Mnemonics"):
    st.session_state.mnemonics = mnemonic_input
    st.sidebar.success("Saved!")


if mode == "Exam Mode":
    background = """
    <style>
    .stApp {
        background-color: #1e1e1e;
        color: white;
    }
    </style>
    """

elif mode == "Practice Mode":
    background = """
    <style>
    .stApp {
        background-color: #0f172a;
        color: white;
    }
    </style>
    """

else:
    background = """
    <style>
    .stApp {
        background: linear-gradient(135deg,#667eea,#764ba2);
        color:white;
    }
    </style>
    """

st.markdown(background, unsafe_allow_html=True)

# -----------------------
# Global Styling
# -----------------------
st.markdown("""
<style>

div.stButton > button {
    border-radius: 12px;
    height: 3em;
    font-weight: 600;
}

textarea {
    border-radius:10px !important;
}

section[data-testid="stSidebar"] {
    background-color:#111827;
}

</style>
""", unsafe_allow_html=True)

# -----------------------
# Title
# -----------------------
st.markdown('<div class="animated-title">Mathos 🧠</div>', unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.metric("Score", st.session_state.score)

with col2:
    st.write(f"Hint Level: {st.session_state.hint_level}")
st.progress(min(st.session_state.score / 10, 1.0))
st.markdown("### Adaptive AI Scaffolding for Matriculation Mathematics")
st.markdown(
'<div class="animated-subtitle">Guided hints • Cognitive tracking • Independent learning</div>',
unsafe_allow_html=True
)
st.write("I give hints, not answers.")

# -----------------------
# Difficulty
# -----------------------
difficulty = st.selectbox(
    "Select Difficulty Level:",
    ["Beginner", "Intermediate", "Advanced"]
)

# -----------------------
# Input
# -----------------------
st.markdown('<div class="animated-section">### 📝 Enter Your Problem</div>', unsafe_allow_html=True)

user_input = st.text_area(
    "",
    height=150,
    placeholder="Type your math question here..."
)

uploaded_file = st.file_uploader(
    "Upload a photo of your math problem",
    type=["png", "jpg", "jpeg"]
)

# -----------------------
# Image Extraction
# -----------------------
if uploaded_file:

    image_bytes = uploaded_file.read()
    encoded_image = base64.b64encode(image_bytes).decode()

    response = client.responses.create(
        model="gpt-4.1",
        input=[{
            "role":"user",
            "content":[
                {"type":"input_text","text":"Extract the math problem only."},
                {
                    "type":"input_image",
                    "image_url":f"data:image/jpeg;base64,{encoded_image}"
                }
            ]
        }]
    )

    user_input = response.output_text
    st.info("📷 Problem extracted from image.")

# -----------------------
# Reset hints if new problem
# -----------------------
if user_input != st.session_state.current_problem:

    st.session_state.current_problem = user_input
    st.session_state.hint_level = 0
    st.session_state.answer = ""

if not user_input:
    st.stop()

st.success("Problem detected")
# -----------------------
# Student Attempt Section
# -----------------------

st.markdown("### ✏️ Try Solving")

student_answer = st.text_input(
    "Enter your answer:",
    placeholder="Example: x = 4"
)

if st.button("Check My Answer"):
    response = client.responses.create(
        model="gpt-4.1",
        input=f"""
Check if the student's answer is correct.

Rules:
- Only say "Correct ✅" or "Incorrect ❌"
- If incorrect, give a very small hint.
- Do NOT show full solution.

Problem:
{user_input}

Student Answer:
{student_answer}
"""
    )

    st.write(response.output_text)

if st.button("📊 Generate Graph"):

    response = client.responses.create(
        model="gpt-4.1",
        input=f"""
Extract the function from this problem.

Rules:
- Return only the function in terms of x
- Example: x^2 + 3*x - 2
- Do not include 'y ='

Problem:
{user_input}
"""
    )

    expr_text = response.output_text.strip()
    expr_text = expr_text.replace("^", "**")

    st.write("Detected function:", expr_text)

    roots = []
    critical_points = []

    try:
        x = sp.symbols('x')
        expr = sp.sympify(expr_text)

        f = sp.lambdify(x, expr, "numpy")

        x_vals = np.linspace(-5, 5, 400)
        y_vals = f(x_vals)

        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals)

        # ROOTS
        roots = sp.solve(expr, x)

        for r in roots:
            if r.is_real:
                ax.scatter(float(r), 0)
                st.write("Root:", r)

        # TURNING POINTS
        derivative = sp.diff(expr, x)
        critical_points = sp.solve(derivative, x)

        for cp in critical_points:
            if cp.is_real:
                y_val = expr.subs(x, cp)
                ax.scatter(float(cp), float(y_val))
                st.write(f"Turning point: ({cp}, {y_val})")

        ax.set_title("Graph of the Function")
        ax.grid(True)

        st.pyplot(fig)

    except Exception as e:
        st.error(f"Graph error: {e}")
      
    for r in roots:
        ax.scatter(float(r), 0)

    for cp in critical_points:
        ax.scatter(float(cp), float(expr.subs(x, cp)))

# -----------------------
# Identify Topic
# -----------------------
if st.button("🔎 Identify Topic"):

    response = client.responses.create(
        model="gpt-4.1",
        input=f"""
Identify the math topic only.

Output format:
Chapter → Topic

Do NOT solve.

Student mnemonics:
{st.session_state.mnemonics}

Problem:
{user_input}
"""
    )

    st.write(response.output_text)

# -----------------------
# Hint System
# -----------------------
st.markdown("---")
st.subheader("🧠 Guided Hint System")

# HINT 1
if st.session_state.hint_level == 0:

    if st.button("💡 Reveal Hint 1"):

        response = client.responses.create(
            model="gpt-4.1",
            input=f"""
You are a Malaysian SPM / Matriculation math tutor.

Give Hint 1 (concept hint).

Rules
• No solution
• No final answer
• Short clue only
• Match difficulty: {difficulty}

Student mnemonics:
{st.session_state.mnemonics}

Problem:
{user_input}
""",
            max_output_tokens=100
        )

        st.session_state.hint1 = response.output_text
        st.session_state.hint_level = 1
        st.rerun()

if st.session_state.hint_level >= 1:
    st.write("### Hint 1")
    st.write(st.session_state.hint1)

# Understanding check
understanding = st.radio(
    "Did this hint help?",
    ["Yes", "Not sure", "Still confused"]
)

# HINT 2
if st.session_state.hint_level == 1:

    if st.button("💡 Reveal Hint 2"):

        if understanding == "Still confused":
            instruction = "Explain more simply."
        elif understanding == "Not sure":
            instruction = "Clarify with a small clue."
        else:
            instruction = "Give a strategic hint."

        response = client.responses.create(
            model="gpt-4.1",
            input=f"""
Give Hint 2.

Rules
• 2 sentences max
• No solution
• No answer

{instruction}

Student mnemonics:
{st.session_state.mnemonics}

Problem:
{user_input}
""",
            max_output_tokens=80
        )

        st.session_state.hint2 = response.output_text
        st.session_state.hint_level = 2
        st.rerun()

if st.session_state.hint_level >= 2:
    st.write("### Hint 2")
    st.write(st.session_state.hint2)

# HINT 3
if st.session_state.hint_level == 2:

    if st.button("💡 Reveal Hint 3"):

        response = client.responses.create(
            model="gpt-4.1",
            input=f"""
Give final directional hint.

No answer.

Student mnemonics:
{st.session_state.mnemonics}

Problem:
{user_input}
""",
            max_output_tokens=80
        )

        st.session_state.hint3 = response.output_text
        st.session_state.hint_level = 3
        st.rerun()

if st.session_state.hint_level >= 3:
    st.write("### Hint 3")
    st.write(st.session_state.hint3)

# -----------------------
# Show Answer
# -----------------------
if st.session_state.hint_level >= 3:

    if st.button("📘 Show Answer (0 points)"):

        response = client.responses.create(
            model="gpt-4.1",
            input=f"""
Give full worked solution using Malaysian method.

Show steps clearly.

Student mnemonics:
{st.session_state.mnemonics}

Problem:
{user_input}
""",
    max_output_tokens=900
        )

        st.session_state.answer = response.output_text
        st.session_state.hint_level = 4
        st.rerun()

if st.session_state.hint_level >= 4:
    with st.container():
        st.markdown("### ✅ Full Answer")
        st.write(st.session_state.answer)

# -----------------------
# Solved Button
# -----------------------
if 0 < st.session_state.hint_level < 4:

    if st.button("✅ I Solved It"):

        if st.session_state.hint_level == 1:
            st.session_state.score += 3
        elif st.session_state.hint_level == 2:
            st.session_state.score += 2
        else:
            st.session_state.score += 1

        st.success(f"Score: {st.session_state.score}")

        st.session_state.hint_level = 0

        st.rerun()
