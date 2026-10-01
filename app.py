"""
Railway Fault Diagnosis & Predictive Maintenance System
Official shadcn/ui Dashboard Template Implementation
"""

import streamlit as st
import pandas as pd
import numpy as np
import psycopg2
import os
import sys
import time
import re
import altair as alt
from datetime import datetime
from pathlib import Path

# Setup Project Root & Path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR) if os.path.basename(CURRENT_DIR).lower() == "dashboard" else CURRENT_DIR

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

os.chdir(PROJECT_ROOT)

# Import existing backend modules (preserved 100%)
from fault_detection.detector import detect_fault
from ai_diagnosis import (
    build_knowledge_index,
    retrieve_knowledge,
    get_ai_diagnosis
)
try:
    from dashboard.ui_components import (
        inject_custom_css,
        render_header,
        metric_card,
        section_header,
        info_card,
        status_badge,
        fault_status_card,
        risk_assessment_card,
        risk_card,
        ai_card,
        pipeline_diagram,
        scada_footer,
        parse_ai_diagnosis,
        icon_svg
    )
except ImportError:
    from ui_components import (
        inject_custom_css,
        render_header,
        metric_card,
        section_header,
        info_card,
        status_badge,
        fault_status_card,
        risk_assessment_card,
        risk_card,
        ai_card,
        pipeline_diagram,
        scada_footer,
        parse_ai_diagnosis,
        icon_svg
    )


# ============================================================
# 1. PAGE CONFIGURATION & SHADCN/UI CSS INJECTION
# ============================================================

st.set_page_config(
    page_title="Railway Intelligence | shadcn/ui Dashboard",
    page_icon="🚆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Manage Theme (Default: White Theme / Light Mode)
if "app_theme" not in st.session_state:
    st.session_state.app_theme = "light"

inject_custom_css(theme=st.session_state.app_theme)
is_light = (st.session_state.app_theme == "light")


# ============================================================
# 2. DATABASE & DATASET CONFIGURATION
# ============================================================

DB_CONFIG = {
    "host": "localhost",
    "database": "railway_monitoring",
    "user": "postgres",
    "password": "123@abesec",
    "port": "5432",
    "connect_timeout": 3
}

DATA_PATH = os.path.join(
    PROJECT_ROOT,
    "Data",
    "raw",
    "indian_railway_predictive_maintenance_100k.csv"
)


@st.cache_data(show_spinner=False)
def load_fleet_dataset():
    """Loads and caches the 100k railway predictive maintenance dataset."""
    if os.path.exists(DATA_PATH):
        try:
            return pd.read_csv(DATA_PATH)
        except Exception:
            return pd.DataFrame()
    return pd.DataFrame()


def get_db_connection():
    """Returns a psycopg2 database connection with graceful error handling."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception:
        return None


@st.cache_resource(show_spinner=False)
def get_cached_rag_resources():
    """Caches the RAG FAISS index and SentenceTransformer embeddings."""
    try:
        model, index, chunks = build_knowledge_index()
        return model, index, chunks
    except Exception:
        return None, None, None


# Load Dataset
fleet_df = load_fleet_dataset()

# Test DB Connection
db_conn = get_db_connection()
db_connected = db_conn is not None

# Query DB Telemetry if available
live_sensor_df = pd.DataFrame()
live_fault_df = pd.DataFrame()
db_train_list = []

if db_connected:
    try:
        db_train_query = "SELECT DISTINCT train_id FROM sensor_readings ORDER BY train_id;"
        db_train_df = pd.read_sql(db_train_query, db_conn)
        db_train_list = db_train_df["train_id"].tolist() if not db_train_df.empty else []
    except Exception:
        db_train_list = []

# ============================================================
# 3. SHADCN/UI SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 0.625rem; padding: 0.25rem 0 0.5rem 0;">
        <div style="background-color: {'#18181b' if is_light else '#fafafa'}; color: {'#ffffff' if is_light else '#18181b'}; padding: 0.35rem; border-radius: 0.375rem; display: flex; align-items: center; justify-content: center;">
            {icon_svg('train', size=18, color='#ffffff' if is_light else '#18181b')}
        </div>
        <div>
            <div style="font-size: 0.9375rem; font-weight: 600; color: {'#09090b' if is_light else '#fafafa'}; letter-spacing: -0.02em;">
                Railway Intelligence
            </div>
            <div style="font-size: 0.75rem; color: {'#71717a' if is_light else '#a1a1aa'};">Predictive Maintenance</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Theme Switcher (Default: White / Light Theme)
    st.markdown('<div style="font-size: 0.6875rem; font-weight: 600; text-transform: uppercase; color: #71717a; letter-spacing: 0.05em; margin-bottom: 0.375rem;">Color Theme</div>', unsafe_allow_html=True)
    theme_choice = st.radio(
        "Theme",
        ["☀️ Light (Clean White)", "🌙 Dark (Zinc)"],
        index=0 if st.session_state.app_theme == "light" else 1,
        label_visibility="collapsed",
        key="theme_radio_select"
    )
    chosen_theme = "light" if "Light" in theme_choice else "dark"
    if chosen_theme != st.session_state.app_theme:
        st.session_state.app_theme = chosen_theme
        st.rerun()

    st.divider()

    # System Status Section
    st.markdown('<div style="font-size: 0.6875rem; font-weight: 600; text-transform: uppercase; color: #71717a; letter-spacing: 0.05em; margin-bottom: 0.5rem;">System Status</div>', unsafe_allow_html=True)

    if not fleet_df.empty:
        st.markdown(f"""
        <div class="shadcn-card" style="padding: 0.75rem; margin-bottom: 0.5rem;">
            <div style="font-size: 0.6875rem; color: {'#71717a' if is_light else '#a1a1aa'}; text-transform: uppercase;">Dataset Fleet Store</div>
            <div style="font-size: 0.9375rem; font-weight: 600; color: {'#09090b' if is_light else '#fafafa'}; margin-top: 0.15rem; display: flex; align-items: center; gap: 0.375rem;">
                <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background-color: #16a34a;"></span>
                {len(fleet_df):,} Records
            </div>
            <div style="font-size: 0.6875rem; color: {'#71717a' if is_light else '#a1a1aa'}; margin-top: 0.2rem;">35 Telemetry Channels</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="shadcn-card" style="padding: 0.75rem; margin-bottom: 0.5rem;">
            <div style="font-size: 0.6875rem; color: #71717a;">Dataset Fleet Store</div>
            <div style="font-size: 0.875rem; font-weight: 600; color: #dc2626;">Offline</div>
        </div>
        """, unsafe_allow_html=True)

    if db_connected:
        st.markdown(f"""
        <div class="shadcn-card" style="padding: 0.75rem; margin-bottom: 0.5rem;">
            <div style="font-size: 0.6875rem; color: {'#71717a' if is_light else '#a1a1aa'}; text-transform: uppercase;">PostgreSQL Database</div>
            <div style="font-size: 0.9375rem; font-weight: 600; color: {'#09090b' if is_light else '#fafafa'}; margin-top: 0.15rem; display: flex; align-items: center; gap: 0.375rem;">
                <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background-color: #16a34a;"></span>
                Connected (:5432)
            </div>
            <div style="font-size: 0.6875rem; color: {'#71717a' if is_light else '#a1a1aa'}; margin-top: 0.2rem;">railway_monitoring</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="shadcn-card" style="padding: 0.75rem; margin-bottom: 0.5rem;">
            <div style="font-size: 0.6875rem; color: #71717a;">PostgreSQL Database</div>
            <div style="font-size: 0.875rem; font-weight: 600; color: #d97706;">Local Dataset Mode</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="shadcn-card" style="padding: 0.75rem; margin-bottom: 0.75rem;">
        <div style="font-size: 0.6875rem; color: {'#71717a' if is_light else '#a1a1aa'}; text-transform: uppercase; margin-bottom: 0.35rem;">Pipeline Engines</div>
        <div style="font-size: 0.75rem; color: {'#3f3f46' if is_light else '#d4d4d8'}; display: flex; flex-direction: column; gap: 0.25rem;">
            <div><span style="color: #16a34a;">●</span> MQTT Broker (:1883)</div>
            <div><span style="color: #8b5cf6;">●</span> Ollama LLM (Llama 3.2)</div>
            <div><span style="color: #2563eb;">●</span> FAISS RAG Index</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # Workspace Mode Selector
    st.markdown('<div style="font-size: 0.6875rem; font-weight: 600; text-transform: uppercase; color: #71717a; letter-spacing: 0.05em; margin-bottom: 0.375rem;">Workspace Mode</div>', unsafe_allow_html=True)
    
    monitoring_mode = st.radio(
        "Select Workspace Mode",
        [
            "🛰️ Fleet Predictive Maintenance (100k Dataset)",
            "⚡ Live IoT Telemetry (PostgreSQL Stream)"
        ],
        label_visibility="collapsed"
    )

    is_fleet_mode = "Fleet" in monitoring_mode

    st.divider()

    # Train Selection
    st.markdown('<div style="font-size: 0.6875rem; font-weight: 600; text-transform: uppercase; color: #71717a; letter-spacing: 0.05em; margin-bottom: 0.375rem;">Train Selection</div>', unsafe_allow_html=True)

    if is_fleet_mode:
        if not fleet_df.empty:
            filter_choice = st.selectbox(
                "Condition Filter",
                ["All Fleet Units", "Critical Anomaly Units", "Warning Condition Units", "Normal Units"],
                label_visibility="collapsed"
            )

            if filter_choice == "Critical Anomaly Units":
                filtered_trains = fleet_df[fleet_df["risk_score"] >= 80]["train_id"].head(50).tolist()
            elif filter_choice == "Warning Condition Units":
                filtered_trains = fleet_df[(fleet_df["risk_score"] >= 50) & (fleet_df["risk_score"] < 80)]["train_id"].head(50).tolist()
            elif filter_choice == "Normal Units":
                filtered_trains = fleet_df[fleet_df["risk_score"] < 50]["train_id"].head(50).tolist()
            else:
                filtered_trains = fleet_df["train_id"].head(100).tolist()

            if not filtered_trains:
                filtered_trains = fleet_df["train_id"].head(100).tolist()

            selected_train_id = st.selectbox(
                "Select Train Unit ID",
                filtered_trains,
                format_func=lambda x: f"Train #{x}"
            )
            selected_train_display = f"TRAIN #{selected_train_id}"
        else:
            selected_train_id = 1
            selected_train_display = "TRAIN #1"
    else:
        if db_train_list:
            live_train_options = ["All Trains"] + db_train_list
            selected_live_train = st.selectbox(
                "Select Live Train Stream",
                live_train_options
            )
            selected_train_display = selected_live_train
        else:
            selected_live_train = "TRAIN_001"
            selected_train_display = "TRAIN_001"

    st.divider()

    # Manual Sync Button
    if st.button("🔄 Sync Telemetry", use_container_width=True):
        st.rerun()


# ============================================================
# 4. DATA RETRIEVAL (FLEET VS LIVE)
# ============================================================

current_time_str = datetime.now().strftime("%H:%M:%S")

if is_fleet_mode and not fleet_df.empty:
    matched_records = fleet_df[fleet_df["train_id"] == selected_train_id]
    if not matched_records.empty:
        record = matched_records.iloc[0]
    else:
        record = fleet_df.iloc[0]

    fault_result = detect_fault(record)
    fault_status = fault_result["status"]
    detected_faults = fault_result["faults"]
    risk_level = fault_result["risk_level"]
    detected_risk_score = fault_result["risk_score"]

    speed_val = record["average_speed_kmph"]
    bearing_temp_val = record["bearing_temperature_c"]
    track_vib_val = record["track_vibration_level"]
    if pd.isna(track_vib_val):
        track_vib_val = 0.0
    brake_pressure_val = record["brake_pressure_psi"]

    train_id_val = str(record["train_id"])
    region_val = str(record.get("region", "Northern Railway"))
    train_type_val = str(record.get("train_type", "High-Speed Express"))
    train_age_val = f"{record.get('train_age_years', 4)} Years"

    dataset_risk_score_val = record.get("risk_score", 0.0)
    sensor_health_val = record.get("sensor_health_index", 92.0)
    failure_severity_val = record.get("failure_severity", "Normal")
    dataset_failure_type = record.get("failure_type", None)

    distance_val = f"{record.get('distance_travelled_km', 0):,.0f} km"
    delay_val = f"{record.get('delay_minutes', 0):.0f} min"
    load_factor_val = f"{record.get('load_factor_percent', 0):.1f}%"
    daily_trips_val = f"{record.get('daily_trips', 0):.0f} trips/day"

    last_maint_val = f"{record.get('last_maintenance_days', 0):.0f} days ago"
    inspection_score_val = f"{record.get('inspection_score', 0):.1f} / 100"
    wheel_wear_val = f"{record.get('wheel_wear_percent', 0):.1f}%"
    rail_wear_val = f"{record.get('rail_wear_mm', 0):.2f} mm"
    maintenance_required = record.get("maintenance_required", 0)

else:
    if db_connected:
        try:
            if selected_live_train == "All Trains":
                sensor_q = "SELECT * FROM sensor_readings ORDER BY id DESC LIMIT 50;"
                fault_q = "SELECT * FROM fault_results ORDER BY id DESC LIMIT 50;"
                live_sensor_df = pd.read_sql(sensor_q, db_conn)
                live_fault_df = pd.read_sql(fault_q, db_conn)
            else:
                sensor_q = "SELECT * FROM sensor_readings WHERE train_id = %s ORDER BY id DESC LIMIT 50;"
                fault_q = "SELECT * FROM fault_results WHERE train_id = %s ORDER BY id DESC LIMIT 50;"
                live_sensor_df = pd.read_sql(sensor_q, db_conn, params=(selected_live_train,))
                live_fault_df = pd.read_sql(fault_q, db_conn, params=(selected_live_train,))
        except Exception:
            live_sensor_df = pd.DataFrame()
            live_fault_df = pd.DataFrame()

    if not live_sensor_df.empty:
        latest_sensor = live_sensor_df.iloc[0]
        speed_val = latest_sensor.get("speed", 82.0)
        bearing_temp_val = latest_sensor.get("temperature", 72.0)
        track_vib_val = latest_sensor.get("vibration", 3.2)
        brake_pressure_val = latest_sensor.get("brake_pressure", 70.0)
        train_id_val = str(latest_sensor.get("train_id", selected_live_train))
    else:
        speed_val = 84.5
        bearing_temp_val = 74.2
        track_vib_val = 3.8
        brake_pressure_val = 72.1
        train_id_val = selected_live_train

    if not live_fault_df.empty:
        latest_fault = live_fault_df.iloc[0]
        raw_fault_str = str(latest_fault.get("faults", "No Fault"))
        risk_level = str(latest_fault.get("risk", "LOW")).upper()
        detected_faults = [f.strip() for f in raw_fault_str.split(",") if f.strip() and f.strip() != "No Fault"]
        if detected_faults:
            fault_status = "CRITICAL" if risk_level == "HIGH" else "WARNING"
        else:
            fault_status = "NORMAL"
    else:
        raw_fault_str = "No Fault"
        risk_level = "LOW"
        detected_faults = []
        fault_status = "NORMAL"

    detected_risk_score = 85.0 if risk_level == "HIGH" else (55.0 if risk_level == "MEDIUM" else 18.0)
    dataset_risk_score_val = detected_risk_score
    sensor_health_val = 100.0 - detected_risk_score
    failure_severity_val = "Critical" if risk_level == "HIGH" else ("Elevated" if risk_level == "MEDIUM" else "Nominal")
    dataset_failure_type = raw_fault_str if raw_fault_str != "No Fault" else None

    region_val = "Northern Railway Telemetry Grid"
    train_type_val = "Heavy Freight Telemetry Line"
    train_age_val = "5 Years (Active Telemetry)"

    distance_val = "142,800 km"
    delay_val = "4 min"
    load_factor_val = "82.4%"
    daily_trips_val = "8 trips/day"

    last_maint_val = "12 days ago"
    inspection_score_val = "89.5 / 100"
    wheel_wear_val = "34.2%"
    rail_wear_val = "2.10 mm"
    maintenance_required = 1 if risk_level == "HIGH" else 0


# ============================================================
# 5. SHADCN/UI TOP HEADER
# ============================================================

render_header(
    train_id_display=selected_train_display,
    is_online=True,
    last_sync=current_time_str
)

# ============================================================
# 6. SHADCN/UI METRIC CARDS (Top KPI Grid)
# ============================================================

speed_status = "warning" if speed_val > 105 else ("critical" if speed_val > 120 else "normal")
bearing_status = "critical" if bearing_temp_val >= 80 else ("warning" if bearing_temp_val >= 72 else "normal")
vib_status = "critical" if track_vib_val >= 7.0 else ("warning" if track_vib_val >= 4.0 else "normal")
brake_status = "critical" if brake_pressure_val < 60 else ("warning" if brake_pressure_val < 70 else "normal")

col1, col2, col3, col4 = st.columns(4)

with col1:
    metric_card(
        title="Train Speed",
        value=f"{speed_val:.1f}",
        unit="km/h",
        icon_name="speed",
        status=speed_status,
        subtitle="Nominal: 70–100 km/h"
    )

with col2:
    metric_card(
        title="Bearing Temperature",
        value=f"{bearing_temp_val:.1f}",
        unit="°C",
        icon_name="temp",
        status=bearing_status,
        subtitle="Threshold: < 80 °C"
    )

with col3:
    metric_card(
        title="Track Vibration",
        value=f"{track_vib_val:.2f}",
        unit="mm/s",
        icon_name="vib",
        status=vib_status,
        subtitle="Tolerance: < 7.0 mm/s"
    )

with col4:
    metric_card(
        title="Brake Pressure",
        value=f"{brake_pressure_val:.1f}",
        unit="psi",
        icon_name="brake",
        status=brake_status,
        subtitle="Baseline: ≥ 70 psi"
    )

# ============================================================
# 7. TRAIN INFORMATION SECTION
# ============================================================

section_header(
    title="Train Unit Information",
    subtitle="Operational specifications, assignment corridor, and asset lifecycle data",
    icon_name="train",
    badge=selected_train_display
)

tcol1, tcol2, tcol3, tcol4 = st.columns(4)

with tcol1:
    info_card(
        title="Train Asset ID",
        value=selected_train_display,
        subtitle="Active Monitoring Unit",
        icon_name="train"
    )

with tcol2:
    info_card(
        title="Operating Region",
        value=region_val,
        subtitle="Zonal Railway Command",
        icon_name="compass"
    )

with tcol3:
    info_card(
        title="Rolling Stock Type",
        value=train_type_val,
        subtitle="Service Classification",
        icon_name="layers"
    )

with tcol4:
    info_card(
        title="Asset Service Age",
        value=train_age_val,
        subtitle="Mid-Lifecycle Operations",
        icon_name="clock"
    )

# ============================================================
# 8. FAULT DETECTION & RISK ASSESSMENT (DUAL COLUMN)
# ============================================================

f_col, r_col = st.columns([1.1, 0.9])

with f_col:
    section_header(
        title="Fault Detection Status",
        subtitle="Multi-parameter telemetry anomaly analysis & threshold verification",
        icon_name="alert_triangle"
    )
    fault_status_card(
        status=fault_status,
        detected_faults=detected_faults,
        dataset_failure=dataset_failure_type
    )

with r_col:
    section_header(
        title="Risk & Health Assessment",
        subtitle="Ground truth baseline vs dynamic sensor health scoring",
        icon_name="activity"
    )
    risk_assessment_card(
        risk_level=risk_level,
        detected_risk_score=detected_risk_score,
        dataset_risk_score=dataset_risk_score_val,
        sensor_health=sensor_health_val,
        severity=failure_severity_val
    )

# ============================================================
# 9. AI RAILWAY DIAGNOSIS (CRITICAL SECTION)
# ============================================================

section_header(
    title="AI Railway Diagnosis Engine",
    subtitle="AI-powered fault analysis using sensor data, railway fault knowledge and local LLM reasoning.",
    icon_name="sparkles",
    badge="RAG + Ollama (Llama 3.2)"
)

ai_session_key = f"diagnosis_{selected_train_display}_{fault_status}"
if ai_session_key not in st.session_state:
    st.session_state[ai_session_key] = None

if detected_faults:
    query_fault_str = ", ".join(detected_faults)
elif dataset_failure_type and str(dataset_failure_type).lower() != "nan":
    query_fault_str = str(dataset_failure_type)
else:
    query_fault_str = "Nominal Parameters - No Active Fault"

ai_action_col1, ai_action_col2 = st.columns([3, 1])

with ai_action_col1:
    st.markdown(f"""
    <div class="shadcn-card" style="padding: 0.75rem 1rem; font-size: 0.8125rem; color: {'#71717a' if is_light else '#a1a1aa'};">
        Target Unit: <strong style="color: {'#09090b' if is_light else '#fafafa'};">{selected_train_display}</strong> &nbsp;|&nbsp; 
        Active Condition: <strong style="color: {'#dc2626' if fault_status=='CRITICAL' else ('#d97706' if fault_status=='WARNING' else '#16a34a')};">{query_fault_str}</strong> &nbsp;|&nbsp; 
        Risk Grade: <strong style="color: {'#09090b' if is_light else '#fafafa'};">{risk_level}</strong>
    </div>
    """, unsafe_allow_html=True)

with ai_action_col2:
    generate_ai_btn = st.button("Generate AI Diagnosis", use_container_width=True, key="ai_diag_btn_shadcn")

if generate_ai_btn:
    with st.spinner("Searching RAG knowledge base & generating AI diagnosis via local Ollama (Llama 3.2)..."):
        try:
            model, index, chunks = get_cached_rag_resources()

            if model and index and chunks:
                retrieved_knowledge = retrieve_knowledge(
                    query_fault_str,
                    model,
                    index,
                    chunks
                )
            else:
                retrieved_knowledge = "Railway maintenance standards: inspect bearings, wheel profiles, track alignment, and brake pneumatic pressures."

            raw_ai_response = get_ai_diagnosis(
                train_id=selected_train_display,
                fault=query_fault_str,
                risk=risk_level,
                knowledge=retrieved_knowledge
            )

            if "❌" in raw_ai_response or "failed" in raw_ai_response.lower():
                st.warning("⚠ AI diagnosis temporarily unavailable. Please verify that Ollama is running (`ollama run llama3.2`).")
            else:
                parsed_sections = parse_ai_diagnosis(raw_ai_response)
                st.session_state[ai_session_key] = {
                    "raw": raw_ai_response,
                    "parsed": parsed_sections,
                    "knowledge": retrieved_knowledge,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                }
                st.toast("AI Diagnosis generated successfully.", icon="🤖")

        except Exception:
            st.warning("⚠ AI diagnosis temporarily unavailable. Please verify that Ollama is running (`ollama run llama3.2`).")

cached_ai_result = st.session_state.get(ai_session_key, None)

if cached_ai_result and cached_ai_result.get("parsed"):
    parsed = cached_ai_result["parsed"]
    
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    
    ai_c1, ai_c2 = st.columns(2)
    with ai_c1:
        ai_card(
            title="Subsystem Diagnosis",
            content=parsed.get("diagnosis", "Sensor anomaly detected."),
            icon_name="sparkles"
        )
    with ai_c2:
        ai_card(
            title="Possible Root Causes",
            content=parsed.get("possible_causes", "Mechanical vibration or elevated bearing thermal friction."),
            icon_name="cpu"
        )

    st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)

    ai_c3, ai_c4 = st.columns(2)
    with ai_c3:
        ai_card(
            title="Recommended Engineering Action",
            content=parsed.get("recommended_action", "Schedule immediate physical depot inspection of wheelset and axle bearings."),
            icon_name="wrench"
        )
    with ai_c4:
        ai_card(
            title="Safety & Operational Directives",
            content=parsed.get("safety_recommendation", "Impose temporary speed restriction and enforce standard workshop PPE."),
            icon_name="shield"
        )

    with st.expander("Retrieved Engineering Knowledge (FAISS Vector Index)", expanded=False):
        st.markdown(f"""
        ```markdown
        {cached_ai_result.get('knowledge', 'No external chunks retrieved.')}
        ```
        """)
        st.caption(f"Knowledge retrieved at {cached_ai_result.get('timestamp')} via SentenceTransformers (all-MiniLM-L6-v2) & FAISS L2 Index.")
else:
    if fault_status == "NORMAL":
        st.info("🟢 All monitored parameters are within nominal safety envelopes. Click 'Generate AI Diagnosis' to run a proactive advisory check.")
    else:
        st.info("💡 Sensor anomalies detected. Click **Generate AI Diagnosis** above to invoke the LangChain RAG pipeline and Ollama Llama-3.2 reasoning.")

# ============================================================
# 10. MULTI-CHANNEL SENSOR ANALYTICS (SHADCN CHART)
# ============================================================

section_header(
    title="Sensor Analytics & Telemetry Channels",
    subtitle="Continuous breakdown across 8 mission-critical railway channels",
    icon_name="activity"
)

if is_fleet_mode and not fleet_df.empty:
    sensors_dict = {
        "Train Speed": (record["average_speed_kmph"], "km/h", 100.0),
        "Track Temperature": (record["track_temperature_c"], "°C", 50.0),
        "Track Vibration": (record["track_vibration_level"] if not pd.isna(record["track_vibration_level"]) else 0.0, "mm/s", 7.0),
        "Axle Temperature": (record["axle_temperature_c"], "°C", 75.0),
        "Bearing Temperature": (record["bearing_temperature_c"], "°C", 80.0),
        "Brake Pressure": (record["brake_pressure_psi"], "psi", 70.0),
        "Battery Voltage": (record["battery_voltage"], "V", 24.0),
        "Traction Motor Temp": (record["traction_motor_temp_c"], "°C", 85.0),
    }
else:
    sensors_dict = {
        "Train Speed": (speed_val, "km/h", 100.0),
        "Track Temperature": (42.5, "°C", 50.0),
        "Track Vibration": (track_vib_val, "mm/s", 7.0),
        "Axle Temperature": (64.2, "°C", 75.0),
        "Bearing Temperature": (bearing_temp_val, "°C", 80.0),
        "Brake Pressure": (brake_pressure_val, "psi", 70.0),
        "Battery Voltage": (24.2, "V", 24.0),
        "Traction Motor Temp": (78.5, "°C", 85.0),
    }

sensor_chart_rows = []
for s_name, (s_val, s_unit, s_limit) in sensors_dict.items():
    if s_name == "Brake Pressure":
        st_label = "Critical" if s_val < 60 else ("Warning" if s_val < 70 else "Normal")
    elif s_name == "Battery Voltage":
        st_label = "Warning" if s_val < 22 else "Normal"
    else:
        st_label = "Critical" if s_val >= s_limit else ("Warning" if s_val >= (s_limit * 0.88) else "Normal")

    sensor_chart_rows.append({
        "Sensor": s_name,
        "Value": round(float(s_val), 2),
        "Unit": s_unit,
        "Status": st_label,
        "Limit": s_limit
    })

sensor_plot_df = pd.DataFrame(sensor_chart_rows)

# Clean shadcn monochromatic + semantic accent scale
if is_light:
    color_scale = alt.Scale(
        domain=["Normal", "Warning", "Critical"],
        range=["#18181b", "#d97706", "#dc2626"]
    )
    chart_bg = "#ffffff"
    axis_color = "#71717a"
    grid_color = "#f4f4f5"
    domain_color = "#e4e4e7"
else:
    color_scale = alt.Scale(
        domain=["Normal", "Warning", "Critical"],
        range=["#fafafa", "#fbbf24", "#f87171"]
    )
    chart_bg = "#09090b"
    axis_color = "#a1a1aa"
    grid_color = "#27272a"
    domain_color = "#27272a"

telemetry_chart = alt.Chart(sensor_plot_df).mark_bar(
    cornerRadiusTopRight=4,
    cornerRadiusBottomRight=4,
    size=18
).encode(
    y=alt.Y("Sensor:N", sort=None, title=None),
    x=alt.X("Value:Q", title="Observed Telemetry Value"),
    color=alt.Color("Status:N", scale=color_scale, legend=alt.Legend(title="Status", orient="top")),
    tooltip=[
        alt.Tooltip("Sensor:N", title="Sensor"),
        alt.Tooltip("Value:Q", title="Value"),
        alt.Tooltip("Unit:N", title="Unit"),
        alt.Tooltip("Status:N", title="Condition"),
        alt.Tooltip("Limit:Q", title="Limit")
    ]
).properties(
    height=320,
    background=chart_bg
).configure_axis(
    labelColor=axis_color,
    titleColor=axis_color,
    gridColor=grid_color,
    domainColor=domain_color,
    labelFontSize=12,
    titleFontSize=12
).configure_view(
    strokeWidth=0
)

st.altair_chart(telemetry_chart, use_container_width=True)

# ============================================================
# 11. OPERATIONS & MAINTENANCE GRIDS
# ============================================================

op_col, mt_col = st.columns(2)

with op_col:
    section_header(
        title="Fleet Operational Metrics",
        subtitle="Deployment runtime, scheduling delays, and payload coefficients",
        icon_name="activity"
    )
    oc1, oc2 = st.columns(2)
    with oc1:
        info_card(title="Distance Travelled", value=distance_val, subtitle="Cumulative Kilometer Count", icon_name="compass")
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        info_card(title="Payload Coefficient", value=load_factor_val, subtitle="Current Capacity Utilization", icon_name="layers")
    with oc2:
        info_card(title="Schedule Variance", value=delay_val, subtitle="Station Time Deviation", icon_name="clock")
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        info_card(title="Daily Frequency", value=daily_trips_val, subtitle="Daily Route Invocations", icon_name="train")

with mt_col:
    section_header(
        title="Predictive Maintenance Status",
        subtitle="Shop interval inspection ratings, wheel wear and depot schedules",
        icon_name="wrench"
    )
    mc1, mc2 = st.columns(2)
    with mc1:
        info_card(title="Last Depot Check", value=last_maint_val, subtitle="Days Since Physical Inspection", icon_name="clock")
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        info_card(title="Wheel Flange Wear", value=wheel_wear_val, subtitle="Mechanical Wear Measure", icon_name="wrench")
    with mc2:
        info_card(title="Inspection Score", value=inspection_score_val, subtitle="Safety Compliance Rating", icon_name="shield")
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        info_card(title="Track Rail Wear", value=rail_wear_val, subtitle="Linear Rail Wear Loss", icon_name="activity")

    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    if maintenance_required == 1:
        st.markdown("""
        <div class="shadcn-alert alert-warning" style="margin-bottom: 0;">
            <div class="shadcn-alert-title">
                <span>⚠️</span>
                <span>Maintenance Service Order Required</span>
            </div>
            <div class="shadcn-alert-desc">
                Elevated sensor parameters or inspection wear criteria have triggered a mandatory depot maintenance service order.
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="shadcn-alert alert-normal" style="margin-bottom: 0;">
            <div class="shadcn-alert-title">
                <span>✓</span>
                <span>Maintenance Not Required</span>
            </div>
            <div class="shadcn-alert-desc">
                Asset is operating within calibrated mechanical tolerances. Routine service schedule remains in effect.
            </div>
        </div>
        """, unsafe_allow_html=True)

# ============================================================
# 12. SHADCN/UI SYSTEM PIPELINE (ARCHITECTURE)
# ============================================================

section_header(
    title="System Architecture & Data Pipeline",
    subtitle="End-to-end telemetry flow: IoT ingestion, fault classification, FAISS RAG, and local LLM diagnosis",
    icon_name="layers"
)

pipeline_diagram()

# ============================================================
# 13. DATASET INFORMATION & DATABASE AUDIT LOGS (SHADCN TABS)
# ============================================================

section_header(
    title="Dataset Records & Telemetry Logs",
    subtitle="Detailed inspection of 100,000 historical records and live PostgreSQL telemetry tables",
    icon_name="database"
)

with st.expander("Indian Railway Predictive Maintenance Dataset & Raw Telemetry Stream", expanded=False):
    tab1, tab2, tab3 = st.tabs([
        "Fleet Dataset (100k Records)",
        "PostgreSQL Sensor Stream",
        "PostgreSQL Fault Logs"
    ])

    with tab1:
        if not fleet_df.empty:
            st.markdown(f"**Total Registered Records:** `{len(fleet_df):,}` &nbsp;|&nbsp; **Features:** `{len(fleet_df.columns)}`")
            st.dataframe(fleet_df.head(15), use_container_width=True)
        else:
            st.info("Dataset CSV not loaded.")

    with tab2:
        if db_connected and not live_sensor_df.empty:
            st.markdown("**Live Database Telemetry Stream** (`sensor_readings` table)")
            st.dataframe(live_sensor_df, use_container_width=True)
        elif db_connected:
            st.info("No records found in `sensor_readings` for selected filter.")
        else:
            st.warning("PostgreSQL database is currently disconnected. Run `psql` or launch database service on port 5432.")

    with tab3:
        if db_connected and not live_fault_df.empty:
            st.markdown("**Live Database Fault Results** (`fault_results` table)")
            st.dataframe(live_fault_df, use_container_width=True)

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            st.markdown("**Historical Fault Frequency Distribution:**")
            fault_counts = live_fault_df["faults"].value_counts().reset_index()
            fault_counts.columns = ["Fault Condition", "Incidents"]
            st.bar_chart(fault_counts.set_index("Fault Condition"))
        elif db_connected:
            st.info("No fault logs found in `fault_results` table.")
        else:
            st.warning("PostgreSQL database is currently disconnected.")

# ============================================================
# 14. CLOSE DATABASE CONNECTION & RENDER FOOTER
# ============================================================

if db_conn:
    try:
        db_conn.close()
    except Exception:
        pass

scada_footer()