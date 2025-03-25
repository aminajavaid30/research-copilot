import os
import json
import re
from pdf_from_json import generate_pdf_from_json

def extract_metadata(response_content: str):
    metadata = []
    paper_sections = response_content.split("## ")[1:]  # Splitting by section titles
    
    for section in paper_sections:
        lines = section.strip().split("\n")
        title = lines[0].strip()
        
        # Skip non-research sections
        if title.lower() in ["conclusion", "references"]:
            continue

        authors = re.search(r"\*\*Authors\*\*: (.+)", section)
        publication_date = re.search(r"\*\*Publication Date\*\*: (.+)", section)
        keywords = re.search(r"\*\*Keywords\*\*: (.+)", section)
        journal = re.search(r"\*\*Journal\*\*: (.+)", section)
        review_match = re.search(r"\*\*Review\*\*: \*(.+?)\*", section, re.DOTALL)
        source_link = re.search(r"(http[s]?://[^\s]+)", section)

        metadata.append({
            "title": title,
            "authors": authors.group(1) if authors else "",
            "publication_date": publication_date.group(1) if publication_date else "",
            "keywords": [kw.strip() for kw in keywords.group(1).split(",")] if keywords else [],
            "journal": journal.group(1) if journal else "",
            "source_link": source_link.group(1) if source_link else ""
        })

    return metadata

# Save paper metadata as JSON
def save_paper_metadata(topic, papers):
    PAPERS_DIR = "../papers_metadata"
    os.makedirs(PAPERS_DIR, exist_ok=True)

    file_path = os.path.join(PAPERS_DIR, f"{topic}_papers.json")
    with open(file_path, "w") as f:
        json.dump(papers, f, indent=4)
    return file_path

def generate_pdf(topic, response):
    PDF_DIR = "../literature_reviews"
    os.makedirs(PDF_DIR, exist_ok=True)

    pdf_path = os.path.join(PDF_DIR, f"{topic.replace(' ', '_')}_literature_review.pdf")

    print("Generating PDF...")

    # Generate PDF from JSON
    json_response = json.loads(response)
    generate_pdf_from_json(topic, json_response, pdf_path)

    print(f"PDF successfully generated: {pdf_path}")
    return pdf_path