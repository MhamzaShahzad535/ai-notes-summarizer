from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from xml.sax.saxutils import escape


def create_notes_report(notes):
    filename = "notes_report.pdf"

    doc = SimpleDocTemplate(
        filename,
        pagesize=A4
    )

    styles = getSampleStyleSheet()
    elements = []

    elements.append(
        Paragraph("AI Notes Summarizer Report", styles["Title"])
    )

    elements.append(Spacer(1, 20))

    for note in notes:
        elements.append(
            Paragraph(
                f"<b>Title:</b> {escape(note.title)}",
                styles["Heading2"]
            )
        )

        elements.append(
            Paragraph(
                f"<b>Original Note:</b> {escape(note.content)}",
                styles["BodyText"]
            )
        )

        elements.append(Spacer(1, 10))

        summary = note.summary or "No AI summary generated yet."

        elements.append(
            Paragraph(
                f"<b>AI Summary:</b> {escape(summary)}",
                styles["BodyText"]
            )
        )

        elements.append(Spacer(1, 25))

    doc.build(elements)

    return filename