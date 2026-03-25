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

    # -----------------------
    # ✅ Persist difficulty
    # -----------------------
    if "difficulty" not in st.session_state:
        st.session_state.difficulty = "Intermediate"

    difficulty = st.selectbox(
        "Select Difficulty Level:",
        ["Beginner", "Intermediate", "Advanced"],
        index=["Beginner","Intermediate","Advanced"].index(st.session_state.difficulty)
    )

    st.session_state.difficulty = difficulty

    # -----------------------
    # 📘 Topic Input
    # -----------------------
    pspm_topic = st.text_input(
        "Enter topic (e.g. Differentiation, Integration, Probability):",
        key="pspm_topic"
    )

    # -----------------------
    # 🧩 Question Structure Controls
    # -----------------------
    st.markdown("### 🧩 Question Structure")

    multi_part = st.checkbox("Enable multi-part question", value=True)

    num_parts = st.slider(
        "Number of main parts (a, b, c...):",
        min_value=1,
        max_value=5,
        value=3
    )

    include_roman = st.checkbox("Include sub-parts (i, ii, iii)", value=False)

    num_subparts = 0
    if include_roman:
        num_subparts = st.slider(
            "Number of sub-parts per section:",
            min_value=2,
            max_value=4,
            value=2
        )

    marks = st.checkbox("Include marks allocation", value=True)

    # -----------------------
    # 🚀 Generate Button
    # -----------------------
    if st.button("Generate PSPM Question"):

        if pspm_topic:

            # -----------------------
            # 🧠 Structure Instruction Builder
            # -----------------------
            structure_instruction = ""

            if multi_part:
                structure_instruction += f"- The question MUST have {num_parts} main parts labelled (a), (b), (c)...\n"

                if include_roman:
                    structure_instruction += f"- EACH main part MUST contain {num_subparts} sub-parts labelled (i), (ii), (iii)...\n"
            else:
                structure_instruction += "- The question should be a single structured question without parts.\n"

            if marks:
                structure_instruction += "- Include marks for each part like (3 marks)\n"

            # -----------------------
            # 🧾 Prompt
            # -----------------------
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
    - You MUST follow the structure exactly. No exceptions.

    Structure Rules:
    {structure_instruction}

    Formatting:
    - Use proper exam formatting
    - Make it look like a real PSPM paper
    """

            generated_q = ask_ai(prompt, max_tokens=400)

            # -----------------------
            # 💾 Save State
            # -----------------------
            st.session_state.current_problem = generated_q
            st.session_state.answer = ""
            st.session_state.hint_level = 0

            # -----------------------
            # 📤 Output
            # -----------------------
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
            Create SHORT and CONCISE revision notes for: {topic}

            Rules:
            - Focus on KEY POINTS only (no long explanations)
            - Use bullet points
            - Keep it exam-focused (Matriculation / PSPM style)
            - Include:
            • Definitions (very short)
            • Important formulas using $$...$$
            • Key concepts
            • Important conditions (parallel, perpendicular, etc.)
            - DO NOT give long paragraphs
            - DO NOT copy textbook style
            - Keep everything simple and easy to memorize

            If topic is VECTORS, prioritize:
            - formulas
            - relationships
            - conditions (e.g. perpendicular, parallel)
            - steps (ONLY if important)

            Make it look like a QUICK REVISION SHEET.
            """
            )

            # ✅ STORE RAW OUTPUT
            st.session_state.notes_output = response.output_text

        else:
            st.warning("Please enter a topic first.")

        import re

        if st.session_state.notes_output:

            with st.expander("📖 View Generated Notes", expanded=True):

                raw = st.session_state.notes_output

                import re
                parts = re.split(r"(\|.*\|)", raw)

                cleaned_parts = []

                for part in parts:
                    if "|" in part:
                        part = re.sub(r"\\frac{(.*?)}{(.*?)}", r"\1/\2", part)
                        part = re.sub(r"\\sqrt{(.*?)}", r"sqrt(\1)", part)
                        part = part.replace("\\leq", "<=").replace("\\geq", ">=")
                        part = part.replace("^{2}", "^2")
                    else:
                        part = re.sub(r"##", "\n##", part)
                        part = re.sub(r"###", "\n###", part)

                    cleaned_parts.append(part)

                content = "".join(cleaned_parts)

                st.markdown(content)

            # Split tables vs normal text
            parts = re.split(r"(\|.*\|)", raw)

            cleaned_parts = []

            for part in parts:
                if "|" in part:
                    # Clean tables only
                    part = re.sub(r"\\frac{(.*?)}{(.*?)}", r"\1/\2", part)
                    part = re.sub(r"\\sqrt{(.*?)}", r"sqrt(\1)", part)
                    part = part.replace("\\leq", "<=").replace("\\geq", ">=")
                    part = part.replace("^{2}", "^2")
                else:
                    # Improve headings spacing
                    part = re.sub(r"##", "\n##", part)
                    part = re.sub(r"###", "\n###", part)

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

        if chapter == "Chapter 2: Equations, Inequalities and Absolute Values":

            st.markdown("## 📘 Chapter 2: Equations, Inequalities and Absolute Values")

            # =========================
            # 2.1 EQUATIONS
            # =========================
            with st.expander("🧮 2.1 Equations", expanded=True):

                st.markdown("### 📌 Learning Outcomes")
                st.info("""
                LO1: Rules of indices  
                LO2: Surds and conjugates  
                LO3: Operations on surds  
                LO4: Laws of logarithms  
                LO5: Change base of logarithm  
                LO6: Solve equations  
                """)

                # -------------------------
                # INDICES
                # -------------------------
                with st.expander("🔢 Indices (Laws)"):

                    st.latex(r"a^m \cdot a^n = a^{m+n}")
                    st.latex(r"\frac{a^m}{a^n} = a^{m-n}")
                    st.latex(r"(a^m)^n = a^{mn}")
                    st.latex(r"a^0 = 1")
                    st.latex(r"a^{-m} = \frac{1}{a^m}")

                    st.markdown("### ✏️ Example")
                    st.markdown("""
            2³ × 2² = 2⁵ = **32**
                    """)

                # -------------------------
                # SURDS
                # -------------------------
                with st.expander("🧩 Surds"):

                    st.markdown("""
            - Surd: irrational number (e.g. √2, √3)
            - Conjugate: a + b√c → a − b√c
                    """)

                    st.latex(r"\sqrt{ab} = \sqrt{a}\sqrt{b}")

                    st.markdown("### ✏️ Example")
                    st.markdown("""
            √45 = √(9×5) = 3√5
                    """)

                    st.markdown("### 🔄 Rationalising")

                    st.markdown("""
            Multiply by conjugate
                    """)

                    st.markdown("### ✏️ Example")

                    st.markdown("""
            1/(2 + √3)

            Multiply by (2 − √3):

            = (2 − √3)/(4 − 3)  
            = **2 − √3**
                    """)

                # -------------------------
                # LOGARITHMS
                # -------------------------
                with st.expander("📊 Logarithms"):

                    st.latex(r"\log_a (xy) = \log_a x + \log_a y")
                    st.latex(r"\log_a \left(\frac{x}{y}\right) = \log_a x - \log_a y")
                    st.latex(r"\log_a x^n = n \log_a x")

                    st.latex(r"\log_a x = \frac{\log_b x}{\log_b a}")

                    st.markdown("### ✏️ Example")

                    st.markdown("""
            log₂ 8 = **3**
                    """)

                # -------------------------
                # SOLVING EQUATIONS
                # -------------------------
                with st.expander("🧠 Solving Equations"):

                    st.markdown("### 🔢 Index Equation")

                    st.markdown("""
            2ˣ = 8 → 2ˣ = 2³  

            x = **3**
                    """)

                    st.markdown("### 🧩 Surd Equation")

                    st.markdown("""
            √(x+1) = 3  

            x+1 = 9  
            x = **8**
                    """)

                    st.markdown("### 📊 Log Equation")

                    st.markdown("""
            log x = 2  

            x = **100**
                    """)


            # =========================
            # 2.2 INEQUALITIES
            # =========================
            with st.expander("📏 2.2 Inequalities"):

                st.markdown("### 📌 Key Rule")
                st.warning("⚠️ Reverse sign when multiply/divide by negative")

                # -------------------------
                # LINEAR
                # -------------------------
                with st.expander("📘 Linear Inequalities"):

                    st.markdown("### ✏️ Example")

                    st.markdown("""
            2x − 4 > 8  

            2x > 12  
            x > **6**
                    """)

                # -------------------------
                # QUADRATIC
                # -------------------------
                with st.expander("📊 Quadratic Inequalities"):

                    st.markdown("### 🧠 Steps")
                    st.markdown("""
            1. Factorise  
            2. Find critical values  
            3. Use sign table  
                    """)

                    st.markdown("### ✏️ Example")

                    st.markdown("""
            x² − 5x − 6 ≥ 0  

            (x − 6)(x + 1) ≥ 0  

            x ≤ −1 or x ≥ 6
                    """)

                # -------------------------
                # RATIONAL
                # -------------------------
                with st.expander("📉 Rational Inequalities"):

                    st.markdown("### ⚠️ Important")
                    st.warning("Do NOT cross multiply")

                    st.markdown("### ✏️ Example")

                    st.markdown("""
            (x − 2)/(x + 1) > 0  

            Critical: x = 2, -1  

            Answer: x < −1 or x > 2
                    """)


            # =========================
            # 2.3 ABSOLUTE VALUES
            # =========================
            with st.expander("📦 2.3 Absolute Values"):

                st.markdown("### 📌 Definition")
                st.latex(r"|x| = \begin{cases} x, & x \ge 0 \\ -x, & x < 0 \end{cases}")

                st.markdown("### 📌 Key Idea")
                st.markdown("""
            Distance from 0 → always positive
                """)

                # -------------------------
                # EQUATIONS
                # -------------------------
                with st.expander("🧮 Absolute Equations"):

                    st.markdown("### 📌 Rule")
                    st.markdown("""
            |x| = a → x = ±a
                    """)

                    st.markdown("### ✏️ Example")

                    st.markdown("""
            |x − 2| = 3  

            x − 2 = 3 → x = 5  
            x − 2 = −3 → x = -1  

            Answer: **x = 5 or x = -1**
                    """)

                # -------------------------
                # INEQUALITIES
                # -------------------------
                with st.expander("📏 Absolute Inequalities"):

                    st.markdown("### 📌 Rules")

                    st.markdown("""
            |x| < a → -a < x < a  
            |x| > a → x < -a or x > a  
                    """)

                    st.markdown("### ✏️ Example")

                    st.markdown("""
            |x − 1| < 2  

            -2 < x − 1 < 2  

            -1 < x < 3
                    """)

        if chapter == "Chapter 3: Sequences and Series":

            st.markdown("## 📘 Chapter 3: Sequences and Series")

            # =========================
            # 3.1 SEQUENCES & SERIES
            # =========================
            with st.expander("🔢 3.1 Sequences and Series", expanded=True):

                st.markdown("### 📌 Learning Outcomes")
                st.info("""
                LO1: Write nth term  
                LO2: Arithmetic sequences & sums  
                LO3: Geometric sequences & sums  
                LO4: Sum to infinity  
                """)

                # -------------------------
                # BASIC IDEA
                # -------------------------
                st.markdown("### 🧠 Basic Concepts")

                st.markdown("""
            - **Sequence**: ordered list of numbers  
            - **Series**: sum of sequence  

            Example:  
            Sequence → 2, 4, 6, 8  
            Series → 2 + 4 + 6 + 8  
                """)

                st.latex(r"S_n = T_1 + T_2 + T_3 + \cdots + T_n")

                st.markdown("""
            - Finite series → limited terms  
            - Infinite series → continues forever  
                """)

                # -------------------------
                # EXAMPLE
                # -------------------------
                st.markdown("### ✏️ Example")

                st.markdown("""
            Find first 5 terms of: Tₙ = 2n − 1  

            T₁ = 1  
            T₂ = 3  
            T₃ = 5  
            T₄ = 7  
            T₅ = 9  

            Answer: **1, 3, 5, 7, 9**
                """)


            # =========================
            # ARITHMETIC PROGRESSION
            # =========================
            with st.expander("📈 Arithmetic Progression (AP)"):

                st.markdown("### 📌 Definition")
                st.markdown("""
            Constant difference between terms  
                """)

                st.markdown("### 📐 Formula")

                st.latex(r"T_n = a + (n-1)d")
                st.latex(r"S_n = \frac{n}{2}[2a + (n-1)d]")

                st.markdown("""
            - a = first term  
            - d = common difference  
                """)

                # -------------------------
                # EXAMPLE
                # -------------------------
                st.markdown("### ✏️ Example 1")

                st.markdown("""
            Sequence: 2, 5, 8, 11,...

            a = 2, d = 3  

            Find T₁₀  

            T₁₀ = 2 + (10−1)(3)  
            = 2 + 27  
            = **29**
                """)

                st.markdown("### ✏️ Example 2 (Sum)")

                st.markdown("""
            Find sum of first 20 terms  

            S₂₀ = 20/2 [2(2) + 19(3)]  
            = 10 [4 + 57]  
            = 10(61)  
            = **610**
                """)


            # =========================
            # GEOMETRIC PROGRESSION
            # =========================
            with st.expander("📊 Geometric Progression (GP)"):

                st.markdown("### 📌 Definition")
                st.markdown("""
            Constant ratio between terms  
                """)

                st.latex(r"T_n = ar^{n-1}")
                st.latex(r"S_n = \frac{a(1-r^n)}{1-r}")
                st.latex(r"S_\infty = \frac{a}{1-r}, \quad |r| < 1")

                st.markdown("""
            - a = first term  
            - r = common ratio  
                """)

                # -------------------------
                # EXAMPLE
                # -------------------------
                st.markdown("### ✏️ Example 1")

                st.markdown("""
            Sequence: 3, 6, 12, 24,...

            a = 3, r = 2  

            Find T₆  

            T₆ = 3(2⁵) = 3(32) = **96**
                """)

                st.markdown("### ✏️ Example 2 (Sum to infinity)")

                st.markdown("""
            a = 4, r = 1/2  

            S∞ = 4 / (1 − 1/2)  
            = 4 / (1/2)  
            = **8**
                """)


            # =========================
            # APPLICATIONS
            # =========================
            with st.expander("🚗 Applications"):

                st.markdown("### 💰 Depreciation (GP)")

                st.markdown("""
            Car price = 60000  
            Depreciation = 10%  

            r = 0.9  

            After 2 years:  

            T₃ = 60000(0.9²)  
            = 60000(0.81)  
            = **48600**
                """)

                st.markdown("### 🏟️ Seats Problem (AP)")

                st.markdown("""
            First row = 30 seats  
            Increase = 2  

            Find total seats for 50 rows  

            S₅₀ = 50/2 [2(30) + 49(2)]  
            = 25 [60 + 98]  
            = 25(158)  
            = **3950 seats**
                """)


            # =========================
            # BINOMIAL EXPANSION
            # =========================
            with st.expander("🧩 3.2 Binomial Expansion"):

                st.markdown("### 📌 Factorial")
                st.latex(r"n! = n(n-1)(n-2)...1")

                st.markdown("""
            Example:  
            5! = 120  
            0! = 1  
                """)

                st.markdown("### 📌 Binomial Coefficient")
                st.latex(r"\binom{n}{r} = \frac{n!}{r!(n-r)!}")

                # -------------------------
                # EXPANSION
                # -------------------------
                st.markdown("### 📐 Expansion Formula")

                st.latex(r"(a+b)^n = \sum_{r=0}^{n} \binom{n}{r} a^{n-r} b^r")

                st.markdown("### ✏️ Example")

                st.markdown("""
            Expand (x + 1)³  

            = x³ + 3x² + 3x + 1
                """)

                # -------------------------
                # GENERAL TERM
                # -------------------------
                st.markdown("### 📌 General Term")

                st.latex(r"T_{r+1} = \binom{n}{r} a^{n-r} b^r")

                st.markdown("### ✏️ Example")

                st.markdown("""
            Find coefficient of x² in (x + 1)⁵  

            General term:  

            Tᵣ₊₁ = 5Cr x^(5−r)

            Set power = 2  

            5 − r = 2 → r = 3  

            Coefficient = 5C3 = **10**
                """)

                # -------------------------
                # NEGATIVE / FRACTION
                # -------------------------
                st.markdown("### 📊 For Negative / Fraction Power")

                st.latex(r"(1+x)^n = 1 + nx + \frac{n(n-1)}{2!}x^2 + ...")

                st.warning("⚠️ Valid only when |x| < 1")

                st.markdown("### ✏️ Example")

                st.markdown("""
            Expand (1 + x)^(-1)  

            = 1 − x + x² − x³ + ...
                """)

        if chapter == "Chapter 4: Matrices":

            st.markdown("## 📘 Chapter 4: Matrices & System of Linear Equations")

            # =========================
            # 4.1 MATRICES
            # =========================
            with st.expander("📊 4.1 Matrices", expanded=True):

                st.markdown("### 📌 Learning Outcomes")
                st.info("""
                LO1: Identify types of matrices  
                LO2: Perform matrix operations  
                LO3: Find transpose  
                """)

                st.markdown("### 🧠 Types of Matrices")

                st.markdown("""
            - **Row Matrix**: 1 × n  
            - **Column Matrix**: m × 1  
            - **Square Matrix**: n × n  
            - **Zero Matrix (O)**: All elements = 0  
            - **Identity Matrix (I)**: Diagonal = 1  
            - **Diagonal Matrix**: Non-diagonal = 0  
            - **Upper Triangular**: Below diagonal = 0  
            - **Lower Triangular**: Above diagonal = 0  
                """)

                st.markdown("### ➕ Matrix Operations")

                st.markdown("""
            **Addition/Subtraction**
            - Same order required  
            - Add corresponding elements  

            **Scalar Multiplication**
            - Multiply each element by constant  

            **Matrix Multiplication**
            - Columns of A = Rows of B  
            - Not commutative (AB ≠ BA)
                """)

                st.markdown("### 🧪 Example")

                st.latex(r"A = \begin{pmatrix}1 & 2 \\ 3 & 4\end{pmatrix},\ B = \begin{pmatrix}5 & 6 \\ 7 & 8\end{pmatrix}")

                st.markdown("""
            **A + B =**
            """)
                st.latex(r"\begin{pmatrix}6 & 8 \\ 10 & 12\end{pmatrix}")

            # =========================
            # TRANSPOSE
            # =========================
            with st.expander("🔄 Transpose of Matrix"):

                st.markdown("### 📌 Definition")

                st.latex(r"A^T = \text{interchange rows and columns}")

                st.markdown("### 🧪 Example")

                st.latex(r"A = \begin{pmatrix}1 & 2 \\ 3 & 4\end{pmatrix}")
                st.latex(r"A^T = \begin{pmatrix}1 & 3 \\ 2 & 4\end{pmatrix}")

            # =========================
            # 4.2 DETERMINANT
            # =========================
            with st.expander("📐 4.2 Determinant"):

                st.markdown("### 📌 Key Concepts")

                st.markdown("""
            - Determinant only for **square matrices**
            - Notation: |A| or det(A)
                """)

                st.markdown("### 🔢 2×2 Determinant")

                st.latex(r"\begin{vmatrix} a & b \\ c & d \end{vmatrix} = ad - bc")

                st.markdown("### 🧪 Example")

                st.latex(r"\begin{vmatrix} 2 & 5 \\ 3 & 8 \end{vmatrix} = (2)(8) - (5)(3) = 16 - 15 = 1")

                st.markdown("### 🔺 3×3 Concept")

                st.markdown("""
            Use **cofactors + minors**  
            Choose row/column with most zeros (faster)
                """)

            # =========================
            # MINORS & COFACTORS
            # =========================
            with st.expander("🧩 Minors & Cofactors"):

                st.markdown("### 📌 Definitions")

                st.markdown("""
            - **Minor (Mᵢⱼ)**: determinant after removing row i, column j  
            - **Cofactor (Cᵢⱼ)**:  
            """)

                st.latex(r"C_{ij} = (-1)^{i+j} M_{ij}")

                st.markdown("### 🧪 Example")

                st.markdown("""
            For element at (1,1), remove row 1 and column 1, then find determinant.
                """)

            # =========================
            # 4.3 INVERSE MATRIX
            # =========================
            with st.expander("🔁 4.3 Inverse Matrix"):

                st.markdown("### 📌 Formula")

                st.latex(r"A^{-1} = \frac{1}{|A|} \cdot adj(A)")

                st.warning("⚠️ Only exists if |A| ≠ 0")

                st.markdown("### 🔢 2×2 Inverse")

                st.latex(r"A = \begin{pmatrix}a & b \\ c & d\end{pmatrix}")
                st.latex(r"A^{-1} = \frac{1}{ad - bc} \begin{pmatrix}d & -b \\ -c & a\end{pmatrix}")

                st.markdown("### 🧪 Example")

                st.latex(r"A = \begin{pmatrix}2 & 1 \\ 3 & 4\end{pmatrix}")

                st.markdown("""
            Determinant = (2×4 - 1×3) = 5
                """)

                st.latex(r"A^{-1} = \frac{1}{5} \begin{pmatrix}4 & -1 \\ -3 & 2\end{pmatrix}")

            # =========================
            # ERO METHOD
            # =========================
            with st.expander("⚙️ Inverse using Row Operations"):

                st.markdown("### 📌 Steps")

                st.markdown("""
            1. Write augmented matrix [A | I]  
            2. Convert A → I using row operations  
            3. Final form becomes [I | A⁻¹]
                """)

            # =========================
            # 4.4 SYSTEM OF EQUATIONS
            # =========================
            with st.expander("📊 4.4 System of Linear Equations"):

                st.markdown("### 📌 Matrix Form")

                st.latex(r"AX = B")

                st.markdown("""
            Where:
            - A = coefficient matrix  
            - X = variables  
            - B = constants  
                """)

                st.markdown("### 🧠 Types of Solutions")

                st.markdown("""
            - **Unique** → |A| ≠ 0  
            - **Infinite** → |A| = 0  
            - **No solution** → inconsistent  
                """)

            # =========================
            # METHODS
            # =========================
            with st.expander("🛠️ Methods to Solve"):

                st.markdown("""
            1. Inverse Matrix Method  
            2. Gauss Elimination  
            3. Gauss-Jordan  
            4. Cramer’s Rule  
                """)

            # =========================
            # CRAMER'S RULE
            # =========================
            with st.expander("📌 Cramer's Rule"):

                st.markdown("### 📌 Formula")

                st.latex(r"x = \frac{A_x}{A}, \quad y = \frac{A_y}{A}, \quad z = \frac{A_z}{A}")

                st.markdown("### 🧪 Example")

                st.markdown("""
            Solve system using determinants of modified matrices.
                """)

        if chapter == "Chapter 5: Functions":

            st.markdown("## 📘 Chapter 5: Functions")

            # =========================
            # 5.1 FUNCTIONS
            # =========================
            with st.expander("📌 5.1 Functions", expanded=True):

                st.markdown("### 📌 Learning Outcomes")
                st.info("""
                LO1: Define function  
                LO2: Identify function (vertical line test)  
                LO3: Identify one-to-one function  
                LO4: Sketch graphs  
                LO5: State domain and range  
                """)

                # -------------------------
                # Definition
                # -------------------------
                st.markdown("### 🧠 Definition")

                st.markdown("""
            - A **function** is a relation where **each input has exactly ONE output**  
            - Notation: **y = f(x)**  
                """)

                # -------------------------
                # Vertical Line Test
                # -------------------------
                st.markdown("### 📏 Vertical Line Test")

                st.markdown("""
            - Used to check if a graph is a function  
            - If a vertical line cuts graph **once → function**  
            - If more than once → **NOT a function**
                """)

                # -------------------------
                # One-to-One
                # -------------------------
                st.markdown("### 🔁 One-to-One Function")

                st.markdown("""
            - Each output comes from only ONE input  
                """)

                st.markdown("**Horizontal Line Test:**")
                st.markdown("""
            - Line intersects graph once → one-to-one  
                """)

                st.markdown("**Algebra Test:**")
                st.latex(r"f(x_1) = f(x_2) \Rightarrow x_1 = x_2")

                # -------------------------
                # Domain & Range
                # -------------------------
                st.markdown("### 📊 Domain & Range")

                st.markdown("""
            - **Domain (D)**: possible x-values  
            - **Range (R)**: possible y-values  
            - Can be written in **interval notation**
                """)

            # =========================
            # GRAPH TYPES
            # =========================
            with st.expander("📈 5.1 Graph Sketching"):

                # CONSTANT
                st.markdown("### 📌 Constant Function")
                st.latex(r"f(x) = k")

                st.markdown("""
            - Horizontal line  
            - Domain: all real numbers  
            - Range: constant value  
                """)

                # LINEAR
                st.markdown("### 📌 Linear Function")
                st.latex(r"f(x) = mx + c")

                st.markdown("""
            - Straight line  
            - Gradient = m  
                """)

                # QUADRATIC
                st.markdown("### 📌 Quadratic Function")
                st.latex(r"f(x) = ax^2 + bx + c")

                st.markdown("""
            - Parabola  
            - Turning point exists  
                """)

                st.latex(r"\text{Vertex} = \left(-\frac{b}{2a}, f\left(-\frac{b}{2a}\right)\right)")

                # CUBIC
                st.markdown("### 📌 Cubic Function")
                st.latex(r"f(x) = ax^3 + bx^2 + cx + d")

                st.markdown("""
            - S-shaped graph  
            - Has inflection point  
                """)

                # RATIONAL
                st.markdown("### 📌 Rational Function")
                st.latex(r"f(x) = \frac{a}{x}")

                st.markdown("""
            - Has asymptotes  
            - Undefined at x = 0  
                """)

                # ABSOLUTE
                st.markdown("### 📌 Absolute Function")
                st.latex(r"f(x) = |x|")

                st.markdown("""
            - V-shaped graph  
            - Always positive  
                """)

                # ROOT
                st.markdown("### 📌 Square Root Function")
                st.latex(r"f(x) = \sqrt{x}")

                st.markdown("""
            - Starts at (0,0)  
            - Domain: x ≥ 0  
                """)

                # EXPONENTIAL
                st.markdown("### 📌 Exponential Function")
                st.latex(r"f(x) = e^x")

                st.markdown("""
            - Always increasing  
            - Horizontal asymptote  
                """)

                # LOG
                st.markdown("### 📌 Logarithmic Function")
                st.latex(r"f(x) = \ln x")

                st.markdown("""
            - Domain: x > 0  
            - Vertical asymptote  
                """)

            # =========================
            # 5.2 COMPOSITE FUNCTION
            # =========================
            with st.expander("🔗 5.2 Composite Functions"):

                st.markdown("### 📌 Definition")

                st.latex(r"(f \circ g)(x) = f(g(x))")

                st.markdown("""
            - Apply **g first**, then **f**
                """)

                st.markdown("### 🧠 Example")

                st.markdown("""
            Let:
            - f(x) = 2x − 1  
            - g(x) = x³  

            Then:
            - f(g(x)) = 2x³ − 1  
                """)

            # =========================
            # 5.3 INVERSE FUNCTION
            # =========================
            with st.expander("🔄 5.3 Inverse Functions"):

                st.markdown("### 📌 Definition")

                st.markdown("""
            - Reverse input and output  
            - Only exists if function is **one-to-one**
                """)

                st.markdown("### 📐 Key Property")

                st.latex(r"f(f^{-1}(x)) = x")

                st.markdown("### 🧠 Steps")

                st.markdown("""
            1. Let y = f(x)  
            2. Swap x and y  
            3. Solve for y  
                """)

                st.markdown("### 📊 Graph")

                st.markdown("""
            - Symmetric about line y = x  
                """)

            # =========================
            # 5.4 EXP & LOG
            # =========================
            with st.expander("📊 5.4 Exponential & Log Functions"):

                st.markdown("### 🔁 Relationship")

                st.latex(r"a^x \leftrightarrow \log_a x")

                st.markdown("""
            - They are **inverse functions**
                """)

                st.markdown("### 📊 Domain & Range")

                st.markdown("""
            - Exponential:
            - Domain: ℝ  
            - Range: y > 0  

            - Logarithm:
            - Domain: x > 0  
            - Range: ℝ  
                """)

            # =========================
            # 5.5 TRIG FUNCTIONS
            # =========================
            with st.expander("📐 5.5 Trigonometric Functions"):

                st.markdown("### 📌 Basic Graphs")

                st.markdown("""
            - **sin x**
            - **cos x**
            - **tan x**
                """)

                st.markdown("### 📊 Domain & Range")

                st.markdown("""
            - sin x:
            - Domain: ℝ  
            - Range: [-1,1]

            - cos x:
            - Domain: ℝ  
            - Range: [-1,1]

            - tan x:
            - Domain: ℝ (except asymptotes)  
            - Range: ℝ  
                """)

                st.markdown("### 📈 General Form")

                st.latex(r"y = a \sin(bx + c)")

                st.markdown("""
            - a → amplitude  
            - b → period  
            - c → phase shift  
                """)

        if chapter == "Chapter 6: Polynomials":

            st.markdown("## 📘 Chapter 6: Polynomials")

            # =========================
            # 6.1 POLYNOMIALS
            # =========================
            with st.expander("📌 6.1 Polynomials", expanded=True):

                st.markdown("### 📌 Learning Outcomes")
                st.info("""
                LO1: Perform operations on polynomials  
                LO2: Perform division of polynomials  
                """)

                # -------------------------
                # Definition
                # -------------------------
                st.markdown("### 🧠 Definition")

                st.latex(r"P(x) = a_n x^n + a_{n-1} x^{n-1} + ... + a_0")

                st.markdown("""
            - **n** = degree  
            - **aₙ ≠ 0**  
            - Coefficients are constants  
                """)

                # -------------------------
                # Degree
                # -------------------------
                st.markdown("### 📊 Degree")

                st.markdown("""
            - Highest power of x  

            Examples:
            - 2x + 5 → degree 1  
            - x² + 3x + 1 → degree 2  
            - x³ − x² + 4 → degree 3  
                """)

                # -------------------------
                # Operations
                # -------------------------
                st.markdown("### ➕ Operations")

                st.markdown("""
            - Add / subtract → combine like terms  
            - Multiply → expand brackets  
                """)

                st.markdown("### 🧠 Example")

                st.markdown("""
            (2x + 3) + (x + 5) = **3x + 8**  

            (2x)(x + 3) = **2x² + 6x**  
                """)

            # =========================
            # DIVISION
            # =========================
            with st.expander("📏 Polynomial Division"):

                st.markdown("### 📌 Long Division")

                st.markdown("""
            When dividing:

            P(x) = D(x)Q(x) + R(x)
                """)

                st.latex(r"\frac{P(x)}{D(x)} = Q(x) + \frac{R(x)}{D(x)}")

                st.markdown("""
            - Q(x) = quotient  
            - R(x) = remainder  
                """)

                st.markdown("### 🧠 Example")

                st.markdown("""
            Divide: x³ + 2x² + 3x + 4 by (x + 1)

            → Result:  
            Quotient = x² + x + 2  
            Remainder = 2  
                """)

            # =========================
            # 6.2 REMAINDER THEOREM
            # =========================
            with st.expander("🧩 6.2 Remainder Theorem"):

                st.markdown("### 📌 Key Idea")

                st.markdown("""
            If P(x) is divided by (x − a), then:

            Remainder = P(a)
                """)

                st.markdown("### 🧠 Example")

                st.markdown("""
            Find remainder of P(x) = x³ + 2x² − x + 1 when divided by (x − 2)

            P(2) = 8 + 8 − 2 + 1 = **15**
                """)

            # =========================
            # FACTOR THEOREM
            # =========================
            with st.expander("🔄 Factor Theorem"):

                st.markdown("### 📌 Key Idea")

                st.markdown("""
            - If P(a) = 0 → (x − a) is a factor  
            - If (x − a) is a factor → P(a) = 0  
                """)

                st.markdown("### 🧠 Example")

                st.markdown("""
            Check if (x − 1) is a factor of P(x) = x³ − x² − x + 1  

            P(1) = 1 − 1 − 1 + 1 = 0  

            → YES, it is a factor  
                """)

            # =========================
            # ROOTS / ZEROES
            # =========================
            with st.expander("🎯 Roots / Zeroes of Polynomial"):

                st.markdown("### 📌 Definition")

                st.markdown("""
            - If P(a) = 0 → a is a **root (zero)**  
            - Solve P(x) = 0  
                """)

                st.markdown("### 🧠 Steps (VERY IMPORTANT)")

                st.markdown("""
            1. Trial values  
            2. Use factor theorem  
            3. Long division  
            4. Factorise completely  
            5. Solve P(x) = 0  
                """)

                st.markdown("### 🧠 Example")

                st.markdown("""
            Solve: x³ − 6x² + 11x − 6 = 0  

            Factorised: (x−1)(x−2)(x−3)  

            Roots: **1, 2, 3**
                """)

            # =========================
            # 6.3 PARTIAL FRACTIONS
            # =========================
            with st.expander("📊 6.3 Partial Fractions"):

                st.markdown("### 📌 Learning Outcomes")
                st.info("""
                LO1: Decompose proper fractions  
                LO2: Handle improper fractions  
                """)

                # -------------------------
                # Proper Fraction
                # -------------------------
                st.markdown("### 📏 Proper Fraction")

                st.markdown("""
            - Degree (numerator) < Degree (denominator)
                """)

                # CASE 1
                st.markdown("### 📌 Case 1: Distinct Linear Factors")

                st.latex(r"\frac{px + q}{(x-a)(x-b)} = \frac{A}{x-a} + \frac{B}{x-b}")

                # CASE 2
                st.markdown("### 📌 Case 2: Repeated Factors")

                st.latex(r"\frac{px + q}{(x-a)^2} = \frac{A}{x-a} + \frac{B}{(x-a)^2}")

                # CASE 3
                st.markdown("### 📌 Case 3: Quadratic Factor")

                st.latex(r"\frac{px + q}{x^2 + bx + c} = \frac{Ax + B}{x^2 + bx + c}")

                # -------------------------
                # Example
                # -------------------------
                st.markdown("### 🧠 Example")

                st.markdown("""
            Express:

            (2x + 3)/(x−1)(x+2)

            → A/(x−1) + B/(x+2)  

            Solve → A = 1, B = 1  

            Final:
            = 1/(x−1) + 1/(x+2)
                """)

            # =========================
            # IMPROPER FRACTION
            # =========================
            with st.expander("⚠️ Improper Fractions"):

                st.markdown("### 📌 Key Idea")

                st.markdown("""
            - Degree numerator ≥ denominator  
            - MUST use long division first  
                """)

                st.markdown("### 🧠 Steps")

                st.markdown("""
            1. Long division  
            2. Rewrite expression  
            3. Apply partial fractions  
                """)

        if chapter == "Chapter 7: Trigonometry":

            st.markdown("## 📘 Chapter 7: Trigonometry")

            # =========================
            # 7.1 BASIC IDENTITIES
            # =========================
            with st.expander("📐 7.1 Basic Trigonometric Identities", expanded=True):

                st.markdown("### 📌 Learning Outcomes")
                st.info("""
                LO1: Understand basic trigonometric ratios  
                LO2: Use fundamental identities  
                """)

                st.markdown("### 🔺 Basic Ratios")

                st.latex(r"\sin \theta = \frac{\text{opposite}}{\text{hypotenuse}}")
                st.latex(r"\cos \theta = \frac{\text{adjacent}}{\text{hypotenuse}}")
                st.latex(r"\tan \theta = \frac{\text{opposite}}{\text{adjacent}}")

                st.markdown("### 🔁 Important Identities")

                st.latex(r"\sin^2 \theta + \cos^2 \theta = 1")
                st.latex(r"\tan \theta = \frac{\sin \theta}{\cos \theta}")
                st.latex(r"1 + \tan^2 \theta = \sec^2 \theta")

                st.markdown("### 🧠 Example")

                st.markdown("""
            If sinθ = 3/5, find cosθ  

            Using identity:  
            cos²θ = 1 − sin²θ = 1 − (3/5)² = 16/25  

            cosθ = **4/5**
                """)

            # =========================
            # 7.2 UNIT CIRCLE
            # =========================
            with st.expander("⭕ 7.2 Unit Circle"):

                st.markdown("### 📌 Key Idea")

                st.markdown("""
            - Circle with radius 1  
            - Coordinates: (cosθ, sinθ)  
                """)

                st.markdown("### 🎯 Special Angles")

                st.markdown("""
            0° → (1, 0)  
            90° → (0, 1)  
            180° → (−1, 0)  
            270° → (0, −1)  
                """)

                st.markdown("### ⚠️ Signs (Quadrants)")

                st.info("""
            Q1: All positive  
            Q2: sin positive  
            Q3: tan positive  
            Q4: cos positive  
                """)

            # =========================
            # 7.3 GRAPHS
            # =========================
            with st.expander("📈 7.3 Graphs of Trigonometric Functions"):

                st.markdown("### 📊 Key Features")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("""
            **sin x / cos x**
            - Range: [-1, 1]  
            - Period: 2π  
                    """)

                with col2:
                    st.markdown("""
            **tan x**
            - Range: (-∞, ∞)  
            - Period: π  
            - Has asymptotes  
                    """)

                st.markdown("### 🧠 Example")

                st.markdown("""
            y = 2 sin x  

            - Amplitude = 2  
            - Period = 2π  
                """)

            # =========================
            # 7.4 TRIG IDENTITIES
            # =========================
            with st.expander("🧩 7.4 Trigonometric Identities"):

                st.markdown("### 📌 Key Idea")

                st.markdown("""
            Simplify expressions using identities  
                """)

                st.markdown("### 🔁 Common Identities")

                st.latex(r"1 - \sin^2 \theta = \cos^2 \theta")
                st.latex(r"1 - \cos^2 \theta = \sin^2 \theta")

                st.markdown("### 🧠 Example")

                st.markdown("""
            Simplify: (1 − cos²θ)/sinθ  

            = sin²θ / sinθ  
            = **sinθ**
                """)

            # =========================
            # 7.5 TRIG EQUATIONS
            # =========================
            with st.expander("🎯 7.5 Trigonometric Equations"):

                st.markdown("### 📌 Key Idea")

                st.markdown("""
            Solve equations involving trigonometric functions  
                """)

                st.markdown("### 🧠 Steps")

                st.markdown("""
            1. Simplify equation  
            2. Solve basic trig equation  
            3. Find all solutions in interval  
                """)

                st.markdown("### 🧠 Example")

                st.markdown("""
            Solve: sin x = 1/2, 0 ≤ x ≤ 2π  

            x = π/6, 5π/6  
                """)

            # =========================
            # 7.6 ANGLE IDENTITIES
            # =========================
            with st.expander("🔄 7.6 Angle Identities"):

                st.markdown("### ➕ Angle Sum")

                st.latex(r"\sin(A+B) = \sin A \cos B + \cos A \sin B")
                st.latex(r"\cos(A+B) = \cos A \cos B - \sin A \sin B")

                st.markdown("### ➖ Angle Difference")

                st.latex(r"\sin(A-B) = \sin A \cos B - \cos A \sin B")
                st.latex(r"\cos(A-B) = \cos A \cos B + \sin A \sin B")

                st.markdown("### 🧠 Example")

                st.markdown("""
            Find cos(60° + 30°)

            = cos60 cos30 − sin60 sin30  
            = (1/2)(√3/2) − (√3/2)(1/2)  
            = **0**
                """)

            # =========================
            # 7.7 DOUBLE ANGLE
            # =========================
            with st.expander("⚡ 7.7 Double Angle Formulas"):

                st.markdown("### 📌 Formulas")

                st.latex(r"\sin 2\theta = 2\sin\theta\cos\theta")
                st.latex(r"\cos 2\theta = \cos^2\theta - \sin^2\theta")

                st.markdown("### Alternative Forms")

                st.latex(r"\cos 2\theta = 2\cos^2\theta - 1")
                st.latex(r"\cos 2\theta = 1 - 2\sin^2\theta")

                st.markdown("### 🧠 Example")

                st.markdown("""
            If sinθ = 3/5  

            cosθ = 4/5  

            sin2θ = 2(3/5)(4/5) = **24/25**
                """)

            # =========================
            # 7.8 TRIG IDENTITIES PROOF
            # =========================
            with st.expander("🧠 Proving Identities (Exam Skill)"):

                st.markdown("### 📌 Strategy")

                st.info("""
            - Start from ONE side only  
            - Convert everything to sin & cos  
            - Simplify step-by-step  
                """)

                st.markdown("### 🧠 Example")

                st.markdown("""
            Prove: (1 − cos²θ)/(1 + cosθ) = 1 − cosθ  

            LHS = sin²θ/(1 + cosθ)  

            = (1 − cosθ)(1 + cosθ)/(1 + cosθ)  

            = **1 − cosθ (RHS)**
                """)

        if chapter == "Chapter 8: Limits and Continuity":

            st.markdown("## 📘 Chapter 8: Limits and Continuity")

            # =========================
            # 8.1 LIMITS
            # =========================
            with st.expander("📊 8.1 Limits", expanded=True):

                st.markdown("### 📌 Learning Outcomes")
                st.info("""
                LO1: Understand the concept of limits  
                LO2: Evaluate limits algebraically  
                """)

                st.markdown("### 🧠 Key Idea")

                st.markdown("""
            Limit describes the value a function approaches as x → a  

            It does NOT require x = a  
                """)

                st.latex(r"\lim_{x \to a} f(x) = L")

                st.markdown("""
            - x → a → input approaches a  
            - f(x) → L → output approaches L  
                """)

                # =========================
                # EXAMPLE
                # =========================
                st.markdown("### 🧠 Example")

                st.markdown("""
            Find: lim (x² − 4)/(x − 2) as x → 2  

            Factor:
            (x² − 4) = (x − 2)(x + 2)  

            Cancel:
            = x + 2  

            Substitute:
            = 4  
                """)

            # =========================
            # 8.2 LIMIT LAWS
            # =========================
            with st.expander("📘 8.2 Laws of Limits"):

                st.markdown("### 📦 Basic Laws")

                st.latex(r"\lim (f + g) = \lim f + \lim g")
                st.latex(r"\lim (fg) = (\lim f)(\lim g)")
                st.latex(r"\lim \frac{f}{g} = \frac{\lim f}{\lim g}")

                st.markdown("### 🧠 Direct Substitution")

                st.markdown("""
            If function is continuous → just substitute x = a  
                """)

                st.markdown("### 🧠 Example")

                st.markdown("""
            Find: lim (3x + 2) as x → 1  

            = 3(1) + 2  
            = **5**
                """)

            # =========================
            # 8.3 INDETERMINATE FORMS
            # =========================
            with st.expander("⚠️ 8.3 Indeterminate Forms"):

                st.markdown("### 📌 Key Idea")

                st.info("""
            Forms like 0/0 are undefined → need simplification  
                """)

                st.markdown("### 🔧 Methods")

                st.markdown("""
            - Factorisation  
            - Rationalisation  
            - Simplify expression  
                """)

                st.markdown("### 🧠 Example")

                st.markdown("""
            Find: lim (√(x+1) − 1)/x as x → 0  

            Multiply conjugate:

            = [(√(x+1) − 1)(√(x+1) + 1)] / [x(√(x+1)+1)]  

            = x / [x(√(x+1)+1)]  

            Cancel x:

            = 1 / (√(x+1)+1)  

            Substitute x = 0:

            = **1/2**
                """)

            # =========================
            # 8.4 ONE-SIDED LIMITS
            # =========================
            with st.expander("➡️ 8.4 One-Sided Limits"):

                st.markdown("### 📌 Definitions")

                st.latex(r"\lim_{x \to a^-} f(x) = \text{left-hand limit}")
                st.latex(r"\lim_{x \to a^+} f(x) = \text{right-hand limit}")

                st.markdown("### 🧠 Key Condition")

                st.info("""
            Limit exists ONLY IF:
            LHL = RHL  
                """)

                st.markdown("### 🧠 Example")

                st.markdown("""
            If:
            f(x) = { x²  , x < 1  
                { 2x , x ≥ 1  

            LHL = 1² = 1  
            RHL = 2(1) = 2  

            Since not equal → limit does NOT exist  
                """)

            # =========================
            # 8.5 LIMITS AT INFINITY
            # =========================
            with st.expander("∞ 8.5 Limits at Infinity"):

                st.markdown("### 📌 Key Idea")

                st.markdown("""
            Used to determine end behaviour of function  
                """)

                st.markdown("### 🧠 Rules")

                st.info("""
            Divide by highest power of x  
                """)

                st.markdown("### 🧠 Example")

                st.markdown("""
            Find: lim (2x² + 1)/(x² − 3) as x → ∞  

            Divide by x²:

            = (2 + 1/x²)/(1 − 3/x²)  

            As x → ∞:
            = 2/1  

            = **2**
                """)

            # =========================
            # 8.6 CONTINUITY
            # =========================
            with st.expander("🔗 8.6 Continuity"):

                st.markdown("### 📌 Definition")

                st.markdown("""
            Function is continuous at x = a if:

            1. f(a) exists  
            2. lim f(x) exists  
            3. lim f(x) = f(a)  
                """)

                st.latex(r"\lim_{x \to a} f(x) = f(a)")

                st.markdown("### ❌ Types of Discontinuity")

                st.markdown("""
            - Removable (hole)  
            - Jump discontinuity  
            - Infinite discontinuity  
                """)

                st.markdown("### 🧠 Example")

                st.markdown("""
            Find k such that function is continuous:

            f(x) = { x² , x ≠ 2  
                { k  , x = 2  

            lim x→2 x² = 4  

            So k = **4**
                """)

            # =========================
            # 8.7 GRAPHICAL INTERPRETATION
            # =========================
            with st.expander("📈 8.7 Graph Interpretation"):

                st.markdown("### 🧠 Key Idea")

                st.markdown("""
            - Continuous graph → no breaks  
            - Hole → removable discontinuity  
            - Jump → different left/right limits  
                """)

                st.info("""
            💡 If you can DRAW it smoothly → it's continuous  
                """)

        if chapter == "Chapter 9: Differentiation":

            st.markdown("## 📘 Chapter 9: Differentiation")

            # =========================
            # 9.1 FIRST PRINCIPLE
            # =========================
            with st.expander("🧠 9.1 First Principle of Derivative", expanded=True):

                st.markdown("### 📌 Learning Outcomes")
                st.info("""
                LO1: Find derivative using first principle  
                LO2: Understand differentiability  
                """)

                st.markdown("### 📌 Definition")

                st.latex(r"f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}")

                st.markdown("""
            - Measures **rate of change**  
            - Foundation of ALL differentiation  
                """)

                st.markdown("### 🧠 Example")

                st.markdown("""
            Find derivative of f(x) = x²  

            f'(x) = lim ( (x+h)² − x² ) / h  

            = lim (x² + 2xh + h² − x²)/h  

            = lim (2x + h)  

            = **2x**
                """)

            # =========================
            # DIFFERENTIABILITY
            # =========================
            with st.expander("🔗 Differentiability"):

                st.markdown("### 📌 Key Idea")

                st.markdown("""
            A function is differentiable at x = a if derivative exists  
                """)

                st.markdown("### ⚠️ Important")

                st.info("""
            Differentiable ⇒ Continuous  
            BUT  
            Continuous ≠ Differentiable  
                """)

                st.markdown("### 🧠 Example")

                st.markdown("""
            Sharp corner → NOT differentiable  
                """)

            # =========================
            # 9.2 RULES
            # =========================
            with st.expander("⚡ 9.2 Rules of Differentiation"):

                st.markdown("### 🔹 Basic Rules")

                st.latex(r"\frac{d}{dx}(k) = 0")
                st.latex(r"\frac{d}{dx}(x^n) = nx^{n-1}")
                st.latex(r"\frac{d}{dx}(kx^n) = knx^{n-1}")

                st.markdown("### 🔹 Sum Rule")

                st.latex(r"\frac{d}{dx}(u+v) = u' + v'")

                st.markdown("### 🔹 Product Rule")

                st.latex(r"\frac{d}{dx}(uv) = u'v + uv'")

                st.markdown("### 🔹 Quotient Rule")

                st.latex(r"\frac{d}{dx}\left(\frac{u}{v}\right) = \frac{u'v - uv'}{v^2}")

                st.markdown("### 🔹 Chain Rule")

                st.latex(r"\frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx}")

                st.markdown("### 🧠 Example")

                st.markdown("""
            Differentiate: y = (x² + 1)(x³)

            = (2x)(x³) + (x²+1)(3x²)  
            = **2x⁴ + 3x²(x²+1)**
                """)

            # =========================
            # GENERAL POWER RULE
            # =========================
            with st.expander("📐 General Power Rule"):

                st.latex(r"\frac{d}{dx}[f(x)]^n = n[f(x)]^{n-1} f'(x)")

                st.markdown("### 🧠 Example")

                st.markdown("""
            y = (x² + 1)³  

            dy/dx = 3(x² + 1)²(2x)  
            = **6x(x²+1)²**
                """)

            # =========================
            # HIGHER ORDER
            # =========================
            with st.expander("📊 Higher Order Derivatives"):

                st.markdown("### 📌 Notation")

                st.latex(r"y' = \frac{dy}{dx}")
                st.latex(r"y'' = \frac{d^2y}{dx^2}")
                st.latex(r"y''' = \frac{d^3y}{dx^3}")

                st.markdown("### 🧠 Example")

                st.markdown("""
            y = x³  

            y' = 3x²  
            y'' = 6x  
            y''' = 6  
                """)

            # =========================
            # EXPONENTIAL & LOG
            # =========================
            with st.expander("📈 Exponential & Logarithmic Functions"):

                st.markdown("### 🔹 Exponential")

                st.latex(r"\frac{d}{dx}(e^x) = e^x")
                st.latex(r"\frac{d}{dx}(e^{f(x)}) = e^{f(x)} f'(x)")

                st.markdown("### 🔹 Logarithm")

                st.latex(r"\frac{d}{dx}(\ln x) = \frac{1}{x}")
                st.latex(r"\frac{d}{dx}(\ln f(x)) = \frac{f'(x)}{f(x)}")

                st.markdown("### 🧠 Example")

                st.markdown("""
            y = ln(x² + 1)  

            dy/dx = 2x/(x²+1)
                """)

            # =========================
            # TRIG
            # =========================
            with st.expander("📐 Trigonometric Differentiation"):

                st.latex(r"\frac{d}{dx}(\sin x) = \cos x")
                st.latex(r"\frac{d}{dx}(\cos x) = -\sin x")
                st.latex(r"\frac{d}{dx}(\tan x) = \sec^2 x")

                st.markdown("### 🧠 Example")

                st.markdown("""
            y = sin(3x)  

            dy/dx = 3cos(3x)
                """)

            # =========================
            # IMPLICIT
            # =========================
            with st.expander("🔄 Implicit Differentiation"):

                st.markdown("### 📌 Key Idea")

                st.markdown("""
            Used when y is NOT isolated  
                """)

                st.markdown("### 🧠 Steps")

                st.markdown("""
            1. Differentiate both sides  
            2. Treat y as function of x  
            3. Solve for dy/dx  
                """)

                st.markdown("### 🧠 Example")

                st.markdown("""
            xy + y² = 2x  

            Differentiate:

            x(dy/dx) + y + 2y(dy/dx) = 2  

            Group dy/dx:

            (x + 2y)(dy/dx) = 2 − y  

            dy/dx = (2 − y)/(x + 2y)
                """)

            # =========================
            # PARAMETRIC
            # =========================
            with st.expander("🌀 Parametric Differentiation"):

                st.markdown("### 📌 Formula")

                st.latex(r"\frac{dy}{dx} = \frac{dy/dt}{dx/dt}")

                st.markdown("### 🧠 Example")

                st.markdown("""
            x = t², y = t³  

            dx/dt = 2t  
            dy/dt = 3t²  

            dy/dx = 3t² / 2t = **3t/2**
                """)

            # =========================
            # SECOND DERIV PARAMETRIC
            # =========================
            with st.expander("⚡ Second Derivative (Parametric)"):

                st.latex(r"\frac{d^2y}{dx^2} = \frac{d}{dt}\left(\frac{dy}{dx}\right) \div \frac{dx}{dt}")

                st.markdown("### 🧠 Idea")

                st.markdown("""
            Differentiate AGAIN using chain rule  
                """)

        if chapter == "Chapter 10: Application of Differentiation":

            st.markdown("## 📘 Chapter 10: Application of Differentiation")

            # =========================
            # 10.1 EXTREMUM PROBLEMS
            # =========================
            with st.expander("📊 10.1 Extremum Problems", expanded=True):

                st.markdown("### 📌 Learning Outcomes")
                st.info("""
                LO1: Find critical points  
                LO2: Determine relative extrema  
                LO3: Identify point of inflection  
                LO4: Sketch graphs  
                LO5: Solve optimization problems  
                """)

            # =========================
            # CRITICAL POINTS
            # =========================
            with st.expander("🧠 Critical Points & Stationary Points"):

                st.markdown("### 📌 Definitions")

                st.latex(r"f'(x) = 0 \quad \text{or undefined}")

                st.markdown("""
            - **Critical number**: value of x where f'(x)=0 or undefined  
            - **Stationary point**: where f'(x)=0  
            - **Stationary value**: corresponding y-value  
                """)

                st.markdown("### 🧠 Example")

                st.markdown("""
            Find stationary points of:  
            y = x³ − 6x² + 9x  

            y' = 3x² − 12x + 9  
            = 3(x² − 4x + 3)  
            = 3(x−1)(x−3)

            Stationary points:  
            x = 1, 3  

            Substitute into y:

            y(1) = 4  
            y(3) = 0  

            👉 Points: (1,4), (3,0)
                """)

            # =========================
            # FIRST DERIVATIVE TEST
            # =========================
            with st.expander("⚡ First Derivative Test"):

                st.markdown("### 📌 Idea")

                st.markdown("""
            Check sign of f'(x) before and after critical point  
                """)

                st.markdown("""
            - + → − → **Maximum**  
            - − → + → **Minimum**  
            - no sign change → **No extremum**  
                """)

                st.markdown("### 🧠 Example")

                st.markdown("""
            For x = 1:

            f'(x) changes from + to − → Maximum  

            For x = 3:

            f'(x) changes from − to + → Minimum  
                """)

            # =========================
            # SECOND DERIVATIVE TEST
            # =========================
            with st.expander("📐 Second Derivative Test"):

                st.markdown("### 📌 Rules")

                st.latex(r"f''(x) > 0 \Rightarrow \text{Minimum}")
                st.latex(r"f''(x) < 0 \Rightarrow \text{Maximum}")
                st.latex(r"f''(x) = 0 \Rightarrow \text{Test fails}")

                st.markdown("### 🧠 Example")

                st.markdown("""
            y = x³ − 6x² + 9x  

            y'' = 6x − 12  

            At x = 1 → y'' = -6 → Maximum  
            At x = 3 → y'' = 6 → Minimum  
                """)

            # =========================
            # INFLECTION POINT
            # =========================
            with st.expander("🔄 Point of Inflection"):

                st.markdown("### 📌 Definition")

                st.markdown("""
            Point where concavity changes  
                """)

                st.markdown("### 🧠 Steps")

                st.markdown("""
            1. Find f''(x)  
            2. Solve f''(x)=0  
            3. Check sign change  
                """)

                st.markdown("### 🧠 Example")

                st.markdown("""
            y = x³  

            y'' = 6x  

            6x = 0 → x = 0  

            Check sign: changes → inflection  

            👉 Point: (0,0)
                """)

            # =========================
            # GRAPH SKETCHING
            # =========================
            with st.expander("📈 Sketching Graphs"):

                st.markdown("### 🧠 Key Features")

                st.markdown("""
            1. Intercepts  
            2. Stationary points  
            3. Increasing/decreasing intervals  
            4. Concavity  
            5. Inflection points  
                """)

                st.markdown("### 🎯 Tip")

                st.info("""
            Always combine:
            - f'(x) → shape  
            - f''(x) → curvature  
                """)

            # =========================
            # OPTIMIZATION
            # =========================
            with st.expander("🎯 Optimization Problems"):

                st.markdown("### 📌 Steps")

                st.markdown("""
            1. Define variables  
            2. Form equation (Area/Volume)  
            3. Express in ONE variable  
            4. Differentiate  
            5. Solve f'(x)=0  
            6. Verify using f''(x)  
                """)

                st.markdown("### 🧠 Example")

                st.markdown("""
            Rectangular field with 800m fencing (3 sides):

            Let width = x, length = y  

            Equation:  
            2x + y = 800 → y = 800 − 2x  

            Area:  
            A = xy = x(800−2x)  
            = 800x − 2x²  

            A' = 800 − 4x  

            Set = 0:  
            x = 200  

            y = 400  

            👉 Max area = 80,000 m²
                """)

            # =========================
            # RATE OF CHANGE
            # =========================
            with st.expander("⏱️ 10.2 Rate of Change"):

                st.markdown("### 📌 Formula")

                st.latex(r"\frac{dy}{dt}")

                st.markdown("""
            - Positive → increasing  
            - Negative → decreasing  
                """)

                st.latex(r"\frac{dy}{dx} = \frac{dy}{dt} \cdot \frac{dt}{dx}")

                st.markdown("### 🧠 Example")

                st.markdown("""
            If y = t²  

            dy/dt = 2t  

            At t = 3 → rate = 6  
                """)

            # =========================
            # RELATED RATES
            # =========================
            with st.expander("🔗 Related Rates Problems"):

                st.markdown("### 📌 Steps")

                st.markdown("""
            1. Draw diagram  
            2. Write equation  
            3. Differentiate w.r.t time  
            4. Substitute values  
                """)

                st.markdown("### 🧠 Example")

                st.markdown("""
            Sphere: V = (4/3)πr³  

            dV/dt = 4πr² dr/dt  

            Given: dV/dt = 2  

            2 = 4π(12²) dr/dt  

            dr/dt ≈ 0.0011 m/min  
                """)

            # =========================
            # SUMMARY
            # =========================
            with st.expander("🔥 Final Summary"):

                st.markdown("""
            - f'(x)=0 → stationary point  
            - f''(x)>0 → minimum  
            - f''(x)<0 → maximum  
            - f''(x)=0 → possible inflection  

            💡 Optimization = real-life application  
            💡 Related rates = time-based change  
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

        if chapter == "Chapter 5: Vectors":

            st.markdown("## 📘 Chapter: Vectors")

            # =========================
            # 1.1 INTRODUCTION TO VECTORS
            # =========================
            with st.expander("📌 1.1 Introduction to Vectors", expanded=True):

                st.markdown("### 📌 Learning Outcomes")
                st.info("""
                LO1: Understand scalar and vector quantities  
                LO2: Represent vectors in 2D and 3D  
                LO3: Perform basic vector operations  
                """)

                st.markdown("### 🧠 Key Concepts")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("""
            - **Scalar**: Magnitude only (e.g. mass, time)  
            - **Vector**: Magnitude + direction (e.g. velocity, force)  
            - **Notation**: **a**, **AB**, or column vector  
                    """)

                with col2:
                    st.markdown("""
            - **Zero Vector**: magnitude = 0  
            - **Unit Vector**: magnitude = 1  
            - **Position Vector**: from origin to a point  
                    """)

            # =========================
            # 1.2 VECTOR REPRESENTATION
            # =========================
            with st.expander("📐 1.2 Representation of Vectors"):

                st.markdown("### 📌 Column Form")

                st.latex(r"\vec{a} = \begin{pmatrix} a_1 \\ a_2 \end{pmatrix}")

                st.markdown("### 📌 3D Form")

                st.latex(r"\vec{a} = \begin{pmatrix} a_1 \\ a_2 \\ a_3 \end{pmatrix}")

                st.markdown("""
            - Components represent direction along axes  
            - Can be written as **ai + bj (+ ck)**  
                """)

            # =========================
            # 1.3 VECTOR OPERATIONS
            # =========================
            with st.expander("➕ 1.3 Vector Operations"):

                st.markdown("### ➕ Addition")

                st.latex(r"\vec{a} + \vec{b} = \begin{pmatrix} a_1 + b_1 \\ a_2 + b_2 \end{pmatrix}")

                st.markdown("### ➖ Subtraction")

                st.latex(r"\vec{a} - \vec{b} = \begin{pmatrix} a_1 - b_1 \\ a_2 - b_2 \end{pmatrix}")

                st.markdown("### ✖️ Scalar Multiplication")

                st.latex(r"k\vec{a} = \begin{pmatrix} ka_1 \\ ka_2 \end{pmatrix}")

            # =========================
            # 1.4 MAGNITUDE OF VECTOR
            # =========================
            with st.expander("📏 1.4 Magnitude of a Vector"):

                st.markdown("### 📌 Formula")

                st.latex(r"|\vec{a}| = \sqrt{a_1^2 + a_2^2}")

                st.markdown("### 📌 3D Case")

                st.latex(r"|\vec{a}| = \sqrt{a_1^2 + a_2^2 + a_3^2}")

                st.markdown("""
            - Represents length of vector  
            - Always positive  
                """)

            # =========================
            # 1.5 UNIT VECTOR
            # =========================
            with st.expander("🧭 1.5 Unit Vector"):

                st.markdown("### 📌 Definition")

                st.latex(r"\hat{a} = \frac{\vec{a}}{|\vec{a}|}")

                st.markdown("""
            - Direction same as original vector  
            - Magnitude = 1  
                """)

            # =========================
            # 1.6 DOT PRODUCT
            # =========================
            with st.expander("🔗 1.6 Dot Product"):

                st.markdown("### 📌 Formula")

                st.latex(r"\vec{a} \cdot \vec{b} = a_1b_1 + a_2b_2")

                st.markdown("### 📐 Angle Form")

                st.latex(r"\vec{a} \cdot \vec{b} = |\vec{a}||\vec{b}|\cos\theta")

                st.markdown("""
            - Result is a scalar  
            - Used to find angle between vectors  
                """)

            # =========================
            # 1.7 PARALLEL & PERPENDICULAR
            # =========================
            with st.expander("📊 1.7 Vector Relationships"):

                st.markdown("### 📌 Parallel Vectors")

                st.markdown("""
            - One vector is scalar multiple of another  
            - **a = k b**
                """)

                st.markdown("### 📌 Perpendicular Vectors")

                st.markdown("""
            - Dot product = 0  
            - **a · b = 0**
                """)

            # =========================
            # 1.8 POSITION VECTOR
            # =========================
            with st.expander("📍 1.8 Position Vector"):

                st.markdown("### 📌 Definition")

                st.markdown("""
            - Vector from origin to a point  
            - Example: A(x, y) → **OA = (x, y)**  
                """)

                st.markdown("### 📌 Vector Between Two Points")

                st.latex(r"\vec{AB} = \vec{OB} - \vec{OA}")

        if chapter == "Chapter 6: Data Description":

            st.markdown("## 📊 Chapter: Data Description")

            # =========================
            # 1.1 TYPES OF DATA
            # =========================
            with st.expander("📂 1.1 Types of Data", expanded=True):

                st.markdown("### 📌 Learning Outcomes")
                st.info("""
                LO1: Understand types of data  
                LO2: Distinguish between qualitative and quantitative data  
                """)

                st.markdown("### 🧠 Classification of Data")

                col1, col2 = st.columns(2)

                with col1:
                    st.markdown("""
            - **Qualitative Data**: Non-numerical  
            Example: Gender  

            - **Quantitative Data**: Numerical  
            Example: Height  
                    """)

                with col2:
                    st.markdown("""
            - **Discrete Data**: Countable  
            Example: Number of students  

            - **Continuous Data**: Measurable  
            Example: Weight  
                    """)

                st.markdown("### ✏️ Example")

                st.markdown("""
            Classify the following:
            1. Number of cars → **Discrete**  
            2. Temperature → **Continuous**  
            3. Eye colour → **Qualitative**
                """)


            # =========================
            # 1.2 FREQUENCY DISTRIBUTION
            # =========================
            with st.expander("📊 1.2 Frequency Distribution"):

                st.markdown("### 📌 Learning Outcomes")
                st.info("""
                LO1: Construct frequency tables  
                LO2: Understand class intervals  
                """)

                st.markdown("### 📦 Key Terms")

                st.markdown("""
            - Class Interval  
            - Frequency (f)  
            - Midpoint (x)  
                """)

                st.markdown("### ✏️ Example")

                st.markdown("""
            Class: 0–10, 10–20  
            Find midpoint of 0–10:

            Midpoint = (0 + 10)/2 = **5**
                """)


            # =========================
            # 1.3 MEAN (UNGROUPED & GROUPED)
            # =========================
            with st.expander("📍 1.3 Mean"):

                st.markdown("### 📌 Learning Outcomes")
                st.info("""
                LO1: Calculate mean for data  
                """)

                st.markdown("### 📊 Formula")

                st.latex(r"\bar{x} = \frac{\sum x}{n}")

                st.markdown("### ✏️ Example (Ungrouped)")

                st.markdown("""
            Data: 2, 4, 6, 8  

            Mean = (2+4+6+8)/4 = **5**
                """)

                st.markdown("### 📊 Grouped Data")

                st.latex(r"\bar{x} = \frac{\sum fx}{\sum f}")

                st.markdown("### ✏️ Example (Grouped)")

                st.markdown("""
            | Class | f | Midpoint (x) | fx |
            |------|---|-------------|----|
            | 0–10 | 2 | 5 | 10 |
            | 10–20 | 3 | 15 | 45 |

            Σf = 5, Σfx = 55  

            Mean = 55 / 5 = **11**
                """)


            # =========================
            # 1.4 MEDIAN & MODE
            # =========================
            with st.expander("📊 1.4 Median & Mode"):

                st.markdown("### 📌 Learning Outcomes")
                st.info("""
                LO1: Find median and mode  
                """)

                st.markdown("### 📊 Median")

                st.markdown("""
            - Middle value after arranging  
                """)

                st.markdown("### ✏️ Example")

                st.markdown("""
            Data: 1, 3, 5, 7, 9  

            Median = **5**
                """)

                st.markdown("### 📊 Mode")

                st.markdown("""
            - Most frequent value  
                """)

                st.markdown("### ✏️ Example")

                st.markdown("""
            Data: 2, 2, 3, 4  

            Mode = **2**
                """)


            # =========================
            # 1.5 DISPERSION
            # =========================
            with st.expander("📈 1.5 Measures of Dispersion"):

                st.markdown("### 📌 Learning Outcomes")
                st.info("""
                LO1: Measure spread of data  
                """)

                st.markdown("### 📏 Range")

                st.latex(r"\text{Range} = \text{Max} - \text{Min}")

                st.markdown("### ✏️ Example")

                st.markdown("""
            Data: 3, 7, 10  

            Range = 10 − 3 = **7**
                """)

                st.markdown("### 📊 Variance & Standard Deviation")

                st.latex(r"\sigma = \sqrt{\frac{\sum (x - \bar{x})^2}{n}}")

                st.markdown("### ✏️ Example")

                st.markdown("""
            Data: 2, 4, 6  

            Mean = 4  

            (2−4)² = 4  
            (4−4)² = 0  
            (6−4)² = 4  

            Variance = (4+0+4)/3 = 8/3  

            SD = √(8/3) ≈ **1.63**
                """)


            # =========================
            # 1.6 GRAPHICAL REPRESENTATION
            # =========================
            with st.expander("📉 1.6 Graphs"):

                st.markdown("### 📌 Learning Outcomes")
                st.info("""
                LO1: Interpret graphs  
                """)

                st.markdown("""
            - Histogram → Continuous  
            - Bar Chart → Discrete  
            - Ogive → Cumulative frequency  
                """)

                st.markdown("### ✏️ Example")

                st.markdown("""
            Ogive is used to find:
            - Median  
            - Quartiles  
                """)

        if chapter == "Chapter 7: Probability": 

            st.markdown("## 📘 Chapter 7: Probability")

            # =========================
            # 1.1 RANDOM VARIABLES
            # =========================
            with st.expander("🎯 1.1 Random Variables", expanded=True):

                st.markdown("### 📌 Learning Outcomes")
                st.info("""
                LO1: Define discrete random variables  
                LO2: Identify possible values of X  
                """)

                st.markdown("""
            - A **random variable (X)** is a function that assigns a number to each outcome  
            - **Discrete random variable** → takes countable values  
                """)

                st.markdown("### ✏️ Example")

                st.markdown("""
            Let X = number of heads when tossing 2 coins  

            Possible values of X:  
            X = 0, 1, 2  
                """)


            # =========================
            # 1.2 PROBABILITY DISTRIBUTION
            # =========================
            with st.expander("📊 1.2 Probability Distribution"):

                st.markdown("### 📌 Learning Outcomes")
                st.info("""
                LO1: Construct probability distribution table  
                """)

                st.markdown("""
            - A **probability distribution** lists all values of X and their probabilities  
            - Must satisfy:
            """)

                st.latex(r"\sum P(X) = 1")

                st.markdown("### ✏️ Example")

                st.markdown("""
            | X | 0 | 1 | 2 |
            |---|---|---|---|
            | P(X) | 0.25 | 0.5 | 0.25 |

            Check: 0.25 + 0.5 + 0.25 = **1 ✔**
                """)


            # =========================
            # 1.3 EXPECTATION (MEAN)
            # =========================
            with st.expander("📍 1.3 Expectation (Mean)"):

                st.markdown("### 📌 Learning Outcomes")
                st.info("""
                LO1: Find expected value  
                """)

                st.latex(r"E(X) = \sum xP(x)")

                st.markdown("### ✏️ Example")

                st.markdown("""
            | X | 0 | 1 | 2 |
            |---|---|---|---|
            | P(X) | 0.25 | 0.5 | 0.25 |

            E(X) = (0)(0.25) + (1)(0.5) + (2)(0.25)  
                = 0 + 0.5 + 0.5  
                = **1**
                """)


            # =========================
            # 1.4 VARIANCE & STANDARD DEVIATION
            # =========================
            with st.expander("📈 1.4 Variance & Standard Deviation"):

                st.markdown("### 📌 Learning Outcomes")
                st.info("""
                LO1: Calculate variance and standard deviation  
                """)

                st.latex(r"\mathrm{Var}(X) = E(X^2) - [E(X)]^2")

                st.latex(r"\sigma = \sqrt{\mathrm{Var}(X)}")

                st.markdown("### ✏️ Example")

                st.markdown("""
            Using previous table:

            E(X) = 1  

            E(X²) = (0²)(0.25) + (1²)(0.5) + (2²)(0.25)  
                = 0 + 0.5 + 1  
                = 1.5  

            Var(X) = 1.5 − (1)² = 0.5  

            σ = √0.5 ≈ **0.707**
                """)


            # =========================
            # 1.5 FUNCTIONS OF RANDOM VARIABLES
            # =========================
            with st.expander("🔄 1.5 Functions of Random Variables"):

                st.markdown("### 📌 Learning Outcomes")
                st.info("""
                LO1: Find expectation of aX + b  
                """)

                st.latex(r"E(aX + b) = aE(X) + b")

                st.markdown("### ✏️ Example")

                st.markdown("""
            Given E(X) = 2  

            Find E(3X + 1):

            E(3X + 1) = 3(2) + 1 = **7**
                """)


            # =========================
            # 1.6 PROPERTIES
            # =========================
            with st.expander("📘 1.6 Important Properties"):

                st.markdown("""
            - P(X) ≥ 0  
            - ΣP(X) = 1  
            - Variance is always ≥ 0  
                """)

                st.markdown("### ✏️ Example")

                st.markdown("""
            If probabilities add to 1.2 → ❌ Invalid  

            If variance = -3 → ❌ Impossible  
                """)

        if chapter == "Chapter 8: Random Variables":

            st.markdown("## 📘 Chapter 8: Random Variables")

            # =========================
            # 1.1 BASIC CONCEPT
            # =========================
            with st.expander("📌 1.1 Random Variables", expanded=True):

                st.markdown("### 📌 Learning Outcomes")
                st.info("""
                LO1: Define random variables  
                LO2: Distinguish discrete and continuous  
                """)

                st.markdown("""
            - A **random variable (X)** assigns a numerical value to outcomes  
            - Types:
            - **Discrete** → countable values  
            - **Continuous** → values in interval  
                """)

                st.markdown("### ✏️ Example")

                st.markdown("""
            - Number of students → **Discrete**  
            - Time taken → **Continuous**  
                """)


            # =========================
            # 1.2 DISCRETE DISTRIBUTION
            # =========================
            with st.expander("📊 1.2 Discrete Probability Distribution"):

                st.markdown("### 📌 Key Rule")

                st.latex(r"\sum P(X=x) = 1")

                st.markdown("### ✏️ Example")

                st.markdown("""
            P(X=x) = k(4 - x), x = 0,1,2,3  

            Sum = k(4+3+2+1) = 10k = 1  

            k = **0.1**
                """)


            # =========================
            # 1.3 CUMULATIVE DISTRIBUTION (DISCRETE)
            # =========================
            with st.expander("📈 1.3 Cumulative Distribution Function (CDF)"):

                st.latex(r"F(x) = P(X \le x)")

                st.markdown("### ✏️ Example")

                st.markdown("""
            If:
            P(X=1)=0.2, P(X=2)=0.3, P(X=3)=0.5  

            F(2) = 0.2 + 0.3 = **0.5**  
                """)

                st.markdown("### 📌 Important")

                st.markdown("""
            - P(X = a) = F(a) − F(a−1)  
            - P(X > a) = 1 − F(a)  
                """)


            # =========================
            # 1.4 EXPECTATION (DISCRETE)
            # =========================
            with st.expander("📍 1.4 Expectation (Discrete)"):

                st.latex(r"E(X) = \sum xP(X=x)")

                st.markdown("### ✏️ Example")

                st.markdown("""
            X: 1, 2, 3  
            P: 1/6, 2/6, 3/6  

            E(X) = (1)(1/6)+(2)(2/6)+(3)(3/6)  
                = 14/6 = **2.33**
                """)

                st.markdown("### 📌 Properties")

                st.markdown("""
            - E(aX + b) = aE(X) + b  
                """)


            # =========================
            # 1.5 VARIANCE (DISCRETE)
            # =========================
            with st.expander("📊 1.5 Variance (Discrete)"):

                st.latex(r"\mathrm{Var}(X) = E(X^2) - [E(X)]^2")

                st.markdown("### ✏️ Example")

                st.markdown("""
            E(X) = 2  

            E(X²) = 5  

            Var(X) = 5 − 4 = **1**
                """)


            # =========================
            # 1.6 CONTINUOUS PDF
            # =========================
            with st.expander("📉 1.6 Probability Density Function (PDF)"):

                st.markdown("### 📌 Conditions")

                st.latex(r"f(x) \ge 0")

                st.latex(r"\int_{-\infty}^{\infty} f(x)\,dx = 1")

                st.markdown("### ✏️ Example")

                st.markdown("""
            f(x) = kx, 0 ≤ x ≤ 2  

            ∫ kx dx = k(x²/2) from 0 to 2 = 2k = 1  

            k = **1/2**
                """)

        if chapter == "Chapter 9: Special Probability Distribution":

            st.markdown("## 🎲 Chapter: Special Probability Distribution")

            # =========================
            # 9.1 BINOMIAL DISTRIBUTION
            # =========================
            with st.expander("📊 9.1 Binomial Distribution", expanded=True):

                st.markdown("### 📌 Learning Outcomes")
                st.info("""
                LO1: Identify binomial distribution  
                LO2: Find mean and variance  
                LO3: Calculate probability  
                """)

                st.markdown("### 📌 Conditions (Must satisfy all)")
                st.markdown("""
            1. Fixed number of trials (n)  
            2. Only 2 outcomes (success/failure)  
            3. Constant probability p  
            4. Independent trials  
                """)

                st.markdown("### 📌 Notation")
                st.latex(r"X \sim B(n, p)")

                st.markdown("### 📌 Probability Formula")
                st.latex(r"P(X = r) = {n \choose r} p^r (1-p)^{n-r}")

                st.markdown("### 📌 Mean & Variance")
                st.latex(r"E(X) = np")
                st.latex(r"\mathrm{Var}(X) = np(1-p)")

                st.markdown("### ✏️ Example")

                st.markdown("""
            A coin is tossed 3 times  

            Find P(X = 2 heads)

            P(X=2) = 3C2 (0.5)^2 (0.5)^1  
                = 3 × 0.25 × 0.5  
                = **0.375**
                """)


            # =========================
            # BINOMIAL PROBABILITY
            # =========================
            with st.expander("📘 Binomial Probability Cases"):

                st.markdown("""
            - P(X ≥ r) → use table or complement  
            - P(X ≤ r) → sum probabilities  
            - P(X > r) = 1 − P(X ≤ r)  
            - P(X < r) = P(X ≤ r−1)  
                """)

                st.markdown("### ✏️ Example")

                st.markdown("""
            P(X ≤ 2) = P(0) + P(1) + P(2)
                """)


            # =========================
            # 9.2 POISSON DISTRIBUTION
            # =========================
            with st.expander("📊 9.2 Poisson Distribution"):

                st.markdown("### 📌 Definition")
                st.markdown("""
            Used for counting events in fixed interval (time/space)
                """)

                st.latex(r"X \sim Po(\lambda)")

                st.markdown("### 📌 Formula")
                st.latex(r"P(X=x) = \frac{e^{-\lambda}\lambda^x}{x!}")

                st.markdown("### 📌 Mean & Variance")
                st.latex(r"E(X)=\lambda")
                st.latex(r"\mathrm{Var}(X)=\lambda")

                st.markdown("### ✏️ Example")

                st.markdown("""
            λ = 3  

            Find P(X=2)

            P(X=2) = e^{-3} * 3^2 / 2!  
                = e^{-3} * 9 / 2  
                ≈ **0.224**
                """)


            # =========================
            # 9.3 NORMAL DISTRIBUTION
            # =========================
            with st.expander("📈 9.3 Normal Distribution"):

                st.markdown("### 📌 Notation")
                st.latex(r"X \sim N(\mu, \sigma^2)")

                st.markdown("### 📌 Properties")
                st.markdown("""
            - Bell-shaped curve  
            - Symmetric  
            - Mean = median = mode  
            - Total area = 1  
                """)

                st.markdown("### 📌 Standardisation")
                st.latex(r"Z = \frac{X - \mu}{\sigma}")

                st.markdown("### 📌 Standard Normal")
                st.latex(r"Z \sim N(0,1)")

                st.markdown("### ✏️ Example")

                st.markdown("""
            X ~ N(10, 9), find Z when X = 14  

            Z = (14 - 10) / 3  
            = **1.33**
                """)


            # =========================
            # NORMAL PROBABILITY RULES
            # =========================
            with st.expander("📘 Normal Probability Rules"):

                st.markdown("""
            - P(Z > a) = 1 − P(Z < a)  
            - P(a < Z < b) = P(Z < b) − P(Z < a)  
            - Use Z-table (area under curve)  
                """)

                st.markdown("### ✏️ Example")

                st.markdown("""
            P(0 < Z < 1.5)

            = 0.9332 − 0.5  
            = **0.4332**
                """)


            # =========================
            # 9.4 NORMAL APPROXIMATION
            # =========================
            with st.expander("🔄 9.4 Normal Approximation to Binomial"):

                st.markdown("### 📌 Conditions")
                st.markdown("""
            - n is large  
            - np ≥ 5 and n(1-p) ≥ 5  
                """)

                st.markdown("### 📌 Approximation")
                st.latex(r"X \sim B(n,p) \approx N(np, np(1-p))")

                st.markdown("### 📌 Continuity Correction")
                st.markdown("""
            Discrete → Continuous adjustment:

            - P(X ≤ a) → P(X ≤ a + 0.5)  
            - P(X ≥ a) → P(X ≥ a − 0.5)  
                """)

                st.markdown("### ✏️ Example")

                st.markdown("""
            X ~ B(100, 0.5)

            Find P(X ≥ 60)

            Approx:

            μ = 50, σ = 5  

            P(X ≥ 59.5)

            Z = (59.5 − 50)/5  
            = 1.9  

            Answer from table ≈ **0.0287**
                """)

                # =========================
                # 1.7 CONTINUOUS PROBABILITY
                # =========================
                with st.expander("📊 1.7 Finding Probability (Continuous)"):

                    st.latex(r"P(a < X < b) = \int_a^b f(x)\,dx")

                    st.markdown("### ✏️ Example")

                    st.markdown("""
                f(x)=x/2, 0≤x≤2  

                P(1<X<2) = ∫₁² x/2 dx  
                        = [x²/4]₁²  
                        = (4/4 − 1/4)  
                        = **3/4**
                    """)


                # =========================
                # 1.8 CDF (CONTINUOUS)
                # =========================
                with st.expander("📈 1.8 CDF (Continuous)"):

                    st.latex(r"F(x) = \int_{-\infty}^{x} f(u)\,du")

                    st.markdown("### ✏️ Example")

                    st.markdown("""
                If f(x)=x/2, 0≤x≤2  

                F(x) = x²/4  
                    """)


                # =========================
                # 1.9 EXPECTATION (CONTINUOUS)
                # =========================
                with st.expander("📍 1.9 Expectation (Continuous)"):

                    st.latex(r"E(X) = \int_{-\infty}^{\infty} x f(x)\,dx")

                    st.markdown("### ✏️ Example")

                    st.markdown("""
                f(x)=x/2, 0≤x≤2  

                E(X) = ∫ x(x/2) dx  
                    = ∫ x²/2 dx  
                    = [x³/6]₀²  
                    = 8/6 = **4/3**
                    """)


                # =========================
                # 1.10 VARIANCE (CONTINUOUS)
                # =========================
                with st.expander("📊 1.10 Variance (Continuous)"):

                    st.latex(r"\mathrm{Var}(X) = E(X^2) - [E(X)]^2")

                    st.markdown("### ✏️ Example")

                    st.markdown("""
                E(X)=4/3  

                E(X²)=2  

                Var = 2 − (16/9) = **2/9**
                    """)


                # =========================
                # 1.11 MEDIAN
                # =========================
                with st.expander("📌 1.11 Median"):

                    st.markdown("""
                Median m satisfies:
                """)

                    st.latex(r"F(m) = 0.5")

                    st.markdown("### ✏️ Example")

                    st.markdown("""
                If F(x)=x²/4  

                Set x²/4 = 0.5  

                x² = 2  

                m = **√2**
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
                    "Conics (Circles, Parabola, Ellipse)",
                    "Vectors"
                ]
            )

            if topic == "Functions":

                expr_input = st.text_area(
                    "Enter functions (one per line):",
                    "x**2\nx**3\nsin(x)"
                )

                # ✅ correct splitting (ONLY here)
                expressions = [e.strip() for e in expr_input.split("\n") if e.strip()]

                if st.button("Plot"):

                    x = sp.symbols('x')
                    x_vals = np.linspace(-10, 10, 1000)

                    fig = go.Figure()

                    for expr in expressions:
                        try:
                            import re

                            expr = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr)
                            expr = expr.replace("^", "**")

                            f = sp.sympify(expr)
                            f_lamb = sp.lambdify(x, f, "numpy")

                            y_vals = f_lamb(x_vals)

                            fig.add_trace(go.Scatter(
                                x=x_vals,
                                y=y_vals,
                                mode='lines',
                                name=expr
                            ))

                        except Exception as e:
                            st.error(f"Invalid function: {expr}")

                    fig.update_layout(title="Multiple Function Graph")

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
            # TRIG (UPGRADED)
            # =========================
            elif topic == "Trigonometry":

                st.markdown("### 📐 Trigonometry Visualizer")

                expr_input = st.text_area(
                    "Enter trigonometric functions (one per line):",
                    "sin(x)\ncos(x)\ntan(x)"
                )

                expressions = [e.strip() for e in expr_input.split("\n") if e.strip()]

                col1, col2 = st.columns(2)

                with col1:
                    x_min = st.number_input("Min x", value=-2*np.pi)

                with col2:
                    x_max = st.number_input("Max x", value=2*np.pi)

                if x_min >= x_max:
                    st.error("Min x must be less than Max x")
                    st.stop()

                if st.button("Plot Trig"):

                    import re

                    x = sp.symbols('x')
                    x_vals = np.linspace(x_min, x_max, 2000)

                    fig = go.Figure()

                    for expr in expressions:
                        try:
                            # 🔥 Fix input
                            expr_fixed = expr.replace("^", "**")
                            expr_fixed = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', expr_fixed)

                            # 🔥 Support extra trig functions
                            expr_fixed = expr_fixed.replace("sec(x)", "1/cos(x)")
                            expr_fixed = expr_fixed.replace("cosec(x)", "1/sin(x)")
                            expr_fixed = expr_fixed.replace("cot(x)", "1/tan(x)")

                            f = sp.sympify(expr_fixed)
                            f_lamb = sp.lambdify(x, f, "numpy")

                            y_vals = f_lamb(x_vals)

                            # 🔥 Handle asymptotes (VERY IMPORTANT)
                            y_vals = np.array(y_vals, dtype=float)
                            y_vals[np.abs(y_vals) > 10] = np.nan

                            fig.add_trace(go.Scatter(
                                x=x_vals,
                                y=y_vals,
                                mode='lines',
                                name=expr
                            ))

                        except:
                            st.error(f"Invalid function: {expr}")

                    fig.update_layout(
                        title="Trigonometric Functions",
                        xaxis_title="x",
                        yaxis_title="y"
                    )

                    st.plotly_chart(fig, use_container_width=True)

                    st.info("""
                    💡 Tips:
                    - Use radians (π ≈ 3.14)
                    - Try: sin(2*x), cos(x/2), tan(x)+1
                    - sec, cosec, cot are supported
                    """)

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
            # VECTORS
            # =========================
            elif topic == "Vectors":

                st.markdown("### 🧭 Vector Visualiser")

                mode = st.selectbox(
                    "Choose Mode",
                    [
                        "2D Vectors",
                        "3D Vectors",
                        "Dot Product",
                        "Cross Product",
                        "Angle Between Vectors",
                        "Vector Projection",
                        "3D Line"
                    ]
                )

                # =========================
                # 2D VECTORS
                # =========================
                if mode == "2D Vectors":

                    col1, col2 = st.columns(2)

                    with col1:
                        x1 = st.slider("Vector A - x", -10, 10, 3)
                        y1 = st.slider("Vector A - y", -10, 10, 2)

                    with col2:
                        x2 = st.slider("Vector B - x", -10, 10, 1)
                        y2 = st.slider("Vector B - y", -10, 10, 4)

                    fig = go.Figure()

                    # Vector A
                    fig.add_trace(go.Scatter(
                        x=[0, x1],
                        y=[0, y1],
                        mode='lines+markers',
                        name='A'
                    ))

                    # Vector B
                    fig.add_trace(go.Scatter(
                        x=[0, x2],
                        y=[0, y2],
                        mode='lines+markers',
                        name='B'
                    ))

                    # Resultant A+B
                    fig.add_trace(go.Scatter(
                        x=[0, x1 + x2],
                        y=[0, y1 + y2],
                        mode='lines+markers',
                        name='A + B'
                    ))

                    fig.update_layout(
                        title="2D Vector Addition",
                        xaxis=dict(range=[-10, 10]),
                        yaxis=dict(range=[-10, 10]),
                        showlegend=True
                    )

                    st.plotly_chart(fig, use_container_width=True)

                    st.latex(rf"\vec{{A}} = ({x1},{y1}), \quad \vec{{B}} = ({x2},{y2})")
                    st.latex(rf"\vec{{A}} + \vec{{B}} = ({x1 + x2},{y1 + y2})")

                # =========================
                # 3D VECTORS
                # =========================
                elif mode == "3D Vectors":

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        x = st.number_input("x", value=2.0, step=0.1)
                    with col2:
                        y = st.number_input("y", value=3.0, step=0.1)
                    with col3:
                        z = st.number_input("z", value=1.0, step=0.1)

                    fig = go.Figure(data=[go.Cone(
                        x=[0], y=[0], z=[0],
                        u=[x], v=[y], w=[z]
                    )])

                    limit = max(abs(x), abs(y), abs(z), 5)

                    fig.update_layout(
                        scene=dict(
                            xaxis=dict(range=[-limit, limit]),
                            yaxis=dict(range=[-limit, limit]),
                            zaxis=dict(range=[-limit, limit])
                        )
                    )

                    fig.update_layout(title="3D Vector")

                    st.plotly_chart(fig, use_container_width=True)

                    mag = np.sqrt(x**2 + y**2 + z**2)
                    st.latex(rf"|\vec{{v}}| = \sqrt{{{x}^2 + {y}^2 + {z}^2}} = {mag:.2f}")

                # =========================
                # DOT PRODUCT
                # =========================
                elif mode == "Dot Product":

                    col1, col2 = st.columns(2)

                    with col1:
                        a1 = st.slider("A_x", -10, 10, 2)
                        a2 = st.slider("A_y", -10, 10, 3)

                    with col2:
                        b1 = st.slider("B_x", -10, 10, 4)
                        b2 = st.slider("B_y", -10, 10, 1)

                    dot = a1*b1 + a2*b2

                    st.latex(rf"\vec{{A}} \cdot \vec{{B}} = {dot}")

                    if dot == 0:
                        st.success("Vectors are perpendicular 🔥")

                # =========================
                # CROSS PRODUCT
                # =========================
                elif mode == "Cross Product":

                    col1, col2 = st.columns(2)

                    with col1:
                        a1 = st.slider("A_x", -5, 5, 1)
                        a2 = st.slider("A_y", -5, 5, 2)
                        a3 = st.slider("A_z", -5, 5, 3)

                    with col2:
                        b1 = st.slider("B_x", -5, 5, 2)
                        b2 = st.slider("B_y", -5, 5, 1)
                        b3 = st.slider("B_z", -5, 5, 0)

                    cross = np.cross([a1, a2, a3], [b1, b2, b3])

                    st.latex(rf"\vec{{A}} \times \vec{{B}} = ({cross[0]}, {cross[1]}, {cross[2]})")

                    mag = np.linalg.norm(cross)
                    st.success(f"Area of parallelogram = {mag:.2f}")

                elif mode == "Angle Between Vectors":

                    step = st.selectbox("Step size", [1.0, 0.1, 0.01], index=1)

                    col1, col2 = st.columns(2)

                    with col1:
                        a1 = st.number_input("A_x", value=3.0, step=step)
                        a2 = st.number_input("A_y", value=2.0, step=step)

                    with col2:
                        b1 = st.number_input("B_x", value=1.0, step=step)
                        b2 = st.number_input("B_y", value=4.0, step=step)

                    A = np.array([a1, a2])
                    B = np.array([b1, b2])

                    dot = np.dot(A, B)
                    magA = np.linalg.norm(A)
                    magB = np.linalg.norm(B)

                    if magA == 0 or magB == 0:
                        st.error("Vector magnitude cannot be zero")
                        st.stop()

                    theta = np.arccos(dot / (magA * magB))
                    theta_deg = np.degrees(theta)

                    st.latex(rf"\cos\theta = \frac{{{dot}}}{{{magA:.2f} \times {magB:.2f}}}")
                    st.success(f"Angle ≈ {theta_deg:.2f}°")

                    # Plot
                    fig = go.Figure()

                    fig.add_trace(go.Scatter(x=[0, a1], y=[0, a2], mode='lines+markers', name='A'))
                    fig.add_trace(go.Scatter(x=[0, b1], y=[0, b2], mode='lines+markers', name='B'))

                    limit = max(abs(a1), abs(a2), abs(b1), abs(b2), 5) * 1.2

                    fig.update_layout(
                        xaxis=dict(range=[-limit, limit]),
                        yaxis=dict(range=[-limit, limit]),
                        title="Vector Graph"

                    )

                    st.plotly_chart(fig, use_container_width=True)

                elif mode == "Vector Projection":

                    step = st.selectbox("Step size", [1.0, 0.1, 0.01], index=1)

                    col1, col2 = st.columns(2)

                    with col1:
                        a1 = st.number_input("A_x", value=3.0, step=step)
                        a2 = st.number_input("A_y", value=2.0, step=step)

                    with col2:
                        b1 = st.number_input("B_x", value=1.0, step=step)
                        b2 = st.number_input("B_y", value=4.0, step=step)

                    A = np.array([a1, a2])
                    B = np.array([b1, b2])

                    dot = np.dot(A, B)
                    magB_sq = np.dot(B, B)

                    if magB_sq == 0:
                        st.error("Vector B cannot be zero")
                        st.stop()

                    proj = (dot / magB_sq) * B

                    st.latex(r"\text{proj}_B A = \frac{A \cdot B}{|B|^2} B")
                    st.latex(rf"\text{{Projection}} = ({proj[0]:.2f}, {proj[1]:.2f})")

                    # Plot
                    fig = go.Figure()

                    fig.add_trace(go.Scatter(x=[0, a1], y=[0, a2], mode='lines+markers', name='A'))
                    fig.add_trace(go.Scatter(x=[0, b1], y=[0, b2], mode='lines+markers', name='B'))

                    # Projection vector
                    fig.add_trace(go.Scatter(
                        x=[0, proj[0]],
                        y=[0, proj[1]],
                        mode='lines+markers',
                        name='Projection',
                        line=dict(dash='dash')
                    ))

                    st.plotly_chart(fig, use_container_width=True)

                elif mode == "3D Line":

                    st.markdown("### 📐 Line: r = a + λd")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        x0 = st.slider("Point x", -5, 5, 0)
                        y0 = st.slider("Point y", -5, 5, 0)
                        z0 = st.slider("Point z", -5, 5, 0)

                    with col2:
                        dx = st.slider("Direction x", -5, 5, 1)
                        dy = st.slider("Direction y", -5, 5, 2)
                        dz = st.slider("Direction z", -5, 5, 1)

                    t = np.linspace(-5, 5, 100)

                    x = x0 + dx * t
                    y = y0 + dy * t
                    z = z0 + dz * t

                    fig = go.Figure()

                    fig.add_trace(go.Scatter3d(
                        x=x, y=y, z=z,
                        mode='lines',
                        name='Line'
                    ))

                    # Point
                    fig.add_trace(go.Scatter3d(
                        x=[x0], y=[y0], z=[z0],
                        mode='markers+text',
                        text=["Point"],
                        textposition="top center"
                    ))

                    fig.update_layout(title="3D Line")

                    st.plotly_chart(fig, use_container_width=True)

                    st.latex(rf"\vec{{r}} = ({x0},{y0},{z0}) + \lambda({dx},{dy},{dz})")

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
