import streamlit as st
from openai import OpenAI
import os
import matplotlib.pyplot as plt
import base64
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp
import streamlit.components.v1 as components

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

    difficulty = st.selectbox(
        "Select Difficulty Level:",
        ["Beginner", "Intermediate", "Advanced"]
    )

    # -----------------------
    # Input
    # -----------------------
    st.markdown('<div class="animated-section"><h3>📝 Enter Your Problem</h3></div>', unsafe_allow_html=True)

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
                {
                    "type":"input_text",
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

    Rules:
    • Outline the steps clearly
    • Do NOT perform calculations
    • Do NOT substitute numbers
    • Do NOT give final answer
    • Max 3–4 short steps

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

            response = client.responses.create(
        model="gpt-4.1",
        input=f"""
    Solve using the correct method.

    RULES:
    - Use LaTeX (wrap equations in $$)
    - No code formatting
    - Max 5 steps only
    - Be concise

    If Newton-Raphson:
    - Show formula
    - Show 3 iterations
    - Give final answer

    Problem:
    {user_input}
    """,
        max_output_tokens=1000
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
        # (input, hints, graph, difficulty, etc.)

    # =========================
    # 📖 NOTES TAB
    # =========================
    with tab_notes:

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

            # TEMP CONTENT (you replace later)
            st.info("Notes will appear here")

        # =========================
        # SEMESTER 2
        # =========================
        # =========================
# SEMESTER 2
# =========================
        with sem2_tab:

            chapter = st.selectbox(
                "Choose Chapter",
                [
                    "Chapter 1: Numerical Solution",
                    "Chapter 2: Integration",
                    "Chapter 3: First Order Differential Equation",
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

    # =========================
    # 📊 VISUAL TAB
    # =========================
    with tab_visual:
        st.write("Graphs / visual tools here")

    # =========================
    # 🏆 PROGRESS TAB
    # =========================
    with tab_progress:
        st.write("Score, analytics here")
