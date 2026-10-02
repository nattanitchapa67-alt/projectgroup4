import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go

# ---------------------------------------------------------
# การตั้งค่าหน้าเว็บ (Page Config)
# ---------------------------------------------------------
st.set_page_config(
    page_title="การเรียนรู้ฟังก์ชัน Exponential และเส้นตรง",
    page_icon="📈",
    layout="wide"
)

# ---------------------------------------------------------
# ส่วน Sidebar สำหรับ Input Controls
# ---------------------------------------------------------
st.sidebar.title("⚙️ ปรับแต่งค่าพารามิเตอร์")

mode = st.sidebar.selectbox(
    "เลือกฟังก์ชันที่ต้องการศึกษา",
    ["Exponential Function", "Linear Function (เส้นตรง)"]
)

st.sidebar.markdown("---")

if mode == "Exponential Function":
    st.sidebar.header("พารามิเตอร์ $y = b(a^{c(x+h)}) + k$")
    a = st.sidebar.number_input("ค่าฐาน $a$ (ต้อง > 0)", value=2.0, min_value=0.01, step=0.5)
    b = st.sidebar.slider("ค่า $b$ (ตัวคูณด้านหน้า)", -10.0, 10.0, 1.0, 0.5)
    c = st.sidebar.slider("ค่า $c$ (ตัวคูณเลขชี้กำลัง)", -5.0, 5.0, 1.0, 0.5)
    h = st.sidebar.slider("ค่า $h$ (การเลื่อนขนานแนวแกน X)", -10.0, 10.0, 0.0, 0.5)
    k = st.sidebar.slider("ค่า $k$ (การเลื่อนขนานแนวแกน Y)", -10.0, 10.0, 0.0, 0.5)
else:
    st.sidebar.header("พารามิเตอร์ $y = mx + c$")
    m = st.sidebar.slider("ความชัน $m$", -10.0, 10.0, 1.0, 0.5)
    c_line = st.sidebar.slider("จุดตัดแกน Y ($c$)", -10.0, 10.0, 0.0, 0.5)

st.sidebar.markdown("---")
x_range = st.sidebar.slider("ช่วงของค่า X บนกราฟ", -20, 20, (-10, 10))


# ---------------------------------------------------------
# ส่วน Layout หลัก (st.tabs)
# ---------------------------------------------------------
st.title("แอปพลิเคชันช่วยเรียนรู้ฟังก์ชันคณิตศาสตร์")
st.write("เว็บไซต์นี้จัดทำขึ้นเพื่อช่วยเรียนรู้พฤติกรรมของฟังก์ชัน Exponential และสมการเส้นตรง")

tab1, tab2, tab3 = st.tabs(["กราฟและการแสดงผล", "ตารางคำนวณ Step-by-Step", "สรุปพฤติกรรมและทฤษฎี"])

# ---------------------------------------------------------
# TAB 1: แสดงกราฟและสมการ
# ---------------------------------------------------------
with tab1:
    if mode == "Exponential Function":
        st.subheader("1. สมการฟังก์ชัน Exponential")
        st.latex(r"y = b \cdot a^{c(x+h)} + k")
        st.latex(f"y = ({b}) \\cdot ({a})^{{{c}(x + ({h}))}} + ({k})")
        
        x_vals = np.linspace(x_range[0], x_range[1], 400)
        y_vals = b * (a ** (c * (x_vals + h))) + k

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name='Exponential', line=dict(color='blue', width=3)))
        fig.add_hline(y=k, line_dash="dash", line_color="red", annotation_text=f"เส้นกำกับแนวนอน y = {k}")
        fig.update_layout(title="กราฟของฟังก์ชัน Exponential", xaxis_title="ค่า X", yaxis_title="ค่า Y", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.subheader("1. สมการเส้นตรง")
        st.latex(r"y = mx + c")
        st.latex(f"y = ({m})x + ({c_line})")
        
        x_vals = np.linspace(x_range[0], x_range[1], 400)
        y_vals = m * x_vals + c_line

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name='Linear', line=dict(color='green', width=3)))
        fig.update_layout(title="กราฟของสมการเส้นตรง", xaxis_title="ค่า X", yaxis_title="ค่า Y", template="plotly_white")
        st.plotly_chart(fig, use_container_width=True)

# ---------------------------------------------------------
# TAB 2: Step-by-Step Calculation
# ---------------------------------------------------------
with tab2:
    st.subheader("2. ตารางแสดงการคำนวณค่า X และ Y แบบ Step-by-Step")
    x_steps = np.arange(x_range[0], x_range[1] + 1, 1)
    
    if mode == "Exponential Function":
        y_steps = b * (a ** (c * (x_steps + h))) + k
        df = pd.DataFrame({
            "ค่า X": x_steps,
            "คำนวณเลขชี้กำลัง c(x+h)": c * (x_steps + h),
            "ค่า y = b*a^(c(x+h)) + k": y_steps
        })
    else:
        y_steps = m * x_steps + c_line
        df = pd.DataFrame({
            "ค่า X": x_steps,
            "คำนวณ mx": m * x_steps,
            "ค่า y = mx + c": y_steps
        })
    st.dataframe(df, use_container_width=True)

# ---------------------------------------------------------
# TAB 3: สรุปพฤติกรรมฟังก์ชัน + รูปทฤษฎีประกอบ (st.image)
# ---------------------------------------------------------
with tab3:
    st.subheader("3. รายละเอียด พฤติกรรม และรูปภาพประกอบทฤษฎี")

    # --- ส่วนการแสดงผล Media Element (st.image) ---
    st.markdown("### 🖼️ แผนภาพทฤษฎีประกอบการเรียนรู้ (Media Element)")
    if mode == "Exponential Function":
        # แสดงรูปภาพทฤษฎีฟังก์ชัน Exponential (Growth vs Decay)
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Exponential_growth_and_decay_1.svg/640px-Exponential_growth_and_decay_1.svg.png",
            caption="รูปที่ 1: เปรียบเทียบลักษณะฟังก์ชัน Exponential เพิ่ม (Growth) และ ฟังก์ชัน Exponential ลด (Decay)",
            use_container_width=True
        )
    else:
        # แสดงรูปภาพทฤษฎีสมการเส้นตรงและความชัน
        st.image(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Linear_Function_graph.svg/640px-Linear_Function_graph.svg.png",
            caption="รูปที่ 2: ลักษณะของสมการเส้นตรงและความชัน (Slope: m) ในรูปแบบต่างๆ",
            use_column_width=True
        )

    st.markdown("---")
    
    col1, col2 = st.columns(2)
    if mode == "Exponential Function":
        with col1:
            st.metric(label="เส้นกำกับแนวนอน (Horizontal Asymptote)", value=f"y = {k}")
            st.metric(label="จุดตัดแกน Y (เมื่อ x = 0)", value=f"y = {round(b * (a ** (c * h)) + k, 4)}")
        with col2:
            st.write("### 📌 วิเคราะห์ลักษณะฟังก์ชัน:")
            effective_base = a ** c
            if (effective_base > 1 and b > 0) or (0 < effective_base < 1 and b < 0):
                st.success("ลักษณะกราฟ: **ฟังก์ชันเพิ่ม (Increasing Function)**")
            else:
                st.warning("ลักษณะกราฟ: **ฟังก์ชันลด (Decreasing Function)**")

            st.write(f"- **โดเมน (Domain):** $\\mathbb{{R}}$ (จำนวนจริงทั้งหมด)")
            st.write(f"- **เรนจ์ (Range):** " + (f"$({k}, \\infty)$" if b > 0 else f"$(-\\infty, {k})$"))
    else:
        with col1:
            st.metric(label="ความชัน (Slope: m)", value=m)
            st.metric(label="จุดตัดแกน Y (y-intercept)", value=f"(0, {c_line})")
        with col2:
            st.write("### 📌 วิเคราะห์ลักษณะเส้นตรง:")
            if m > 0:
                st.success("ลักษณะกราฟ: **เส้นตรงมีความชันเป็นบวก (เฉียงขึ้นทางขวา)**")
            elif m < 0:
                st.warning("ลักษณะกราฟ: **เส้นตรงมีความชันเป็นลบ (เฉียงลงทางขวา)**")
            else:
                st.info("ลักษณะกราฟ: **เส้นตรงขนานกับแกน X (ความชันเป็น 0)**")

            if m != 0:
                x_intercept = -c_line / m
                st.write(f"- **จุดตัดแกน X:** ({round(x_intercept, 4)}, 0)")
            else:
                st.write("- **จุดตัดแกน X:** ไม่มี (ขนานกับแกน X)")

            st.write("- **โดเมน (Domain):** $\\mathbb{R}$")
            st.write("- **เรนจ์ (Range):** " + ("$\\mathbb{R}$" if m != 0 else f"{{{c_line}}}"))
