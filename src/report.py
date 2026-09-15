from pathlib import Path
from html import escape

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle
)
from reportlab.lib import colors

def create_report(df, analysis, graph_paths, report_path):
    report_path = Path(report_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(report_path),
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="Small", parent=styles["BodyText"], fontSize=8, leading=10
    ))

    story = []

    story.append(Paragraph("Superstore Sales & Profit Analysis", styles["Title"]))
    story.append(Paragraph(
        "Executive analytics report based on the supplied Sample Superstore dataset.",
        styles["BodyText"]
    ))
    story.append(Spacer(1, 15))

    kpi_data = [
        ["KPI", "Value"],
        ["Total Orders", f'{analysis["Total Orders"]:,}'],
        ["Total Sales", f'${analysis["Total Sales"]:,.2f}'],
        ["Total Profit", f'${analysis["Total Profit"]:,.2f}'],
        ["Average Order Value", f'${analysis["Average Order Value"]:,.2f}'],
        ["Average Discount", f'{analysis["Average Discount"]:.2f}%'],
        ["Profit Margin", f'{analysis["Profit Margin"]:.2f}%'],
        ["Top Performing Region", str(analysis["Top Performing Region"])],
    ]

    table = Table(kpi_data, colWidths=[2.7*inch, 2.7*inch])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
        ("ALIGN", (1,1), (1,-1), "RIGHT"),
        ("PADDING", (0,0), (-1,-1), 6),
    ]))
    story.append(table)
    story.append(Spacer(1, 18))

    story.append(Paragraph("Executive Summary", styles["Heading2"]))
    summary = (
        f"The dataset contains {analysis['Total Orders']:,} distinct orders with "
        f"total sales of ${analysis['Total Sales']:,.2f} and total profit of "
        f"${analysis['Total Profit']:,.2f}. "
        f"{escape(str(analysis['Top Performing Region']))} is the top region by profit, "
        f"while {escape(str(analysis['Most Profitable Category']))} is the most profitable category. "
        f"The most preferred shipping mode by record count is "
        f"{escape(str(analysis['Most Preferred Shipping Mode']))}. "
        f"The analysis also highlights the relationship between discount levels and profitability."
    )
    story.append(Paragraph(summary, styles["BodyText"]))
    story.append(Spacer(1, 15))

    story.append(Paragraph("Business Insights", styles["Heading2"]))
    for key, value in analysis.items():
        if isinstance(value, float):
            value = round(value, 2)
        story.append(Paragraph(f"<b>{escape(str(key))}:</b> {escape(str(value))}", styles["BodyText"]))
        story.append(Spacer(1, 5))

    story.append(PageBreak())
    story.append(Paragraph("Charts", styles["Heading1"]))

    for i, graph in enumerate(graph_paths):
        story.append(Paragraph(graph.stem.replace("_", " ").title(), styles["Heading2"]))
        story.append(Image(str(graph), width=6.6*inch, height=3.8*inch))
        if i < len(graph_paths) - 1:
            story.append(PageBreak())

    story.append(PageBreak())
    story.append(Paragraph("Recommendations", styles["Heading1"]))
    recommendations = [
        "Focus on profitable categories and sub-categories while investigating products with repeated losses.",
        "Review high-discount transactions because heavy discounting can reduce or reverse profitability.",
        "Compare regional profit, not only sales, before allocating inventory and marketing budgets.",
        "Use customer-segment profitability to target promotions toward high-value segments.",
        "Monitor shipping-mode usage together with order value and service expectations.",
        "Track monthly sales and profit together so revenue growth is not mistaken for healthy profitability."
    ]
    for rec in recommendations:
        story.append(Paragraph("• " + rec, styles["BodyText"]))
        story.append(Spacer(1, 7))

    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "Note: Sales in the supplied Superstore dataset already represent the recorded sales amount. "
        "Discount is stored as a fraction (for example 0.20 = 20%).",
        styles["Small"]
    ))

    doc.build(story)
