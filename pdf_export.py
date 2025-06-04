from fpdf import FPDF

def export_audit_pdf(df, filename="audit_risk_report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Audit Trail Risk Report", ln=True, align='C')
    pdf.ln(10)

    for index, row in df.iterrows():
        line = f"{row['Timestamp']} | {row['User']} | {row['Action']} | {row['System']} | Score: {row['Risk_Score']} | Flags: {row['Risk_Flags']}"
        pdf.multi_cell(0, 10, txt=line)
        pdf.ln(1)

    pdf.output(filename)
    return filename
