from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)

from reportlab.lib.styles import getSampleStyleSheet


class PDFReportGenerator:

    def __init__(
        self,
        profile,
        dts_report,
        recommendations,
        findings_df
    ):

        self.profile = profile
        self.dts_report = dts_report
        self.recommendations = recommendations
        self.findings_df = findings_df

    def generate(
        self,
        output_path="data/output/DATATSTY_Report.pdf"
    ):

        doc = SimpleDocTemplate(output_path)

        styles = getSampleStyleSheet()

        elements = []

        elements.append(
            Paragraph(
                "DATATSTY AI Data Readiness Assessment",
                styles["Title"]
            )
        )

        elements.append(Spacer(1, 20))

        elements.append(
            Paragraph(
                "Executive Summary",
                styles["Heading1"]
            )
        )

        elements.append(
            Paragraph(
                f"DTS Score: {self.dts_report['DTS Score']}",
                styles["BodyText"]
            )
        )

        elements.append(
            Paragraph(
                f"AI Readiness: {self.dts_report['Status']}",
                styles["BodyText"]
            )
        )

        elements.append(
            Paragraph(
                f"Rows: {self.profile['Total Rows']}",
                styles["BodyText"]
            )
        )

        elements.append(
            Paragraph(
                f"Columns: {self.profile['Total Columns']}",
                styles["BodyText"]
            )
        )

        elements.append(PageBreak())

        elements.append(
            Paragraph(
                "Recommendations",
                styles["Heading1"]
            )
        )

        for rec in self.recommendations:

            elements.append(
                Paragraph(
                    f"• {rec['Issue']}",
                    styles["BodyText"]
                )
            )

        elements.append(PageBreak())

        elements.append(
            Paragraph(
                "Quality Findings",
                styles["Heading1"]
            )
        )

        top_findings = self.findings_df.head(20)

        for _, row in top_findings.iterrows():

            elements.append(
                Paragraph(
                    str(row.to_dict()),
                    styles["BodyText"]
                )
            )

        doc.build(elements)

        return output_path