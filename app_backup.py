import streamlit as st
import psycopg2
import pandas as pd

from ai_diagnosis import (
    build_knowledge_index,
    retrieve_knowledge,
    get_ai_diagnosis
)


# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="Railway Monitoring",
    page_icon="🚆",
    layout="wide"
)

st.title("🚆 Railway Monitoring Dashboard")
st.caption("Real-Time Train Sensor & AI Fault Monitoring")


# ==============================
# REFRESH BUTTON
# ==============================

if st.button("🔄 Refresh Data"):
    st.rerun()


# ==============================
# DATABASE CONNECTION
# ==============================

conn = psycopg2.connect(
    host="localhost",
    database="railway_monitoring",
    user="postgres",
    password="123@abesec",
    port="5432"
)


# ==============================
# GET TRAINS
# ==============================

train_query = """
SELECT DISTINCT train_id
FROM sensor_readings
ORDER BY train_id
"""

train_df = pd.read_sql(train_query, conn)


# ==============================
# TRAIN FILTER
# ==============================

if not train_df.empty:

    train_list = ["All Trains"] + train_df["train_id"].tolist()

    selected_train = st.selectbox(
        "🚆 Select Train",
        train_list
    )

else:

    selected_train = "All Trains"


# ==============================
# SENSOR DATA
# ==============================

if selected_train == "All Trains":

    sensor_query = """
    SELECT *
    FROM sensor_readings
    ORDER BY id DESC
    LIMIT 50
    """

    sensor_df = pd.read_sql(
        sensor_query,
        conn
    )

else:

    sensor_query = """
    SELECT *
    FROM sensor_readings
    WHERE train_id = %s
    ORDER BY id DESC
    LIMIT 50
    """

    sensor_df = pd.read_sql(
        sensor_query,
        conn,
        params=(selected_train,)
    )


# ==============================
# FAULT DATA
# ==============================

if selected_train == "All Trains":

    fault_query = """
    SELECT *
    FROM fault_results
    ORDER BY id DESC
    LIMIT 50
    """

    fault_df = pd.read_sql(
        fault_query,
        conn
    )

else:

    fault_query = """
    SELECT *
    FROM fault_results
    WHERE train_id = %s
    ORDER BY id DESC
    LIMIT 50
    """

    fault_df = pd.read_sql(
        fault_query,
        conn,
        params=(selected_train,)
    )


# ==============================
# CURRENT TRAIN STATUS
# ==============================

if not sensor_df.empty:

    latest = sensor_df.iloc[0]

    st.subheader("📊 Current Train Status")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🚆 Train",
        latest["train_id"]
    )

    col2.metric(
        "⚡ Speed",
        f'{latest["speed"]:.2f}'
    )

    col3.metric(
        "📳 Vibration",
        f'{latest["vibration"]:.2f}'
    )

    col4.metric(
        "🌡️ Temperature",
        f'{latest["temperature"]:.2f}'
    )


# ==============================
# SYSTEM OVERVIEW
# ==============================

st.subheader("📊 System Overview")

total_readings = len(sensor_df)

if not fault_df.empty:
    total_faults = len(
        fault_df[fault_df["faults"] != "No Fault"]
    )
else:
    total_faults = 0


col1, col2 = st.columns(2)

with col1:

    st.metric(
        "📡 Total Sensor Readings",
        total_readings
    )

with col2:

    st.metric(
        "🚨 Total Faults",
        total_faults
    )


# ==============================
# RISK SUMMARY
# ==============================

st.subheader("⚠️ Risk Summary")

if not fault_df.empty:

    low = len(
        fault_df[fault_df["risk"] == "LOW"]
    )

    medium = len(
        fault_df[fault_df["risk"] == "MEDIUM"]
    )

    high = len(
        fault_df[fault_df["risk"] == "HIGH"]
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.success(
            f"🟢 LOW RISK\n\n### {low}"
        )

    with col2:
        st.warning(
            f"🟡 MEDIUM RISK\n\n### {medium}"
        )

    with col3:
        st.error(
            f"🔴 HIGH RISK\n\n### {high}"
        )

else:

    st.info("No fault data available.")


# ==============================
# SENSOR MONITORING
# ==============================

st.subheader("📈 Sensor Monitoring")

if not sensor_df.empty:

    chart_data = sensor_df.sort_values("id")

    st.write("⚡ Speed")

    st.line_chart(
        chart_data.set_index("id")["speed"]
    )

    st.write("📳 Vibration")

    st.line_chart(
        chart_data.set_index("id")["vibration"]
    )

    st.write("🌡️ Temperature")

    st.line_chart(
        chart_data.set_index("id")["temperature"]
    )

    st.write("🛑 Brake Pressure")

    st.line_chart(
        chart_data.set_index("id")["brake_pressure"]
    )

else:

    st.info("No sensor data available.")


# ==============================
# LATEST FAULT
# ==============================

st.subheader("🚨 Latest Fault")

if not fault_df.empty:

    latest_fault = fault_df.iloc[0]

    train = latest_fault["train_id"]
    fault = latest_fault["faults"]
    risk = latest_fault["risk"]

    st.write(f"🚆 **Train:** {train}")
    st.write(f"⚠️ **Fault:** {fault}")

    if risk == "HIGH":

        st.error("🔴 HIGH RISK")

    elif risk == "MEDIUM":

        st.warning("🟡 MEDIUM RISK")

    else:

        st.success("🟢 LOW RISK")

else:

    st.info("No fault detected.")


# ==============================
# 🤖 AI RAILWAY DIAGNOSIS
# ==============================

st.subheader("🤖 AI Railway Diagnosis")

if not fault_df.empty:

    latest_fault = fault_df.iloc[0]

    train = latest_fault["train_id"]
    fault = latest_fault["faults"]
    risk = latest_fault["risk"]

    if fault != "No Fault":

        st.write(
            f"**Train:** {train}  |  "
            f"**Fault:** {fault}  |  "
            f"**Risk:** {risk}"
        )

        if st.button(
            "🤖 Generate AI Diagnosis",
            key="ai_diagnosis_button"
        ):

            with st.spinner(
                "🔎 Searching knowledge base and generating AI diagnosis..."
            ):

                # Build RAG index
                model, index, chunks = build_knowledge_index()

                # Retrieve relevant railway knowledge
                knowledge = retrieve_knowledge(
                    fault,
                    model,
                    index,
                    chunks
                )

                # Generate AI diagnosis
                diagnosis = get_ai_diagnosis(
                    train,
                    fault,
                    risk,
                    knowledge
                )

            st.success("✅ AI Diagnosis Generated")

            st.markdown(diagnosis)

    else:

        st.info(
            "✅ No fault detected. AI diagnosis is not required."
        )

else:

    st.info(
        "No fault data available for AI diagnosis."
    )


# ==============================
# FAULT HISTORY
# ==============================

st.subheader("📊 Fault History")

if not fault_df.empty:

    fault_count = (
        fault_df["faults"]
        .value_counts()
        .reset_index()
    )

    fault_count.columns = [
        "Fault",
        "Count"
    ]

    st.bar_chart(
        fault_count.set_index("Fault")
    )

else:

    st.info("No fault history available.")


# ==============================
# TRAIN FAULT SUMMARY
# ==============================

st.subheader("🚆 Train Fault Summary")

if not fault_df.empty:

    train_summary = (
        fault_df
        .groupby(["train_id", "risk"])
        .size()
        .reset_index(name="Count")
    )

    st.dataframe(
        train_summary,
        use_container_width=True
    )

else:

    st.info("No fault data available.")


# ==============================
# SENSOR TABLE
# ==============================

st.subheader("📡 Sensor Data")

st.dataframe(
    sensor_df,
    use_container_width=True
)


# ==============================
# FAULT TABLE
# ==============================

st.subheader("⚠️ Fault Data")

st.dataframe(
    fault_df,
    use_container_width=True
)


# ==============================
# CLOSE DATABASE
# ==============================

conn.close()