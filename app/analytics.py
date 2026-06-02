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

    graph_path = "../reports/posture_graph.png"

    if df.empty:

        plt.figure(figsize=(10, 5))
        plt.title("Longitudinal Posture Analytics - No Data")
        plt.text(0.5, 0.5, "No capture records available for this session.",
                 ha='center', va='center', fontsize=12)
        plt.savefig(graph_path)
        plt.close()
        return graph_path

    # Clean double Y-axis configuration
    fig, ax1 = plt.subplots(figsize=(12, 6))

    x = range(len(df))

    # Format X-axis with timestamps if available
    if "timestamp" in df.columns and len(df) > 0:
        try:
            x_labels = pd.to_datetime(df["timestamp"]).dt.strftime("%H:%M:%S")
        except:
            x_labels = df["timestamp"].astype(str)
    else:
        x_labels = [str(i) for i in x]

    # Primary Y-axis: Posture Score (0 - 100)
    color_score = "#10ac84"  # Emerald green
    ax1.set_xlabel("Time (HH:MM:SS)", fontsize=11, fontweight='bold', labelpad=10)
    ax1.set_ylabel("Posture Score (0-100)", color=color_score, fontsize=11, fontweight='bold')
    
    line1 = ax1.plot(
        x,
        df["posture_score"],
        color=color_score,
        linewidth=2.5,
        marker="o",
        markersize=6,
        label="Posture Score"
    )
    
    # Draw horizontal line at fatigue threshold
    thresh_line = ax1.axhline(
        y=70,
        color="#ff4757",  # Soft red
        linestyle="--",
        linewidth=1.5,
        label="Fatigue Threshold (70)"
    )
    
    ax1.tick_params(axis='y', labelcolor=color_score)
    ax1.set_ylim(0, 105)
    ax1.grid(True, linestyle=":", alpha=0.6)

    # Secondary Y-axis: Angles (degrees)
    ax2 = ax1.twinx()
    color_angles = "#2f3542"  # Charcoal
    ax2.set_ylabel("Angles (Degrees)", color=color_angles, fontsize=11, fontweight='bold')
    
    color_torso = "#2b7bba"  # Soft blue
    line2 = ax2.plot(
        x,
        df["torso_angle"],
        color=color_torso,
        linewidth=1.8,
        linestyle="-",
        marker="s",
        markersize=5,
        label="Torso Angle"
    )
    
    color_neck = "#ff9f43"  # Soft orange
    line3 = ax2.plot(
        x,
        df["neck_angle"],
        color=color_neck,
        linewidth=1.8,
        linestyle="-",
        marker="^",
        markersize=5,
        label="Neck Angle"
    )
    
    ax2.tick_params(axis='y', labelcolor=color_angles)
    
    # Scale secondary Y-axis dynamically based on maximum angle detected
    max_angle = max(df["torso_angle"].max(), df["neck_angle"].max())
    ax2.set_ylim(0, max(45, max_angle + 10))
    ax2.grid(False)

    # Clean up X-axis tick display to prevent crowding
    max_ticks = 10
    if len(df) > max_ticks:
        step = len(df) // max_ticks
        ax1.set_xticks(x[::step])
        ax1.set_xticklabels(x_labels[::step], rotation=15, ha='right')
    else:
        ax1.set_xticks(x)
        ax1.set_xticklabels(x_labels, rotation=15, ha='right')

    # Combine legends from both axes
    lines = line1 + [thresh_line] + line2 + line3
    labels = [l.get_label() for l in lines]
    ax1.legend(lines, labels, loc="lower left", frameon=True, facecolor="white", edgecolor="#dfe4ea")

    plt.title("Silent Longitudinal Posture Analytics", fontsize=13, fontweight='bold', pad=15)
    
    fig.tight_layout()

    plt.savefig(graph_path, dpi=120)
    plt.close()

    print(f"✅ Graph saved: {graph_path}")

    return graph_path


# ============================================================
# FATIGUE ANALYSIS
# ============================================================

def analyze_fatigue(df):

    if df.empty:

        return {

            "average_score": 0.0,

            "minimum_score": 0.0,

            "maximum_score": 0.0,

            "fatigue_start_index": None

        }

    avg_score = df["posture_score"].mean()

    min_score = df["posture_score"].min()

    max_score = df["posture_score"].max()

    # Prevent nan or null errors
    avg_score = round(avg_score, 2) if not pd.isna(avg_score) else 0.0
    min_score = round(min_score, 2) if not pd.isna(min_score) else 0.0
    max_score = round(max_score, 2) if not pd.isna(max_score) else 0.0

    fatigue_start = None

    for idx, score in enumerate(df["posture_score"]):

        if score < 70:

            fatigue_start = idx

            break

    analysis = {

        "average_score": avg_score,

        "minimum_score": min_score,

        "maximum_score": max_score,

        "fatigue_start_index": fatigue_start

    }

    return analysis