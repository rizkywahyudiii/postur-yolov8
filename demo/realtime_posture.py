# ============================================================
# REALTIME POSTURE ANALYTICS SYSTEM
# ============================================================

import cv2
import math
import time
import numpy as np
from collections import deque

from ultralytics import YOLO

# ============================================================
# TEMPORAL SMOOTHING HISTORY (15-30 frames)
# ============================================================

torso_history = deque(maxlen=20)
neck_history = deque(maxlen=20)

# ============================================================
# LOAD TRAINED MODEL
# ============================================================

MODEL_PATH = "../notebook/runs/pose/runs/posture_pose/weights/best.pt"

model = YOLO(MODEL_PATH)

print("✅ Model berhasil dimuat")

# ============================================================
# OPEN WEBCAM
# ============================================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():

    print("❌ Webcam tidak ditemukan")
    exit()

print("✅ Webcam berhasil dibuka")

# ============================================================
# MAIN LOOP
# ============================================================

prev_time = 0

while True:

    success, frame = cap.read()

    if not success:

        break

    # ========================================================
    # INFERENCE
    # ========================================================

    results = model.predict(
        source=frame,
        conf=0.5,
        verbose=False
    )

    result = results[0]

    annotated_frame = result.plot()

    # ========================================================
    # FPS
    # ========================================================

    current_time = time.time()

    fps = 1 / (current_time - prev_time)

    prev_time = current_time

    # ========================================================
    # KEYPOINT EXTRACTION
    # ========================================================

    try:

        keypoints = result.keypoints.xy.cpu().numpy()

        if len(keypoints) > 0:

            kp = keypoints[0]

            # =================================================
            # DEFENSIVE KEYPOINT SAFETY CHECK
            # =================================================

            if len(kp) < 4:

                continue

            # KP0 = Hip
            # KP1 = Shoulder
            # KP2 = Head
            # KP3 = Spine

            x1, y1 = kp[0]  # Hip
            x2, y2 = kp[1]  # Shoulder
            x3, y3 = kp[2]  # Head
            x4, y4 = kp[3]  # Spine

            # =================================================
            # TORSO ANGLE (WEIGHTED STRATEGY)
            # =================================================

            # Lower torso: Hip (kp[0]) to Spine (kp[3])
            dx_lower = x4 - x1
            dy_lower = y1 - y4
            lower_torso_angle = math.degrees(
                math.atan2(abs(dx_lower), abs(dy_lower))
            )

            # Upper torso: Spine (kp[3]) to Shoulder (kp[1])
            dx_upper = x2 - x4
            dy_upper = y4 - y2
            upper_torso_angle = math.degrees(
                math.atan2(abs(dx_upper), abs(dy_upper))
            )

            # Weighted torso angle favoring upper spine slouching (30% lower, 70% upper)
            torso_angle = lower_torso_angle * 0.3 + upper_torso_angle * 0.7

            # =================================================
            # NECK ANGLE
            # =================================================

            dx2 = x3 - x2  # Head to Shoulder
            dy2 = y2 - y3

            neck_angle = math.degrees(
                math.atan2(abs(dx2), abs(dy2))
            )

            # =================================================
            # TEMPORAL SMOOTHING
            # =================================================

            torso_history.append(torso_angle)
            neck_history.append(neck_angle)

            smooth_torso_angle = sum(torso_history) / len(torso_history)
            smooth_neck_angle = sum(neck_history) / len(neck_history)

            # =================================================
            # CONTINUOUS SCORING
            # =================================================

            torso_score = max(0.0, 100.0 - smooth_torso_angle * 2.5)
            neck_score = max(0.0, 100.0 - smooth_neck_angle * 1.5)
            final_score = 0.5 * torso_score + 0.5 * neck_score

            # =================================================
            # STATUS
            # =================================================

            if final_score >= 80:

                posture_status = "Excellent"

            elif final_score >= 60:

                posture_status = "Moderate"

            else:

                posture_status = "Poor"

            # =================================================
            # OVERLAY TEXT
            # =================================================

            cv2.putText(
                annotated_frame,
                f"Torso: {smooth_torso_angle:.1f} deg",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,0),
                2
            )

            cv2.putText(
                annotated_frame,
                f"Neck : {smooth_neck_angle:.1f} deg",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,0),
                2
            )

            cv2.putText(
                annotated_frame,
                f"Score : {final_score:.1f}/100",
                (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,0),
                2
            )

            cv2.putText(
                annotated_frame,
                f"Status: {posture_status}",
                (20, 160),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0,255,0),
                2
            )

    except:

        pass

    # ========================================================
    # FPS DISPLAY
    # ========================================================

    cv2.putText(
        annotated_frame,
        f"FPS: {fps:.1f}",
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
        "Realtime Posture Analytics",
        annotated_frame
    )

    # Keyboard Interaction
    key = cv2.waitKey(1)

    if key == ord("q"):

        break

    elif key == ord("s") or key == ord("S"):

        import os
        screenshot_path = "../docs/assets/latest/latest-demo.png"
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        cv2.imwrite(screenshot_path, annotated_frame)
        print(f"📸 Screenshot saved to {screenshot_path}")

# ============================================================
# CLEANUP
# ============================================================

cap.release()

cv2.destroyAllWindows()