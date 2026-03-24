import streamlit as st
from openai import OpenAI
import os
import matplotlib.pyplot as plt
import base64
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import streamlit.components.v1 as components
import random
import plotly.graph_objects as go
import math
import plotly.graph_objects as go
from scipy.stats import norm
import numpy as np

if "score" not in st.session_state:
    st.session_state.score = 0

if "streak" not in st.session_state:
    st.session_state.streak = 0

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "correct" not in st.session_state:
    st.session_state.correct = 0

if "topic_stats" not in st.session_state:
    st.session_state.topic_stats = {}

quotes = [
    "Mathematics is not about numbers, it's about thinking.",
    "Struggle in math today builds clarity tomorrow.",
    "Do not memorise. Understand.",
    "Every problem you solve rewires your brain.",
    "Mistakes mean you are learning.",
    "Mathematics rewards patience, not speed.",
    "Think deeply, not quickly.",
    "Confusion is the beginning of understanding.",
    "Small steps every day lead to big mastery.",
    "You don't need talent, just persistence."
]

st.markdown("""
<style>

/* IMPORT FONTS */
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Poppins:wght@300;400;600&display=swap');

/* GLOBAL FONT */
html, body, [class*="css"] {
    font-family: 'Poppins', sans-serif;
}

/* BACKGROUND */
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

/* FLOATING SYMBOLS */
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

/* TEXT ANIMATION */
@keyframes fadeSlide {
0% {opacity:0; transform:translateY(20px);}
100% {opacity:1; transform:translateY(0);}
}

@keyframes glow {
0% {text-shadow:0 0 5px #a5b4fc;}
50% {text-shadow:0 0 20px #818cf8;}
100% {text-shadow:0 0 5px #a5b4fc;}
}

/* TITLE */
.animated-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size:42px;
    font-weight:700;
    letter-spacing:2px;
    animation:fadeSlide 1.2s ease-out, glow 3s ease-in-out infinite;
}

/* SUBTITLE */
.animated-subtitle {
    font-size:18px;
    animation:fadeSlide 1.5s ease forwards;
}

/* SECTION */
.animated-section {
    animation:fadeSlide 1s ease-out;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
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

def ask_ai(prompt, max_tokens=300):
    response = client.responses.create(
        model="gpt-4.1",
        input=prompt,
        max_output_tokens=max_tokens
    )
    return response.output_text

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

# ✅ ADD THIS
if "topic_stats" not in st.session_state:
    st.session_state.topic_stats = {}

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

# ✅ Put warning AFTER columns (correct placement)
st.warning("""
⚠️ AI is not always perfect.

Always verify solutions and avoid relying fully on it.
Use this as a guide, not a replacement for your own thinking.
""")

if "quote" not in st.session_state:
    st.session_state.quote = random.choice(quotes)

st.success(f"“{st.session_state.quote}”")

st.progress(min(st.session_state.score / 10, 1.0))
st.markdown("### Adaptive AI Scaffolding for Matriculation Mathematics")

# =========================
# MAIN TABS
# =========================
tab_practice, tab_notes, tab_visual, tab_progress = st.tabs([
    "🧠 Practice",
    "📖 Notes",
    "📊 Visualize",
    "🏆 Progress"
])

st.markdown(
'<div class="animated-subtitle">Guided hints • Cognitive tracking • Independent learning</div>',
unsafe_allow_html=True
)

    # =========================
    # 🧠 PRACTICE TAB
    # =========================
with tab_practice:

    st.write("I give hints, not answers.")

    # -----------------------
    # 🎯 PSPM Question Generator
    # -----------------------
    st.markdown("### 🎯 Generate PSPM Questions")

    # ✅ MOVE THIS UP
    # ✅ Persist difficulty
    if "difficulty" not in st.session_state:
        st.session_state.difficulty = "Intermediate"

    difficulty = st.selectbox(
        "Select Difficulty Level:",
        ["Beginner", "Intermediate", "Advanced"],
        index=["Beginner","Intermediate","Advanced"].index(st.session_state.difficulty)
    )

    st.session_state.difficulty = difficulty

    pspm_topic = st.text_input(
        "Enter topic (e.g. Differentiation, Integration, Probability):",
        key="pspm_topic"
    )

    if st.button("Generate PSPM Question"):

        if pspm_topic:

            prompt = f"""
    Create a Malaysian Matriculation (PSPM) mathematics question.

    Topic: {pspm_topic}
    Difficulty: {difficulty}

    Rules:
    - Follow real PSPM exam style
    - Clear wording
    - Include numbers and context if needed
    - DO NOT give solution
    - Only output the question

    Optional:
    - Add (a), (b) parts if suitable
    """

            generated_q = ask_ai(prompt, max_tokens=300)

            # ✅ SET AS CURRENT PROBLEM
            st.session_state.current_problem = generated_q
            st.session_state.answer = ""
            st.session_state.hint_level = 0

            st.success("PSPM Question Generated!")
            st.write(generated_q)

        else:
            st.warning("Please enter a topic.")

    # -----------------------
    # Input
    # -----------------------
    st.markdown('<div class="animated-section"><h3>📝 Enter Your Problem</h3></div>', unsafe_allow_html=True)

    user_input = st.text_area(
        "",
        height=150,
        placeholder="Type your math question here..."
    )

    if st.session_state.current_problem:
        user_input = st.session_state.current_problem

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

        def extract_math_from_image(encoded_image):
            return client.responses.create(
                model="gpt-4.1",
                input=[{
                    "role": "user",
                    "content": [
                        {
                            "type": "input_text",
                            "text": """
        Extract the math function and convert it into a valid Python SymPy expression.

        STRICT RULES:
        - Use * for multiplication (2*x, not 2x)
        - Use ** for powers (x**2, not x^2)
        - Use standard functions: sin(x), cos(x), log(x), sqrt(x)
        - Do NOT include explanations
        - Do NOT include words
        - Output ONLY the expression

        Example:
        x^2 + 2x + 1 → x**2 + 2*x + 1
        """
                        },
                        {
                            "type": "input_image",
                            "image_url": f"data:image/jpeg;base64,{encoded_image}"
                        }
                    ]
                }]
            ).output_text

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
        st.info("Enter a problem to start.")
    else:
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

            result = response.output_text
            st.write(result)

            is_correct = result.strip().lower().startswith("correct")

            topic_name = topic

            if topic_name not in st.session_state.topic_stats:
                st.session_state.topic_stats[topic_name] = {
                    "attempts": 0,
                    "correct": 0
                }

            st.session_state.topic_stats[topic_name]["attempts"] += 1

            if is_correct:
                st.session_state.topic_stats[topic_name]["correct"] += 1

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

    Give Hint 1 (concept hint ONLY).

    Rules:
    • State the concept or method needed
    • Do NOT show steps
    • Do NOT show formulas in full
    • Do NOT solve anything
    • Max 1–2 sentences

    Problem:
    {user_input}
    """,
        max_output_tokens=80
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

            # 🔥 ADAPT BASED ON STUDENT FEEDBACK
            if understanding == "Still confused":
                instruction = """
    Explain more clearly using very simple words.
    Break it into smaller steps.
    """

            elif understanding == "Not sure":
                instruction = """
    Clarify the idea and give a slightly stronger hint.
    """

            else:
                instruction = """
    Give a minimal strategic hint only.
    """

            response = client.responses.create(
        model="gpt-4.1",
        input=f"""
    You are a Malaysian SPM / Matriculation math tutor.

    Give Hint 2 (direction hint).

    {instruction}

    Difficulty: {difficulty}

    Rules:
    • Tell the student what to do next
    • You may mention formulas briefly (no full expansion)
    • Do NOT calculate
    • Do NOT substitute values
    • Max 2–3 sentences
    • Do NOT write code or programming style
    • Do NOT use _ , ** , or Python-like expressions
    • ALL formulas must be written in LaTeX using $$ $$ 
    • Explain in words like a teacher

    Problem:
    {user_input}
    """,
        max_output_tokens=150
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

            # 🔥 ADAPT BASED ON UNDERSTANDING
            if understanding == "Still confused":
                instruction = """
    Guide step-by-step clearly.
    Show the method.
    You may show intermediate steps, but DO NOT reveal final answer.
    """

            elif understanding == "Not sure":
                instruction = """
    Give structured steps to solve.
    Show method but stop before final answer.
    """

            else:
                instruction = """
    Give a strong strategic push.
    Outline steps briefly without solving.
    """

            response = client.responses.create(
        model="gpt-4.1",
        input=f"""
    You are a Malaysian SPM / Matriculation math tutor.

    Give Hint 3 (final guidance before solving).

    {instruction}

    Difficulty: {difficulty}

    STRICT RULES:
    • Do NOT write code or programming style
    • Do NOT use _ , ** , or Python-like expressions
    • ALL formulas must be written in LaTeX using $$ $$ 
    • Explain in words like a teacher

    Example style:
    Step 1: Define the function  
    Step 2: Differentiate it  
    Step 3: Apply the method  

    Problem:
    {user_input}
    """,
        max_output_tokens=250
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

            prompt = f"""
            Solve using the correct method.

            RULES:
            - Use LaTeX (wrap equations in $$)
            - No code formatting
            - Max 5 steps only
            - Be concise

            Problem:
            {user_input}
            """

            response = ask_ai(prompt, max_tokens=1000)

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
        # (input, hints, graph, difficulty, etc.)

# =========================
# 📖 NOTES TAB
# =========================
with tab_notes:

    if "notes_output" not in st.session_state:
        st.session_state.notes_output = ""

    st.markdown("## 🤖 AI Smart Notes")

    topic = st.text_input(
        "Enter a topic:",
        placeholder="Example: Differentiation",
        key="notes_topic"
    )

    if st.button("Generate Notes"):

        topic = st.session_state.notes_topic.strip()

        if topic:
            st.write(f"Generating notes for: {topic}")

            response = client.responses.create(
                model="gpt-4.1-mini",
                input=f"""
                Create clean mathematics notes for {topic}.

                Rules:
                - DO NOT mention the word "LaTeX"
                - Use proper mathematical formatting with $$...$$ for equations
                - Use clear headings
                - Tables must NOT contain LaTeX (use normal text like a^2/b^2)
                """
            )

            # ✅ STORE RAW OUTPUT
            st.session_state.notes_output = response.output_text

        else:
            st.warning("Please enter a topic first.")

        import re

        if st.session_state.notes_output:

            # ✅ PUT IT HERE
            raw = st.session_state.notes_output

            # split content (tables vs normal text)
            parts = re.split(r"(\|.*\|)", raw)

            cleaned_parts = []

            for part in parts:
                if "|" in part:  # only clean tables
                    part = re.sub(r"\\frac{(.*?)}{(.*?)}", r"\1/\2", part)
                    part = re.sub(r"\\sqrt{(.*?)}", r"sqrt(\1)", part)
                    part = part.replace("\\leq", "<=").replace("\\geq", ">=")
                    part = part.replace("^{2}", "^2")

                cleaned_parts.append(part)

            content = "".join(cleaned_parts)

            st.markdown(content)

    # ✅ KEEP THIS INSIDE
    if "notes_output" not in st.session_state:
        st.session_state.notes_output = ""

    if "notes_title" not in st.session_state:
        st.session_state.notes_title = ""

    col1, col2, col3 = st.columns(3)

    # store result
    if "notes_output" not in st.session_state:
        st.session_state.notes_output = ""

    if "notes_title" not in st.session_state:
        st.session_state.notes_title = ""

    st.markdown("## 📚 Mathematics Notes")

    sem1_tab, sem2_tab = st.tabs(["📘 Semester 1", "📗 Semester 2"])

    # =========================
    # SEMESTER 1
    # =========================
    with sem1_tab:

        chapter = st.selectbox(
            "Choose Chapter",
            [
                "Chapter 1: Number System",
                "Chapter 2: Equations, Inequalities and Absolute Values",
                "Chapter 3: Sequences and Series",
                "Chapter 4: Matrices",
                "Chapter 5: Functions",
                "Chapter 6: Polynomials",
                "Chapter 7: Trigonometry",
                "Chapter 8: Limits and Continuity",
                "Chapter 9: Differentiation",
                "Chapter 10: Application of Differentiation"
            ]
        )

        st.markdown(f"### {chapter}")

        # ✅ Only show when selected
        if chapter == "Chapter 1: Number System":

                st.markdown("## 📘 Chapter 1: Number System")

                # =========================
                # 1.1 REAL NUMBERS
                # =========================
                with st.expander("🔢 1.1 Real Numbers", expanded=True):

                    st.markdown("### 📌 Learning Outcomes")
                    st.info("""
                    LO1: Define natural, whole, integer, rational and irrational numbers  
                    LO2: Represent numbers in decimal form  
                    LO3: Understand relationships between number sets  
                    LO4: Represent intervals on number line  
                    """)

                    st.markdown("### 🧠 Types of Numbers")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.markdown("""
            - **Natural Numbers (N)**: 1, 2, 3, ...
            - **Whole Numbers (W)**: 0, 1, 2, ...
            - **Integers (Z)**: ..., -2, -1, 0, 1, 2
                        """)

                    with col2:
                        st.markdown("""
            - **Rational Numbers (Q)**: Can be written as fraction  
            - **Irrational Numbers**: Non-terminating, non-repeating  
            - **Real Numbers (R)**: All rational + irrational
                        """)

                    st.markdown("### 📊 Relationship of Sets")

                    st.info("""
                    Natural ⊂ Whole ⊂ Integers ⊂ Rational ⊂ Real
                    """)

                # =========================
                # 1.2 COMPLEX NUMBERS
                # =========================
                with st.expander("🧩 1.2 Complex Numbers"):

                    st.markdown("### 📌 Learning Outcomes")
                    st.info("""
                    LO1: Represent complex numbers  
                    LO2: Equality of complex numbers  
                    LO3: Conjugate of complex numbers  
                    LO4: Polar form  
                    """)

                    st.markdown("### 🔢 General Form")
                    st.latex(r"z = a + bi")

                    st.markdown("""
            - **a** = real part  
            - **b** = imaginary part  
            - **i = √(-1)**  
                    """)

                    st.markdown("### ⚖️ Equality")

                    st.latex(r"a + bi = c + di \Rightarrow a=c,\ b=d")

                # =========================
                # CONJUGATE
                # =========================
                with st.expander("🔄 Conjugate of Complex Numbers"):

                    st.markdown("### 📌 Definition")

                    st.latex(r"\overline{z} = a - bi")

                    st.markdown("""
            - Changes sign of imaginary part  
            - Useful for division
                    """)

                    st.markdown("### ➕ Operations")

                    st.latex(r"(a+bi)+(c+di) = (a+c) + (b+d)i")
                    st.latex(r"(a+bi)-(c+di) = (a-c) + (b-d)i")
                    st.latex(r"(a+bi)(c+di) = (ac - bd) + (ad + bc)i")

                # =========================
                # MODULUS & ARGUMENT
                # =========================
                with st.expander("📐 Modulus & Argand Diagram"):

                    st.markdown("### 📏 Modulus")

                    st.latex(r"|z| = \sqrt{a^2 + b^2}")

                    st.markdown("### 📐 Argument (θ)")

                    st.latex(r"\theta = \tan^{-1}\left(\frac{b}{a}\right)")

                    st.warning("⚠️ Adjust θ based on quadrant!")

                # =========================
                # POLAR FORM
                # =========================
                with st.expander("🌀 Polar Form of Complex Numbers"):

                    st.markdown("### 📌 Formula")

                    st.latex(r"z = r(\cos \theta + i \sin \theta)")

                    st.markdown("""
            Where:
            - r = modulus  
            - θ = argument  
                    """)

                    st.markdown("### 🧠 Steps")

                    st.markdown("""
            1. Find modulus: r = √(a² + b²)  
            2. Find argument θ  
            3. Substitute into polar form  
                    """)

                # =========================
                # NUMBER LINE & INTERVALS
                # =========================
                with st.expander("📏 Number Line & Intervals"):

                    st.markdown("### 🔢 Inequalities")

                    st.markdown("""
            - a = b → equal  
            - a < b → less than  
            - a > b → greater than  
            - a ≤ b → less than or equal  
            - a ≥ b → greater than or equal  
                    """)

                    st.markdown("### 📦 Intervals")

                    st.markdown("""
            - (a, b) → open interval  
            - [a, b] → closed interval  
            - (a, b] or [a, b) → mixed  
                    """)

    # =========================
    # SEMESTER 2
    # =========================
    with sem2_tab:

        chapter = st.selectbox(
            "Choose Chapter",
            [
                "Chapter 1: Numerical Solution",
                "Chapter 2: Integration",
                "Chapter 3: First Order Differential Equations",
                "Chapter 4: Conics",
                "Chapter 5: Vectors",
                "Chapter 6: Data Description",
                "Chapter 7: Probability",
                "Chapter 8: Random Variables",
                "Chapter 9: Special Probability Distribution"
            ]
        )

        # ✅ Only show when selected
        if chapter == "Chapter 1: Numerical Solution":

            st.markdown("## 📘 Chapter 1: Numerical Solutions")

            # =========================
            # 1.1 SECTION
            # =========================
            with st.expander("📊 1.1 Numerical Solution of Equations", expanded=True):

                st.markdown("### 📌 Learning Outcome")
                st.info("Locate approximately a root of an equation using graphical or algebraic methods.")

                st.markdown("""
    Many equations **cannot be solved exactly**, so we use **numerical methods** to find approximate solutions.

    ### 🧠 Key Idea
    There are two main steps:
    1. Find an **initial approximate value**
    2. Improve it using an **iterative process**
    """)

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("### 📊 Graphical Method")
                    st.markdown("""
    - Sketch the graph of **y = f(x)**
    - Root = where graph cuts x-axis
    """)

                with col2:
                    st.markdown("### 🔢 Algebraic Method")
                    st.markdown("""
    - Choose a and b
    - f(a), f(b) opposite signs
    → root exists between them
    """)

            # =========================
            # 1.2 SECTION
            # =========================
            with st.expander("🧩 1.2 Newton-Raphson Method"):

                st.markdown("### 📌 Learning Outcome")
                st.info("Find the root using Newton-Raphson Method")

                st.latex(r"x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}")

                st.markdown("""
    Steps:
    1. Find f(x), f'(x)
    2. Choose x₀
    3. Iterate until accurate
    """)
        if chapter == "Chapter 2: Integration":

            st.markdown("## 📗 Chapter 2: Integration")

            # =========================
            # 2.1 Integration of Functions
            # =========================
            with st.expander("📘 2.1 Integration of Functions", expanded=True):

                st.markdown("### 📌 Learning Outcomes")
                st.info("""
                LO1: Relate integration and differentiation  
                LO2: Define basic rules of integration  
                LO3: Integrate exponential functions
                """)

                st.markdown("### 🔁 Relationship")
                st.latex(r"F(x) = x^3 \quad \Rightarrow \quad f(x) = 3x^2")

                st.markdown("Integration is the reverse of differentiation.")

                st.latex(r"\int f'(x)\,dx = f(x) + C")

            # =========================
            # 2.2 Basic Rules
            # =========================
            with st.expander("📘 2.2 Basic Rules of Integration"):

                st.markdown("### 📦 Core Rules")

                col1, col2 = st.columns(2)

                with col1:
                    st.latex(r"\int k\,dx = kx + C")
                    st.latex(r"\int x^n dx = \frac{x^{n+1}}{n+1} + C")
                    st.latex(r"\int kf(x)dx = k \int f(x)dx")

                with col2:
                    st.latex(r"\int [f(x) \pm g(x)]dx = \int f(x)dx \pm \int g(x)dx")
                    st.latex(r"\int \frac{1}{x}dx = \ln|x| + C")
                    st.latex(r"\int \frac{1}{ax+b}dx = \frac{1}{a}\ln|ax+b| + C")

                st.warning("⚠️ ∫f(x)g(x)dx ≠ ∫f(x)dx × ∫g(x)dx")

            # =========================
            # 2.3 Techniques
            # =========================
            with st.expander("📘 2.3 Techniques of Integration"):

                st.markdown("### 🔄 Substitution Method")
                st.latex(r"\int f(x)g'(x)dx = \int f(u)du")

                st.markdown("""
                Steps:
                1. Let u = g(x)
                2. Find du
                3. Substitute
                """)

                st.markdown("### 🧩 Integration by Parts")
                st.latex(r"\int u\,dv = uv - \int v\,du")

                st.info("Use **LPET** → Logarithmic, Polynomial, Exponential, Trigonometric")

            # =========================
            # 2.4 Definite Integrals
            # =========================
            with st.expander("📘 2.4 Definite Integrals"):

                st.latex(r"\int_a^b f(x)dx = F(b) - F(a)")

                st.markdown("### Properties")

                st.latex(r"\int_a^b f(x)dx = -\int_b^a f(x)dx")
                st.latex(r"\int_a^a f(x)dx = 0")
                st.latex(r"\int_a^c f(x)dx = \int_a^b f(x)dx + \int_b^c f(x)dx")

            # =========================
            # 2.5 Area of Region
            # =========================
            with st.expander("📘 2.5 Area of a Region"):

                st.markdown("### 📐 Area under curve")
                st.latex(r"Area = \int_a^b f(x)dx")

                st.markdown("### Between two curves")
                st.latex(r"Area = \int_a^b [f(x) - g(x)]dx")

                st.info("Area is always positive")

            # =========================
            # Volume of Revolution
            # =========================
            with st.expander("🧊 Volume of Solid of Revolution"):

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("About x-axis")
                    st.latex(r"V = \pi \int_a^b y^2 dx")

                with col2:
                    st.markdown("About y-axis")
                    st.latex(r"V = \pi \int_c^d x^2 dy")

            # =========================
            # Trapezoidal Rule
            # =========================
            with st.expander("📊 Trapezoidal Rule"):

                st.latex(r"\int_a^b f(x)dx \approx \frac{h}{2}[y_0 + y_n + 2(y_1 + ... + y_{n-1})]")

                st.markdown("""
                Steps:
                1. Find h = (b-a)/n  
                2. Create table  
                3. Apply formula  
                """)

            # =========================
            # Trigonometric Integrals
            # =========================
            with st.expander("📐 Trigonometric Integrals"):

                st.latex(r"\int \sin x dx = -\cos x + C")
                st.latex(r"\int \cos x dx = \sin x + C")
                st.latex(r"\int \sec^2 x dx = \tan x + C")

                st.info("If power is odd → use substitution")

            # =========================
            # Test Yourself
            # =========================
            with st.expander("📝 Test Yourself"):

                st.markdown("""
                1. ∫(e^x + e^{-x})dx  
                2. ∫4^x dx  
                3. ∫(x+3)^4 dx  
                """)

        if chapter == "Chapter 3: First Order Differential Equations":

            st.markdown("## 📚 Chapter 3: First Order Differential Equations")

            # -----------------------
            # 1. Basic Concepts
            # -----------------------
            with st.expander("📌 Basic Concepts of Differential Equations"):

                st.markdown("""
            **Differential Equation (DE):**  
            An equation involving derivatives of a function.

            **Order:** Highest derivative in the equation  
            **Degree:** Power of the highest derivative  

            **General Solution:**  
            Contains arbitrary constant  
            Example: y = Ae^(kx)

            **Particular Solution:**  
            Obtained by substituting given conditions
                """)

            # -----------------------
            # 2. Separable Variables
            # -----------------------
            with st.expander("🔀 Separable Variables"):

                st.latex(r"\frac{dy}{dx} = P(x)Q(y)")

                st.markdown("### Steps:")
                st.markdown("""
            1. Separate variables  
            2. Integrate both sides  
                """)

                st.latex(r"\frac{1}{Q(y)} dy = P(x) dx")
                st.latex(r"\int \frac{1}{Q(y)} dy = \int P(x) dx")

            # -----------------------
            # 3. Integrating Factor
            # -----------------------
            with st.expander("🧠 Integrating Factor Method"):

                st.latex(r"\frac{dy}{dx} + P(x)y = Q(x)")

                st.markdown("### Steps:")

                st.markdown("""
            1. Standard form: dy/dx + P(x)y = Q(x)  
            2. Integrating factor:  
                """)

                st.latex(r"V(x) = e^{\int P(x) dx}")

                st.markdown("""
            3. Multiply entire equation by V(x)  
            4. Apply product rule  
            5. Integrate both sides  
                """)

                st.latex(r"\frac{d}{dx}(V(x)y) = V(x)Q(x)")

            # -----------------------
            # 4. Applications
            # -----------------------
            with st.expander("🌍 Applications of Differential Equations"):

                st.markdown("### (a) Population Growth")

                st.latex(r"\frac{dP}{dt} = kP")
                st.latex(r"P = Ae^{kt}")

                st.markdown("""
            - Growth rate proportional to population  
            - Used in bacteria growth problems  
                """)

                st.markdown("### (b) Radioactive Decay")

                st.latex(r"\frac{dC}{dt} = -kC")
                st.latex(r"C = Ae^{-kt}")

                st.markdown("""
            - Decay rate proportional to amount present  
                """)

                st.markdown("### (c) Newton's Law of Cooling")

                st.latex(r"\frac{d\theta}{dt} = -k(\theta - a)")
                st.latex(r"\theta = Ae^{-kt} + a")

                st.markdown("""
            - Temperature approaches surrounding temperature  
                """)

        if chapter == "Chapter 4: Conics":

            st.markdown("## 📘 Chapter 4: Conics")

            # =========================
            # 4.1 CIRCLES
            # =========================
            with st.expander("🔵 4.1 Circles", expanded=True):

                st.markdown("### 📌 Learning Outcomes")
                st.info("""
                LO1: Equation of circle  
                LO2: Centre & radius  
                LO3: Intersection  
                LO4: Tangent & normal  
                LO5: Length of tangent  
                """)

                # -------------------------
                # Equation
                # -------------------------
                with st.expander("📘 Equation of Circle"):

                    st.markdown("### Standard Form")
                    st.latex(r"(x - h)^2 + (y - k)^2 = r^2")

                    st.markdown("### General Form")
                    st.latex(r"x^2 + y^2 + 2gx + 2fy + c = 0")

                    st.markdown("""
                    Centre = (-g, -f)  
                    Radius = √(g² + f² - c)
                    """)

                # -------------------------
                # Centre & Radius
                # -------------------------
                with st.expander("📍 Centre & Radius (Completing Square)"):

                    st.markdown("""
                    Steps:
                    1. Group x and y terms  
                    2. Complete the square  
                    3. Compare with standard form  
                    """)

                # -------------------------
                # Intersection
                # -------------------------
                with st.expander("🔀 Points of Intersection"):

                    st.markdown("### Circle & Line")

                    st.latex(r"d = \frac{|ax + by + c|}{\sqrt{a^2 + b^2}}")

                    st.markdown("""
                    - d > r → no intersection  
                    - d = r → tangent  
                    - d < r → 2 points  
                    """)

                    st.markdown("### Two Circles")

                    st.markdown("""
                    Use discriminant:

                    - > 0 → 2 points  
                    - = 0 → 1 point  
                    - < 0 → no intersection  
                    """)

                # -------------------------
                # Tangent & Normal
                # -------------------------
                with st.expander("📏 Tangent & Normal"):

                    st.latex(r"xx_1 + yy_1 + g(x + x_1) + f(y + y_1) + c = 0")

                    st.markdown("""
                    Steps:
                    1. Find gradient of radius  
                    2. Use m₁m₂ = -1  
                    3. Use y - y₁ = m(x - x₁)  
                    """)

                # -------------------------
                # Length of Tangent
                # -------------------------
                with st.expander("📐 Length of Tangent"):

                    st.latex(r"d = \sqrt{x_1^2 + y_1^2 + 2gx_1 + 2fy_1 + c}")
                    st.latex(r"d^2 = D^2 - r^2")

            # =========================
            # 4.2 ELLIPSE
            # =========================
            with st.expander("🟠 4.2 Ellipse"):

                st.markdown("### Standard Equation")
                st.latex(r"\frac{(x-h)^2}{a^2} + \frac{(y-k)^2}{b^2} = 1")

                st.markdown("### Relationships")
                st.latex(r"c^2 = a^2 - b^2 \ (a > b)")
                st.latex(r"c^2 = b^2 - a^2 \ (b > a)")

                st.markdown("### Key Terms")

                st.markdown("""
                Centre: (h, k)

                Major vertices:
                - (h ± a, k) or (h, k ± a)

                Minor vertices:
                - (h ± b, k) or (h, k ± b)

                Foci:
                - (h ± c, k) or (h, k ± c)
                """)

            # =========================
            # 4.3 PARABOLA
            # =========================
            with st.expander("🟣 4.3 Parabola"):

                st.markdown("### Definition")
                st.write("""
                A parabola is a set of points equidistant from:
                - a focus
                - a directrix
                """)

                st.markdown("### Standard Forms")

                st.latex(r"(y-k)^2 = 4p(x-h)")
                st.latex(r"(x-h)^2 = 4p(y-k)")

                st.markdown("""
                Vertex: (h, k)

                Focus:
                - (h + p, k)
                - (h, k + p)

                Directrix:
                - x = h - p
                - y = k - p
                """)

        # =========================
        # 📊 VISUAL TAB
        # =========================
        with tab_visual:

            st.subheader("📊 Visual Learning")

            topic = st.selectbox(
                "Choose Topic to Visualize",
                [
                    "Functions",
                    "3D Graph",
                    "Trigonometry",
                    "Differentiation",
                    "Numerical Solution",
                    "Probability Distribution",
                    "Complex Numbers (Argand)",
                    "Conics (Circles, Parabola, Ellipse)"
                ]
            )

            if topic == "Functions":

                expr = st.text_input("Enter f(x):", "x**2")

                if st.button("Plot"):

                    x = sp.symbols('x')
                    f = sp.sympify(expr)
                    f_lamb = sp.lambdify(x, f, "numpy")

                    x_vals = np.linspace(-10, 10, 1000)
                    y_vals = f_lamb(x_vals)

                    fig = go.Figure()

                    fig.add_trace(go.Scatter(
                        x=x_vals,
                        y=y_vals,
                        mode='lines',
                        name='f(x)'
                    ))

                    fig.update_layout(title="Interactive Graph")

                    st.plotly_chart(fig, use_container_width=True)

            # =========================
            # 3D GRAPH
            # =========================
            elif topic == "3D Graph":

                expr = st.text_input("Enter z = f(x, y):", "x**2 + y**2")

                if st.button("Plot 3D"):

                    import re  # ✅ can also put this at top of file

                    # 🔥 FIX USER INPUT HERE (RIGHT BEFORE sympify)
                    expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)

                    x, y = sp.symbols('x y')
                    f = sp.sympify(expr)  # ✅ now safe
                    f_lamb = sp.lambdify((x, y), f, "numpy")

                    x_vals = np.linspace(-5, 5, 50)
                    y_vals = np.linspace(-5, 5, 50)
                    X, Y = np.meshgrid(x_vals, y_vals)
                    Z = f_lamb(X, Y)

                    fig = go.Figure(data=[go.Surface(z=Z, x=X, y=Y)])
                    fig.update_layout(title="3D Surface Plot")

                    st.plotly_chart(fig, use_container_width=True)

            # =========================
            # TRIG
            # =========================
            elif topic == "Trigonometry":

                func = st.selectbox("Choose Function", ["sin", "cos", "tan"])

                x_vals = np.linspace(-2*np.pi, 2*np.pi, 1000)

                if func == "sin":
                    y_vals = np.sin(x_vals)
                elif func == "cos":
                    y_vals = np.cos(x_vals)
                else:
                    y_vals = np.tan(x_vals)
                    y_vals[np.abs(y_vals) > 10] = np.nan  # fix asymptote explosion

                fig = go.Figure()

                fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines'))

                st.plotly_chart(fig, use_container_width=True)

            # =========================
            # DIFFERENTIATION
            # =========================
            elif topic == "Differentiation":

                st.markdown("### 📈 Differentiation Visualizer")

                expr = st.text_input("Enter function:", "x**2")

                col1, col2 = st.columns(2)

                with col1:
                    x_min = st.number_input("Min x", value=-10.0)

                with col2:
                    x_max = st.number_input("Max x", value=10.0)

                if x_min >= x_max:
                    st.error("Min x must be less than Max x")
                    st.stop()

                x = sp.symbols('x')
                f = sp.sympify(expr)
                f_prime = sp.diff(f, x)

                f_lamb = sp.lambdify(x, f, "numpy")
                f_prime_lamb = sp.lambdify(x, f_prime, "numpy")

                # ✅ STEP 2 GOES HERE
                x_vals = np.linspace(x_min, x_max, 1000)

                a = st.slider(
                    "Choose point x = a",
                    float(x_min),
                    float(x_max),
                    float((x_min + x_max)/2)
                )

                import re

                # Fix missing multiplication like 3x → 3*x
                expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)

                # Fix x(x+1) → x*(x+1)
                expr = re.sub(r'([a-zA-Z])\(', r'\1*(', expr)

                # Fix )( → )*(
                expr = re.sub(r'\)([a-zA-Z])', r')*\1', expr)

                # Convert ^ → **
                expr = expr.replace("^", "**")

                f = sp.sympify(expr)
                f_prime = sp.diff(f, x)

                st.latex(rf"f'(x) = {sp.latex(f_prime)}")

                # Convert to numpy
                f_lamb = sp.lambdify(x, f, "numpy")
                f_prime_lamb = sp.lambdify(x, f_prime, "numpy")

                # Range
                x_vals = np.linspace(-10, 10, 1000)
                y_vals = f_lamb(x_vals)

                y_a = f_lamb(a)
                slope = f_prime_lamb(a)

                # Tangent line: y = m(x - a) + f(a)
                tangent = slope * (x_vals - a) + y_a

                fig = go.Figure()

                # Function curve
                fig.add_trace(go.Scatter(
                    x=x_vals,
                    y=y_vals,
                    mode='lines',
                    name='f(x)'
                ))

                # Tangent line
                fig.add_trace(go.Scatter(
                    x=x_vals,
                    y=tangent,
                    mode='lines',
                    name='Tangent',
                    line=dict(dash='dash')
                ))

                # Point of contact
                fig.add_trace(go.Scatter(
                    x=[a],
                    y=[y_a],
                    mode='markers+text',
                    text=[f"x={a:.2f}"],
                    textposition="top center"
                ))

                fig.update_layout(
                    title="Function and Tangent Line",
                    xaxis_title="x",
                    yaxis_title="y"
                )

                st.plotly_chart(fig, use_container_width=True)

                # Show gradient value
                st.success(f"Gradient at x = {a:.2f} is {slope:.3f}")

            # =========================
            # NUMERICAL SOLUTION
            # =========================
            elif topic == "Numerical Solution":

                st.markdown("### 🔍 Intersection of Two Functions")

                expr1 = st.text_input("Enter f(x):", "x**2")
                expr2 = st.text_input("Enter g(x) (leave blank for x-axis):", "")

                is_root_mode = False

                if expr2.strip() == "":
                    expr2 = "0"
                    is_root_mode = True

                if expr2.strip() == "":
                    expr2 = "0"

                x0 = st.number_input("Initial guess (x0)", value=1.0)

                if st.button("Find Intersection"):

                    x = sp.symbols('x')

                    f = sp.sympify(expr1)
                    g = sp.sympify(expr2)

                    h = f - g   # 🔥 key idea
                    h_prime = sp.diff(h, x)

                    # Convert to numpy
                    f_lamb = sp.lambdify(x, f, "numpy")
                    g_lamb = sp.lambdify(x, g, "numpy")

                    # Newton Method
                    for i in range(10):
                        x1 = x0 - float(h.subs(x, x0)) / float(h_prime.subs(x, x0))
                        x0 = x1

                    root = x0
                    y_val = f_lamb(root)

                    # ✅ PUT YOUR MESSAGE HERE
                    if float(expr2) == 0:
                        st.success(f"Root at x ≈ {root:.4f}")
                    else:
                        st.success(f"Intersection at x ≈ {root:.4f}, y ≈ {y_val:.4f}")

                    # =========================
                    # 📊 GRAPH
                    # =========================
                    x_vals = np.linspace(-10, 10, 1000)

                    y1 = f_lamb(x_vals)
                    y2 = g_lamb(x_vals)

                    # 🔥 Fix for constant functions
                    if np.isscalar(y1):
                        y1 = np.full_like(x_vals, y1)

                    if np.isscalar(y2):
                        y2 = np.full_like(x_vals, y2)

                    fig = go.Figure()

                    # f(x)
                    fig.add_trace(go.Scatter(
                        x=x_vals,
                        y=y1,
                        mode='lines',
                        name='f(x)'
                    ))

                    # g(x)
                    fig.add_trace(go.Scatter(
                        x=x_vals,
                        y=y2,
                        mode='lines',
                        name='g(x)'
                    ))

                    # Intersection point
                    fig.add_trace(go.Scatter(
                        x=[root],
                        y=[y_val],
                        mode='markers+text',
                        text=[f"x ≈ {root:.2f}"],
                        textposition="top center",
                        marker=dict(size=10)
                    ))

                    fig.update_layout(
                        title="Intersection of Two Functions",
                        xaxis_title="x",
                        yaxis_title="y"
                    )

                    st.plotly_chart(fig, use_container_width=True)

            # =========================
            # COMPLEX NUMBERS (ARGAND)
            # =========================
            elif topic == "Complex Numbers (Argand)":

                st.markdown("### 🧩 Argand Diagram Visualiser")

                col1, col2 = st.columns(2)

                with col1:
                    real = st.slider("Real part (a)", -10.0, 10.0, 3.0)
                with col2:
                    imag = st.slider("Imaginary part (b)", -10.0, 10.0, 4.0)

                # Modulus
                r = np.sqrt(real**2 + imag**2)

                st.latex(rf"|z| = \sqrt{{{real}^2 + {imag}^2}} = {r:.2f}")

                # Argument
                theta = np.arctan2(imag, real)
                st.latex(rf"\theta = {theta:.2f} \text{{ rad}}")

                # Plot Argand diagram
                fig = go.Figure()

                # Vector from origin
                fig.add_trace(go.Scatter(
                    x=[0, real],
                    y=[0, imag],
                    mode='lines+markers',
                    name='z',
                ))

                # Point label
                fig.add_trace(go.Scatter(
                    x=[real],
                    y=[imag],
                    mode='text',
                    text=[f"{real} + {imag}i"],
                    textposition="top center"
                ))

                fig.update_layout(
                    title="Argand Diagram",
                    xaxis_title="Real Axis",
                    yaxis_title="Imaginary Axis",
                    xaxis=dict(range=[-10, 10]),
                    yaxis=dict(range=[-10, 10]),
                    showlegend=False
                )

                st.plotly_chart(fig, use_container_width=True)

                # Polar form
                st.markdown("### 🌀 Polar Form")
                st.latex(rf"z = {r:.2f}(\cos({theta:.2f}) + i\sin({theta:.2f}))")

            # =========================
            # PROBABILITY DISTRIBUTION
            # =========================
            elif topic == "Probability Distribution":

                st.markdown("### 📊 Probability Distributions")

                dist = st.selectbox(
                    "Choose Distribution",
                    ["Binomial", "Poisson", "Standard Normal"],
                    key="dist_select_visual"
                )

                # =========================
                # BINOMIAL
                # =========================
                if dist == "Binomial":

                    n = st.slider("Number of trials (n)", 1, 50, 10)
                    p = st.slider("Probability of success (p)", 0.0, 1.0, 0.5)

                    x_vals = np.arange(0, n+1)

                    def binomial_pmf(x, n, p):
                        return math.comb(n, x) * (p**x) * ((1-p)**(n-x))

                    y_vals = [binomial_pmf(x, n, p) for x in x_vals]

                    fig = go.Figure()
                    fig.add_trace(go.Bar(x=x_vals, y=y_vals))
                    st.plotly_chart(fig, use_container_width=True)

                    # 🎯 Probability
                    st.markdown("### 🎯 Calculate Probability")

                    prob_type = st.selectbox(
                        "Select Type",
                        ["P(X = x)", "P(X < a)", "P(X > a)", "P(a < X < b)"],
                        key="binomial_prob"
                    )

                    if prob_type == "P(X = x)":
                        x_val = st.slider("x", 0, n, 3)
                        prob = binomial_pmf(x_val, n, p)

                    elif prob_type == "P(X < a)":
                        a = st.slider("a", 0, n, 3)
                        prob = sum(binomial_pmf(x, n, p) for x in range(a))

                    elif prob_type == "P(X > a)":
                        a = st.slider("a", 0, n, 3)
                        prob = sum(binomial_pmf(x, n, p) for x in range(a+1, n+1))

                    else:
                        a = st.slider("a", 0, n-1, 2)
                        b = st.slider("b", 1, n, 5)

                        if a >= b:
                            st.warning("Ensure a < b")
                            st.stop()

                        prob = sum(binomial_pmf(x, n, p) for x in range(a+1, b))

                    st.success(f"Probability ≈ {prob:.4f}")

                # =========================
                # POISSON
                # =========================
                elif dist == "Poisson":

                    lam = st.slider("Lambda (λ)", 0.1, 10.0, 3.0)

                    x_vals = np.arange(0, 20)

                    def poisson_pmf(x, lam):
                        return (lam**x * math.exp(-lam)) / math.factorial(x)

                    y_vals = [poisson_pmf(x, lam) for x in x_vals]

                    fig = go.Figure()
                    fig.add_trace(go.Bar(x=x_vals, y=y_vals))
                    st.plotly_chart(fig, use_container_width=True)

                    # 🎯 Probability
                    st.markdown("### 🎯 Calculate Probability")

                    prob_type = st.selectbox(
                        "Select Type",
                        ["P(X = x)", "P(X < a)", "P(X > a)", "P(a < X < b)"],
                        key="poisson_prob"
                    )

                    if prob_type == "P(X = x)":
                        x_val = st.slider("x", 0, 20, 3)
                        prob = poisson_pmf(x_val, lam)

                    elif prob_type == "P(X < a)":
                        a = st.slider("a", 0, 20, 3)
                        prob = sum(poisson_pmf(x, lam) for x in range(a))

                    elif prob_type == "P(X > a)":
                        a = st.slider("a", 0, 20, 3)
                        prob = sum(poisson_pmf(x, lam) for x in range(a+1, 20))

                    else:
                        a = st.slider("a", 0, 19, 2)
                        b = st.slider("b", 1, 20, 5)

                        if a >= b:
                            st.warning("Ensure a < b")
                            st.stop()

                        prob = sum(poisson_pmf(x, lam) for x in range(a+1, b))

                    st.success(f"Probability ≈ {prob:.4f}")

                # =========================
                # STANDARD NORMAL
                # =========================
                elif dist == "Standard Normal":

                    st.markdown("### 📊 Standard Normal Distribution")

                    mode = st.selectbox(
                    "Choose Mode",
                    ["Z given", "X → Z conversion"],
                    key="mode_select"
                )

                    prob_type = st.selectbox(
                    "Select Probability",
                    ["P(Z < a)", "P(Z > a)", "P(a < Z < b)"],
                    key="prob_type_select"
                )

                    x_vals = np.linspace(-4, 4, 1000)

                    def normal_pdf(x):
                        return (1 / np.sqrt(2*np.pi)) * np.exp(-0.5 * x**2)

                    y_vals = normal_pdf(x_vals)

                    fig = go.Figure()

                    fig.add_trace(go.Scatter(
                        x=x_vals,
                        y=y_vals,
                        mode='lines',
                        name='PDF'
                    ))

                    # =========================
                    # MODE 1: Z GIVEN
                    # =========================
                    if mode == "Z given":

                        if prob_type == "P(Z < a)":

                            a = st.slider("Z value", -3.0, 3.0, 1.0)

                            mask = x_vals <= a

                            prob = 0.5 * (1 + math.erf(a / np.sqrt(2)))

                        elif prob_type == "P(Z > a)":

                            a = st.slider("Z value", -3.0, 3.0, 2.0)

                            mask = x_vals >= a

                            prob = 1 - (0.5 * (1 + math.erf(a / np.sqrt(2))))

                        else:

                            a = st.slider("a", -3.0, 3.0, -1.0)
                            b = st.slider("b", -3.0, 3.0, 1.0)

                            if a >= b:
                                st.warning("Ensure a < b")
                                st.stop()

                            mask = (x_vals >= a) & (x_vals <= b)

                            prob = (0.5 * (1 + math.erf(b / np.sqrt(2)))) - \
                                (0.5 * (1 + math.erf(a / np.sqrt(2))))

                    # =========================
                    # MODE 2: X → Z CONVERSION
                    # =========================
                    else:

                        mean = st.number_input("Mean (μ)", value=0.0)
                        sd = st.number_input("Standard Deviation (σ)", value=1.0)

                        st.markdown("### 🔄 Standardisation Formula")


                        if prob_type == "P(Z < a)":

                            x_val = st.number_input("Enter X value", value=1.0)

                            z = (x_val - mean) / sd
                            st.write(f"Z = {z:.3f}")

                            mask = x_vals <= z

                            prob = 0.5 * (1 + math.erf(z / np.sqrt(2)))

                        elif prob_type == "P(Z > a)":

                            x_val = st.number_input("Enter X value", value=2.0)

                            z = (x_val - mean) / sd
                            st.write(f"Z = {z:.3f}")

                            mask = x_vals >= z

                            prob = 1 - (0.5 * (1 + math.erf(z / np.sqrt(2))))

                        else:

                            x1 = st.number_input("X1", value=-1.0)
                            x2 = st.number_input("X2", value=1.0)

                            z1 = (x1 - mean) / sd
                            z2 = (x2 - mean) / sd

                            st.write(f"Z1 = {z1:.3f}, Z2 = {z2:.3f}")

                            mask = (x_vals >= z1) & (x_vals <= z2)

                            prob = (0.5 * (1 + math.erf(z2 / np.sqrt(2)))) - \
                                (0.5 * (1 + math.erf(z1 / np.sqrt(2))))

                    # =========================
                    # SHADED AREA
                    # =========================
                    fig.add_trace(go.Scatter(
                        x=x_vals[mask],
                        y=y_vals[mask],
                        fill='tozeroy',
                        mode='lines',
                        name='Probability Area'
                    ))

                    fig.update_layout(title="Standard Normal Distribution")

                    st.plotly_chart(fig, use_container_width=True)

                    # =========================
                    # RESULT
                    # =========================
                    st.success(f"Probability ≈ {prob:.4f}")

                    # =========================
                    # Z-TABLE INSIGHT
                    # =========================
                    st.info("""
                    💡 Interpretation:
                    - This value represents the **area under the curve**
                    - Equivalent to values from the **Z-table**
                    - Graph helps you SEE what the table means
                    """)

                    st.markdown("## 📈 Normal Distribution Visualizer")

                    case = st.selectbox(
                        "Select Probability Type",
                        ["P(Z < a)", "P(Z > a)", "P(a < Z < b)"]
                    )

                    # X values
                    x = np.linspace(-4, 4, 1000)
                    y = norm.pdf(x)

                    fig = go.Figure()

                    # Base curve
                    fig.add_trace(go.Scatter(
                        x=x,
                        y=y,
                        mode='lines',
                        name='Normal Curve'
                    ))

                    if case == "P(Z < a)":

                        a = st.slider("Select a", -3.0, 3.0, 1.0)

                        mask = x <= a
                        prob = norm.cdf(a)

                        fig.add_trace(go.Scatter(
                            x=x[mask],
                            y=y[mask],
                            fill='tozeroy',
                            mode='lines',
                            name='Shaded Area'
                        ))

                        st.success(f"P(Z < {a}) = {prob:.4f}")

                    elif case == "P(Z > a)":

                        a = st.slider("Select a", -3.0, 3.0, 1.0)

                        mask = x >= a
                        prob = 1 - norm.cdf(a)

                        fig.add_trace(go.Scatter(
                            x=x[mask],
                            y=y[mask],
                            fill='tozeroy',
                            mode='lines',
                            name='Shaded Area'
                        ))

                        st.success(f"P(Z > {a}) = {prob:.4f}")

                    elif case == "P(a < Z < b)":

                        a = st.slider("Select a", -3.0, 3.0, -1.0)
                        b = st.slider("Select b", -3.0, 3.0, 1.0)

                        if a < b:

                            mask = (x >= a) & (x <= b)
                            prob = norm.cdf(b) - norm.cdf(a)

                            fig.add_trace(go.Scatter(
                                x=x[mask],
                                y=y[mask],
                                fill='tozeroy',
                                mode='lines',
                                name='Shaded Area'
                            ))

                            st.success(f"P({a} < Z < {b}) = {prob:.4f}")
                        else:
                            st.error("Make sure a < b")

                    frames = []

                    for i in range(50):
                        cutoff = -4 + i * (8 / 50)
                        mask = x <= cutoff

                        frames.append(go.Frame(
                            data=[go.Scatter(
                                x=x[mask],
                                y=y[mask],
                                fill='tozeroy',
                                mode='lines'
                            )]
                        ))

                    fig.frames = frames

                    fig.update_layout(
                        title="Standard Normal Distribution",
                        xaxis_title="Z",
                        yaxis_title="Density",
                        updatemenus=[{
                            "type": "buttons",
                            "buttons": [{
                                "label": "▶ Animate",
                                "method": "animate",
                                "args": [None, {"frame": {"duration": 50}}]
                            }]
                        }]
                    )

                    st.plotly_chart(fig, use_container_width=True)

            elif topic == "Conics (Circles, Parabola, Ellipse)":

                st.markdown("### 📐 Conics Visualiser")

                conic_type = st.selectbox(
                    "Choose Conic",
                    ["Circle", "Parabola", "Ellipse"]
                )

                # =========================
                # CIRCLE
                # =========================
                if conic_type == "Circle":

                    h = st.slider("Center x (h)", -5.0, 5.0, 0.0)
                    k = st.slider("Center y (k)", -5.0, 5.0, 0.0)
                    r = st.slider("Radius", 1.0, 10.0, 3.0)

                    theta = np.linspace(0, 2*np.pi, 500)
                    x = h + r * np.cos(theta)
                    y = k + r * np.sin(theta)

                    fig = go.Figure()

                    # Circle
                    fig.add_trace(go.Scatter(x=x, y=y, mode='lines'))

                    # Center
                    fig.add_trace(go.Scatter(x=[h], y=[k], mode='markers+text',
                                            text=["Center"],
                                            textposition="top center"))

                    fig.update_layout(
                        title="Circle",
                        xaxis=dict(scaleanchor="y"),
                        yaxis=dict(),
                    )

                    st.plotly_chart(fig, use_container_width=True)

                    st.latex(rf"(x - {h})^2 + (y - {k})^2 = {r}^2")

                # =========================
                # PARABOLA
                # =========================
                elif conic_type == "Parabola":

                    h = st.slider("Vertex x (h)", -5.0, 5.0, 0.0)
                    k = st.slider("Vertex y (k)", -5.0, 5.0, 0.0)
                    p = st.slider("p (focus distance)", 0.5, 5.0, 2.0)

                    x = np.linspace(-10, 10, 500)
                    y = (1/(4*p))*(x - h)**2 + k

                    fig = go.Figure()

                    # Parabola
                    fig.add_trace(go.Scatter(x=x, y=y, mode='lines'))

                    # Vertex
                    fig.add_trace(go.Scatter(x=[h], y=[k], mode='markers+text',
                                            text=["Vertex"],
                                            textposition="bottom center"))

                    # Focus
                    fig.add_trace(go.Scatter(x=[h], y=[k+p], mode='markers+text',
                                            text=["Focus"],
                                            textposition="top center"))

                    # Directrix
                    fig.add_shape(
                        type="line",
                        x0=-10, x1=10,
                        y0=k-p, y1=k-p,
                        line=dict(dash='dash')
                    )

                    fig.update_layout(title="Parabola")

                    st.plotly_chart(fig, use_container_width=True)

                    st.latex(rf"(x - {h})^2 = {4*p}(y - {k})")

                # =========================
                # ELLIPSE
                # =========================
                elif conic_type == "Ellipse":

                    h = st.slider("Center x (h)", -5.0, 5.0, 0.0)
                    k = st.slider("Center y (k)", -5.0, 5.0, 0.0)
                    a = st.slider("a (major axis)", 2.0, 10.0, 5.0)
                    b = st.slider("b (minor axis)", 1.0, 8.0, 3.0)

                    t = np.linspace(0, 2*np.pi, 500)
                    x = h + a * np.cos(t)
                    y = k + b * np.sin(t)

                    fig = go.Figure()

                    # Ellipse
                    fig.add_trace(go.Scatter(x=x, y=y, mode='lines'))

                    # Center
                    fig.add_trace(go.Scatter(x=[h], y=[k], mode='markers+text',
                                            text=["Center"],
                                            textposition="top center"))

                    # Foci
                    c = np.sqrt(abs(a**2 - b**2))

                    fig.add_trace(go.Scatter(
                        x=[h + c, h - c],
                        y=[k, k],
                        mode='markers+text',
                        text=["F1", "F2"],
                        textposition="top center"
                    ))

                    fig.update_layout(
                        title="Ellipse",
                        xaxis=dict(scaleanchor="y")
                    )

                    st.plotly_chart(fig, use_container_width=True)

                    st.latex(rf"\frac{{(x - {h})^2}}{{{a**2}}} + \frac{{(y - {k})^2}}{{{b**2}}} = 1")

# =========================
# 🏆 PROGRESS TAB
# =========================
with tab_progress:

    st.subheader("🏆 Your Learning Dashboard")

    # =========================
    # 📊 OVERALL PERFORMANCE
    # =========================
    st.markdown("### 📊 Overall Performance")

    if "streak" not in st.session_state:
        st.session_state.streak = 0

    streak = st.session_state.streak

    # ✅ GET REAL DATA
    topic_stats = st.session_state.get("topic_stats", {})

    total_attempts = sum(d["attempts"] for d in topic_stats.values())
    total_correct = sum(d["correct"] for d in topic_stats.values())

    # ✅ CALCULATE REAL ACCURACY
    if total_attempts > 0:
        avg_score = int((total_correct / total_attempts) * 100)
    else:
        avg_score = 0

    attempts = total_attempts

    # Initialize session state if not exists
    if "scores" not in st.session_state:
        st.session_state.scores = {
            "Functions": 80,
            "Trigonometry": 60,
            "Probability": 45,
            "Differentiation": 70
        }

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("📈 Accuracy", f"{avg_score}%")

    with col2:
        st.metric("🧠 Questions Attempted", attempts)

    with col3:
        st.metric("🔥 Study Streak", f"{streak} days")

    st.progress(avg_score / 100)

    # =========================
    # 🎉 REWARD SYSTEM (POINTS)
    # =========================
    if "score" not in st.session_state:
        st.session_state.score = 0

    score = st.session_state.score

    st.markdown("### 🎯 Points System")
    st.metric("Points", score)

    st.progress(min(score / 10, 1.0))

    if score >= 10 and not st.session_state.get("reward_given", False):
        st.success("🎉 You reached 10 points!")
        st.audio("https://www.soundjay.com/buttons/sounds/button-3.mp3")
        st.balloons()
        st.session_state.reward_given = True

    # =========================
    # 🏅 LEVEL SYSTEM
    # =========================
    if score >= 10 and not st.session_state.get("reward10", False):
        st.session_state.reward10 = True

    if score >= 20 and not st.session_state.get("reward20", False):
        st.balloons()
        st.success("🔥 Level Up!")
        st.session_state.reward20 = True

    # =========================
    # 📊 PERFORMANCE FEEDBACK
    # =========================
    if avg_score < 50:
        st.error("⚠️ You need more practice. Focus on weak topics below.")
    elif avg_score < 80:
        st.warning("⚡ You're improving. Keep practicing consistently.")
    else:
        st.success("🔥 Strong performance! Try harder questions.")

    topic_stats = st.session_state.get("topic_stats", {})

    scores = {}

    for topic, data in topic_stats.items():
        if data["attempts"] > 0:
            scores[topic] = int((data["correct"] / data["attempts"]) * 100)
        else:
            scores[topic] = 0
    # =========================
    # 📚 TOPIC PERFORMANCE
    # =========================
    st.markdown("### 📚 Topic Performance")

    topic_stats = st.session_state.topic_stats
    scores = {}

    for topic, data in topic_stats.items():
        if data["attempts"] > 0:
            scores[topic] = int((data["correct"] / data["attempts"]) * 100)
        else:
            scores[topic] = 0

    if scores:
        for topic, score in scores.items():
            st.write(f"**{topic}**")
            st.progress(score / 100)
    else:
        st.info("No data yet. Start practicing to see your progress.")

    # =========================
    # 🔍 WEAKNESS DETECTION
    # =========================
    st.markdown("### 🔍 Areas to Improve")

    weak_topics = [t for t, s in scores.items() if s < 60]

    if weak_topics:
        for t in weak_topics:
            st.error(f"🔴 {t}")
    else:
        st.success("✅ No major weak areas!")

    # =========================
    # 🤖 AI RECOMMENDATION
    # =========================
    st.markdown("### 🤖 AI Recommendations")

    if not weak_topics:
        st.info("You're doing well across all topics. Try harder questions.")
    else:
        for t in weak_topics:
            if t == "Probability":
                st.info("📊 Practice Probability in Visualize tab")
            elif t == "Trigonometry":
                st.info("📐 Revise trig graphs")
            elif t == "Functions":
                st.info("📈 Focus on transformations")
            elif t == "Differentiation":
                st.info("📉 Practice derivatives")

    # =========================
    # 🎯 NEXT STEP
    # =========================
    st.markdown("### 🎯 Suggested Next Step")

    if weak_topics:
        st.warning(f"Focus on **{weak_topics[0]}** next.")
    else:
        st.success("Try mixed practice questions.")
