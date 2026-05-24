# ============================================================
# POSTURE ENGINE
# ============================================================

import cv2
import math
import numpy as np

from ultralytics import YOLO

# ============================================================
# LOAD MODEL
# ============================================================

MODEL_PATH = (
    "../notebook/runs/pose/runs/posture_pose/weights/best.pt"
)

model = YOLO(MODEL_PATH)

print("✅ Posture model loaded")


# ============================================================
# CALCULATE POSTURE
# ============================================================

def analyze_posture(frame):

    results = model.predict(
        source=frame,
        conf=0.5,
        verbose=False
    )

    result = results[0]

    annotated_frame = result.plot()

    posture_data = None

    try:

        keypoints = result.keypoints.xy.cpu().numpy()

        if len(keypoints) > 0:

            kp = keypoints[0]

            # =================================================
            # KEYPOINTS
            # =================================================

            x1, y1 = kp[0]  # Hip
            x2, y2 = kp[1]  # Shoulder
            x3, y3 = kp[2]  # Head

            # =================================================
            # TORSO ANGLE
            # =================================================

            dx = x2 - x1
            dy = y1 - y2

            torso_angle = math.degrees(
                math.atan2(abs(dx), abs(dy))
            )

            # =================================================
            # NECK ANGLE
            # =================================================

            dx2 = x3 - x2
            dy2 = y2 - y3

            neck_angle = math.degrees(
                math.atan2(abs(dx2), abs(dy2))
            )

            # =================================================
            # SCORING
            # =================================================

            if torso_angle < 10:

                torso_score = 100

            elif torso_angle < 20:

                torso_score = 70

            else:

                torso_score = 40

            if neck_angle < 15:

                neck_score = 100

            elif neck_angle < 30:

                neck_score = 70

            else:

                neck_score = 40

            final_score = (
                torso_score + neck_score
            ) / 2

            # =================================================
            # STATUS
            # =================================================

            if final_score >= 85:

                posture_status = "Excellent"

            elif final_score >= 70:

                posture_status = "Moderate"

            else:

                posture_status = "Poor"

            # =================================================
            # RETURN DATA
            # =================================================

            posture_data = {

                "torso_angle": round(torso_angle, 2),

                "neck_angle": round(neck_angle, 2),

                "posture_score": round(final_score, 2),

                "posture_status": posture_status

            }

    except:

        pass

    return annotated_frame, posture_data