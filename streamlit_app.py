import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# =========================================================
# Math Function Explorer
# Project 2569 | กลุ่ม 4
# Exponential & Linear Functions
# =========================================================

st.set_page_config(
    page_title="Math Function Explorer",
    page_icon="📐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ------------------------- CSS ----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"], .stApp {
    font-family: 'Prompt', sans-serif;
}

.stApp {
    background: #f5f7fb;
}

.block-container {
    max-width: 1400px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

.hero {
    background: linear-gradient(135deg, #172554 0%, #1d4ed8 100%);
    color: white;
    padding: 28px 32px;
    border-radius: 20px;
    margin-bottom: 22px;
    box-shadow: 0 10px 30px rgba(30, 64, 175, .18);
}

.hero h1 {
    margin: 0;
    font-size: 2.15rem;
    font-weight: 700;
}

.hero p {
    margin: 7px 0 0;
    opacity: .9;
    font-size: 1rem;
}

.badge {
    display: inline-block;
    background: rgba(255,255,255,.15);
    border: 1px solid rgba(255,255,255,.25);
    padding: 5px 11px;
    border-radius: 999px;
    font-size: .8rem;
    margin-top: 14px;
}

.section-title {
    color: #172554;
    font-size: 1.2rem;
    font-weight: 700;
    margin: 5px 0 12px;
}

.card {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 18px 20px;
    margin-bottom: 16px;
    box-shadow: 0 4px 14px rgba(15, 23, 42, .04);
}

.formula {
    background: #eff6ff;
    border-left: 5px solid #2563eb;
    padding: 16px 18px;
    border-radius: 10px;
    font-size: 1.15rem;
    margin: 8px 0 14px;
}

.info-box {
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 13px 16px;
    margin: 8px 0;
}

.result-box {
    background: linear-gradient(135deg, #eff6ff, #f8fafc);
    border: 1px solid #bfdbfe;
    border-radius: 14px;
    padding: 16px;
}

.small-muted {
    color: #64748b;
    font-size: .88rem;
}

div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    padding: 12px 14px;
    border-radius: 12px;
}

[data-testid="stSidebar"] {
    background: #172554;
}

[data-testid="stSidebar"] * {
    color: white;
}

[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] .stSelectbox label {
    color: white !important;
}

div.stButton > button {
    border-radius: 10px;
}

hr {
    border-color: #e2e8f0;
}
</style>
""", unsafe_allow_html=True)

# ---------------------- Header ----------------------------
st.markdown("""
<div class="hero">
    <h1>📐 Math Function Explorer</h1>
    <p>แอปพลิเคชันสำหรับศึกษาและทดลองฟังก์ชันเอ็กซ์โพเนนเชียลและฟังก์ชันเชิงเส้น
    พร้อมกราฟ ตารางค่า และการคำนวณแบบ Step-by-Step</p>
    <div class="badge">Project 2569 · กลุ่ม 4 · Interactive Mathematics</div>
</div>
""", unsafe_allow_html=True)

# ---------------------- Sidebar ---------------------------
with st.sidebar:
    st.markdown("## 🎛️ ตัวควบคุม")
    st.caption("ปรับค่าพารามิเตอร์แล้วดูผลลัพธ์แบบ Real-time")

    st.markdown("### ฟังก์ชันเอ็กซ์โพเนนเชียล")
    a = st.slider("ฐาน a", 0.1, 5.0, 2.0, 0.1)
    b = st.slider("ตัวคูณ b", -10.0, 10.0, 1.5, 0.5)
    c = st.slider("อัตราการเปลี่ยนแปลง c", -2.0, 2.0, 0.7, 0.1)
    h = st.slider("การเลื่อนแนวนอน h", -5.0, 5.0, 1.0, 0.5)
    k = st.slider("การเลื่อนแนวตั้ง k", -10.0, 10.0, 0.0, 0.5)

    st.markdown("---")
    st.markdown("### ฟังก์ชันเชิงเส้น")
    m = st.slider("ความชัน m", -10.0, 10.0, 2.0, 0.5)
    intercept = st.slider("จุดตัดแกน y (c)", -10.0, 10.0, 1.0, 0.5)

    st.markdown("---")
    st.markdown("### ค่าที่ต้องการคำนวณ")
    x0 = st.number_input("กำหนดค่า x", value=2.0, step=0.5)
    table_step = st.selectbox("ระยะห่างของ x ในตาราง", [0.5, 1.0, 2.0], index=1)

    st.markdown("---")
    st.caption("💡 คำแนะนำ: ลองปรับทีละพารามิเตอร์เพื่อสังเกตผลต่อรูปร่างกราฟ")

# ---------------------- Helper functions ------------------
def make_table(func, step):
    xs = np.arange(-5, 5 + 1e-9, step)
    ys = func(xs)
    return pd.DataFrame({
        "x": np.round(xs, 3),
        "y": np.round(ys, 4)
    })

def make_graph(func, label, asymptote=None, x_min=-5, x_max=5):
    xs = np.linspace(x_min, x_max, 500)
    ys = func(xs)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=xs,
        y=ys,
        mode="lines",
        name=label,
        line=dict(width=3)
    ))

    sample_x = np.arange(x_min, x_max + 1e-9, 1)
    fig.add_trace(go.Scatter(
        x=sample_x,
        y=func(sample_x),
        mode="markers",
        name="จุดตัวอย่าง",
        marker=dict(size=7)
    ))

    if asymptote is not None:
        fig.add_hline(
            y=asymptote,
            line_dash="dash",
            annotation_text=f"เส้นกำกับ y = {asymptote:g}"
        )

    fig.update_layout(
        template="plotly_white",
        height=430,
        margin=dict(l=10, r=10, t=35, b=10),
        xaxis_title="x",
        yaxis_title="y",
        hovermode="x unified",
        legend=dict(orientation="h", y=1.08)
    )
    return fig

# ---------------------- Tabs ------------------------------
tab_home, tab_exp, tab_linear, tab_summary = st.tabs([
    "🏠 ภาพรวม",
    "📈 Exponential Function",
    "📏 Linear Function",
    "📝 สรุปผล"
])

# =========================================================
# HOME
# =========================================================
with tab_home:
    st.markdown('<div class="section-title">ภาพรวมของแอปพลิเคชัน</div>',
                unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="card">
        <h3>📈 Exponential</h3>
        <p>ศึกษาฟังก์ชันเอ็กซ์โพเนนเชียล การเติบโต การลดลง
        การเลื่อนกราฟ และเส้นกำกับแนวนอน</p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card">
        <h3>📏 Linear</h3>
        <p>ศึกษาความชัน จุดตัดแกน y จุดตัดแกน x
        และความสัมพันธ์ระหว่าง x กับ y</p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="card">
        <h3>🧮 Step-by-Step</h3>
        <p>ทดลองแทนค่า x และติดตามขั้นตอนการคำนวณ
        จนได้คำตอบสุดท้าย</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### วิธีใช้งาน")
    st.markdown("""
    <div class="info-box">
    <b>1.</b> ใช้แถบด้านซ้ายเพื่อปรับพารามิเตอร์<br>
    <b>2.</b> เลือกแท็บ Exponential หรือ Linear<br>
    <b>3.</b> สังเกตการเปลี่ยนแปลงของกราฟและตารางค่า<br>
    <b>4.</b> กำหนดค่า x เพื่อดูการคำนวณแบบ Step-by-Step<br>
    <b>5.</b> ดูผลสรุปเพื่อเชื่อมโยงพารามิเตอร์กับลักษณะของกราฟ
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# EXPONENTIAL
# =========================================================
with tab_exp:
    if a == 1 or b == 0 or c == 0:
        st.warning("⚠️ สำหรับฟังก์ชันเอ็กซ์โพเนนเชียลในรูปแบบนี้ ควรกำหนด a ≠ 1, b ≠ 0 และ c ≠ 0")

    f_exp = lambda x: b * np.power(a, c * (x + h)) + k

    growth_value = b * c * np.log(a)
    is_growth = growth_value > 0

    st.markdown('<div class="section-title">ฟังก์ชันเอ็กซ์โพเนนเชียล</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="formula">
    <b>สมการ:</b> &nbsp; y = b(a<sup>c(x+h)</sup>) + k
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([2.2, 1])

    with left:
        st.plotly_chart(
            make_graph(
                f_exp,
                f"y = {b:g}({a:g}^( {c:g}(x + {h:g}) )) + {k:g}",
                asymptote=k
            ),
            use_container_width=True
        )

    with right:
        st.markdown("### 🔎 วิเคราะห์กราฟ")
        if a > 0 and a != 1 and b != 0 and c != 0:
            if is_growth:
                st.success("แนวโน้ม: กราฟเพิ่มขึ้น (Growth)")
            else:
                st.info("แนวโน้ม: กราฟลดลง (Decay)")
        st.metric("ค่า b·c·ln(a)", f"{growth_value:.3f}")
        st.metric("เส้นกำกับแนวนอน", f"y = {k:g}")

    st.markdown("### 📊 ตารางค่า")
    st.dataframe(
        make_table(f_exp, table_step),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### 🧮 การคำนวณแบบ Step-by-Step")
    expo = c * (x0 + h)
    power_value = a ** expo
    y_value = f_exp(x0)

    st.markdown(f"""
    <div class="card">
    <b>ขั้นที่ 1: กำหนดค่าพารามิเตอร์</b><br>
    a = {a:g}, &nbsp; b = {b:g}, &nbsp; c = {c:g},
    &nbsp; h = {h:g}, &nbsp; k = {k:g}
    <hr>
    <b>ขั้นที่ 2: แทนค่า x = {x0:g}</b><br>
    y = {b:g}({a:g}<sup>{c:g}({x0:g} + {h:g})</sup>) + {k:g}
    <br><br>
    <b>ขั้นที่ 3: คำนวณเลขชี้กำลัง</b><br>
    c(x+h) = {c:g}({x0:g} + {h:g}) = {expo:.4f}
    <br><br>
    <b>ขั้นที่ 4: คำนวณค่ากำลัง</b><br>
    {a:g}<sup>{expo:.4f}</sup> = {power_value:.6f}
    <br><br>
    <b>ขั้นที่ 5: คำนวณคำตอบ</b><br>
    y = {b:g}({power_value:.6f}) + {k:g}
    </div>
    """, unsafe_allow_html=True)

    st.metric(f"ผลลัพธ์เมื่อ x = {x0:g}", f"{y_value:.4f}")

    st.markdown("### 📚 ความหมายของพารามิเตอร์")
    st.markdown("""
    | พารามิเตอร์ | ความหมาย |
    |---|---|
    | **a** | ฐานของฟังก์ชันเอ็กซ์โพเนนเชียล โดย a > 0 และ a ≠ 1 |
    | **b** | ตัวคูณหรือการยืด/สะท้อนในแนวตั้ง |
    | **c** | อัตราการเปลี่ยนแปลงในเลขชี้กำลัง |
    | **h** | การเลื่อนกราฟในแนวนอน |
    | **k** | การเลื่อนกราฟในแนวตั้ง และกำหนดเส้นกำกับ y = k |
    """)

# =========================================================
# LINEAR
# =========================================================
with tab_linear:
    f_linear = lambda x: m * x + intercept

    st.markdown('<div class="section-title">ฟังก์ชันเชิงเส้น</div>',
                unsafe_allow_html=True)

    st.markdown("""
    <div class="formula">
    <b>สมการ:</b> &nbsp; y = mx + c
    </div>
    """, unsafe_allow_html=True)

    left, right = st.columns([2.2, 1])

    with left:
        st.plotly_chart(
            make_graph(
                f_linear,
                f"y = {m:g}x + {intercept:g}"
            ),
            use_container_width=True
        )

    with right:
        st.markdown("### 🔎 วิเคราะห์กราฟ")

        if m > 0:
            st.success("กราฟเพิ่มขึ้น")
        elif m < 0:
            st.info("กราฟลดลง")
        else:
            st.warning("กราฟเป็นเส้นแนวนอน")

        st.metric("ความชัน m", f"{m:g}")
        st.metric("จุดตัดแกน y", f"(0, {intercept:g})")

        if m != 0:
            x_intercept = -intercept / m
            st.metric("จุดตัดแกน x", f"x = {x_intercept:.3f}")
        else:
            st.metric("จุดตัดแกน x", "ไม่มี / ไม่จำกัด")

    st.markdown("### 📊 ตารางค่า")
    st.dataframe(
        make_table(f_linear, table_step),
        use_container_width=True,
        hide_index=True
    )

    st.markdown("### 🧮 การคำนวณแบบ Step-by-Step")
    y_linear = f_linear(x0)

    st.markdown(f"""
    <div class="card">
    <b>ขั้นที่ 1: กำหนดค่าพารามิเตอร์</b><br>
    m = {m:g}, &nbsp; c = {intercept:g}
    <hr>
    <b>ขั้นที่ 2: แทนค่า x = {x0:g}</b><br>
    y = ({m:g})({x0:g}) + ({intercept:g})
    <br><br>
    <b>ขั้นที่ 3: คำนวณ</b><br>
    y = {m * x0:g} + ({intercept:g})
    <br><br>
    <b>ขั้นที่ 4: ผลลัพธ์</b>
    </div>
    """, unsafe_allow_html=True)

    st.metric(f"ผลลัพธ์เมื่อ x = {x0:g}", f"{y_linear:.4f}")

    st.markdown("### 📚 ความหมายของพารามิเตอร์")
    st.markdown("""
    | พารามิเตอร์ | ความหมาย |
    |---|---|
    | **m** | ความชันของเส้นตรง |
    | **c** | จุดตัดแกน y |
    | **x-intercept** | จุดที่กราฟตัดแกน x โดยคำนวณจาก x = −c/m เมื่อ m ≠ 0 |
    """)

# =========================================================
# SUMMARY
# =========================================================
with tab_summary:
    st.markdown('<div class="section-title">สรุปผลการทดลอง</div>',
                unsafe_allow_html=True)

    exp_status = "เพิ่มขึ้น (Growth)" if is_growth else "ลดลง (Decay)"

    st.markdown(f"""
    <div class="result-box">
    <h3>📈 Exponential Function</h3>
    <p>
    จากค่าพารามิเตอร์ปัจจุบัน ฟังก์ชันมีแนวโน้ม
    <b>{exp_status}</b>
    โดยค่า b·c·ln(a) = <b>{growth_value:.3f}</b>
    </p>
    <p>
    เส้นกำกับแนวนอนคือ <b>y = {k:g}</b>
    และมีการเลื่อนแนวนอนด้วยค่า <b>h = {h:g}</b>
    </p>
    </div>
    """, unsafe_allow_html=True)

    linear_status = (
        "เพิ่มขึ้น" if m > 0
        else "ลดลง" if m < 0
        else "คงที่"
    )

    st.markdown(f"""
    <div class="result-box">
    <h3>📏 Linear Function</h3>
    <p>
    ฟังก์ชันมีความชัน <b>m = {m:g}</b>
    ดังนั้นกราฟมีแนวโน้ม <b>{linear_status}</b>
    </p>
    <p>
    จุดตัดแกน y คือ <b>(0, {intercept:g})</b>
    </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🎓 สิ่งที่สามารถสังเกตได้จากการทดลอง")
    st.markdown("""
    - การเปลี่ยนค่าพารามิเตอร์แต่ละตัวส่งผลต่อรูปร่างและตำแหน่งของกราฟ
    - ฟังก์ชันเอ็กซ์โพเนนเชียลสามารถแสดงพฤติกรรมการเติบโตหรือการลดลงได้
    - ฟังก์ชันเชิงเส้นพิจารณาแนวโน้มของกราฟจากค่าความชัน
    - ตารางค่าช่วยตรวจสอบความสัมพันธ์ระหว่างค่า x และ y
    - การคำนวณแบบ Step-by-Step ช่วยเชื่อมโยงสูตรกับผลลัพธ์ที่เกิดขึ้นจริง

    <div class="small-muted">
    หมายเหตุ: แอปนี้จัดทำเพื่อใช้เป็นสื่อประกอบการเรียนรู้และการทดลองทางคณิตศาสตร์
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")
st.caption("Math Function Explorer · Project 2569 · กลุ่ม 4")
