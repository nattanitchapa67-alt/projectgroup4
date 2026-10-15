import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# ============================================================
# 1) ตั้งค่าหน้าเพจ
# ============================================================
st.set_page_config(page_title="Math Learning", page_icon="📚", layout="wide")

# สีพาสเทลตามแบบ (ชมพู / พีช / ม่วงลาเวนเดอร์ / มิ้นต์)
PINK, PEACH, LAV, MINT = "#F2C4C8", "#F9DDB8", "#CFC8F5", "#B9EBD3"
DARK, PURPLE = "#2B2B33", "#7C6FE0"

# CSS ตกแต่ง: พื้นหลังมิ้นต์, การ์ดมุมมน
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Sarabun:wght@400;600;700&display=swap');
html, body, [class*="css"] {{ font-family: 'Sarabun', sans-serif !important; }}
.stApp {{ background: #DDF5EA; color: {DARK}; }}
[data-testid="stSidebar"] {{ background: #FBF8F4; border-radius: 0 28px 28px 0; }}
.big-title {{ font-size: 3rem; font-weight: 700; line-height: 1.15; margin: 10px 0 18px 0; }}
.card {{ padding: 16px 20px; border-radius: 20px; margin-bottom: 12px; }}
.card small {{ color: #555; }}
.card h3 {{ margin: 4px 0 0 0; font-size: 1.6rem; }}
[data-testid="stVerticalBlockBorderWrapper"] {{ background: #FBF8F4; border-radius: 24px; }}
.stTabs [aria-selected="true"] {{ background: {DARK}; color: white; border-radius: 20px; }}
.stTabs [data-baseweb="tab"] {{ border-radius: 20px; padding: 6px 18px; }}
</style>
""", unsafe_allow_html=True)


def card(color, title, value):
    """สร้างการ์ดสีพาสเทล"""
    st.markdown(f'<div class="card" style="background:{color}"><small>{title}</small>'
                f'<h3>{value}</h3></div>', unsafe_allow_html=True)


def g(v):
    """แปลงตัวเลขเป็นข้อความสั้นๆ เช่น 2.0 -> 2"""
    return f"{v:g}"


# ============================================================
# 2) Sidebar: รับค่าจากผู้ใช้ (widgets)
# ============================================================
st.sidebar.title("📚 เมนู")
mode = st.sidebar.selectbox("เลือกฟังก์ชัน", ["Exponential", "เส้นตรง"])

if mode == "Exponential":
    st.sidebar.latex(r"y=b\left(a^{c(x+h)}\right)+k")
    a = st.sidebar.number_input("a (ฐาน, a > 0, a ≠ 1)", 0.1, 20.0, 2.0, 0.1)
    b = st.sidebar.slider("b", -5.0, 5.0, 1.0, 0.1)
    c = st.sidebar.slider("c", -3.0, 3.0, 1.0, 0.1)
    h = st.sidebar.slider("h", -5.0, 5.0, 0.0, 0.5)
    k = st.sidebar.slider("k", -10.0, 10.0, 0.0, 0.5)
else:
    st.sidebar.latex(r"y=mx+c")
    m = st.sidebar.slider("m (ความชัน)", -10.0, 10.0, 1.0, 0.1)
    c = st.sidebar.number_input("c (จุดตัดแกน y)", -50.0, 50.0, 0.0, 0.5)

xmin, xmax = st.sidebar.slider("ช่วงของ x ที่แสดงบนกราฟ", -15.0, 15.0, (-5.0, 5.0), 0.5)
x0 = st.sidebar.number_input("x ที่ต้องการคำนวณ", value=1.0, step=0.5)

# ============================================================
# 3) กำหนดฟังก์ชัน f(x) และข้อมูลสรุป
# ============================================================
if mode == "Exponential":
    if a == 1:
        st.error("a = 1 ทำให้เป็นค่าคงที่ กรุณาเลือก a ≠ 1")
        st.stop()

    def f(x):
        return b * a ** (c * (np.asarray(x, dtype=float) + h)) + k

    equation = rf"y = {g(b)}\left({g(a)}^{{{g(c)}(x{h:+g})}}\right){k:+g}"

    # ทิศทาง: ดูจากเครื่องหมายของ b*c*ln(a)
    s = b * c * np.log(a)
    trend = "เพิ่มขึ้น" if s > 0 else "ลดลง" if s < 0 else "คงที่"
    value_range = f"y > {g(k)}" if b > 0 else f"y < {g(k)}" if b < 0 else f"y = {g(k)}"
    asymptote = f"y = {g(k)}"
    # จุดตัดแกน x: b*a^(c(x+h)) = -k  (ต้องมี -k/b > 0)
    if b != 0 and c != 0 and -k / b > 0:
        x_int = np.log(-k / b) / (c * np.log(a)) - h
        x_int_text = f"x = {x_int:.3f}"
    else:
        x_int, x_int_text = None, "ไม่มี"

    top_cards = [(PINK, "a (ฐาน)", g(a)), (PEACH, "b (ตัวคูณ)", g(b)),
                 (LAV, "c (เลขชี้กำลัง)", g(c)), (MINT, "h , k (เลื่อน)", f"{g(h)} , {g(k)}")]
else:
    def f(x):
        return m * np.asarray(x, dtype=float) + c

    equation = rf"y = {g(m)}x{c:+g}"
    trend = "เพิ่มขึ้น" if m > 0 else "ลดลง" if m < 0 else "คงที่"
    value_range = "ℝ" if m != 0 else f"y = {g(c)}"
    asymptote = "ไม่มี"
    x_int = -c / m if m != 0 else None
    x_int_text = f"x = {x_int:.3f}" if m != 0 else "ไม่มี"

    top_cards = [(PINK, "m (ความชัน)", g(m)), (PEACH, "c (จุดตัดแกน y)", g(c)),
                 (LAV, "จุดตัดแกน x", x_int_text), (MINT, "ทิศทาง", trend)]

# ============================================================
# 4) ส่วนหัวของหน้าเว็บ
# ============================================================
st.markdown('<div class="big-title">Learn math,<br>one graph at a time</div>',
            unsafe_allow_html=True)
st.caption(f"กำลังเรียนรู้: ฟังก์ชัน {mode}  |  ปรับค่าที่แถบด้านซ้าย กราฟจะเปลี่ยนทันที")

# การ์ดสีพาสเทล 4 ใบ
cols = st.columns(4)
for col, (color, title, value) in zip(cols, top_cards):
    with col:
        card(color, title, value)

# แบ่งหน้าเป็น 2 ฝั่ง: ซ้าย = เนื้อหาหลัก, ขวา = แผงสรุป
left, right = st.columns([3, 1.3])

# ============================================================
# 5) ฝั่งซ้าย: แท็บ ทฤษฎี / กราฟ / คำนวณทีละขั้น
# ============================================================
with left:
    tab1, tab2, tab3 = st.tabs(["📖 ทฤษฎี", "📈 กราฟ", "🧮 คำนวณทีละขั้น"])

    # ---------- แท็บทฤษฎี ----------
    with tab1:
        if mode == "Exponential":
            st.latex(r"y = b\left(a^{c(x+h)}\right) + k")
            st.markdown("""
- **a** : ฐาน (a > 1 เพิ่มขึ้นเร็ว, 0 < a < 1 ลดลง)
- **b** : ยืด/หดแนวตั้ง (ถ้า b < 0 กราฟพลิกลง)
- **c** : ปรับอัตราการเพิ่ม/ลด (ถ้า c < 0 กราฟพลิกซ้าย-ขวา)
- **h** : เลื่อนซ้าย-ขวา
- **k** : เลื่อนขึ้น-ลง และเป็นเส้นกำกับ y = k
""")
        else:
            st.latex(r"y = mx + c")
            st.markdown("""
- **m** : ความชัน (m > 0 ขึ้น, m < 0 ลง, m = 0 แนวนอน)
- **c** : จุดตัดแกน y (ค่า y เมื่อ x = 0)
- จุดตัดแกน x หาจาก 0 = mx + c
""")
        st.latex(equation)

    # ---------- แท็บกราฟ ----------
    with tab2:
        x = np.linspace(xmin, xmax, 400)
        y = f(x)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="y = f(x)",
                                 line=dict(color=PURPLE, width=4)))
        if mode == "Exponential":
            fig.add_hline(y=k, line_dash="dash", line_color="#E58B97",
                          annotation_text=f"เส้นกำกับ y = {g(k)}")
        # จุดตัดแกน y และจุดที่เลือก
        fig.add_trace(go.Scatter(x=[0], y=[float(f(0))], mode="markers", name="จุดตัดแกน y",
                                 marker=dict(size=12, color="#F2A65A")))
        fig.add_trace(go.Scatter(x=[x0], y=[float(f(x0))], mode="markers", name="จุดที่เลือก",
                                 marker=dict(size=12, color="#4CB68A")))
        fig.update_layout(paper_bgcolor="#FBF8F4", plot_bgcolor="#FBF8F4", height=480,
                          xaxis_title="x", yaxis_title="y", legend=dict(orientation="h"))
        st.plotly_chart(fig, use_container_width=True)

    # ---------- แท็บคำนวณทีละขั้น ----------
    with tab3:
        st.write(f"**หาค่า y เมื่อ x = {g(x0)}**")
        if mode == "Exponential":
            e = c * (x0 + h)
            p = a ** e
            st.latex(rf"x+h = {g(x0)}{h:+g} = {g(x0 + h)}")
            st.latex(rf"c(x+h) = {g(c)}\times {g(x0 + h)} = {g(e)}")
            st.latex(rf"a^{{c(x+h)}} = {g(a)}^{{{g(e)}}} = {g(p)}")
            st.latex(rf"y = {g(b)}\times {g(p)}{k:+g} = {g(b * p + k)}")
        else:
            st.latex(rf"mx = {g(m)}\times {g(x0)} = {g(m * x0)}")
            st.latex(rf"y = mx + c = {g(m * x0)}{c:+g} = {g(m * x0 + c)}")

        st.metric("ผลลัพธ์ y", g(float(f(x0))))

        # ตารางสรุป
        xs = np.arange(np.floor(xmin), np.ceil(xmax) + 1, max(1, int((xmax - xmin) // 8)))
        table = pd.DataFrame({"x": xs, "y": np.round(f(xs), 4)})
        st.dataframe(table, use_container_width=True, hide_index=True)

# ============================================================
# 6) ฝั่งขวา: แผงสรุปพฤติกรรมของฟังก์ชัน
# ============================================================
with right:
    with st.container(border=True):
        st.subheader("🔍 สรุปพฤติกรรม")
        st.metric("ทิศทางของฟังก์ชัน", trend)
        st.metric("เรนจ์", value_range)
        st.metric("จุดตัดแกน y", f"(0, {g(round(float(f(0)), 3))})")
        st.metric("จุดตัดแกน x", x_int_text)
        st.write(f"**โดเมน:** ℝ (ทุกจำนวนจริง)")
        st.write(f"**เส้นกำกับแนวนอน:** {asymptote}")
