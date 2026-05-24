# ============================================================
# LONGITUDINAL ANALYTICS
# ============================================================

import os
import pandas as pd
import matplotlib.pyplot as plt

from datetime import datetime

# ============================================================
# CREATE RECORD
# ============================================================

def create_posture_record():

    columns = [

        "timestamp",

        "torso_angle",

        "neck_angle",

        "posture_score",

        "posture_status"

    ]

    df = pd.DataFrame(columns=columns)

    return df


# ============================================================
# APPEND DATA
# ============================================================

def append_posture_data(df, posture_data):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    new_row = {

        "timestamp": timestamp,

        "torso_angle":
            posture_data["torso_angle"],

        "neck_angle":
            posture_data["neck_angle"],

        "posture_score":
            posture_data["posture_score"],

        "posture_status":
            posture_data["posture_status"]

    }

    df.loc[len(df)] = new_row

    return df


# ============================================================
# SAVE CSV
# ============================================================

def save_record(df):

    os.makedirs("../records", exist_ok=True)

    filename = datetime.now().strftime(
        "posture_record_%Y%m%d_%H%M%S.csv"
    )

    filepath = f"../records/{filename}"

    df.to_csv(filepath, index=False)

    print(f"✅ Record saved: {filepath}")

    return filepath


# ============================================================
# GENERATE GRAPH
# ============================================================

def generate_posture_graph(df):

    os.makedirs("../reports", exist_ok=True)

    # ========================================================
    # X AXIS
    # ========================================================

    x = range(len(df))

    # ========================================================
    # PLOT
    # ========================================================

    plt.figure(figsize=(12,6))

    plt.plot(
        x,
        df["torso_angle"],
        marker="o",
        label="Torso Angle"
    )

    plt.plot(
        x,
        df["neck_angle"],
        marker="o",
        label="Neck Angle"
    )

    plt.plot(
        x,
        df["posture_score"],
        marker="o",
        label="Posture Score"
    )

    # ========================================================
    # THRESHOLD
    # ========================================================

    plt.axhline(
        y=70,
        linestyle="--",
        label="Fatigue Threshold"
    )

    # ========================================================
    # LABEL
    # ========================================================

    plt.xlabel("Capture Index")

    plt.ylabel("Angle / Score")

    plt.title(
        "Longitudinal Posture Analytics"
    )

    plt.legend()

    plt.grid(True)

    # ========================================================
    # SAVE GRAPH
    # ========================================================

    graph_path = (
        "../reports/posture_graph.png"
    )

    plt.savefig(graph_path)

    plt.close()

    print(f"✅ Graph saved: {graph_path}")

    return graph_path


# ============================================================
# FATIGUE ANALYSIS
# ============================================================

def analyze_fatigue(df):

    avg_score = df["posture_score"].mean()

    min_score = df["posture_score"].min()

    max_score = df["posture_score"].max()

    fatigue_start = None

    for idx, score in enumerate(df["posture_score"]):

        if score < 70:

            fatigue_start = idx

            break

    analysis = {

        "average_score": round(avg_score, 2),

        "minimum_score": round(min_score, 2),

        "maximum_score": round(max_score, 2),

        "fatigue_start_index": fatigue_start

    }

    return analysis