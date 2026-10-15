# ==============================================================================
# โครงงานวิชาคณิตศาสตร์คอมพิวเตอร์ (Project 4) - คะแนน 20%
# เรื่อง: สื่อการเรียนรู้ฟังก์ชัน Exponential และสมการเส้นตรง
# ==============================================================================

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# ------------------------------------------------------------------------------
# 1. ตั้งค่าหน้าเว็บและกำหนดธีมสีพาสเทล (สไตล์ Mint & Peach ตามรูปอ้างอิง)
# ------------------------------------------------------------------------------
st.set_page_config(page_title="MathEdu Studio - โครงงานที่ 4",page_icon="📐",layout="wide")

# Custom CSS ตกแต่งให้พื้นหลังเป็นสีมินต์พาสเทล และการ์ดสีพาสเทลนุ่มนวล
st.markdown("""
<style>
    /* สีพื้นหลังของแอป */
    .stApp {
        background-color: #F8F5FD;
    }
    
    /* สไตล์การ์ดข้อมูลแบบพาสเทล */
    .pastel-card {padding: 18px;border-radius: 18px;margin-bottom: 12px;box-shadow: 0 4px 12px rgba(0,0,0,0.03);}
    .card-peach { background-color: #FFEADB; border: 1px solid #FED0B8; }
    .card-butter { background-color: #FEF3C7; border: 1px solid #FDE68A; }
    .card-lavender { background-color: #EEE8FC; border: 1px solid #DDD4FA; }
    .card-mint { background-color: #E2F8EB; border: 1px solid #C3EED4; }
    .card-title { font-size: 13px; font-weight: 600; color: #555; }
    .card-value { font-size: 20px; font-weight: 700; color: #222; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 2. เมนูด้านข้าง (Sidebar) สำหรับรับค่าตัวแปร (Input Widgets)
# ------------------------------------------------------------------------------
with st.sidebar:
    st.title("⚙️ แผงควบคุม")
    st.caption("โครงงานศึกษา Project 2569")
    st.divider()

    # ข้อกำหนดที่ 1: เลือกประเภทฟังก์ชัน (st.radio)
    func_type = st.radio(
        "เลือกฟังก์ชันที่ต้องการศึกษา:",
        ["Exponential: y = b(a^{c(x+h)}) + k", "Linear: y = mx + c"])
    st.divider()

    # สไลเดอร์ปรับขอบเขตแกน X
    x_range = st.slider("ช่วงขอบเขตแกน X ([-X, X])", min_value=3, max_value=12, value=6)

    # รับค่าพารามิเตอร์ตามประเภทฟังก์ชัน
    if "Exponential" in func_type:
        st.subheader("พารามิเตอร์ Exponential")
        # a, b, c, h, k ตามโจทย์ Project 4
        a = st.slider("ฐาน a (a > 0)", min_value=0.2, max_value=4.0, value=2.0, step=0.1)
        b = st.slider("สเกลแนวตั้ง b", min_value=-4.0, max_value=4.0, value=1.0, step=0.5)
        c = st.slider("ตัวคูณกำลัง c", min_value=-3.0, max_value=3.0, value=1.0, step=0.5)
        h = st.slider("เลื่อนแนวนอน h", min_value=-5.0, max_value=5.0, value=0.0, step=0.5)
        k = st.slider("เลื่อนแนวตั้ง k (เส้นกำกับ y=k)", min_value=-5.0, max_value=5.0, value=0.0, step=0.5)
    else:
        st.subheader("พารามิเตอร์สมการเส้นตรง")
        # m, c สำหรับสมการเส้นตรง
        m = st.slider("ความชัน m (Slope)", min_value=-4.0, max_value=4.0, value=1.0, step=0.5)
        c_line = st.slider("จุดตัดแกน Y (c)", min_value=-6.0, max_value=6.0, value=2.0, step=0.5)

# ------------------------------------------------------------------------------
# 3. ส่วนหัวของหน้าเว็บ (Header Banner)
# ------------------------------------------------------------------------------
st.markdown("""
<div style="background: white; padding: 22px; border-radius: 24px; margin-bottom: 20px; border: 1px solid #E2E8F0;">
    <span style="background: #FEF3C7; color: #92400E; padding: 4px 10px; border-radius: 99px; font-size: 12px; font-weight: bold;">
        PROJECT 4 • INTERACTIVE MATH LAB
    </span>
    <h1 style="font-size: 28px; margin: 8px 0 4px 0; color: #1E293B;">
        Invest in your math knowledge 📐
    </h1>
    <p style="color: #64748B; font-size: 14px; margin: 0;">
        สื่อการเรียนรู้เชิงปฏิสัมพันธ์: สำรวจพฤติกรรมฟังก์ชันเอกซ์โพเนนเชียลและสมการเส้นตรง
    </p>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# 4. ฟังก์ชันคำนวณทางคณิตศาสตร์แบบเข้าใจง่าย
# ------------------------------------------------------------------------------
def calc_expo(x, a, b, c, h, k):
    return b * (np.power(a, c * (x + h))) + k

def calc_linear(x, m, c):
    return m * x + c

# ------------------------------------------------------------------------------
# 5. จัดระเบียบหน้าเว็บด้วย st.tabs (ข้อกำหนดที่ 5: ทฤษฎี -> ตัวจำลอง -> สรุปผล)
# ------------------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs([
    "📈 กราฟจำลอง & พารามิเตอร์ (Simulation)",
    "📖 ทฤษฎี & สูตรคำนวณ (Theory)",
    "📋 ตารางพิกัดคู่ลำดับ (Step-by-Step Table)"])

# ================= TAB 1: ตัวจำลองกราฟ =================
with tab1:
    # ข้อกำหนดที่ 2: แสดงสมการทางคณิตศาสตร์ด้วย st.latex
    st.write("##### 📌 สมการปัจจุบัน:")
    if "Exponential" in func_type:
        st.latex(f"f(x) = {b} \\cdot ({a})^{{{c}(x + {h})}} + ({k})")
    else:
        st.latex(f"f(x) = {m}x + ({c_line})")

    col_plot, col_info = st.columns([7, 3])

    # คำนวณจุดสำหรับวาดกราฟ
    x_points = np.linspace(-x_range, x_range, 300)

    with col_plot:
        # ข้อกำหนดที่ 3: Dynamic Visualization ด้วย Plotly
        fig = go.Figure()

        if "Exponential" in func_type:
            y_points = calc_expo(x_points, a, b, c, h, k)
            
            # เส้นกราฟหลัก
            fig.add_trace(go.Scatter(
                x=x_points, y=y_points,
                mode="lines",
                name="f(x) Exponential",
                line=dict(color="#1E293B", width=3)))
            # เส้นกำกับแนวนอน y = k
            fig.add_trace(go.Scatter(
                x=[-x_range, x_range], y=[k, k],
                mode="lines",
                name=f"เส้นกำกับ y = {k}",
                line=dict(color="#EF4444", width=2, dash="dash")))
            # จุดตัดแกน Y (x = 0)
            y_intercept = calc_expo(0, a, b, c, h, k)
            fig.add_trace(go.Scatter(
                x=[0], y=[y_intercept],
                mode="markers+text",
                name="จุดตัดแกน Y",
                text=[f"(0, {y_intercept:.2f})"],
                textposition="top right",
                marker=dict(size=9, color="#F97316")))
        else:
            y_points = calc_linear(x_points, m, c_line)
            # เส้นกราฟตรง
            fig.add_trace(go.Scatter(
                x=x_points, y=y_points,
                mode="lines",
                name="f(x) = mx + c",
                line=dict(color="#1E293B", width=3)))
            # จุดตัดแกน Y (x = 0)
            fig.add_trace(go.Scatter(
                x=[0], y=[c_line],
                mode="markers+text",
                name="จุดตัดแกน Y",
                text=[f"(0, {c_line:.2f})"],
                textposition="top right",
                marker=dict(size=9, color="#F97316")))
            # จุดตัดแกน X (ถ้า m != 0)
            if m != 0:
                x_intercept = -c_line / m
                fig.add_trace(go.Scatter(
                    x=[x_intercept], y=[0],
                    mode="markers+text",
                    name="จุดตัดแกน X",
                    text=[f"({x_intercept:.2f}, 0)"],
                    textposition="bottom right",
                    marker=dict(size=9, color="#8B5CF6")))

        # ตกแต่งกราฟให้สวยและคลีน
        fig.update_layout(
            height=430,
            margin=dict(l=30, r=20, t=30, b=30),
            plot_bgcolor="white",
            paper_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(range=[-x_range, x_range], zeroline=True, gridcolor="#F1F5F9", title="แกน X"),
            yaxis=dict(range=[-x_range, x_range], zeroline=True, gridcolor="#F1F5F9", title="แกน Y"))
        st.plotly_chart(fig, use_container_width=True)

    with col_info:
        st.write("##### 📊 พฤติกรรมของฟังก์ชัน")
        
        if "Exponential" in func_type:
            # ตรวจสอบฟังก์ชันเพิ่มหรือลด
            net_base = a ** c
            is_inc = (net_base > 1 and b > 0) or (net_base < 1 and b < 0)
            beh_text = "📈 ฟังก์ชันเพิ่ม" if is_inc else "📉 ฟังก์ชันลด"
            y0 = calc_expo(0, a, b, c, h, k)
            range_text = f"({k:.1f}, +∞)" if b > 0 else f"(-∞, {k:.1f})"

            st.markdown(f"""
            <div class="pastel-card card-peach">
                <div class="card-title">พฤติกรรม</div>
                <div class="card-value">{beh_text}</div>
            </div>
            <div class="pastel-card card-butter">
                <div class="card-title">จุดตัดแกน Y (เมื่อ x=0)</div>
                <div class="card-value">(0, {y0:.2f})</div>
            </div>
            <div class="pastel-card card-lavender">
                <div class="card-title">เส้นกำกับแนวนอน</div>
                <div class="card-value">y = {k:.1f}</div>
            </div>
            <div class="pastel-card card-mint">
                <div class="card-title">เรนจ์ (Range)</div>
                <div class="card-value">{range_text}</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            if m > 0:
                beh_text = "📈 ฟังก์ชันเพิ่ม (m > 0)"
            elif m < 0:
                beh_text = "📉 ฟังก์ชันลด (m < 0)"
            else:
                beh_text = "➖ เส้นแนวนอน (m = 0)"
            
            x_int = f"({-c_line/m:.2f}, 0)" if m != 0 else "ไม่ตัดแกน X"

            st.markdown(f"""
            <div class="pastel-card card-butter">
                <div class="card-title">ความชัน (Slope)</div>
                <div class="card-value">{beh_text}</div>
            </div>
            <div class="pastel-card card-peach">
                <div class="card-title">จุดตัดแกน Y</div>
                <div class="card-value">(0, {c_line:.2f})</div>
            </div>
            <div class="pastel-card card-lavender">
                <div class="card-title">จุดตัดแกน X</div>
                <div class="card-value">{x_int}</div>
            </div>
            <div class="pastel-card card-mint">
                <div class="card-title">โดเมน & เรนจ์</div>
                <div class="card-value">ℝ (จำนวนจริง)</div>
            </div>
            """, unsafe_allow_html=True)

# ================= TAB 2: ทฤษฎี =================
with tab2:
    st.subheader("📖 นิยามและทฤษฎีทางคณิตศาสตร์")
    col_t1, col_t2 = st.columns(2)
    
    with col_t1:
        st.markdown("**1. ฟังก์ชันเอกซ์โพเนนเชียล**")
        st.latex(r"y = b(a^{c(x+h)}) + k")
        st.write("""
        - **$a$ (ฐาน):** ต้องมากกว่า 0 และไม่เท่ากับ 1
        - **$b$ (สเกลแนวตั้ง):** ยืด/หดกราฟ หากติดลบกราฟจะคว่ำ
        - **$c$ (ตัวคูณกำลัง):** เร่ง/ชะลออัตราการเพิ่ม
        - **$h$ (การเลื่อนแกน X):** เลื่อนซ้ายเมื่อ $+h$, เลื่อนขวาเมื่อ $-h$
        - **$k$ (การเลื่อนแกน Y):** เลื่อนขึ้น/ลงทั้งเส้น และเป็นเส้นกำกับ $y = k$
        """)
    
    with col_t2:
        st.markdown("**2. สมการเส้นตรง**")
        st.latex(r"y = mx + c")
        st.write("""
        - **$m$ (ความชัน - Slope):** อัตราส่วนการเปลี่ยนค่า $\\frac{\\Delta y}{\\Delta x}$
          - $m > 0$ กราฟเฉียงขึ้น (ฟังก์ชันเพิ่ม)
          - $m < 0$ กราฟเฉียงลง (ฟังก์ชันลด)
          - $m = 0$ กราฟขนานแกน X
        - **$c$ (จุดตัดแกน Y):** จุดที่เส้นตรงตัดแกนดิ่ง $(0, c)$
        """)

# ================= TAB 3: ตารางคำนวณทีละขั้น =================
with tab3:
    st.subheader("📋 ตารางคำนวณพิกัดทีละขั้น (Step-by-Step Table)")
    st.caption("คำนวณจุดพิกัด (x, y) สำหรับการพล็อตและตรวจสอบกราฟ")

    # สร้างตัวเลข x แบบจำนวนเต็ม
    table_x = list(range(-x_range, x_range + 1))
    
    if "Exponential" in func_type:
        table_y = [calc_expo(x, a, b, c, h, k) for x in table_x]
    else:
        table_y = [calc_linear(x, m, c_line) for x in table_x]

    # ทำเป็น DataFrame ตามข้อกำหนดที่ 4
    df = pd.DataFrame({
        "ค่า x": table_x,
        "ค่าคำนวณ y": [round(val, 3) for val in table_y],
        "พิกัดคู่ลำดับ (x, y)": [f"({x}, {round(y, 2)})" for x, y in zip(table_x, table_y)]})

    # แสดงตารางในหน้าเว็บ
    st.dataframe(df, use_container_width=True)
