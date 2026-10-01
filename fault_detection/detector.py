import pandas as pd


def detect_fault(row):
    """
    Railway fault detection using sensor values
    and dataset risk score.
    """

    faults = []

    # -----------------------------
    # SENSOR VALUES
    # -----------------------------

    vibration = row["track_vibration_level"]
    bearing_temp = row["bearing_temperature_c"]
    brake_pressure = row["brake_pressure_psi"]
    wheel_wear = row["wheel_wear_percent"]
    rail_wear = row["rail_wear_mm"]
    risk_score = row["risk_score"]

    # -----------------------------
    # HANDLE MISSING VALUES
    # -----------------------------

    if pd.isna(vibration):
        vibration = 0

    if pd.isna(bearing_temp):
        bearing_temp = 0

    if pd.isna(brake_pressure):
        brake_pressure = 0

    if pd.isna(wheel_wear):
        wheel_wear = 0

    if pd.isna(rail_wear):
        rail_wear = 0

    if pd.isna(risk_score):
        risk_score = 0

    # -----------------------------
    # SENSOR FAULT RULES
    # -----------------------------

    if vibration >= 7:
        faults.append("Track/Wheel Vibration")

    if bearing_temp >= 80:
        faults.append("Bearing Temperature")

    if brake_pressure < 70:
        faults.append("Brake Pressure")

    if wheel_wear >= 70:
        faults.append("Wheel Wear")

    if rail_wear >= 5:
        faults.append("Rail Wear")

    # -----------------------------
    # RISK SCORE
    # -----------------------------

    if risk_score >= 80:
        risk_level = "HIGH"

    elif risk_score >= 50:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"

    # -----------------------------
    # FINAL STATUS
    # -----------------------------

    if len(faults) >= 2 or risk_score >= 80:

        status = "CRITICAL"

    elif len(faults) == 1 or risk_score >= 50:

        status = "WARNING"

    else:

        status = "NORMAL"

    # -----------------------------
    # RETURN RESULT
    # -----------------------------

    return {
        "status": status,
        "faults": faults,
        "risk_level": risk_level,
        "risk_score": risk_score
    }


# ============================================================
# TEST DETECTOR
# ============================================================

if __name__ == "__main__":

    file_path = "Data/raw/indian_railway_predictive_maintenance_100k.csv"

    df = pd.read_csv(file_path)

    print("\nRailway Fault Detection Test")
    print("----------------------------")

    for index, row in df.head(10).iterrows():

        result = detect_fault(row)

        print("\nRecord:", index + 1)
        print("Train ID:", row["train_id"])
        print("Status:", result["status"])
        print("Risk Level:", result["risk_level"])
        print("Risk Score:", result["risk_score"])

        if result["faults"]:

            print(
                "Possible Faults:",
                ", ".join(result["faults"])
            )

        else:

            print("Possible Faults: None")