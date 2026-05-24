# ============================================================
# REPORT GENERATOR
# ============================================================

import os

from datetime import datetime

from reportlab.platypus import (

    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image

)

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.pagesizes import letter


# ============================================================
# GENERATE PDF REPORT
# ============================================================

def generate_pdf_report(

    analysis,
    graph_path,
    total_capture

):

    os.makedirs("../reports", exist_ok=True)

    # ========================================================
    # PDF NAME
    # ========================================================

    filename = datetime.now().strftime(
        "posture_report_%Y%m%d_%H%M%S.pdf"
    )

    pdf_path = f"../reports/{filename}"

    # ========================================================
    # PDF SETUP
    # ========================================================

    doc = SimpleDocTemplate(

        pdf_path,

        pagesize=letter

    )

    styles = getSampleStyleSheet()

    elements = []

    # ========================================================
    # TITLE
    # ========================================================

    title = Paragraph(

        "AI Posture Analytics Report",

        styles["Title"]

    )

    elements.append(title)

    elements.append(Spacer(1, 20))

    # ========================================================
    # SUMMARY
    # ========================================================

    summary_text = f"""

    <b>Total Capture:</b> {total_capture}<br/><br/>

    <b>Average Posture Score:</b>
    {analysis['average_score']}<br/><br/>

    <b>Minimum Posture Score:</b>
    {analysis['minimum_score']}<br/><br/>

    <b>Maximum Posture Score:</b>
    {analysis['maximum_score']}<br/><br/>

    <b>Fatigue Start Index:</b>
    {analysis['fatigue_start_index']}<br/><br/>

    """

    summary = Paragraph(

        summary_text,

        styles["BodyText"]

    )

    elements.append(summary)

    elements.append(Spacer(1, 20))

    # ========================================================
    # INTERPRETATION
    # ========================================================

    if analysis["average_score"] >= 85:

        interpretation = (
            "User maintained a generally "
            "good posture during session."
        )

    elif analysis["average_score"] >= 70:

        interpretation = (
            "User showed moderate posture "
            "degradation during session."
        )

    else:

        interpretation = (
            "User experienced significant "
            "posture degradation and fatigue."
        )

    interpretation_paragraph = Paragraph(

        f"<b>Interpretation:</b><br/>{interpretation}",

        styles["BodyText"]

    )

    elements.append(interpretation_paragraph)

    elements.append(Spacer(1, 20))

    # ========================================================
    # GRAPH IMAGE
    # ========================================================

    graph = Image(

        graph_path,

        width=500,

        height=250

    )

    elements.append(graph)

    # ========================================================
    # BUILD PDF
    # ========================================================

    doc.build(elements)

    print(f"✅ PDF report saved: {pdf_path}")

    return pdf_path