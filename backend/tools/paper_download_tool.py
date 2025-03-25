import requests
import os

def download_arxiv_papers(topic, links):
    """
    Downloads PDFs from given arXiv source links and saves them locally.

    Args:
        topic (str): Topic of the papers (used as the directory name).
        links (list): List of arXiv paper URLs (e.g., "https://arxiv.org/abs/2403.12345").
        
    Returns:
        list: A list of dictionaries containing 'link', 'file_path' (or 'error' if any).
    """
    save_dir = f"downloaded_papers/{topic}"

    if not os.path.exists(save_dir):
        os.makedirs(save_dir)  # Create directory if it doesn't exist

    results = []

    for link in links:
        result_entry = {"link": link}  # Initialize entry with the link

        try:
            # Convert abstract page URL to PDF URL
            if "arxiv.org/abs/" in link:
                pdf_url = link.replace("arxiv.org/abs/", "arxiv.org/pdf/") + ".pdf"
            elif "arxiv.org/pdf/" in link and not link.endswith(".pdf"):
                pdf_url = link + ".pdf"
            else:
                pdf_url = link  # Assume it's already a direct PDF link

            paper_id = pdf_url.split("/")[-1]  # Extract paper ID
            file_path = os.path.join(save_dir, f"{paper_id}")

            # Download the PDF
            response = requests.get(pdf_url, stream=True)
            response.raise_for_status()  # Raise error for failed requests

            with open(file_path, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024):
                    file.write(chunk)

            result_entry["file_path"] = file_path  # Store success result

        except requests.exceptions.RequestException as e:
            result_entry["error"] = str(e)  # Store error message

        results.append(result_entry)  # Append the result entry to the list

    return results
