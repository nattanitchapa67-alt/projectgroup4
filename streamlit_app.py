import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
# ============================================================
# 1) !ง#าห&าเพจ
# ============================================================
st.set_page_config(page_title="Math Learning", page_icon=" ", layout="wide")
# *พาสเทลตามแบบ (ชม3 / 4ช / 5วงลาเวนเดอ: / ;น<)
PINK, PEACH, LAV, MINT = "#F2C4C8", "#F9DDB8", "#CFC8F5", "#B9EBD3"
DARK, PURPLE = "#2B2B33", "#7C6FE0"
# CSS ตกแ>ง: ?นห@ง;น<, กา:ดAมมน
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

# 2) Sidebar: Lบ#าจากMใO (widgets)
# ============================================================
st.sidebar.title(" เมนู")
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
xmin, xmax = st.sidebar.slider("ช่วงของ x Yแสดงบนกราฟ", -15.0, 15.0, (-5.0, 5.0), 0.5)
x0 = st.sidebar.number_input("x ที่ต้องการคำนวณ", value=1.0, step=0.5)
# ============================================================
# 3)กำหนดฟังก์ชัน f(x) และข้อมูลสรุป
# ============================================================
if mode == "Exponential":
if a == 1:
st.error("a = 1 ทำให้เป็นค่าคงที่ กรุณาเลือก a ≠ 1")
st.stop()
def f(x):
return b * a ** (c * (np.asarray(x, dtype=float) + h)) + k
equation = rf"y = {g(b)}\left({g(a)}^{{{g(c)}(x{h:+g})}}\right){k:+g}"
# dศทาง: fจากเคgองหมายของ b*c*ln(a)
s = b * c * np.log(a)
trend = "เพิ่มขึ้น" if s > 0 else "ลดลง" if s < 0 else "คงY"
value_range = f"y > {g(k)}" if b > 0 else f"y < {g(k)}" if b < 0 else f"y = {g(k)}"
asymptote = f"y = {g(k)}"
# XดDดแกน x: b*a^(c(x+h)) = -k ([องk -k/b > 0)
if b != 0 and c != 0 and -k / b > 0:
x_int = np.log(-k / b) / (c * np.log(a)) - h
x_int_text = f"x = {x_int:.3f}"
else:
x_int, x_int_text = None, "ไ5k"
top_cards = [(PINK, "a (ฐาน)", g(a)), (PEACH, "b (Dวmณ)", g(b)),
(LAV, "c (เลขn^@ง)", g(c)), (MINT, "h , k (เoอน)", f"{g(h)} , {g(k)}")]

else:
def f(x):
return m * np.asarray(x, dtype=float) + c
equation = rf"y = {g(m)}x{c:+g}"
trend = "เiมjน" if m > 0 else "ลดลง" if m < 0 else "คงY"
value_range = "R" if m != 0 else f"y = {g(c)}"
asymptote = "ไ5k"
x_int = -c / m if m != 0 else None
x_int_text = f"x = {x_int:.3f}" if m != 0 else "ไ5k"
top_cards = [(PINK, "m (ความTน)", g(m)), (PEACH, "c (XดDดแกน y)", g(c)),
(LAV, "XดDดแกน x", x_int_text), (MINT, "dศทาง", trend)]
# ============================================================
# 4) pวนqวของห&าเrบ
# ============================================================
st.markdown('<div class="big-title">Learn math,<br>one graph at a time</div>',
unsafe_allow_html=True)
st.caption(f"^@งเsยนt: RงSTน {mode} | ปLบ#าYแถบvานwาย กราฟจะเปxยนyนz")
# กา:ด*พาสเทล 4 ใบ
cols = st.columns(4)
for col, (color, title, value) in zip(cols, top_cards):
with col:
card(color, title, value)
# แ{งห&าเFน 2 |ง: wาย = เ}อหาห@ก, ขวา = แผงสaป
left, right = st.columns([3, 1.3])
# ============================================================
# 5) |งwาย: แบ ทฤษÇ / กราฟ / \นวณzละÉน
# ============================================================
with left:
tab1, tab2, tab3 = st.tabs([" ทฤษÇ", " กราฟ", " \นวณzละÉน"])
# ---------- แบทฤษÇ ----------
with tab1:
if mode == "Exponential":
st.latex(r"y = b\left(a^{c(x+h)}\right) + k")
st.markdown("""
- **a** : ฐาน (a > 1 เiมjนเÑว, 0 < a < 1 ลดลง)
- **b** : Öด/หดแนว!ง (Üา b < 0 กราฟพáกลง)
- **c** : ปLบàตราการเiม/ลด (Üา c < 0 กราฟพáกwาย-ขวา)
- **h** : เoอนwาย-ขวา
- **k** : เoอนjน-ลง และเFนเUน^âบ y = k
""")

else:
st.latex(r"y = mx + c")
st.markdown("""
- **m** : ความTน (m > 0 jน, m < 0 ลง, m = 0 แนวนอน)
- **c** : XดDดแกน y (#า y เäอ x = 0)
- XดDดแกน x หาจาก 0 = mx + c
""")
st.latex(equation)
# ---------- แบกราฟ ----------
with tab2:
x = np.linspace(xmin, xmax, 400)
y = f(x)
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name="y = f(x)",
line=dict(color=PURPLE, width=4)))
if mode == "Exponential":
fig.add_hline(y=k, line_dash="dash", line_color="#E58B97",
annotation_text=f"เUน^âบ y = {g(k)}")
# XดDดแกน y และXดYเQอก
fig.add_trace(go.Scatter(x=[0], y=[float(f(0))], mode="markers", name="XดDดแกน y",
marker=dict(size=12, color="#F2A65A")))
fig.add_trace(go.Scatter(x=[x0], y=[float(f(x0))], mode="markers", name="XดYเQอก",
marker=dict(size=12, color="#4CB68A")))
fig.update_layout(paper_bgcolor="#FBF8F4", plot_bgcolor="#FBF8F4", height=480,
xaxis_title="x", yaxis_title="y", legend=dict(orientation="h"))
st.plotly_chart(fig, use_container_width=True)
# ---------- แบ\นวณzละÉน ----------
with tab3:
st.write(f"**หา#า y เäอ x = {g(x0)}**")
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
st.metric("ผล@พã y", g(float(f(x0))))
# ตารางสaป
xs = np.arange(np.floor(xmin), np.ceil(xmax) + 1, max(1, int((xmax - xmin) // 8)))

table = pd.DataFrame({"x": xs, "y": np.round(f(xs), 4)})
st.dataframe(table, use_container_width=True, hide_index=True)
# ============================================================
# 6) |งขวา: แผงสaปพฤåกรรมของRงSTน
# ============================================================
with right:
with st.container(border=True):
st.subheader(" สaปพฤåกรรม")
st.metric("dศทางของRงSTน", trend)
st.metric("เรนç", value_range)
st.metric("XดDดแกน y", f"(0, {g(round(float(f(0)), 3))})")
st.metric("XดDดแกน x", x_int_text)
st.write(f"**โดเมน:** R (èกêนวนจëง)")
st.write(f"**เUน^âบแนวนอน:** {asymptote}")
