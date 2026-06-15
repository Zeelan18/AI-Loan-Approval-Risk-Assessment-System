from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

def generate_report(
    filename,
    decision,
    confidence,
    risk,
    applicant_income,
    loan_amount
):

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Loan Assessment Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1,12)
    )

    content.append(
        Paragraph(
            f"Decision: {decision}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Confidence: {confidence:.2f}%",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Risk Level: {risk}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Applicant Income: ₹{applicant_income}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Loan Amount: ₹{loan_amount}",
            styles["Normal"]
        )
    )

    doc.build(content)