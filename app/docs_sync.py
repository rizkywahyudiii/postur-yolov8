# ============================================================
# DOCUMENTATION SYNC LAYER
# ============================================================

import os
import shutil
import json
from datetime import datetime

def sync_session_data(analysis, csv_path, pdf_path, graph_path):
    print("\n🔄 Syncing latest session data to docs...")
    try:
        # Define destination paths
        dest_dir = "../docs/assets/latest"
        os.makedirs(dest_dir, exist_ok=True)

        csv_dest = os.path.join(dest_dir, "latest_record.csv")
        pdf_dest = os.path.join(dest_dir, "latest_report.pdf")
        graph_dest = os.path.join(dest_dir, "posture_graph.png")

        # Copy CSV
        if os.path.exists(csv_path):
            shutil.copy2(csv_path, csv_dest)
            print(f"  Copied CSV to: {csv_dest}")
        else:
            print(f"  Warning: CSV source file not found at {csv_path}")

        # Copy PDF
        if os.path.exists(pdf_path):
            shutil.copy2(pdf_path, pdf_dest)
            print(f"  Copied PDF to: {pdf_dest}")
        else:
            print(f"  Warning: PDF source file not found at {pdf_path}")

        # Copy Graph
        if os.path.exists(graph_path):
            shutil.copy2(graph_path, graph_dest)
            print(f"  Copied Graph to: {graph_dest}")
        else:
            print(f"  Warning: Graph source file not found at {graph_path}")

        # Construct JSON summary metadata dictionary
        # Explicitly convert numpy numeric types to python native types to prevent serializing crashes
        summary = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "average_score": float(analysis.get("average_score", 0.0)),
            "minimum_score": float(analysis.get("minimum_score", 0.0)),
            "maximum_score": float(analysis.get("maximum_score", 0.0)),
            "fatigue_start_index": int(analysis.get("fatigue_start_index")) if analysis.get("fatigue_start_index") is not None else None,
            "csv_file": "latest_record.csv",
            "pdf_file": "latest_report.pdf",
            "graph_file": "posture_graph.png"
        }

        # Write metadata JSON
        json_path = os.path.join(dest_dir, "session_summary.json")
        with open(json_path, "w") as f:
            json.dump(summary, f, indent=4)
        print(f"  Generated metadata: {json_path}")
        print("✅ Documentation sync completed successfully")
    except Exception as e:
        print(f"❌ Documentation sync failed: {e}")
