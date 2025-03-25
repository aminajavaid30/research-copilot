from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def generate_pdf_from_json(topic, json_data, output_filename="research_report.pdf"):
    """
    Generate a PDF from a JSON response containing research papers, a conclusion, and references.

    Args:
        json_data (dict): JSON response with papers, conclusion, and references.
        output_filename (str): Name of the output PDF file.
    """
    doc = SimpleDocTemplate(output_filename, pagesize=A4)
    elements = []

    # Define styles with Unicode font
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(name="Title", fontName="Helvetica-Bold", fontSize=16, spaceAfter=10)
    heading_style = ParagraphStyle(name="Heading2", fontName="Helvetica", fontSize=14, spaceAfter=8, textColor=colors.darkblue)
    body_style = ParagraphStyle(name="BodyText", fontName="Helvetica", fontSize=12, spaceAfter=6)
    bold_style = ParagraphStyle(name="Bold", parent=body_style, fontName="Helvetica-Bold")


    # Add Title
    elements.append(Paragraph(f"Literature Review: {topic}", title_style))
    elements.append(Spacer(1, 12))

    # Process Papers Section
    if "papers" in json_data:
        elements.append(Paragraph("Papers", heading_style))
        elements.append(Spacer(1, 6))

        for idx, paper in enumerate(json_data["papers"], 1):
            elements.append(Paragraph(f"{idx}. {paper['title']}", bold_style))
            elements.append(Paragraph(f"Authors: {paper['authors']}", body_style))
            elements.append(Paragraph(f"Publication Date: {paper['publication_date'][:10]}", body_style))
            elements.append(Paragraph(f"Keywords: {', '.join(paper['keywords'])}", body_style))
            elements.append(Paragraph(f"Source: <a href='{paper['source_link']}'>{paper['source_link']}</a>", body_style))
            elements.append(Spacer(1, 6))

            # Add Abstract
            # elements.append(Paragraph("Abstract:", bold_style))
            # elements.append(Paragraph(paper["abstract"], body_style))
            # elements.append(Spacer(1, 6))

            # Add Summary
            elements.append(Paragraph("Summary:", bold_style))
            elements.append(Paragraph(paper["summary"], body_style))
            elements.append(Spacer(1, 12))

            # Add Review (if available)
            if "review" in paper and paper["review"]:
                elements.append(Paragraph("Review:", bold_style))
                elements.append(Paragraph(paper["review"], body_style))
                elements.append(Spacer(1, 12))

    # Conclusion Section
    if "conclusion" in json_data:
        elements.append(Paragraph("Conclusion", heading_style))
        elements.append(Spacer(1, 6))
        elements.append(Paragraph(json_data["conclusion"], body_style))
        elements.append(Spacer(1, 12))

    # References Section
    if "references" in json_data:
        elements.append(Paragraph("References", heading_style))
        elements.append(Spacer(1, 6))

        # Format references as a table
        ref_data = [[f"{idx}. {ref}"] for idx, ref in enumerate(json_data["references"], 1)]
        ref_table = Table(ref_data, colWidths=[500])

        # Style the table
        ref_table.setStyle(TableStyle([
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.black),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),  # ✅ Change to built-in font
            ("FONTSIZE", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ]))

        elements.append(ref_table)

    # Build PDF
    doc.build(elements)
    print(f"✅ PDF generated successfully: {output_filename}")


# Example Usage
if __name__ == "__main__":
    sample_json = {
        "papers": [
            {
                "title": "Deep Learning for NLP",
                "authors": "John Doe, Jane Smith",
                "publication_date": "2024-03-10",
                "keywords": ["Deep Learning", "NLP", "Transformer"],
                "source_link": "https://arxiv.org/abs/1234.5678",
                "abstract": "This paper explores deep learning applications in NLP.",
                "summary": "Transformers have revolutionized NLP by introducing self-attention.",
                "review": "The paper provides strong empirical evidence but lacks mathematical rigor."
            },
            {
                "title": "EfficientNet: Rethinking Model Scaling",
                "authors": "Mingxing Tan, Quoc V. Le",
                "publication_date": "2019-05-28",
                "keywords": ["CNN", "Model Scaling", "Image Classification"],
                "source_link": "https://arxiv.org/abs/1905.11946",
                "abstract": "A new CNN architecture that improves efficiency by scaling width, depth, and resolution.",
                "summary": "EfficientNet achieves better accuracy with fewer parameters compared to ResNet.",
                "review": "The proposed scaling method is novel, but real-world performance needs more validation."
            }
        ],
        "conclusion": "Deep learning continues to evolve, with new architectures like Transformers and EfficientNet improving performance in NLP and vision tasks.",
        "references": [
            "Vaswani et al., 'Attention Is All You Need', NeurIPS 2017.",
            "Tan & Le, 'EfficientNet: Rethinking Model Scaling', ICML 2019."
        ]
    }

    generate_pdf_from_json(sample_json, "research_summary.pdf")