import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go


# ============================================================
# PROJECT 2569 | GROUP 4
# Math Function Explorer
#
# Exponential:
# y = b(a^(c(x+h))) + k
#
# Linear:
# y = mx + c
# ============================================================


# ============================================================
# 1. PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Math Function Explorer | Project 2569",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. CSS DESIGN
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #f7f9fc;
}

/* ---------- Sidebar ---------- */

section[data-testid="stSidebar"] {
    background-color: #172b4d;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

.sidebar-title {
    font-size: 1.35rem;
    font-weight: 800;
    color: white;
}

.sidebar-subtitle {
    color: #cbd5e1 !important;
    font-size: 0.85rem;
}


/* ---------- Main Header ---------- */

.main-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: #173b7a;
    margin-bottom: 0;
}

.main-subtitle {
    color: #64748b;
    margin-top: 4px;
    margin-bottom: 20px;
}


/* ---------- Cards ---------- */

.card {
    background-color: white;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 18px;
    box-shadow: 0px 2px 8px rgba(15, 23, 42, 0.04);
}

.card-title {
    color: #174ea6;
    font-size: 1.15rem;
    font-weight: 750;
    margin-bottom: 12px;
}


/* ---------- Result ---------- */

.result-box {
    background-color: #eef6ff;
    border: 1px solid #b9d7ff;
    border-radius: 12px;
    padding: 18px;
    text-align: center;
}

.result-label {
    color: #64748b;
    font-size: 0.9rem;
}

.result-value {
    color: #174ea6;
    font-size: 1.8rem;
    font-weight: 800;
}


/* ---------- Step ---------- */

.step-card {
    background-color: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 15px;
    min-height: 150px;
}

.step-title {
    color: #174ea6;
    font-weight: 700;
    margin-bottom: 10px;
}


/* ---------- Summary ---------- */

.summary-box {
    background-color: #f8fafc;
    border-left: 5px solid #3b82f6;
    padding: 15px;
    border-radius: 8px;
    color: #334155;
}


/* ---------- Footer ---------- */

.footer {
    text-align: center;
    color: #94a3b8;
    padding: 25px;
    font-size: 0.85rem;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# 3. SIDEBAR
# ============================================================

st.sidebar.markdown(
    """
    <div>
        <div class="sidebar-title">
            📈 Math Function Explorer
        </div>

        <div class="sidebar-subtitle">
            Exponential & Linear Functions
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.divider()

st.sidebar.markdown("### เมนู")

page = st.sidebar.radio(
    "เลือกหน้า",
    [
        "หน้าหลัก",
        "ทฤษฎีและสูตร",
        "ตัวจำลอง",
        "กราฟ",
        "Step-by-Step",
        "สรุปผล"
    ],
    label_visibility="collapsed"
)

st.sidebar.divider()

st.sidebar.markdown("### เลือกประเภทฟังก์ชัน")

function_type = st.sidebar.selectbox(
    "Function",
    [
        "Exponential Function",
        "Linear Function"
    ]
)


# ============================================================
# 4. INPUT PARAMETERS
# ============================================================

st.sidebar.markdown("### ปรับค่าพารามิเตอร์")


# ---------- Exponential ----------

if function_type == "Exponential Function":

    a = st.sidebar.number_input(
        "a — ฐานของ Exponential",
        min_value=0.01,
        value=2.0,
        step=0.1
    )

    b = st.sidebar.number_input(
        "b — ตัวคูณ",
        value=1.5,
        step=0.1
    )

    c_exp = st.sidebar.number_input(
        "c — อัตราการเปลี่ยนแปลง",
        value=0.7,
        step=0.1
    )

    h = st.sidebar.number_input(
        "h — การเลื่อนแนวนอน",
        value=1.0,
        step=0.5
    )

    k = st.sidebar.number_input(
        "k — การเลื่อนแนวตั้ง",
        value=0.0,
        step=0.5
    )


# ---------- Linear ----------

else:

    m = st.sidebar.number_input(
        "m — ความชัน",
        value=2.0,
        step=0.5
    )

    intercept = st.sidebar.number_input(
        "c — จุดตัดแกน y",
        value=1.0,
        step=0.5
    )


# ============================================================
# 5. X RANGE
# ============================================================

x_min, x_max = st.sidebar.slider(
    "ช่วงของ x",
    min_value=-10,
    max_value=20,
    value=(-5, 5)
)

st.sidebar.info(
    "💡 เปลี่ยนค่าพารามิเตอร์เพื่อดูการเปลี่ยนแปลงของกราฟแบบ Real-time"
)


# ============================================================
# 6. FUNCTION CALCULATION
# ============================================================

x = np.linspace(x_min, x_max, 600)


if function_type == "Exponential Function":

    # y = b(a^(c(x+h))) + k
    y = b * (a ** (c_exp * (x + h))) + k

    equation_latex = (
        rf"y={b:g}\left({a:g}^{{{c_exp:g}(x+{h:g})}}\right)+{k:g}"
    )

    def calculate(x_value):

        exponent = c_exp * (x_value + h)

        power = a ** exponent

        result = b * power + k

        return exponent, power, result


    if a > 1 and c_exp > 0:
        behavior = "เพิ่ม (Growth)"

    elif 0 < a < 1 and c_exp > 0:
        behavior = "ลด (Decay)"

    elif c_exp < 0:
        behavior = "ลด (Decay)"

    else:
        behavior = "ขึ้นอยู่กับค่าพารามิเตอร์"


# ---------- Linear ----------

else:

    # y = mx + c
    y = m * x + intercept

    equation_latex = rf"y={m:g}x+({intercept:g})"

    def calculate(x_value):

        result = m * x_value + intercept

        return None, None, result


    if m > 0:
        behavior = "เพิ่มขึ้น"

    elif m < 0:
        behavior = "ลดลง"

    else:
        behavior = "เส้นแนวนอน"


# ============================================================
# 7. MAIN HEADER
# ============================================================

st.markdown(
    '<div class="main-title">Math Function Explorer</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="main-subtitle">
        เรียนรู้และสำรวจการเปลี่ยนแปลงของฟังก์ชัน
        ด้วยเครื่องมือ Interactive พร้อมการคำนวณแบบ Step-by-Step
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("**Project 2569 | กลุ่ม 4**")


# ============================================================
# 8. HOME
# ============================================================

if page == "หน้าหลัก":

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="card-title">📌 ฟังก์ชันที่กำลังศึกษา</div>',
        unsafe_allow_html=True
    )

    if function_type == "Exponential Function":

        st.latex(
            r"y=b\left(a^{c(x+h)}\right)+k"
        )

        st.write(
            """
            ฟังก์ชัน Exponential ใช้ศึกษาแนวโน้ม
            การเพิ่มหรือการลดของปริมาณ
            รวมถึงผลของการเปลี่ยนค่าพารามิเตอร์
            ที่มีต่อรูปร่างและตำแหน่งของกราฟ
            """
        )

    else:

        st.latex(
            r"y=mx+c"
        )

        st.write(
            """
            สมการเส้นตรงใช้ศึกษาเรื่องความชัน
            จุดตัดแกน y และความสัมพันธ์ระหว่าง
            ตัวแปร x และ y
            """
        )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


    # ---------- Metrics ----------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "ประเภทฟังก์ชัน",
            function_type
        )

    with col2:

        st.metric(
            "ลักษณะกราฟ",
            behavior
        )

    with col3:

        if function_type == "Exponential Function":

            st.metric(
                "Horizontal Asymptote",
                f"y = {k:g}"
            )

        else:

            st.metric(
                "Slope",
                f"{m:g}"
            )


    # ---------- Graph ----------

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="card-title">📊 ตัวอย่างกราฟ</div>',
        unsafe_allow_html=True
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            name="f(x)"
        )
    )

    fig.add_hline(
        y=0,
        line_width=1
    )

    fig.add_vline(
        x=0,
        line_width=1
    )

    fig.update_layout(
        height=470,
        template="plotly_white",
        xaxis_title="x",
        yaxis_title="y",
        margin=dict(
            l=30,
            r=20,
            t=20,
            b=30
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# 9. THEORY
# ============================================================

elif page == "ทฤษฎีและสูตร":

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="card-title">📖 ทฤษฎีและสูตร</div>',
        unsafe_allow_html=True
    )

    if function_type == "Exponential Function":

        st.latex(
            r"y=b\left(a^{c(x+h)}\right)+k"
        )

        theory = pd.DataFrame(
            {
                "ตัวแปร": [
                    "a",
                    "b",
                    "c",
                    "h",
                    "k"
                ],

                "ความหมาย": [
                    "ฐานของ Exponential",
                    "ตัวคูณ",
                    "อัตราการเพิ่มหรือลด",
                    "การเลื่อนกราฟแนวนอน",
                    "การเลื่อนกราฟแนวตั้ง"
                ],

                "ผลต่อกราฟ": [
                    "กำหนด Growth / Decay",
                    "เปลี่ยนขนาดในแนวตั้ง",
                    "ควบคุมความเร็วในการเปลี่ยนแปลง",
                    "เลื่อนกราฟซ้ายหรือขวา",
                    "เลื่อนกราฟขึ้นหรือลง"
                ]
            }
        )

    else:

        st.latex(
            r"y=mx+c"
        )

        theory = pd.DataFrame(
            {
                "ตัวแปร": [
                    "m",
                    "c"
                ],

                "ความหมาย": [
                    "ความชันของเส้นตรง",
                    "จุดตัดแกน y"
                ],

                "ผลต่อกราฟ": [
                    "กำหนดทิศทางของกราฟ",
                    "เลื่อนกราฟขึ้นหรือลง"
                ]
            }
        )


    st.dataframe(
        theory,
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# 10. SIMULATOR
# ============================================================

elif page == "ตัวจำลอง":

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="card-title">🧮 Interactive Simulator</div>',
        unsafe_allow_html=True
    )

    st.write("สมการปัจจุบัน")

    st.latex(
        equation_latex
    )

    st.divider()

    x_value = st.number_input(
        "กำหนดค่า x",
        value=2.0,
        step=0.5
    )

    _, _, result = calculate(x_value)

    st.markdown(
        f"""
        <div class="result-box">

            <div class="result-label">
                ค่าฟังก์ชันเมื่อ x = {x_value:g}
            </div>

            <div class="result-value">
                y = {result:.6f}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# 11. GRAPH
# ============================================================

elif page == "กราฟ":

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="card-title">📈 Dynamic Graph</div>',
        unsafe_allow_html=True
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            name="f(x)",
            hovertemplate=
            "x = %{x:.3f}<br>"
            "y = %{y:.3f}"
            "<extra></extra>"
        )
    )

    fig.add_hline(
        y=0,
        line_width=1
    )

    fig.add_vline(
        x=0,
        line_width=1
    )


    # Horizontal asymptote
    if function_type == "Exponential Function":

        fig.add_hline(
            y=k,
            line_dash="dash",
            annotation_text=f"y = {k:g}"
        )


    fig.update_layout(
        height=600,
        template="plotly_white",
        title="กราฟฟังก์ชัน",
        xaxis_title="x",
        yaxis_title="y",
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # ---------- Data Table ----------

    st.markdown(
        '<div class="card-title">📋 ตารางค่าฟังก์ชัน</div>',
        unsafe_allow_html=True
    )

    sample_x = np.arange(
        max(x_min, -5),
        min(x_max, 5) + 1,
        1
    )

    rows = []

    for xv in sample_x:

        _, _, yv = calculate(
            float(xv)
        )

        rows.append(
            {
                "x": xv,
                "y": yv
            }
        )

    table = pd.DataFrame(rows)

    table["y"] = table["y"].round(4)

    st.dataframe(
        table,
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# 12. STEP-BY-STEP
# ============================================================

elif page == "Step-by-Step":

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="card-title">📝 Step-by-Step Calculation</div>',
        unsafe_allow_html=True
    )

    x_value = st.number_input(
        "เลือกค่า x ที่ต้องการคำนวณ",
        value=2.0,
        step=0.5,
        key="step_x"
    )


    # ========================================================
    # EXPONENTIAL STEP
    # ========================================================

    if function_type == "Exponential Function":

        exponent, power, result = calculate(
            x_value
        )

        cols = st.columns(4)


        # ---------- STEP 1 ----------

        with cols[0]:

            st.markdown(
                '<div class="step-card">',
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div class="step-title">
                    ① กำหนดค่าพารามิเตอร์
                </div>
                """,
                unsafe_allow_html=True
            )

            st.latex(
                rf"a={a:g},\quad b={b:g}"
            )

            st.latex(
                rf"c={c_exp:g},\quad h={h:g}"
            )

            st.latex(
                rf"k={k:g}"
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


        # ---------- STEP 2 ----------

        with cols[1]:

            st.markdown(
                '<div class="step-card">',
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div class="step-title">
                    ② แทนค่าในสมการ
                </div>
                """,
                unsafe_allow_html=True
            )

            st.latex(
                rf"""
                y={b:g}
                \left(
                {a:g}^
                {{{c_exp:g}({x_value:g}+{h:g})}}
                \right)
                +{k:g}
                """
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


        # ---------- STEP 3 ----------

        with cols[2]:

            st.markdown(
                '<div class="step-card">',
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div class="step-title">
                    ③ คำนวณ
                </div>
                """,
                unsafe_allow_html=True
            )

            st.latex(
                rf"""
                {c_exp:g}
                ({x_value:g}+{h:g})
                ={exponent:g}
                """
            )

            st.latex(
                rf"""
                {a:g}^{{{exponent:g}}}
                ={power:.6f}
                """
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


        # ---------- STEP 4 ----------

        with cols[3]:

            st.markdown(
                '<div class="step-card">',
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div class="step-title">
                    ④ ผลลัพธ์
                </div>
                """,
                unsafe_allow_html=True
            )

            st.latex(
                rf"""
                y={b:g}({power:.6f})+{k:g}
                """
            )

            st.latex(
                rf"""
                \boxed{{y={result:.6f}}}
                """
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


    # ========================================================
    # LINEAR STEP
    # ========================================================

    else:

        result = (
            m * x_value
            + intercept
        )

        cols = st.columns(4)


        # ---------- STEP 1 ----------

        with cols[0]:

            st.markdown(
                '<div class="step-card">',
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div class="step-title">
                    ① กำหนดสมการ
                </div>
                """,
                unsafe_allow_html=True
            )

            st.latex(
                r"y=mx+c"
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


        # ---------- STEP 2 ----------

        with cols[1]:

            st.markdown(
                '<div class="step-card">',
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div class="step-title">
                    ② แทนค่า
                </div>
                """,
                unsafe_allow_html=True
            )

            st.latex(
                rf"""
                y=({m:g})
                ({x_value:g})
                +({intercept:g})
                """
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


        # ---------- STEP 3 ----------

        with cols[2]:

            st.markdown(
                '<div class="step-card">',
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div class="step-title">
                    ③ คำนวณ
                </div>
                """,
                unsafe_allow_html=True
            )

            st.latex(
                rf"""
                y={m*x_value:g}
                +({intercept:g})
                """
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


        # ---------- STEP 4 ----------

        with cols[3]:

            st.markdown(
                '<div class="step-card">',
                unsafe_allow_html=True
            )

            st.markdown(
                """
                <div class="step-title">
                    ④ ผลลัพธ์
                </div>
                """,
                unsafe_allow_html=True
            )

            st.latex(
                rf"""
                \boxed{{y={result:g}}}
                """
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# 13. SUMMARY
# ============================================================

elif page == "สรุปผล":

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="card-title">📌 สรุปผลการทดลอง</div>',
        unsafe_allow_html=True
    )


    if function_type == "Exponential Function":

        if a > 1 and c_exp > 0:

            sentence = (
                "กราฟมีแนวโน้มเพิ่มขึ้น (Growth) "
                "เนื่องจากฐาน a มากกว่า 1 "
                "และ c เป็นบวก"
            )

        elif 0 < a < 1 and c_exp > 0:

            sentence = (
                "กราฟมีแนวโน้มลดลง (Decay) "
                "เนื่องจากฐาน a อยู่ระหว่าง 0 และ 1"
            )

        else:

            sentence = (
                "ลักษณะของกราฟขึ้นอยู่กับ "
                "ความสัมพันธ์ระหว่าง a และ c"
            )


        st.markdown(
            f"""
            <div class="summary-box">
                {sentence}
            </div>
            """,
            unsafe_allow_html=True
        )


        st.write("")

        st.markdown(
            "### ผลของพารามิเตอร์"
        )

        st.write(
            f"• **a = {a:g}** → กำหนดลักษณะ Growth / Decay"
        )

        st.write(
            f"• **b = {b:g}** → ควบคุมขนาดในแนวตั้ง"
        )

        st.write(
            f"• **c = {c_exp:g}** → ควบคุมอัตราการเพิ่มหรือลด"
        )

        st.write(
            f"• **h = {h:g}** → เลื่อนกราฟในแนวนอน"
        )

        st.write(
            f"• **k = {k:g}** → เลื่อนกราฟในแนวตั้ง"
        )


    else:

        if m > 0:

            sentence = (
                "กราฟเพิ่มขึ้นเมื่อ x เพิ่มขึ้น "
                "เนื่องจากความชัน m เป็นบวก"
            )

        elif m < 0:

            sentence = (
                "กราฟลดลงเมื่อ x เพิ่มขึ้น "
                "เนื่องจากความชัน m เป็นลบ"
            )

        else:

            sentence = (
                "กราฟเป็นเส้นแนวนอน "
                "เนื่องจากความชัน m เท่ากับศูนย์"
            )


        st.markdown(
            f"""
            <div class="summary-box">
                {sentence}
            </div>
            """,
            unsafe_allow_html=True
        )


        st.write("")

        st.markdown(
            "### ผลของพารามิเตอร์"
        )

        st.write(
            f"• **m = {m:g}** → ความชันของเส้นตรง"
        )

        st.write(
            f"• **c = {intercept:g}** → จุดตัดแกน y"
        )


    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# ============================================================
# 14. FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        Project 2569 • Group 4 • Math Function Explorer
    </div>
    """,
    unsafe_allow_html=True
)
