# ============================================================
# MAIN APPLICATION
# ============================================================

import cv2
import time

from posture_engine import analyze_posture

from analytics import (

    create_posture_record,
    append_posture_data,
    save_record,
    generate_posture_graph,
    analyze_fatigue

)

from report import generate_pdf_report


# ============================================================
# CONFIGURATION
# ============================================================

# DEMO MODE
# True  = 1 capture per second
# False = 1 capture per minute

DEMO_MODE = True

if DEMO_MODE:

    CAPTURE_INTERVAL = 1

else:

    CAPTURE_INTERVAL = 60


# ============================================================
# CREATE RECORD
# ============================================================

posture_df = create_posture_record()

print("✅ Longitudinal record initialized")


# ============================================================
# OPEN CAMERA
# ============================================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():

    print("❌ Webcam tidak ditemukan")
    exit()

print("✅ Webcam aktif")


# ============================================================
# TIMER
# ============================================================

last_capture_time = time.time()

capture_count = 0


# ============================================================
# MAIN LOOP
# ============================================================

while True:

    success, frame = cap.read()

    if not success:

        break

    # ========================================================
    # POSTURE ANALYSIS
    # ========================================================

    annotated_frame, posture_data = (
        analyze_posture(frame)
    )

    # ========================================================
    # REALTIME OVERLAY
    # ========================================================

    if posture_data is not None:

        cv2.putText(

            annotated_frame,

            f"Torso : "
            f"{posture_data['torso_angle']} deg",

            (20, 40),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            (0,255,0),

            2

        )

        cv2.putText(

            annotated_frame,

            f"Neck : "
            f"{posture_data['neck_angle']} deg",

            (20, 80),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            (0,255,0),

            2

        )

        cv2.putText(

            annotated_frame,

            f"Score : "
            f"{posture_data['posture_score']}",

            (20, 120),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            (0,255,0),

            2

        )

        cv2.putText(

            annotated_frame,

            f"Status : "
            f"{posture_data['posture_status']}",

            (20, 160),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            (0,255,0),

            2

        )

    # ========================================================
    # CAPTURE TIMER
    # ========================================================

    current_time = time.time()

    elapsed_time = (
        current_time - last_capture_time
    )

    # ========================================================
    # SAVE CAPTURE
    # ========================================================

    if elapsed_time >= CAPTURE_INTERVAL:

        if posture_data is not None:

            posture_df = append_posture_data(

                posture_df,

                posture_data

            )

            capture_count += 1

            print(
                f"✅ Capture #{capture_count} saved"
            )

        last_capture_time = current_time

    # ========================================================
    # DISPLAY MODE
    # ========================================================

    if DEMO_MODE:

        mode_text = "DEMO MODE"

    else:

        mode_text = "REAL MODE"

    cv2.putText(

        annotated_frame,

        mode_text,

        (20, 210),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.8,

        (255,0,0),

        2

    )

    # ========================================================
    # SHOW WINDOW
    # ========================================================

    cv2.imshow(

        "AI Posture Analytics",

        annotated_frame

    )

    # ========================================================
    # EXIT
    # ========================================================

    key = cv2.waitKey(1)

    if key == ord("q"):

        break


# ============================================================
# CLEANUP
# ============================================================

cap.release()

cv2.destroyAllWindows()


# ============================================================
# SAVE CSV
# ============================================================

csv_path = save_record(posture_df)


# ============================================================
# GENERATE GRAPH
# ============================================================

graph_path = generate_posture_graph(

    posture_df

)


# ============================================================
# FATIGUE ANALYSIS
# ============================================================

analysis = analyze_fatigue(

    posture_df

)

print("\n📊 SESSION ANALYSIS")
print(analysis)


# ============================================================
# GENERATE PDF
# ============================================================

pdf_path = generate_pdf_report(

    analysis,

    graph_path,

    capture_count

)

print("\n✅ SESSION COMPLETE")
print(f"📄 CSV : {csv_path}")
print(f"📊 Graph : {graph_path}")
print(f"📑 PDF : {pdf_path}")