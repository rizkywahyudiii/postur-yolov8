# ============================================================
# POSTURE ENGINE
# ============================================================

import cv2
import math
import numpy as np
from collections import deque

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
# TEMPORAL SMOOTHING HISTORY (15-30 frames)
# ============================================================

torso_history = deque(maxlen=20)
neck_history = deque(maxlen=20)


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
            # DEFENSIVE KEYPOINT SAFETY CHECK
            # =================================================

            if len(kp) < 4:

                return annotated_frame, None

            # =================================================
            # KEYPOINTS
            # =================================================

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

            torso_score = max(0, 100 - torso_angle * 1.8)
            neck_score  = max(0, 100 - neck_angle * 0.8)
            final_score = (
                torso_score * 0.6 +
                neck_score * 0.4
            )

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
            # RETURN DATA
            # =================================================

            posture_data = {

                "torso_angle": round(smooth_torso_angle, 2),

                "neck_angle": round(smooth_neck_angle, 2),

                "posture_score": round(final_score, 2),

                "posture_status": posture_status

            }

    except:

        pass

    return annotated_frame, posture_data