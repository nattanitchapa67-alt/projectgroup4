# ============================================================
# Project 4: Math Function Explorer
# แอปช่วยเรียนรู้ฟังก์ชัน Exponential และ Linear
# กลุ่ม 4 | Project 2569
# ============================================================

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st


# ============================================================
# 1. ตั้งค่าหน้าเว็บ
# ============================================================

st.set_page_config(
    page_title="Math Function Explorer",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ============================================================
# 2. สีหลัก
# ============================================================

NAVY = "#1B2A6B"
BLUE = "#2563EB"
LIGHT_BLUE = "#EAF0FC"
BORDER = "#D5E0F7"
ORANGE = "#F59E0B"
GREEN = "#10B981"
RED = "#EF4444"


# ============================================================
# 3. CSS ตกแต่งเว็บไซต์
# ============================================================

st.markdown(
    f"""
    <style>

    /* ---------- Global ---------- */

    @import url(
        'https://fonts.googleapis.com/css2?family=Prompt:wght@400;500;600;700&display=swap'
    );

    html, body, [class*="css"] {{
        font-family: 'Prompt', sans-serif;
    }}

    .stApp {{
        background: linear-gradient(
            180deg,
            #F4F7FD 0%,
            #E6EDFA 100%
        );
    }}


    /* ---------- Sidebar ---------- */

    section[data-testid="stSidebar"] {{
        background: linear-gradient(
            180deg,
            #2A4378 0%,
            #1E3160 100%
        );
    }}

    section[data-testid="stSidebar"] * {{
        color: white;
    }}

    section[data-testid="stSidebar"] .stSlider label {{
        color: white !important;
    }}

    section[data-testid="stSidebar"] .stNumberInput label {{
        color: white !important;
    }}

    section[data-testid="stSidebar"] .stSelectbox label {{
        color: white !important;
    }}


    /* ---------- Header ---------- */

    .header {{
        background: white;
        border-radius: 16px;
        padding: 20px 26px;
        margin-bottom: 18px;

        display: flex;
        justify-content: space-between;
        align-items: center;

        border: 1px solid {BORDER};
        box-shadow: 0 4px 15px rgba(27, 42, 107, 0.06);
    }}

    .header-title {{
        color: {NAVY};
        font-family: Georgia, serif;
        font-size: 30px;
        font-weight: 700;
        margin-bottom: 3px;
    }}

    .header-subtitle {{
        color: #52638F;
        font-size: 14px;
    }}

    .project-badge {{
        color: {NAVY};
        font-size: 14px;
        font-weight: 600;
        border-bottom: 3px solid {BLUE};
        padding-bottom: 5px;
    }}


    /* ---------- Section title ---------- */

    .section-title {{
        color: {NAVY};
        font-size: 19px;
        font-weight: 600;
        margin-bottom: 8px;
    }}


    /* ---------- Cards ---------- */

    .info-card {{
        background: #FFFFFF;
        border: 1px solid {BORDER};
        border-radius: 14px;
        padding: 18px;
        margin-bottom: 12px;
        box-shadow: 0 3px 12px rgba(27, 42, 107, 0.04);
    }}

    .blue-card {{
        background: {LIGHT_BLUE};
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 16px;
    }}

    .success-card {{
        background: #ECFDF5;
        border: 1px solid #A7F3D0;
        border-radius: 12px;
        padding: 15px;
    }}

    .formula-card {{
        background: #F8FAFF;
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }}


    /* ---------- Tabs ---------- */

    .stTabs [data-baseweb="tab-list"] {{
        gap: 8px;
    }}

    .stTabs [data-baseweb="tab"] {{
        background: #EEF3FC;
        border-radius: 10px 10px 0 0;
        padding: 12px 24px;
        color: {NAVY};
        font-weight: 600;
    }}

    .stTabs [aria-selected="true"] {{
        background: {BLUE} !important;
        color: white !important;
    }}


    /* ---------- Metric ---------- */

    div[data-testid="stMetric"] {{
        background: white;
        border: 1px solid {BORDER};
        border-radius: 12px;
        padding: 10px;
    }}


    /* ---------- Divider ---------- */

    hr {{
        border-color: {BORDER};
    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 4. Header
# ============================================================

st.markdown(
    """
    <div class="header">

        <div>
            <div class="header-title">
                📐 Math Function Explorer
            </div>

            <div class="header-subtitle">
                Exponential & Linear Functions ·
                เรียนรู้ฟังก์ชันด้วยเครื่องมือ Interactive
                พร้อมการคำนวณแบบ Step-by-Step
            </div>
        </div>

        <div class="project-badge">
            Project 2569 &nbsp;|&nbsp; กลุ่ม 4
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# 5. ฟังก์ชันช่วย
# ============================================================

def section_title(text):
    st.markdown(
        f'<div class="section-title">{text}</div>',
        unsafe_allow_html=True
    )


def create_table(function, step):
    """
    สร้างตารางค่า x และ y
    """

    x_values = np.arange(
        -5,
        5 + 0.0001,
        step
    )

    y_values = function(x_values)

    return pd.DataFrame(
        {
            "x": np.round(x_values, 3),
            "y": np.round(y_values, 3)
        }
    )


def create_function_graph(function, label, asymptote=None):
    """
    สร้างกราฟ Interactive
    """

    x = np.linspace(-5, 5, 500)
    y = function(x)

    fig = go.Figure()

    # เส้นกราฟ
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            name=label,
            line=dict(
                color=BLUE,
                width=4
            )
        )
    )

    # จุดตัวอย่าง
    xi = np.arange(-5, 6, 1)

    fig.add_trace(
        go.Scatter(
            x=xi,
            y=function(xi),
            mode="markers",
            name="จุดตัวอย่าง",
            marker=dict(
                color=BLUE,
                size=7
            )
        )
    )

    # เส้นกำกับแนวนอน
    if asymptote is not None:

        fig.add_hline(
            y=asymptote,
            line_dash="dash",
            line_color=ORANGE,
            annotation_text=f"y = {asymptote:g}"
        )

    fig.update_layout(
        template="plotly_white",
        height=390,
        margin=dict(
            l=20,
            r=20,
            t=25,
            b=20
        ),
        xaxis_title="x",
        yaxis_title="y",
        hovermode="x unified",
        legend=dict(
            x=0.02,
            y=0.98
        )
    )

    return fig


# ============================================================
# 6. รูปประกอบ Exponential Growth / Decay
# ============================================================

def exponential_illustration():

    x = np.linspace(-3, 3, 200)

    growth = 2 ** x
    decay = 2 ** (-x)

    fig = make_subplots(
        rows=1,
        cols=2,
        subplot_titles=(
            "Exponential Growth",
            "Exponential Decay"
        )
    )

    # Growth
    fig.add_trace(
        go.Scatter(
            x=x,
            y=growth,
            mode="lines",
            line=dict(
                color=BLUE,
                width=3
            ),
            showlegend=False
        ),
        row=1,
        col=1
    )

    # Decay
    fig.add_trace(
        go.Scatter(
            x=x,
            y=decay,
            mode="lines",
            line=dict(
                color=GREEN,
                width=3
            ),
            showlegend=False
        ),
        row=1,
        col=2
    )

    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color=ORANGE,
        row=1,
        col=1
    )

    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color=ORANGE,
        row=1,
        col=2
    )

    fig.update_layout(
        template="plotly_white",
        height=300,
        margin=dict(
            l=10,
            r=10,
            t=50,
            b=10
        )
    )

    fig.update_xaxes(title_text="x")
    fig.update_yaxes(title_text="y")

    return fig


# ============================================================
# 7. รูปประกอบ Linear Function
# ============================================================

def linear_illustration():

    x = np.linspace(-5, 5, 100)

    fig = go.Figure()

    # m > 0
    fig.add_trace(
        go.Scatter(
            x=x,
            y=1.5 * x,
            mode="lines",
            name="m > 0",
            line=dict(
                color=BLUE,
                width=3
            )
        )
    )

    # m < 0
    fig.add_trace(
        go.Scatter(
            x=x,
            y=-1.5 * x,
            mode="lines",
            name="m < 0",
            line=dict(
                color=RED,
                width=3
            )
        )
    )

    fig.update_layout(
        template="plotly_white",
        height=300,
        margin=dict(
            l=10,
            r=10,
            t=20,
            b=10
        ),
        xaxis_title="x",
        yaxis_title="y"
    )

    return fig


# ============================================================
# 8. Sidebar
# ============================================================

sb = st.sidebar

st.sidebar.markdown(
    """
    <h2 style="color:white;">
        📚 Math Explorer
    </h2>
    """,
    unsafe_allow_html=True
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    "### 🧭 เมนู"
)

menu = st.sidebar.radio(
    "เลือกหัวข้อ",
    [
        "🏠 Home",
        "📐 ทฤษฎีและสูตร",
        "🧪 ตัวจำลอง (Interactive)",
        "📈 กราฟ",
        "🧮 Step-by-Step Calculation",
        "📝 สรุปผล"
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")


# ============================================================
# 9. Exponential Parameters
# ============================================================

st.sidebar.markdown(
    "### 📈 ปรับค่าพารามิเตอร์ Exponential"
)

a = st.sidebar.slider(
    "a (ฐานของเอ็กซ์โพเนนเชียล)",
    min_value=0.1,
    max_value=5.0,
    value=2.0,
    step=0.1
)

b = st.sidebar.slider(
    "b (ตัวคูณ)",
    min_value=-10.0,
    max_value=10.0,
    value=1.5,
    step=0.5
)

c = st.sidebar.slider(
    "c (อัตราการเปลี่ยนแปลง)",
    min_value=-2.0,
    max_value=2.0,
    value=0.7,
    step=0.1
)

h = st.sidebar.slider(
    "h (การเลื่อนแนวนอน)",
    min_value=-5.0,
    max_value=5.0,
    value=1.0,
    step=0.5
)

k = st.sidebar.slider(
    "k (การเลื่อนแนวตั้ง)",
    min_value=-10.0,
    max_value=10.0,
    value=0.0,
    step=0.5
)


# ============================================================
# 10. Linear Parameters
# ============================================================

st.sidebar.markdown(
    "### 📉 ปรับค่าพารามิเตอร์ Linear"
)

m = st.sidebar.slider(
    "m (ความชัน)",
    min_value=-10.0,
    max_value=10.0,
    value=2.0,
    step=0.5
)

ci = st.sidebar.slider(
    "c (จุดตัดแกน y)",
    min_value=-10.0,
    max_value=10.0,
    value=1.0,
    step=0.5
)


# ============================================================
# 11. Calculation Parameters
# ============================================================

st.sidebar.markdown(
    "### 🧮 ค่าที่ต้องการคำนวณ"
)

x0 = st.sidebar.number_input(
    "ค่า x ที่ต้องการแทน",
    value=2.0,
    step=0.5
)

step = st.sidebar.selectbox(
    "ระยะห่างของ x ในตาราง",
    [1.0, 0.5, 2.0],
    index=0
)

st.sidebar.info(
    "💡 ปรับค่าพารามิเตอร์เพื่อดูการเปลี่ยนแปลงของกราฟแบบ Real-time"
)


# ============================================================
# 12. ตรวจสอบ Exponential
# ============================================================

exp_valid = (
    a > 0
    and a != 1
    and b != 0
    and c != 0
)


# ============================================================
# 13. ฟังก์ชัน Exponential
# ============================================================

if exp_valid:

    def exp_function(x):
        return b * (a ** (c * (x + h))) + k

    growth_indicator = b * c * np.log(a)

    is_growth = growth_indicator > 0

else:

    def exp_function(x):
        return np.zeros_like(np.asarray(x, dtype=float))

    growth_indicator = 0
    is_growth = False


# ============================================================
# 14. ฟังก์ชัน Linear
# ============================================================

def linear_function(x):

    return m * x + ci


# ============================================================
# 15. Main Tabs
# ============================================================

tab_exp, tab_lin = st.tabs(
    [
        "📈 Exponential Function",
        "📉 Linear Function"
    ]
)


# ============================================================
# 16. EXPONENTIAL FUNCTION
# ============================================================

with tab_exp:

    if not exp_valid:

        st.error(
            "⚠️ ต้องกำหนด a > 0, a ≠ 1, b ≠ 0 และ c ≠ 0 "
            "จึงจะเป็นฟังก์ชันเอ็กซ์โพเนนเชียล"
        )

    else:

        # ----------------------------------------------------
        # Formula + Explanation
        # ----------------------------------------------------

        left, right = st.columns(
            [2.2, 1]
        )

        with left:

            st.markdown(
                '<div class="info-card">',
                unsafe_allow_html=True
            )

            section_title(
                "📈 ฟังก์ชันเอ็กซ์โพเนนเชียล "
                "(Exponential Function)"
            )

            formula_col, meaning_col = st.columns(
                [1.1, 1]
            )

            with formula_col:

                st.markdown(
                    '<div class="formula-card">',
                    unsafe_allow_html=True
                )

                st.latex(
                    r"\Large y=b\left(a^{c(x+h)}\right)+k"
                )

                st.markdown(
                    "**รูปแบบทั่วไปของฟังก์ชัน**"
                )

                st.markdown(
                    "</div>",
                    unsafe_allow_html=True
                )

            with meaning_col:

                st.markdown(
                    """
                    **ความหมายของพารามิเตอร์**

                    - **a** : ฐานของเอ็กซ์โพเนนเชียล
                    - **b** : ตัวคูณ (Scale Factor)
                    - **c** : อัตราการเปลี่ยนแปลง
                    - **h** : การเลื่อนแนวนอน
                    - **k** : การเลื่อนแนวตั้ง
                    """,
                    unsafe_allow_html=True
                )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


        with right:

            st.markdown(
                '<div class="info-card">',
                unsafe_allow_html=True
            )

            section_title("📋 ลักษณะกราฟ")

            if growth_indicator > 0:

                st.markdown(
                    """
                    - ถ้า \(b·c·\\ln(a) > 0\)
                      → กราฟเพิ่มขึ้น
                    - เรียกว่า **Growth 📈**
                    """
                )

                st.success(
                    "ตอนนี้: กราฟเพิ่มขึ้น 📈"
                )

            else:

                st.markdown(
                    """
                    - ถ้า \(b·c·\\ln(a) < 0\)
                      → กราฟลดลง
                    - เรียกว่า **Decay 📉**
                    """
                )

                st.warning(
                    "ตอนนี้: กราฟลดลง 📉"
                )

            st.markdown(
                f"""
                เส้นกำกับแนวนอนคือ

                **y = {k:g}**
                """
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


        # ----------------------------------------------------
        # Graph + Table
        # ----------------------------------------------------

        graph_col, table_col = st.columns(
            [2.1, 1]
        )

        with graph_col:

            st.markdown(
                '<div class="info-card">',
                unsafe_allow_html=True
            )

            section_title(
                "📈 กราฟของฟังก์ชัน"
            )

            fig = create_function_graph(
                exp_function,
                f"y = {b:g}({a:g}^({c:g}(x+{h:g}))) + {k:g}",
                k
            )

            st.plotly_chart(
                fig,
                use_container_width=True
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


        with table_col:

            st.markdown(
                '<div class="info-card">',
                unsafe_allow_html=True
            )

            section_title(
                "📋 ตารางค่าของฟังก์ชัน"
            )

            exp_table = create_table(
                exp_function,
                step
            )

            st.dataframe(
                exp_table,
                hide_index=True,
                use_container_width=True,
                height=390
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )


        # ----------------------------------------------------
        # รูปประกอบ
        # ----------------------------------------------------

        st.markdown(
            '<div class="info-card">',
            unsafe_allow_html=True
        )

        section_title(
            "🖼️ รูปประกอบความเข้าใจ"
        )

        st.plotly_chart(
            exponential_illustration(),
            use_container_width=True
        )

        st.caption(
            "ภาพประกอบแสดงแนวโน้มของ Exponential Growth และ Exponential Decay"
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # Step-by-Step
        # ----------------------------------------------------

        st.markdown(
            '<div class="info-card">',
            unsafe_allow_html=True
        )

        section_title(
            f"🧮 Step-by-Step Calculation "
            f"(เมื่อ x = {x0:g})"
        )

        s1, s2, s3, s4, s5 = st.columns(
            [1, 1.35, 1.1, 0.9, 1.35]
        )

        # Step 1
        with s1:

            st.markdown(
                "**1. กำหนดค่าพารามิเตอร์**"
            )

            st.code(
                f"""a = {a:g}
b = {b:g}
c = {c:g}
h = {h:g}
k = {k:g}"""
            )

        # Step 2
        exponent = c * (x0 + h)

        with s2:

            st.markdown(
                "**2. แทนค่าในสมการ**"
            )

            st.latex(
                rf"""
                y={b:g}
                \left(
                {a:g}^{{{c:g}({x0:g}+{h:g})}}
                \right)+{k:g}
                """
            )

            st.latex(
                rf"""
                ={b:g}({a:g}^{{{exponent:.4g}}})+{k:g}
                """
            )

        # Step 3
        exponential_value = a ** exponent
        final_value = exp_function(x0)

        with s3:

            st.markdown(
                "**3. คำนวณค่า**"
            )

            st.latex(
                rf"""
                {a:g}^{{{exponent:.4g}}}
                =
                {exponential_value:.4f}
                """
            )

            st.latex(
                rf"""
                y={b:g}({exponential_value:.4f})+{k:g}
                """
            )

        # Step 4
        with s4:

            st.markdown(
                "**4. ผลลัพธ์**"
            )

            st.metric(
                f"y เมื่อ x = {x0:g}",
                f"{final_value:.2f}"
            )

        # Step 5
        with s5:

            st.success(
                f"""
                **สรุปผลการทดลอง**

                เมื่อ x เพิ่มขึ้น
                ค่าของฟังก์ชันจะ
                **{'เพิ่มขึ้น' if is_growth else 'ลดลง'}**

                แบบเอ็กซ์โพเนนเชียล

                b·c·ln(a)
                = {growth_indicator:.3f}

                เส้นกำกับแนวนอน
                y = {k:g}

                การเลื่อนแนวนอน
                h = {h:g}
                """
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


# ============================================================
# 17. LINEAR FUNCTION
# ============================================================

with tab_lin:

    # --------------------------------------------------------
    # Formula + Explanation
    # --------------------------------------------------------

    left, right = st.columns(
        [2.2, 1]
    )

    with left:

        st.markdown(
            '<div class="info-card">',
            unsafe_allow_html=True
        )

        section_title(
            "📉 ฟังก์ชันเส้นตรง "
            "(Linear Function)"
        )

        formula_col, meaning_col = st.columns(
            [1.1, 1]
        )

        with formula_col:

            st.markdown(
                '<div class="formula-card">',
                unsafe_allow_html=True
            )

            st.latex(
                r"\Large y=mx+c"
            )

            st.markdown(
                "**สมการฟังก์ชันเส้นตรง**"
            )

            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

        with meaning_col:

            st.markdown(
                """
                **ความหมายของพารามิเตอร์**

                - **m** : ความชัน (Slope)
                - **c** : จุดตัดแกน y
                - จุดตัดแกน x คือ

                \[
                x=-\frac{c}{m}
                \]
                """
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    with right:

        st.markdown(
            '<div class="info-card">',
            unsafe_allow_html=True
        )

        section_title(
            "📋 ลักษณะกราฟ"
        )

        if m > 0:

            st.markdown(
                "- m > 0 → กราฟเพิ่มขึ้น 📈"
            )

            st.success(
                "ตอนนี้: กราฟเพิ่มขึ้น"
            )

        elif m < 0:

            st.markdown(
                "- m < 0 → กราฟลดลง 📉"
            )

            st.warning(
                "ตอนนี้: กราฟลดลง"
            )

        else:

            st.markdown(
                "- m = 0 → เส้นตรงแนวนอน"
            )

            st.info(
                "ตอนนี้: กราฟคงที่"
            )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # Graph + Table
    # --------------------------------------------------------

    graph_col, table_col = st.columns(
        [2.1, 1]
    )

    with graph_col:

        st.markdown(
            '<div class="info-card">',
            unsafe_allow_html=True
        )

        section_title(
            "📈 กราฟของฟังก์ชัน"
        )

        linear_fig = create_function_graph(
            linear_function,
            f"y = {m:g}x + {ci:g}"
        )

        st.plotly_chart(
            linear_fig,
            use_container_width=True
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    with table_col:

        st.markdown(
            '<div class="info-card">',
            unsafe_allow_html=True
        )

        section_title(
            "📋 ตารางค่าของฟังก์ชัน"
        )

        linear_table = create_table(
            linear_function,
            step
        )

        st.dataframe(
            linear_table,
            hide_index=True,
            use_container_width=True,
            height=390
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # Linear Illustration
    # --------------------------------------------------------

    st.markdown(
        '<div class="info-card">',
        unsafe_allow_html=True
    )

    section_title(
        "🖼️ รูปประกอบความเข้าใจเรื่องความชัน"
    )

    st.plotly_chart(
        linear_illustration(),
        use_container_width=True
    )

    st.caption(
        "เส้นสีน้ำเงินแสดง m > 0 และเส้นสีแดงแสดง m < 0"
    )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # Step-by-Step
    # --------------------------------------------------------

    st.markdown(
        '<div class="info-card">',
        unsafe_allow_html=True
    )

    section_title(
        f"🧮 Step-by-Step Calculation "
        f"(เมื่อ x = {x0:g})"
    )

    s1, s2, s3, s4, s5 = st.columns(
        [1, 1.35, 1.1, 0.9, 1.35]
    )

    # Step 1
    with s1:

        st.markdown(
            "**1. กำหนดค่าพารามิเตอร์**"
        )

        st.code(
            f"""m = {m:g}
c = {ci:g}"""
        )

    # Step 2
    with s2:

        st.markdown(
            "**2. แทนค่าในสมการ**"
        )

        st.latex(
            rf"""
            y={m:g}({x0:g})+({ci:g})
            """
        )

    # Step 3
    linear_value = linear_function(x0)

    with s3:

        st.markdown(
            "**3. คำนวณค่า**"
        )

        st.latex(
            rf"""
            y={m*x0:g}+({ci:g})
            """
        )

    # Step 4
    with s4:

        st.markdown(
            "**4. ผลลัพธ์**"
        )

        st.metric(
            f"y เมื่อ x = {x0:g}",
            f"{linear_value:.2f}"
        )

    # Step 5
    with s5:

        if m != 0:

            x_intercept = -ci / m

            x_intercept_text = (
                f"x = {x_intercept:.3f}"
            )

        else:

            x_intercept_text = "ไม่มีจุดตัดแกน x แบบจุดเดียว"


        st.success(
            f"""
            **สรุปผลการทดลอง**

            ความชัน
            m = {m:g}

            ฟังก์ชันนี้เป็น
            **{'ฟังก์ชันเพิ่ม' if m > 0 else ('ฟังก์ชันลด' if m < 0 else 'ฟังก์ชันคงที่')}**

            จุดตัดแกน y:
            (0, {ci:g})

            จุดตัดแกน x:
            {x_intercept_text}
            """
        )

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )


# ============================================================
# 18. สรุปผลการเรียนรู้
# ============================================================

st.markdown("---")

st.markdown(
    '<div class="info-card">',
    unsafe_allow_html=True
)

section_title(
    "📝 สรุปผลการเรียนรู้"
)

summary_col1, summary_col2 = st.columns(2)

with summary_col1:

    st.markdown(
        """
        ### 📈 Exponential Function

        รูปแบบ

        \[
        y=b(a^{c(x+h)})+k
        \]

        - **a** → ฐานของฟังก์ชัน
        - **b** → ตัวคูณ
        - **c** → อัตราการเปลี่ยนแปลง
        - **h** → การเลื่อนแนวนอน
        - **k** → การเลื่อนแนวตั้ง
        - มีเส้นกำกับแนวนอนที่ **y = k**
        """
    )

with summary_col2:

    st.markdown(
        """
        ### 📉 Linear Function

        รูปแบบ

        \[
        y=mx+c
        \]

        - **m** → ความชัน
        - **c** → จุดตัดแกน y
        - m > 0 → กราฟเพิ่มขึ้น
        - m < 0 → กราฟลดลง
        - m = 0 → เส้นตรงแนวนอน
        """
    )

st.markdown(
    "</div>",
    unsafe_allow_html=True
)


# ============================================================
# 19. Footer
# ============================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#667085;
        font-size:13px;
        padding:20px;
    ">
        Math Function Explorer · Project 2569 · กลุ่ม 4
        <br>
        Interactive Mathematics Learning Application
    </div>
    """,
    unsafe_allow_html=True
)
```
