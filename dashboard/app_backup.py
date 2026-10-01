import streamlit as st
import pandas as pd
import random
import time
from datetime import datetime

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="Railway Fault Diagnosis",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

    /* Main page */
    .stApp {
        background-color: #f5f7fb;
    }

    .block-container {
        max-width: 1500px;
        padding-top: 25px;
        padding-bottom: 30px;
    }

    /* Hide default Streamlit header */
    [data-testid="stHeader"] {
        background: transparent;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    /* Main title */
    .main-title {
        font-size: 32px;
        font-weight: 800;
        color: #172033;
        margin-bottom: 3px;
    }

    .main-subtitle {
        font-size: 14px;
        color: #64748b;
        margin-bottom: 18px;
    }

    /* Cards */
    .metric-box {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 18px;
        min-height: 125px;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.05);
    }

    .metric-title {
        color: #64748b;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .metric-value {
        color: #172033;
        font-size: 28px;
        font-weight: 800;
    }

    .metric-unit {
        color: #64748b;
        font-size: 13px;
        font-weight: 500;
    }

    .metric-icon {
        font-size: 22px;
        margin-bottom: 7px;
    }

    /* Section title */
    .section-title {
        color: #172033;
        font-size: 20px;
        font-weight: 750;
        margin-top: 25px;
        margin-bottom: 12px;
    }

    /* Status */
    .normal-box {
        background: #ecfdf5;
        border: 1px solid #a7f3d0;
        border-radius: 14px;
        padding: 20px;
    }

    .warning-box {
        background: #fffbeb;
        border: 1px solid #fde68a;
        border-radius: 14px;
        padding: 20px;
    }

    .critical-box {
        background: #fef2f2;
        border: 1px solid #fecaca;
        border-radius: 14px;
        padding: 20px;
    }

    .health-number {
        font-size: 38px;
        font-weight: 800;
        color: #172033;
    }

    .health-label {
        color: #64748b;
        font-size: 12px;
        font-weight: 700;
    }

    /* Pipeline */
    .pipeline-box {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 14px;
        padding: 18px;
        text-align: center;
        min-height: 105px;
        box-shadow: 0 3px 12px rgba(15, 23, 42, 0.04);
    }

    .pipeline-icon {
        font-size: 24px;
    }

    .pipeline-name {
        color: #172033;
        font-size: 12px;
        font-weight: 700;
        margin-top: 7px;
    }

    /* Footer */
    .footer-text {
        text-align: center;
        color: #94a3b8;
        font-size: 11px;
        margin-top: 35px;
    }

</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🚆 Railway Monitor")

    st.caption("Railway Fault Diagnosis System")

    st.divider()

    st.subheader("Train Selection")

    train_id = st.selectbox(
        "Select Train",
        [
            "TRAIN_001",
            "TRAIN_002",
            "TRAIN_003"
        ]
    )

    live_monitoring = st.toggle(
        "Live Monitoring",
        value=True
    )

    st.divider()

    st.subheader("System Connections")

    st.success("MQTT  •  Connected")

    st.success("Simulator  •  Running")

    st.success("Fault Engine  •  Active")

    st.info("RAG  •  Standby")

    st.info("Local LLM  •  Standby")

    st.divider()

    st.caption("Railway Monitoring System")
    st.caption("Dashboard v1.0")


# =========================================================
# SENSOR DATA
# =========================================================

speed = random.randint(70, 115)

temperature = round(
    random.uniform(60, 90),
    2
)

vibration = round(
    random.uniform(2, 8),
    2
)

brake_pressure = round(
    random.uniform(4.5, 7),
    2
)

# =========================================================
# FAULT DETECTION
# =========================================================

faults = []

if temperature >= 85:
    faults.append("High Temperature")

if vibration >= 7.5:
    faults.append("High Vibration")

if brake_pressure < 5:
    faults.append("Low Brake Pressure")

if len(faults) > 0:

    if temperature >= 85 or vibration >= 7.5:
        overall_status = "CRITICAL"
        status_icon = "🔴"
    else:
        overall_status = "WARNING"
        status_icon = "🟠"

else:

    overall_status = "NORMAL"
    status_icon = "🟢"


# =========================================================
# HEALTH SCORE
# =========================================================

health = 100

if temperature > 75:
    health -= int((temperature - 75) * 1.5)

if vibration > 5:
    health -= int((vibration - 5) * 5)

if brake_pressure < 5.5:
    health -= int((5.5 - brake_pressure) * 8)

health = max(0, min(100, health))


# =========================================================
# HEADER
# =========================================================

st.markdown(
    "🚆 Railway Fault Diagnosis System",
    unsafe_allow_html=False
)

st.markdown(
    "Real-time railway condition monitoring and intelligent maintenance support",
    unsafe_allow_html=False
)

header_col1, header_col2 = st.columns([5, 1])

with header_col1:

    st.caption(
        f"Monitoring: {train_id}  •  "
        f"Last update: {datetime.now().strftime('%H:%M:%S')}"
    )

with header_col2:

    if live_monitoring:
        st.success("● LIVE")
    else:
        st.warning("● PAUSED")


# =========================================================
# SENSOR OVERVIEW
# =========================================================

st.markdown(
    '<div class="section-title">Current Sensor Status</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4 = st.columns(4)

with c1:

    st.markdown(
        '<div class="metric-box">'
        '<div class="metric-icon">⚡</div>'
        '<div class="metric-title">TRAIN SPEED</div>',
        unsafe_allow_html=True
    )

    st.metric(
        "Speed",
        f"{speed} km/h",
        label_visibility="collapsed"
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


with c2:

    st.markdown(
        '<div class="metric-box">'
        '<div class="metric-icon">🌡️</div>'
        '<div class="metric-title">TEMPERATURE</div>',
        unsafe_allow_html=True
    )

    st.metric(
        "Temperature",
        f"{temperature} °C",
        label_visibility="collapsed"
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


with c3:

    st.markdown(
        '<div class="metric-box">'
        '<div class="metric-icon">📳</div>'
        '<div class="metric-title">VIBRATION</div>',
        unsafe_allow_html=True
    )

    st.metric(
        "Vibration",
        f"{vibration} mm/s",
        label_visibility="collapsed"
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


with c4:

    st.markdown(
        '<div class="metric-box">'
        '<div class="metric-icon">🛑</div>'
        '<div class="metric-title">BRAKE PRESSURE</div>',
        unsafe_allow_html=True
    )

    st.metric(
        "Brake Pressure",
        f"{brake_pressure} bar",
        label_visibility="collapsed"
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# HISTORY
# =========================================================

if "sensor_history" not in st.session_state:

    st.session_state.sensor_history = []

reading = {
    "Time": datetime.now().strftime("%H:%M:%S"),
    "Speed": speed,
    "Temperature": temperature,
    "Vibration": vibration,
    "Brake Pressure": brake_pressure
}

st.session_state.sensor_history.append(reading)

st.session_state.sensor_history = \
    st.session_state.sensor_history[-30:]

df = pd.DataFrame(
    st.session_state.sensor_history
)


# =========================================================
# MAIN GRAPHS + HEALTH
# =========================================================

graph_col, health_col = st.columns([2.3, 1])

# ---------------- SENSOR GRAPH ----------------

with graph_col:

    st.markdown(
        '<div class="section-title">📊 Sensor Trend</div>',
        unsafe_allow_html=True
    )

    st.caption(
        "Live temperature and vibration behaviour"
    )

    if len(df) > 1:

        chart_df = df.set_index("Time")[
            ["Temperature", "Vibration"]
        ]

        st.line_chart(
            chart_df,
            height=360
        )

    else:

        st.info(
            "Collecting sensor readings..."
        )


# ---------------- HEALTH ----------------

with health_col:

    st.markdown(
        '<div class="section-title">❤️ Train Health</div>',
        unsafe_allow_html=True
    )

    if overall_status == "NORMAL":

        st.markdown(
            '<div class="normal-box">',
            unsafe_allow_html=True
        )

    elif overall_status == "WARNING":

        st.markdown(
            '<div class="warning-box">',
            unsafe_allow_html=True
        )

    else:

        st.markdown(
            '<div class="critical-box">',
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="health-label">OVERALL HEALTH</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f'<div class="health-number">{health}%</div>',
        unsafe_allow_html=True
    )

    st.progress(
        health / 100
    )

    st.markdown(
        f"<b>{status_icon} {overall_status}</b>",
        unsafe_allow_html=True
    )

    st.write("")

    st.write(
        f"Temperature: {temperature} °C"
    )

    st.write(
        f"Vibration: {vibration} mm/s"
    )

    st.write(
        f"Brake Pressure: {brake_pressure} bar"
    )

    st.markdown(
        '</div>',
        unsafe_allow_html=True
    )


# =========================================================
# TRAIN PERFORMANCE
# =========================================================

st.markdown(
    '<div class="section-title">📈 Train Performance</div>',
    unsafe_allow_html=True
)

st.caption(
    "Speed and brake pressure history"
)

if len(df) > 1:

    performance_df = df.set_index("Time")[
        ["Speed", "Brake Pressure"]
    ]

    st.line_chart(
        performance_df,
        height=300
    )


# =========================================================
# FAULT DETECTION + AI DIAGNOSIS
# =========================================================

fault_col, ai_col = st.columns(2)

# ---------------- FAULT DETECTION ----------------

with fault_col:

    st.markdown(
        '<div class="section-title">⚠️ Fault Detection</div>',
        unsafe_allow_html=True
    )

    if overall_status == "NORMAL":

        st.success(
            "🟢 No abnormal condition detected."
        )

        st.write(
            "All monitored parameters are currently "
            "within the configured operating range."
        )

    elif overall_status == "WARNING":

        st.warning(
            "🟠 Warning condition detected."
        )

        for fault in faults:
            st.write(
                f"• {fault}"
            )

    else:

        st.error(
            "🔴 Critical condition detected."
        )

        for fault in faults:
            st.write(
                f"• {fault}"
            )


# ---------------- AI DIAGNOSIS ----------------

with ai_col:

    st.markdown(
        '<div class="section-title">🤖 AI Diagnosis</div>',
        unsafe_allow_html=True
    )

    if overall_status == "NORMAL":

        st.info(
            "AI Assistant: No immediate maintenance "
            "recommendation."
        )

        st.write(
            "RAG knowledge retrieval will provide "
            "maintenance guidance when a fault is detected."
        )

    elif overall_status == "WARNING":

        st.warning(
            "AI Assistant: Parameter monitoring recommended."
        )

        st.write(
            "The system has identified abnormal sensor "
            "behaviour requiring further investigation."
        )

    else:

        st.error(
            "AI Assistant: Immediate inspection recommended."
        )

        st.write(
            "Critical sensor values have been detected. "
            "RAG + Local LLM can be used to generate "
            "a detailed maintenance diagnosis."
        )


# =========================================================
# PROJECT PIPELINE
# =========================================================

st.markdown(
    '<div class="section-title">🔗 System Pipeline</div>',
    unsafe_allow_html=True
)

p1, p2, p3, p4, p5, p6 = st.columns(6)

pipeline = [
    ("📡", "Sensors"),
    ("📨", "MQTT"),
    ("⚠️", "Fault Detection"),
    ("📚", "RAG"),
    ("🤖", "Local LLM"),
    ("👨‍🔧", "Maintenance")
]

for column, (icon, name) in zip(
    [p1, p2, p3, p4, p5, p6],
    pipeline
):

    with column:

        st.markdown(
            '<div class="pipeline-box">',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="pipeline-icon">{icon}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div class="pipeline-name">{name}</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            '</div>',
            unsafe_allow_html=True
        )


# =========================================================
# SYSTEM INFORMATION
# =========================================================

st.markdown(
    '<div class="section-title">⚙️ System Information</div>',
    unsafe_allow_html=True
)

i1, i2, i3, i4 = st.columns(4)

with i1:
    st.info(
        "MQTT\n\nConnected"
    )

with i2:
    st.info(
        "Database\n\nReady"
    )

with i3:
    st.info(
        "RAG Knowledge Base\n\nStandby"
    )

with i4:
    st.info(
        "Local LLM\n\nStandby"
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    '<div class="footer-text">'
    'Railway Fault Diagnosis & Monitoring System '
    '• IoT • MQTT • Fault Detection • RAG • Local LLM'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# AUTO REFRESH
# =========================================================

if live_monitoring:

    time.sleep(3)

    st.rerun()